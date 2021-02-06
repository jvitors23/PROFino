#!/usr/bin/python3
from instrument import *
from monitor import *
from make import *
import sys 
import os
import shutil
import subprocess

# Instrumentar o programa de entrada
filepath = sys.argv[1]

if '/' in filepath:
  shutil.copy(filepath, './')
  filename = filepath.split('/')[-1]
else:
  filename = filepath

functions = instrument(filename)

# Compilar o arquivo instrumentado e fazer upload pro arduino
inst_target = filename.split('.')[0]+'inst'
compile_and_upload_to_arduino(inst_target)

if '/' in filepath:
  os.remove(filename)

# Iniciar monitoramento
monitor(functions)