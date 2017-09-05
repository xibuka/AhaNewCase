#!/usr/bin/python3

import configparser
import argparse

# get the arguments from command line                     
parser = argparse.ArgumentParser()                        
parser.add_argument("--fromAddr",  \
        help="send from email address.")                  
parser.add_argument("--fromAddrPW",\
        help="password of the send from email address.")  
parser.add_argument("--rhuser",    \
        help="RH account to access unified web site")     
parser.add_argument("--rhpass",    \
        help="password for RH account")                   
args = parser.parse_args()                                
args = vars(args)                                         

config = configparser.RawConfigParser()

config['config'] = {'fromAddr'  : args['fromAddr'],
                    'fromAddrPW': args['fromAddrPW'],
                    'rhuser'    : args['rhuser'],
                    'rhpass'    : args['rhpass']}

# Writing our configuration file to 'example.cfg'
with open('/etc/freshcase/auth.conf', 'w') as configfile:
        config.write(configfile)

#  for read
## config2 = configparser.RawConfigParser()       
## config2.read('./auth.cfg')                     
##                                               
## FROM_ADDR=config2["config"]['fromAddr']
## FROM_ADDR_PW=config2['config']['fromAddrPW']       
## RH_ADDR=config2['config']['rhuser']
## RH_ADDR_PW=config2['config']['rhpass']
## 
## print(FROM_ADDR, FROM_ADDR_PW, RH_ADDR, RH_ADDR_PW)
                                                  

