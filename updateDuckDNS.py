#! /usr/bin/python3
'''
   Copyright [2019] [Raúl Eduardo González Argote]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Created on Aug 19, 2019

@author: rafex

'''
import os
import logging
import requests
import re

from sys import exit


URL_DUCK_DNS = 'https://www.duckdns.org/update?domains=${sub_domains}.duckdns.org&token=${token}&ip=${ip}'
PAGE_MY_IP ='https://www.cual-es-mi-ip.net/'
try:
    PATH_LOGS=os.environ["UPDATE_DUCK_DNS_LOGS"]
except KeyError:
    print('log path not found creating in default folder')
    
try:
    logging.basicConfig(
        filename=PATH_LOGS+'/updateDuckDNS.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')
except:
    logging.basicConfig(
        filename='/tmp/updateDuckDNS.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')
        
logging.info('Started')

try:
    TOKEN = os.environ["UPDATE_DUCK_DNS_TOKEN"]
    SUB_DOMAINS = os.environ["UPDATE_DUCK_DNS_SUB_DOMAIN"]
    URL_DUCK_DNS = URL_DUCK_DNS.replace('${sub_domains}', SUB_DOMAINS)
    URL_DUCK_DNS = URL_DUCK_DNS.replace('${token}', TOKEN)
except KeyError:
    logging.warning('there are no environment variables')
    exit()

page_link ='https://domains.google.com/checkip'
page_response = requests.get(page_link, timeout=5)
my_ip = page_response.text

logging.info("My IP: " + my_ip)

try:
    PATH_INSTALL=os.environ["PATH_INSTALL_SCRIPT_PYTHON_DUCK_DNS"]
except Exception:
    logging.warning('not found enviroment PATH_INSTALL_SCRIPT_PYTHON')
    
replace_ip = True
try:
    if(os.path.isfile(PATH_INSTALL+"/my_ip.txt") == True):
        file = open(PATH_INSTALL+"/my_ip.txt", "r+")
        ip_file = file.read()
        logging.info('my_ip.txt: ' + ip_file.strip())
        if(ip_file.strip() != my_ip.strip()):
            ip_file = re.sub(ip_file.strip(), my_ip.strip(), ip_file)
            file.seek(0)
            file.write(ip_file)
            file.close()
            logging.info('update ip')
        else:
            replace_ip = False
            logging.info('not update ip')
    else:
        logging.info('create file my_ip.txt')
        file = open(PATH_INSTALL+"/my_ip.txt","w") 
        file.write(my_ip) 
        file.close()  
    
except Exception as ex:
    logging.warning(ex)
    logging.warning('not found file my_ip.txt')
    exit()

if (replace_ip):
    URL_DUCK_DNS = URL_DUCK_DNS.replace('${ip}', my_ip)
    logging.info("DUCK_URL: " + URL_DUCK_DNS)
    
    page_response = requests.get(URL_DUCK_DNS, timeout=5)
    
    logging.info("Response: " + page_response.text)


logging.info('Finished')
