from pyats.topology import Testbed, Device
import logging
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from datetime import datetime

logging.basicConfig(filename='log_ccollect.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(message)s')

def Create_Testbed(user,pswd,hostnames,device_ips,jump_bool,
                   jump_ip,jump_port,jump_user,jump_pass):
    testbed = Testbed('exampleTestbed')

    if jump_bool:
        jump_server = Device('jump_host',
                    connections = {
                        'mgmt': {
                            'protocol': 'ssh',
                            'ip': jump_ip,
                            'port': jump_port
                        },
                    })
        jump_server.os = 'linux'
        jump_server.testbed = testbed
        jump_server.credentials['default'] = dict(username=jump_user, password=jump_pass)

    for i in range(len(hostnames)):
        if jump_bool:
            dev = Device(hostnames[i],
                connections = {
                            'cli': {
                                'protocol': 'ssh',
                                'ip': device_ips[i],
                                'proxy': 'jump_host',
                                'login_creds': ['default', 'local']
                                },
                            })
        else:
            dev = Device(hostnames[i],
            connections = {
                        'cli': {
                            'protocol': 'ssh',
                            'ip': device_ips[i],
                            'login_creds': ['default']
                            },
                        })
        dev.os = 'iosxr'
        dev.testbed = testbed
        dev.credentials['default'] = dict(username=user, password=pswd)
        logging.debug('Device {} added to testbed'.format(hostnames[i]))
        del dev
    return testbed

def pool_connection(maxthreads,hostname,routine_function):
    start_time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
    pool = ThreadPool(maxthreads)
    pool_result = []
    try:
        #pool.map (funcion to iterate)
        pool_result = pool.map(routine_function,hostname)
    except UnboundLocalError:
        print("Error mapping threads to routine")

    pool.close()
    pool.join()

    end_time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
    print("Info - Start Time:", start_time)
    print("Info - End Time:", end_time)
    print("")

    return pool_result