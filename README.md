# pyATS_collector

python script to run a routine using a manual testbed created on the fly from an excel sheet with hostname/IP tuple

usage: xr_version_smu.py [-h] -f FILE [-c CREDENTIALS] [-j] [-v] [-d] [-e] [-r]

## Arguments
[-h, --help] show this help message and exit

-f FILE, --file FILE  Input File (Mandatory)

[-c CREDENTIALS, --credentials] Optional argument for vRouter creds in format user:pass

[-j, --jump] Optional Flag to ask for SSH Jumphost detail

[-v, --vmc] Optional Flag to ommit check CSCwa80752 on VMC vRouters

[-d, --detail] Optional Flag to print verbose output from pyATS

[-e, --environment] Flag to use enviornment variables

[-r, --replace] Optional Flag to use ssh-keygen -R to update ssh keys if jumphost is used
