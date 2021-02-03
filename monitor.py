import serial
import time

def clean(L):
	newl=[] 
	for i in range(len(L)):
		temp=L[i][2:]
		newl.append(temp[:-5])
	return newl

def monitor(functions):
	try:
		arduino = serial.Serial("/dev/ttyACM0",timeout=1)
		arduino.flushInput()
		arduino.flushOutput()
	except:
		print('Please check the port')
	
	call_stack = []
	func_monitor = {}

	for func in functions: 
		func_monitor[func['name']] = {
			'calls': 0, 
			'time': 0
		}
	

	exec_history = []
	iniCount = 0
	tempoInicial = 0
	last_overflow_counter = 0
	tempoFinal = 0
	timestamp = 0
	iteracoes = 0
	start = False
	ini_interval = 0

	while True:
		rawdata=[]
		rawdata.append(str(arduino.readline()))
		msg = clean(rawdata)[0]
		
		if msg != '' and len(msg.split(':')) > 1 and msg.split(':')[1] == 'inicio':
			iniCount += 1
		if iniCount == 3 and not start:
			ini_interval = time.time()
			print('[INFO] - Iniciando monitoramento')
			start = True	
			tempoInicial = time.time()
			continue

		if start and msg != '':
			overflow = int(msg.split(":")[1])
			overflow_counter = int(msg.split(":")[2])
			func_name = msg.split(":")[3]
			tipo = int(msg.split(":")[4])
			timestamp = overflow_counter*32000*4.096/1000 + overflow*4.096/1000
			if tipo == 1: 
				func_monitor[func_name]['calls'] += 1

				if func_name != 'main':
					exec_history.append({
						'function': call_stack[-1][0], 
						't_ini': call_stack[-1][1],
						't_fim': timestamp 
					})
					func_monitor[call_stack[-1][0]]['time'] += (timestamp - call_stack[-1][1])
				
				call_stack.append([func_name, timestamp])

			else:
				if func_name != 'main':
					last_func_entry = call_stack.pop()
					exec_history.append({
						'function': func_name, 
						't_ini': last_func_entry[1],
						't_fim': timestamp 
					})
					# o tempo de entrada da função anterior passa a ser o atual
					call_stack[-1][1] = timestamp

					func_monitor[func_name]['time'] += (timestamp - last_func_entry[1])
		
		# print(exec_history)

		if start and (time.time() - ini_interval) >= 5 : 
			print("\033c")
			print('===============================================================================================')
			print('function\t\tcalls\t\t\ttime (s)\t\t\ttime (%)')
			print('-----------------------------------------------------------------------------------------------')
			
			for func in func_monitor.keys():
				print(func +'\t\t\t'+ str(func_monitor[func]['calls']) + '\t\t\t' + str(func_monitor[func]['time'])[0:8]+'\t\t\t'+str((func_monitor[func]['time']/timestamp)*100)[0:8] )

			ini_interval = time.time()
			print('-----------------------------------------------------------------------------------------------')
			print('total execution time (s) ' + str(timestamp)[0:8])
			print('===============================================================================================')
