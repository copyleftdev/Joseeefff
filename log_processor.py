#!/usr/bin/env python
import os
import time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def collect_files(rf, fe):
    """Collects files pass rf= root folder, fe = file extention it recursively collects files
    with a pattern of file_with_underscores it only returns file that have not been seen
    in the processed file log pf.txt example: collect_files("test_data/", ".txt")"""
    matches = []
    processed_files = set(line.strip() for line in open("pf.txt", 'r'))
    for root, dirnames, filenames in os.walk(rf):
        for filen in filenames:
            if filen.endswith(fe) and '_' in filen:
                if filen not in processed_files:
                    with open("pf.txt", 'a+') as log:
                        log.write(filen+"\n")
                        matches.append(os.path.join(root, filen))
    return matches

def send_mail(send_from, send_to, subject, text,
              files=None, server='127.0.0.1'):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="{}"' % basename(f)
        msg.attach(part)

        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        print smtp.ehlo
        smtp.close()

def main():
    a = collect_files("test_data/", ".txt")
    send_mail(send_from="dj@cnn.com", send_to=["don.johnson@j2.com", "dj@codetestcode.io"],
          subject="test email", text=" yet another sample log files", files=a)

if __name__ == '__main__':
    main()
