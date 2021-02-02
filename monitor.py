import serial
import time

def clean(L):
	newl=[] 
	for i in range(len(L)):
		temp=L[i][2:]
		newl.append(temp[:-5])
	return newl

def monitor():
	try:
		arduino = serial.Serial("/dev/ttyACM0",timeout=1)
		arduino.flushInput()
		arduino.flushOutput()
	except:
		print('Please check the port')

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

		if msg != '' and len(msg.split(':')) > 0 and msg.split(':')[1] == 'inicio':
			iniCount += 1
		if iniCount == 3 and not start:
			print('[INFO] - Iniciando motiramento')
			start = True	
			tempoInicial = time.time()
			continue

		if start and msg != '':
			overflow = int(msg.split(":")[1])
			overflow_counter = int(msg.split(":")[2])
			func_name = msg.split(":")[3]
			tipo = int(msg.split(":")[4])
			if tipo == 1: 
				print('entrando em '+func_name+ ' - tempo atual ' + str(overflow_counter*32000*4.096/1000 + overflow*4.096/1000) + 's')
			else:
				print('saindo de '+func_name+ ' - tempo atual ' + str(overflow_counter*32000*4.096/1000 + overflow*4.096/1000) + 's')





