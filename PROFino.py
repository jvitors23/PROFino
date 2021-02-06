#!/usr/bin/python3
import os, sys, getopt, shutil
import instrument, make, monitor

# Valida se os parâmetros foram passados corretamente pela linha de comando
def evaluate_args():
	short_options = 'hc:p:'
	long_options = ['help', 'source=', 'port=']
	mandatory_args = 2 # É obrigatório informar o '-c/--source' e o '-p/--port'

	try:
		args, values = getopt.getopt(sys.argv[1:], short_options, long_options)

		if len(args) < mandatory_args:
			args = [('-h', '')]

		filename, port = '', ''
		for arg, value in args:
			if arg in ('-h', '--help'):
				print ('Displaying help')
				sys.exit(0) # Se por acaso o parâmetro de ajuda foi passado, não faz nada senão exibir a ajuda
			elif arg in ('-c', '--source'):
				filename = value
			elif arg in ('-p', '--port'):
				port = value

		return filename, port
	except getopt.error as e:
		print (str(e))
		sys.exit(2)

# ...
def main():
	filepath, port = evaluate_args()
	
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
