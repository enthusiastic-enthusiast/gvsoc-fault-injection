#!/usr/bin/env python3

import random
import os
import ficlib.poi_helpers as poi_helpers

from ficlib.fault_helpers import *
from ficlib.campaign_manager import CampaignManager

THREADS     = 12
TOTAL_RUNS  = 120

""" !!! FOR NOW WE CALL FROM PARENT DIRECTORY: WORKAROUND !!! """
TARGET_DIR  = os.path.join(os.getcwd(), "faulted_toy_system")
BUILD_DIR   = os.path.join(os.getcwd(), "faulted_toy_system/build")
WORK_DIR    = os.path.join(os.getcwd(), "faulted_toy_system/build/work")
BINARY      = os.path.join(os.getcwd(), "faulted_toy_system/build/test/test")

"""
Example program showcasing how user can use the Python campaign 
manager module for performing templated fault injection test runs. 
"""

""" First, we specify arbitrary memory regions as Points of Interest. """
pois_raw = [[0x77770, 4, "target_var"], 
            [0x7770, 4024], 
            [0x100, 2], 
            [0x90000, 0x0fff, "vip_region"]]

""" This list has to be converted first before being passed to start_campaign """
pois_f = poi_helpers.make_pois(pois_raw)

""" We set all global functions as PoI... """
pois_f += poi_helpers.find_pois(binary_path=BINARY, select=poi_helpers.GLOBAL_FUNCTIONS)

""" And a specific object by specifying its name """
poi_names = ["private_key", "msg"]
pois_f += poi_helpers.find_pois(binary_path=BINARY, names=poi_names)

# Do integrity checks with `soc/fic` using global address space
for poi in pois_f:
    poi.checker_path = 'soc/fic'
    poi.target       = -1

campaign = CampaignManager(
    pois=pois_f,
    fics=['soc/fic'],
    target='faulted_toy_system',
    binary=BINARY,
    builddir=BUILD_DIR,
    targetdir=TARGET_DIR,
    print_injections=False,
    print_details=True,
    threads=THREADS,
    total_runs=TOTAL_RUNS
)

def fault_generator(tid, run_id):
    """
    We construct a simple fault model consisting only 
    of bitflips with params distributed uniformly.
    """
    faults = [] 
    cycle_max = campaign.golden_cycles['soc/fic']
    faults_min = int(cycle_max / 20000) # at least every 20'000 cycles
    faults_max = int(cycle_max / 2000)  # at most every 2'000 cycles
    faults_curr = random.randint(faults_min, faults_max)

    for i in range(faults_curr):
        cycle = random.randint(0, cycle_max) 
        location = random.randint(0x0, 0x100000)
        bit = random.randint(0, 7)
        # Constant -1 stands for global address space 
        faults.append(
            mem_bitflip_req(-1, location, bit, cycle, fic='soc/fic')
        )

    return faults

campaign.fault_generator = fault_generator

campaign.do_golden_run()
campaign.start_workers()
campaign.print_results()

exit(0)
