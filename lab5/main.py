# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os.path
from sys import argv


def send_message(message, header, file_name, from_address, to_address, password, flag):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = header

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    with open(file_name, 'rb') as file:
        if (flag):
            attachment = MIMEApplication(file.read())
            attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
            msg.attach(attachment)

    # create server
    server = smtplib.SMTP('smtp.mail.ru')

    # шифрованное соединение
    server.starttls()

    # login in account
    server.login(msg['From'], password)

    # sending message
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

if __name__ == "__main__":


    message = 'hello'
    header = 'header'
    _, to_address, from_address, password, file_name = argv

    if (os.path.exists(file_name)):
        send_message(message, header, file_name, from_address, to_address, password, flag=True)
    else:
        send_message(message, header, file_name, from_address, to_address, password, flag=False)

    print("successfully sent email to " + to_address)