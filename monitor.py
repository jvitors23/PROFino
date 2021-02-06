import serial
import time
from tabulate import tabulate

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
					
					func_monitor[call_stack[-1][0]]['time'] += (timestamp - call_stack[-1][1])
				
				call_stack.append([func_name, timestamp])

			else:
				last_func_entry = call_stack.pop()
				
				# o tempo de entrada da função anterior passa a ser o atual
				if func_name != 'main':
					call_stack[-1][1] = timestamp
				
				func_monitor[func_name]['time'] += (timestamp - last_func_entry[1])
	

		if start and (time.time() - ini_interval) >= 2 : 
			print("\033c")

			print("\
				___________ ___________  _             \n\
				| ___ \ ___ \  _  |  ___(_)           \n \
				| |_/ / |_/ / | | | |_   _ _ __   ___  \n\
				|  __/|    /| | | |  _| | | '_ \ / _ \ \n\
				| |   | |\ \  \_/ / |   | | | | | (_) |\n\
				\_|   \_| \_|\___/\_|   |_|_| |_|\___/ ")														
			
		
			print_list = []
			maior = 0
			for func in func_monitor.keys():
				if len(func) > maior: 
					maior = len(func)
				print_list.append([func,str(func_monitor[func]['calls']), str(func_monitor[func]['time'])[0:8], str((func_monitor[func]['time']/timestamp)*100)[0:8]])

			print('===========================================================================================')
			print('{0:<{1}}{2:<25}{3:<25}{4:<25}'.format('function', maior + 10, 'calls', 'time (s)', 'time(%)'))
			print('-------------------------------------------------------------------------------------------')

			for func in print_list:
				print('{0:<{1}}{2:<25}{3:<25}{4:<25}'.format(func[0], maior + 10, func[1], func[2], func[3]))

			ini_interval = time.time()
			print('-------------------------------------------------------------------------------------------')
			print('total execution time (s) ' + str(timestamp)[0:8])
			print('===========================================================================================')
