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
import time
import os
import logging
import requests

from bs4 import BeautifulSoup
from sys import exit


URL_DUCK_DNS = 'https://www.duckdns.org/update?domains=${domains}&token=${token}&ip=${ip}'
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
    DOMAINS = os.environ["UPDATE_DUCK_DNS_DOMAIN"]
    URL_DUCK_DNS = URL_DUCK_DNS.replace('${domains}', DOMAINS)
    URL_DUCK_DNS = URL_DUCK_DNS.replace('${token}', TOKEN)
except KeyError:
    logging.info('there are no environment variables')
    exit()
    



page_response = requests.get(PAGE_MY_IP, timeout=5)
page = requests.get("https://www.cual-es-mi-ip.net/").text
page_content = BeautifulSoup(page_response.content, "html.parser")
tag = page_content.find_all('span', attrs={'class':'big-text font-arial'})
my_ip = tag[0].get_text()

logging.info("My IP: " + my_ip)

URL_DUCK_DNS = URL_DUCK_DNS.replace('${ip}', my_ip)

logging.info("DUCK_URL: " + URL_DUCK_DNS)
#page_response = requests.get(URL_DUCK_DNS, timeout=5)


logging.info('Finished')
