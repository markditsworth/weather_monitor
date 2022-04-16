import smtplib
import os

def sendMail(to_addr=None, from_addr=None, subject=None, body="", auth_password=None):
    # text = """
    # From: %s
    # To: %s
    # Subject: %s
    # %s
    # """%(from_addr, to_addr, subject, body)
    text = body
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()
        server_ssl.login(from_addr, auth_password)
        server_ssl.sendmail(from_addr, to_addr, text)
        server_ssl.close()
        print("sent email")
        return False
    except Exception as e:
        print(str(e))
        return str(e)