import serial
import time

try:
	arduino = serial.Serial("/dev/ttyACM0",timeout=1)
except:
	print('Please check the port')

def clean(L):#L is a list
	newl=[] #initialising the new list
	for i in range(len(L)):
		temp=L[i][2:]
		newl.append(temp[:-5])
	return newl

def monitor():
	iniCount = 0
	tempoInicial = 0
	last_overflow_counter = 0
	tempoFinal = 0
	iteracoes = 0
	start = False
	while True:
		rawdata=[]
		rawdata.append(str(arduino.readline()))
		msg = clean(rawdata)[0]
		print(msg)		

		if msg == 'inicio':
			iniCount += 1
		if iniCount == 3 and not start:
			print('[INFO] - Iniciando motiramento')
			start = True	
			tempoInicial = time.time()
			continue

		if start and msg != '' and msg != 'inicio':
			overflow = int(msg.split(":")[1])
			overflow_counter = int(msg.split(":")[3])
			print('tempo decorrido ')
			print(str(overflow_counter*65000*4.096/1000 + overflow*4.096/1000) + 's')
	
	
monitor()

	





