#!/usr/bin/python3
from instrument import *
from monitor import *
from make import *
import sys 
import subprocess

# Instrumentar o programa de entrada
filename = sys.argv[1]
instrument(filename)

# Compilar o arquivo instrumentado e fazer upload pro arduino
inst_target = filename.split('.')[0]+'inst'
compile_and_upload_to_arduino(inst_target)

# Iniciar monitoramento
monitor()