from genie.testbed import load
import argparse
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
import logging
import os
import getpass
from utils import Create_Testbed,pool_connection

logging.basicConfig(filename='log_checks.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(message)s')

global cmds
cmds = ["show running-config",
        "show version"]
outputs_folder = ""
folder_type = ""

def store_command(hostname, command, command_output):
    try:
        if '|' in command:
            command = command.replace('|','-')
        log_name = command + '.txt'
        folder = os.path.join(outputs_folder, hostname)
        #folder = os.path.join(folder, daytime)

        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))

        file_log = os.path.join(folder, log_name)
        #print (file_log)
        try:
            with open(file_log, 'w') as f:
                f.write(command_output)
            if os.path.exists(file_log):
                result = 'SUCCESS'
                logging.debug("Info - Log file: '{}' successfuly created:".format(file_log))

            else:
                result = 'FAIL'
                error_msg = "Error - Failed to create log file: " + file_log
                logging.deug(error_msg)
        except Exception as e:
            logging.debug("Error in file creation:\n{}".format(e))
    except Exception as e:
        logging.debug("Eror in file creation\n{}".format(e))
    return result

def Testbed_routine(hostname):

    uut = tb.devices[hostname]
    connected=False
    if jump_replace:
        try:
            jump = tb.devices['jump_host']
            jump.connect(log_stdout=verbose_flag)
            uut_ip = str(uut.connections['cli']['ip'])
            command = 'ssh-keygen -R {}'.format(uut_ip)
            jump.execute(command)
            print("IP {} SSH keys cleared, continue with connection".format(uut_ip))
            logging.debug("IP {} SSH keys cleared, continue with connection".format(uut_ip))
        except Exception as e:
            print("Exception catched on SSH keys clearing on jumphost")
            logging.debug("Exception catched on SSH keys clearing on jumphost:\n{}".format(e))
    try:
        uut.connect(init_config_commands=[],connection_timeout=5,log_stdout=verbose_flag)
        connected=True
    except:
        logging.debug("Error #1 in the connection to: '{}'".format(hostname))

    if not connected:
        try:
            uut.connect(init_config_commands=[],connection_timeout=5,log_stdout=verbose_flag)
            connected=True
        except:
            logging.debug("Error #2 in the connection to: '{}'".format(hostname))

    if not connected:
        try:
            # Last resort creds
            uut.credentials['default'] = dict(username='dummy_user', password='dummy_pass')
            uut.connect(init_config_commands=[],connection_timeout=5,log_stdout=verbose_flag)
            connected=True
        except:
            logging.debug("Error #3 in the connection to: '{}'".format(hostname))
            print("Error #3 in the connection to: '{}'. Check details".format(hostname))

    if connected:
        print('Device: "{}" connected, starting checks'.format(hostname))
        try:
            for cmd in cmds:
                output = uut.execute(cmd)
                store_command(hostname,cmd,output)
                logging.debug('Command: "{}" was stored for hostname: "{}"'.format(hostname,cmd))
        except Exception as e:
            logging.debug('Exception catched on Hostname: "{}" Cmd: "{}"\n{}'.format(hostname,cmd,e))
        print('Checks completed for device: "{}"'.format(hostname))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--file', help='Input File', required=True)
    parser.add_argument('-c','--credentials', help='Send vRouter creds in format user:pass', required=False)
    parser.add_argument('-j','--jump', action='store_true', help='Flag to ask for SSH Jumphost detail', required=False)
    parser.add_argument('-d','--detail', action='store_true', help='Flag to print verbose output from pyATS', required=False)
    parser.add_argument('-e','--environment', action='store_true', help='Flag to use env_variables', required=False)
    parser.add_argument('-r','--replace', action='store_true', help='Flag to use ssh-keygen -R to update ssh keys if jumphost is used',
                        required=False)
    parser.add_argument('-t','--type', help='Type of checks', choices=['pre','post'], required=True)
    args=parser.parse_args()

    file = args.file
    jump_bool = False
    global jump_replace
    jump_replace = False
    jump_ip = ""
    jump_port = ""
    jump_user = ""
    jump_pass = ""
    if args.jump :
        jump_bool = True
        if not args.environment:
            jump_ip = input("Enter Jumphost IP: ")
            jump_port = input("Enter Jumphost Port: ")
            jump_user = input("Enter Jumphost Username: ")
            jump_pass = getpass.getpass('Enter Jumphost Password:')
        else:
            message='''
Using environment variables for Jumphost. Check these if connection fails
    JUMP_IP
    JUMP_PORT
    JUMP_USER
    JUMP_PASS'''
            print(message)
            jump_ip = os.environ.get('JUMP_IP')
            jump_port = os.environ.get('JUMP_PORT')
            jump_user = os.environ.get('JUMP_USER')
            jump_pass = os.environ.get('JUMP_PASS')
        if args.replace:
            jump_replace = True

    if args.environment:
        user = os.environ.get('VROUTER_USER')
        password = os.environ.get('VROUTER_PASS')
        message='''
Using environment variables for device credentials. Check these if connection fails
    VROUTER_USER
    VROUTER_PASS
        '''
        print(message)
    elif args.credentials:
        creds = args.credentials
        user = creds.split(":")[0]
        password = creds.split(":")[1]
    else:
        print("Credential argument or environment not found, enter vRouter credentials/n")
        user = input("Enter vRouter Username:")
        password = getpass.getpass('Enter vRouter Password:')

    type_con = args.type
    global full_table
    global verbose_flag
    if args.detail:
        verbose_flag=True
    else:
        verbose_flag=False
    full_table = load_workbook(file)
    devices = full_table['Device Info']

    device_ips = []
    hostnames = []

    for i in range(1, len(list(list(devices.columns)[0]))):
        hostnames.append(list(list(devices.columns)[0])[i].value)

    for i in range(1, len(list(list(devices.columns)[1]))):
        device_ips.append(list(list(devices.columns)[1])[i].value)

    testbed = Create_Testbed(user,password,hostnames,device_ips,jump_bool,
                             jump_ip,jump_port,jump_user,jump_pass)

    commands = full_table['Commands']
    for i in range(1, len(list(list(commands.columns)[0]))):
        cmds.append(list(list(commands.columns)[0])[i].value)
    try:
        global tb
        tb = load(testbed)
    except Exception as e:
        logging.debug('Exception on load testbed:\n {}'.format(e))

    global outputs_folder
    if "pre" in type_con:
        os.system('rm -rf Precheck')
        outputs_folder = "Precheck"
        folder = "Precheck"
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))

    if "post" in type_con:
        os.system('rm -rf Postcheck')
        outputs_folder = "Postcheck"
        folder = "Postcheck"
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))


    result = pool_connection(12,hostnames,Testbed_routine)
    if result:
        print("Success")

if __name__ == "__main__":
    main()

