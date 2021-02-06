#!/usr/bin/python3
import sys, getopt
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
	filename, port = evaluate_args()
	source = filename.split('.')[0] + '.inst' # "arquivo.inst.c"

	functions = instrument.instrument(filename) # Instrumenta o código-fonte original
	make.run(source) # Compila o código-fonte instrumentado e faz upload para o Arduino
	monitor.monitor(functions) # Inicia o 'live-profiling' do código instrumentado sendo executado no Arduino

if __name__ == '__main__':
	main()
