import concurrent.futures
from daemon import *

good_daemon = daemon()

"""
good_daemon.timing_settings  = {'update_pump_settings'          :       60, 
                                'update_lights_settings'        :       50, 
                                'control_timed_pump'            :       0.5, 
                                'control_timed_lights'          :       0.5,
                                'check_and_control_variables'   :       0.5}

"""

with concurrent.futures.ThreadPoolExecutor() as executor:
    results =  executor.submit(good_daemon.rule_them_all_dady)
    print(results.result())








