import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#http://stackoverflow.com/a/74084/1747721

from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()


def sendmsg(fullname, receiver, msg):
    try:
        muser = quetzal_config['smtp_user']
        smtpserver = smtplib.SMTP(quetzal_config['smtp_server'], int(quetzal_config['smtp_port']))
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(muser, quetzal_config['smtp_pwd'])
        header = 'To:' + receiver + '\n' + 'From: ' + muser + '\n' + 'Subject:Correo de Cliente\n'
        msg = header + '\n Has recibido un mensaje de ' + fullname + ', con correo: ' + receiver + ', contenido del mensaje: ' + msg + '\n\n'
        smtpserver.sendmail(muser, muser, msg)
        smtpserver.close()
        return True
    except Exception as e:
        return None