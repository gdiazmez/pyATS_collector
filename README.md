# pyATS_collector

python script to run a routine using a manual testbed created on the fly from an excel sheet with hostname/IP tuple

usage: xr_version_smu.py [-h] -f FILE [-c CREDENTIALS] [-j] [-v] [-d] [-e] [-r]

##arguments
-h, --help show this help message and exit
 -f FILE, --file FILE  Input File
 -c CREDENTIALS, --credentials CREDENTIALS Send vRouter creds in format user:pass
 -j, --jump            Flag to ask for SSH Jumphost detail
 -v, --vmc             Flag to ommit check CSCwa80752 on VMC vRouters
 -d, --detail          Flag to print verbose output from pyATS
 -e, --environment     Flag to use env_variables
 -r, --replace         Flag to use ssh-keygen -R to update ssh keys if jumphost is used
