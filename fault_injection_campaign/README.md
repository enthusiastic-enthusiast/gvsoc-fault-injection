
# Some problems and questions

- The fault generator function is becoming too long => adjust the interface such that the user specifies fault generating functions for individual device types (e.g. L1 caches, prefetcher buffers, ...). MORE MODULARITY!

- For now, we support "functional" fault injection analysis where we compare the final memory values of faulty runs with those of the golden run. Should we implement a more thorough fault injection analysis which involves dumping all memory reads/writes (with timestamps) of the golden run to account for timing as well? If so, how to do it efficiently?

# Information

- `ficlib` contains Python modules that help performing fault injection campaigns in GVSOC by interfacing the Fault Injection Controller subsystem inside the core.

- `faulted_pulp_open` and `faulted_toy_system` contain fault injection setups that should be complete in the sense that it provides base functionality and the user is free to choose any binary, provide custom fault generating function, specify arbitrary (or symbolic) points of interest, or go with default things.

- The setup code still relies on knowing the layout of FICs inside the target system. This is to be lifted when moved to service based model (?).

## Summary

- **How the faults are communicated into the gvsoc?**
    >  There are two ways:
        (1) By specifying a file containing faults on the command line using `--parameter {FIC path}/faults_path={path to file}`. Faults must be specified in numeric format. Note that no recompilation is needed.
        (2) [Broken?] By issuing proxy commands using `gv._send_cmd("component {FIC component} {fault}")`. In this case, `fault` can be specified both numerically or verbally.

- **Which devices can be fault'ed?**
    > Memory, prefetch buffer, register file.

- **Which fault types are supported?**
    > Multi-bit upsets (incl. bitflips) and stuck-at's in memories and MBU only in all others. More to come?

- **How do we trace the effects of faults?**
    > As of now, only "functional" fault injection campaign is supported where we verify contents of chosen memory regions (Points of Interest) at the end of faulty runs against the contents obtained from golden run. Those Points of Interest can denote either specific variables or large contiguous memory regions (in which case we hash it).

- **How do we specify PoIs?**
    > The direct way is to specify a list of entries `(addr, sizes)`. If the binary contains symbol table, one can further specify a list of symbol names or the type of objects of interest (e.g. all global symbols): the function `ficlib::poi_helpers::find_pois` will parse the binary approprietly.

## Fault effect classification

Now, we classify faults as either: 

- `MASKED`: none PoI value was affected by the fault by the end of the simulation.
- `SDC`: the run did finish but the PoI value/hash differs from the golden one.
- `DUE`: the GVSOC simulation exited with error code (likely detected flawed control flow).
- `SIM_FAULT`: the child process running GVSOC hit TIMEOUT (possibly due to a fault corrupting the executable code and confusing the GVSOC engine, in which case must be DUE, but who knows).

## Numerical fault description

See `core/fault_injection/README.md``
