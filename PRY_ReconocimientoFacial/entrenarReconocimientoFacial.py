import cv2
#manejo de carpetas y archivos
import os
import numpy as np
#ruta Data
dataPath = 'Reconocimiento Facial/Data'
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir
	print('Leyendo las imágenes')

	for fileName in os.listdir(personPath):
		
		labels.append(label)
		#leer las imagines, 0 al final para transformar a escala de grises
		facesData.append(cv2.imread(personPath+'/'+fileName,0))
		#image = cv2.imread(personPath+'/'+fileName,0)
		#cv2.imshow('image',image)
		#cv2.waitKey(10)
	label = label + 1

# Métodos para entrenar el reconocedor
#instalar: python -m pip install --user opencv-contrib-python
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# Entrenando el reconocedor de rostros
face_recognizer.train(facesData, np.array(labels))
# Almacenando el modelo obtenido
face_recognizer.write('modeloReconocimeintoFacial.xml')
