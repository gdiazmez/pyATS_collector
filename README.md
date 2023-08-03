# pyATS Collector

python scripts to run a routine using a manual testbed created on the fly from an excel sheet with hostname/IP tuple

## Pre-requisites
pip install genie

pip install pyats

pip install openpyxl

pip install rich

## Quick Demo

![](https://github.com/pyATS_collector/demo.gif)

## XR full check
Collect Lo0 Ipv4/IPv6, SR Prefix SID, XR Version, SMU list and license registration status from file with tuples

usage: full_info.py [-h] -f FILE [-c CREDENTIALS] [-j] [-d] [-e] [-r]

FILE is an xlsx filled with hostname/ip tuples, see device_info.xlsx example

If no -c (credential) flag used, script would ask interactively for them


To improve execution time and avoid interacting with script use environment variables (-e flag):

VROUTER_USER = String with username of CLI on device

VROUTER_PASS = String with password of CLI on device


If -j flag is used (for jumphost usage):

JUMP_IP = String with IP address of jumphost

JUMP_PORT = Int with TCP port of jumphost CLI 

JUMP_USER = String with username for Jumphost

JUMP_PASS = String with password for Jumphost

### Arguments
[-h, --help] show this help message and exit

-f FILE, --file FILE  Input File (Mandatory)

[-c CREDENTIALS, --credentials] Optional argument for vRouter creds in format user:pass

[-j, --jump] Optional Flag to ask for SSH Jumphost detail

[-d, --detail] Optional Flag to print verbose output from pyATS

[-e, --environment] Flag to use enviornment variables

[-r, --replace] Optional Flag to use ssh-keygen -R to update ssh keys if jumphost is used


## XR version and SMU check
Check Version, SMU and license from file with tuples

usage: xr_version_smu.py [-h] -f FILE [-c CREDENTIALS] [-j] [-v] [-d] [-e] [-r]

### Arguments
[-h, --help] show this help message and exit

-f FILE, --file FILE  Input File (Mandatory)

[-c CREDENTIALS, --credentials] Optional argument for vRouter creds in format user:pass

[-j, --jump] Optional Flag to ask for SSH Jumphost detail

[-v, --vmc] Optional Flag to ommit check CSCwa80752 on VMC vRouters

[-d, --detail] Optional Flag to print verbose output from pyATS

[-e, --environment] Flag to use enviornment variables

[-r, --replace] Optional Flag to use ssh-keygen -R to update ssh keys if jumphost is used

## Pre and Post Check
Collect output per device and per command and sump into a structured .txt file per device

usage: checks.py [-h] -f FILE [-c CREDENTIALS] [-j] [-d] [-e] [-r] -t {pre,post}

### Arguments
  [-h, --help]           show this help message and exit
  
  -f FILE, --file FILE  Input File
  
  [-c CREDENTIALS, --credentials] CREDENTIALS
                        Send vRouter creds in format user:pass
                        
  [-j, --jump]            Flag to ask for SSH Jumphost detail
  
  [-d, --detail]          Flag to print verbose output from pyATS
  
  [-e, --environment]     Flag to use env_variables
  
  [-r, --replace]         Flag to use ssh-keygen -R to update ssh keys if jumphost is used
  
  -t {pre,post}, --type {pre,post}
                        Type of checks
