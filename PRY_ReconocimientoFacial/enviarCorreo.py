#https://ichi.pro/es/como-enviar-un-correo-electronico-con-archivos-adjuntos-en-python-188994555473139

import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


smtp_server = "smtp.gmail.com"
port = 25 
sender_email = "noresponder@aliar.com.co"
password = ""


from_addr = 'noresponder@aliar.com.co'
to = 'jairo.lancheros@aliar.com.co'

msg = MIMEMultipart()
msg['Subject'] = 'Intruso Detectado'
msg['From'] = from_addr
msg['To'] = to

msgText = MIMEText('<b>Intruso Detectado</b>', 'html')
msg.attach(msgText)

with open('rotro_0.jpg', 'rb') as fp:
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', 'attachment', filename="rotro_0.jpg")
    msg.attach(img)
context = ssl.create_default_context()
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo()
    server.starttls(context=context) 
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(from_addr, to, msg.as_string())
except Exception as e:
    print(e)
finally:
    server.quit() 
    print('finalizo')

