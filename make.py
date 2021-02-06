import os, subprocess

def run(source):
  make(source, target='all')
  make(source, target='program')
  make(source, target='clean')
  os.remove(source + '.c') # Apaga o código instrumentado

# Executa uma determinada regra ou a regra 'all', caso nada seja informado
def make(source, target='all'):
  out = subprocess.Popen(['make', target,'SOURCE=' + source], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))
