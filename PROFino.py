#!/usr/bin/python3
import sys, subprocess
import instrument, make, monitor

def main():
	filename = sys.argv[1]
	source = filename.split('.')[0] + 'inst'

	functions = instrument.instrument(filename) # Instrumenta o código-fonte original
	make.run(source) # Compila o código-fonte instrumentado e faz upload para o Arduino
	monitor.monitor(functions) # Inicia o 'live-profiling' do código instrumentado sendo executado no Arduino

if __name__ == '__main__':
	main()
