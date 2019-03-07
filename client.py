#   Tested on python 3.7.2
#   Written by David O'Donohue, constructive feedback is welcome.

import os
import smtplib
import mimetypes
import getpass
import time

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def clear():
    os.system('cls||clear')

msg = MIMEMultipart()

# Get login and name
clear()
FROM = input("Username: ")
if '@' not in FROM:
    # you didn't include the domain
    FROM += "@anu.edu.au"
PASSWORD = getpass.getpass()

print("Authenticating... Please wait")

# connect to server
server = smtplib.SMTP("smtp-mail.outlook.com",587)  ## TODO: edit if not using an outlook account
server.starttls()

#log in
try:
    server.login(FROM, PASSWORD)
except smtplib.SMTPHeloError:
    print("The server didn’t reply properly to the HELO greeting.")
    exit()
except smtplib.SMTPAuthenticationError:
    print("The server didn’t accept the username/password combination.")
    exit()
except smtplib.SMTPNotSupportedError:
    print("The AUTH command is not supported by the server.")
    exit()
except smtplib.SMTPException:
    print("No suitable authentication method was found.")
    exit()
except Exception as e:
    print(str(e))
    exit()

print("Logged in successfully")

msg['From'] = FROM
TO = input("To: ")
if '@' not in TO:
    TO += "@anu.edu.au"
msg['To'] = TO
msg['Subject'] = input("Subject: ")
message = ''
print("Type your email here. Press ` and enter to end the email")
m = input()
while (m != '`'):
    message += m + "\n"
    m = input()
print("Sending now...")

msg.attach(MIMEText(message, 'plain'))
server.sendmail(msg['From'],msg['To'],msg.as_string())

print("Sent mail to "+ msg['To'])

server.quit()
time.sleep(2)