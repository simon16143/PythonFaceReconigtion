import cv2
import os

#correo electronico
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def EnviarCorreoIntruso():
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

	with open('intruso.jpg', 'rb') as fp:
		img = MIMEImage(fp.read())
		img.add_header('Content-Disposition', 'attachment', filename="intruso.jpg")
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
		print('finalizo envio de correo')




dataPath = 'Reconocimiento Facial/Data'
imagePaths = os.listdir(dataPath)
##array con los nombres de las carpetas para imprimir en el reconocimiento
print('imagePaths=',imagePaths)

#EigenFaceRecognizer_create(), FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Leyendo el modelo
face_recognizer.read('modeloReconocimeintoFacial.xml')

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

while True:
	ret,frame = cap.read()
	if ret == False: break
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = gray.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		rostro = auxFrame[y:y+h,x:x+w]
		rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
		result = face_recognizer.predict(rostro)

		cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
		if result[1] < 70:
			cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		else:
			cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
			#enviar correo
			#rostro = auxFrame[y:y+h,x:x+w]
			#rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
			#cv2.imwrite('intruso.jpg',rostro)
			#EnviarCorreoIntruso()
		
	cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
