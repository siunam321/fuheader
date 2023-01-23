#!/usr/bin/env python3

import requests
from threading import Thread
from time import sleep
import argparse

class Requester:
    def __init__(self, url, wordlistPath):
        self.__url = url
        self.__wordlistPath = wordlistPath

    def readFileAndSendRequest(self):
        counter = 0
        with open(self.__wordlistPath, 'r') as file:
            for header in file:
                # Prevent our fuzzing is being cached.
                # Otherwise it won't find the valid HTTP header
                cacheBuster = f'?buster=buster{counter}'

                thread = Thread(target=self.sendRequest, args=(header.strip(), cacheBuster))
                thread.start()
                sleep(0.02)
                counter += 1

    def sendRequest(self, cleanHeader, cacheBuster):
        payload = {cleanHeader: 'web-cache-poisoning-header-fuzzing.com'}
        finalURL = self.__url + cacheBuster

        requestResult = requests.get(finalURL, headers=payload)
        print(f'[*] Trying HTTP header: {cleanHeader:40s}', end='\r')

        if 'web-cache-poisoning-header-fuzzing.com' in requestResult.text:
            print(f'[+] Found valid HTTP header: {cleanHeader}')


def argumentParser():
    parser = argparse.ArgumentParser(description='A Python3 script that fuzzes HTTP headers.')
    parser.add_argument('-u', '--url', metavar='URL', help='The full URL of the target website. For example: https://0a6d0005037e473ec06c22bc000300b7.web-security-academy.net/', required=True)
    parser.add_argument('-w', '--wordlist', metavar='File', help='The absolute of the wordlist. For example: /usr/share/seclists/Discovery/Web-Content/BurpSuite-ParamMiner/lowercase-headers', required=True)

    return parser.parse_args()

def banner():
    bannerString = f'+{"-" * 15}Banner{"-" * 15}+'
    bannerString += '''
 ______     _                    _           
|  ____|   | |                  | |          
| |__ _   _| |__   ___  __ _  __| | ___ _ __ 
|  __| | | | '_ \ / _ \/ _` |/ _` |/ _ \ '__|
| |  | |_| | | | |  __/ (_| | (_| |  __/ |   
|_|   \__,_|_| |_|\___|\__,_|\__,_|\___|_|

Author: siunam (https://siunam321.github.io/)

'''
    bannerString += f'+{"-" * 15}Banner{"-" * 15}+'

    return bannerString

def main():
    # Prepare arguments
    args = argumentParser()

    print(banner())
    
    requester = Requester(args.url, args.wordlist)
    requester.readFileAndSendRequest()

if __name__ == '__main__':
    main()