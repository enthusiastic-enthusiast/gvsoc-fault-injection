import gvsoc.systree as st
import gvsoc.runner as gvsoc

import cpu.iss.riscv
import memory.memory
import vp.clock_domain
import interco.router
import fault_injection.fic
import utils.loader.loader
import gdbserver.gdbserver
from gvrun.parameter import TargetParameter


class Soc(st.Component):

    def __init__(self, parent, name, parser, binary):
        super(Soc, self).__init__(parent, name)

        # Main interconnect
        ico = interco.router.Router(self, 'ico')
        # Add a mapping to the memory and connect it. The remove offset is used to substract
        # the global address to the requests address so that the memory only gets a local offset.

        # FIC must be instantiated before mem such that mem is not deallocated before FIC upon exit.
        fic = fault_injection.fic.FIC(self, 'fic')

        # Main memory
        mem = memory.memory.Memory(self, 'mem', size=0x00100000, fic_enabled=True)
        ico.o_MAP(mem.i_INPUT(), 'mem', base=0x00000000, size=0x00100000, rm_base=True)
        fic.o_GLOBAL_AS(ico.i_INPUT ())

        # Instantiates the main core and connect fetch and data to the interconnect
        host = cpu.iss.riscv.Riscv(self, 'host', isa='rv64imafdc', binaries=[binary])
        host.o_FETCH     (ico.i_INPUT    ())
        host.o_DATA      (ico.i_INPUT    ())
        host.o_DATA_DEBUG(ico.i_INPUT    ())

        # Finally connect an ELF loader, which will execute first and will then
        # send to the core the boot address and notify him he can start
        loader = utils.loader.loader.ElfLoader(self, 'loader', binary=binary)
        loader.o_OUT     (ico.i_INPUT    ())
        loader.o_START   (host.i_FETCHEN ())
        loader.o_ENTRY   (host.i_ENTRY   ())

        gdbserver.gdbserver.Gdbserver(self, 'gdbserver')



# This is a wrapping component of the real one in order to connect a clock generator to it
# so that it automatically propagate to other components
class Rv64(st.Component):

    def __init__(self, parent, name, parser, options):

        super(Rv64, self).__init__(parent, name, options=options)

        self.set_target_name('faulted_toy_system')

        TargetParameter(
            self, name='binary', value=None, description='Binary to be simulated'
        )

        binary = None
        if parser is not None:
            print(parser)
            [args, otherArgs] = parser.parse_known_args()
            binary = args.binary

        clock = vp.clock_domain.Clock_domain(self, 'clock', frequency=100000000)
        soc = Soc(self, 'soc', parser, binary)
        clock.o_CLOCK    (soc.i_CLOCK    ())

# This is the top target that gvrun will instantiate
class Target(gvsoc.Target):

    gapy_description="Toy system for showcasing fault injection features"
    model=Rv64
    name="faulted_toy_system"

    def __init__(self, parser, options=None, name=None):
        super(Target, self).__init__(parser, options,
            model=Rv64, name=name)
