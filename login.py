#!/usr/bin/env python3
import cgi
import os
import secret
from templates import login_page
from templates import secret_page

def parse_cookies(cookie_string):
    result = {}
    if len(cookie_string) > 1:
        cookies = cookie_string.split(";")
        for cookie in cookies:
            split_cookie = cookie.split("=")
            result[split_cookie[0].strip()] = split_cookie[1]

    return result

os_cookies = os.environ["HTTP_COOKIE"]
if os_cookies is not None:
    cookies = parse_cookies(os_cookies)

form = cgi.FieldStorage()

correct_username, correct_password = secret.userpass()
username = form.getfirst("username")
password = form.getfirst("password")


header = ""
header += "Content-Type: text/html\r\n"     # HTML is following


body = ""



if username is not None or ('logged' in cookies and cookies['logged'] == "true"):
# if username is not None:
    if username is None:
        if 'username' in cookies:
            username = cookies['username']
        else:
            username = "none"
    if password is None:
        if 'password' in cookies:
            password = cookies['password']
        else:
            password = "none"
    body += secret_page(username, password)
    if username == correct_username and password == correct_password:
        header += "Set-Cookie: correct_login=true\r\n"
    else:
        header += "Set-Cookie: correct_login=false\r\n"
    header += "Set-Cookie: logged=true\r\n"
    header += "Set-Cookie: cookie=nom\r\n"
    header += "Set-Cookie: username=" + username + "\r\n"
    header += "Set-Cookie: password=" + password + "\r\n"
    body += "<h1>A terrible secret</h1>"
else:
    body += login_page()

print(header)
print()
print(body)
