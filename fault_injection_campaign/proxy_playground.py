#!/usr/bin/env python3

import argparse
import gv.gvsoc_control as gvsoc
import threading
import time

NB_CLUSTER=4

paths = {}

""" Helpers """
def get_cycles(component):
    req = gv._send_cmd(f'component {component} get_cycles', keep_lock=True, wait_reply=False)
    reply = gv.reader._get_payload(req)
    gv._unlock_cmd()
    gv.reader.wait_reply(req)
    return int.from_bytes(reply, byteorder='little')

def get_period(component):
    req = gv._send_cmd(f'component {component} get_period', keep_lock=True, wait_reply=False)
    reply = gv.reader._get_payload(req)
    gv._unlock_cmd()
    gv.reader.wait_reply(req)
    return int.from_bytes(reply, byteorder='little')

def print_cycles(component):
    print(f'{paths[component]}: cycle={get_cycles(component)}')

def print_period(component):
    print(f'{paths[component]}: period={get_period(component)}')

parser = argparse.ArgumentParser(description='Control GVSOC')

parser.add_argument("--host", dest="host", default="localhost", help="Specify host name")
parser.add_argument("--port", dest="port", default=42951, type=int, help="Specify host port")

args = parser.parse_args()

gv = gvsoc.Proxy(args.host, args.port)

"""
# Collect FIC handles
fic_l1_banks = [gv._get_component('chip/cluster/l1/fic_l1_banks')]
paths[fic_l1_banks[0]] = 'chip/cluster/l1/fic_l1_banks'
for cid in range(1, NB_CLUSTER):
    path = f'chip/cluster_{cid}/l1/fic_l1_banks'
    fic_c = gv._get_component(path)
    fic_l1_banks.append(fic_c)
    paths[fic_c] = path

fic_soc_l2_priv = gv._get_component('chip/soc/l2/fic_l2_priv')
paths[fic_soc_l2_priv] = 'chip/soc/l2/fic_l2_priv'

fic_soc = gv._get_component('chip/soc/fic_soc')
paths[fic_soc] = 'chip/soc/fic_soc'
"""

# Collect interconnect handle
axi_ico = gvsoc.Router(gv, '**/soc/axi_ico')

"""
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c00A704, 8):64b}')
print('sending transient injection')
gv._send_cmd(f'component {fic_soc_l2_priv} inject 1 T 0x00002706 6 100 L')
gv.run(1000000)

print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c00A704, 8):64b}')
print_cycles(fic_soc_l2_priv)
#gv._send_cmd(f'component {fic_soc} inject gas B 0x8706 6')

#gv._send_cmd(f'component {fic_soc} inject gas B 0x1c008706 6 10')

gv.run(1000000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c00A704, 8):64b}')
print_cycles(fic_soc_l2_priv)
"""

gv.run(500000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000001, 1):08b}')
gv.run(500000000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000001, 1):08b}')
gv.run()
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000001, 1):08b}')
#gv.run()
#print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
"""
gv.run(30000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
gv.run(30000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
gv.run(30000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
gv.run(30000)
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
gv.run()
print(f'value @0x1c09706={axi_ico.mem_read_int(0x1c000000, 1):08b}')
"""
gv.quit(0)
gv.close()

exit(0)
