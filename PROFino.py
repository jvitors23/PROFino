#!/usr/bin/python3
import os, sys, getopt, shutil
import instrument, make, monitor
from GUI import initGUI

# Exibe a mensagem de ajuda caso os argumentos passados não sejam válidos
def displayHelp(): 
	print('Usage: ')
	print('{0:<20}{1:}'.format('-c --source', 'Path to source code.'))
	print('{0:<20}{1:}'.format('-p --port', 'USB port where the Arduino is connected, Ex: /dev/ttyACM0, /dev/ttyUSB0.'))
	print('{0:<20}{1:}'.format('-g --graphic', 'Flag that indicates if the program must run in GUI mode.'))
	sys.exit(0) # Se por acaso o parâmetro de ajuda foi passado, não faz nada senão exibir a ajuda

# Valida se os parâmetros foram passados corretamente pela linha de comando
def evaluate_args():
	short_options = 'hc:p:g'
	long_options = ['help', 'source=', 'port=', 'graphic']

	try:
		args, values = getopt.getopt(sys.argv[1:], short_options, long_options)
		
		filename, port = '', ''
		graphic = False
		for arg, value in args:
			if arg in ['-h', '--help']:
				displayHelp()
			elif arg in ['-c', '--source']:
				filename = value
			elif arg in ['-p', '--port']:
				port = value
			elif arg in ['-g', '--graphic']:
				graphic = True

		if not graphic: 
			if filename == '' or port == '': 
				print('Invalid arguments!')
				displayHelp()

		return filename, port, graphic
	except getopt.error as e:
		print (str(e))
		sys.exit(2)

# ...
def main():
	
	filepath, port, graphic = evaluate_args()
	
	if graphic: 
		initGUI(filepath, port)	
	else:
		if '/' in filepath:
			shutil.copy(filepath, './')
			filename = filepath.split('/')[-1]
		else:
			filename = filepath

		source = filename.split('.')[0] + '.inst' # "arquivo.inst.c"
		functions = instrument.instrument(filename) # Instrumenta o código-fonte original
		make.run(source, port) # Compila o código-fonte instrumentado e faz upload para o Arduino
		
		if '/' in filepath:
			os.remove(filename)
		
		monitor.monitor(functions, port) # Inicia o 'live-profiling' do código instrumentado sendo executado no Arduino

if __name__ == '__main__':
	main()
