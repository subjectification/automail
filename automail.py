#   INSTRUCTIONS: Place this file in a directory, with other directories that have the names of the classes
#   you are tutoring, within each directory there should be files with uXXXXXXX.ext, where ext is the file extension.

#   Example: automail.py is in a directory, the only other thing in the directory is another directory called
#   COMP1100, within the COMP1100 directory are the feedback files for each student, and each file is named
#   something like u5130810.pdf

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

# Get path
path = os.path.dirname(os.path.abspath(__file__))

# Get login and name
clear()
FROM = input("Username: ")
if '@' not in FROM:
    # you didn't include the domain
    FROM += "@anu.edu.au"
PASSWORD = getpass.getpass()
NAME = input("Your name: ")

print("Authenticating... Please wait.")

# connect to server
server = smtplib.SMTP("smtp-mail.outlook.com",587)  ## TODO: edit if not using an outlook account
server.starttls()

#log in
try:
    server.login(FROM, PASSWORD)
except smtplib.SMTPHeloError:
    clear()
    print("The server didn’t reply properly to the HELO greeting.")
    exit()
except smtplib.SMTPAuthenticationError:
    clear()
    print("The server didn’t accept the username/password combination.")
    exit()
except smtplib.SMTPNotSupportedError:
    clear()
    print("The AUTH command is not supported by the server.")
    exit()
except smtplib.SMTPException:
    clear()
    print("No suitable authentication method was found.")
    exit()
except Exception as e:
    clear()
    print(str(e))
    exit()

print("Successfully logged in. Sending emails...")

for CLASS in os.listdir(path):
    class_path = os.path.join(path,CLASS)
    if CLASS != __file__ and CLASS != ".git" and os.path.isdir(class_path):
        for student in os.listdir(class_path):
            student_path = os.path.join(class_path, student)
            msg = MIMEMultipart()
            msg['From'] = FROM
            student_uid = student.split(".")[0]
            msg['To'] = student_uid + "@anu.edu.au"
            msg['Subject'] = "["+CLASS+"] assignment feedback"
            BODY = "Hi,\n\nAttached is your feedback for the latest %s assignment.\n\nPlease let me know if you have any questions or concerns.\n\nKind regards,\n%s" % (CLASS, NAME)
            msg.attach(MIMEText(BODY, 'plain'))
            ctype, encoding = mimetypes.guess_type(student_path)
            maintype, subtype = ctype.split('/', 1)
            fp = open(student_path,'rb')
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=student)
            msg.attach(attachment)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print("Emailed " + student_uid)

server.quit()
time.sleep(2)