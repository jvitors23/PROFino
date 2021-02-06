import os, subprocess

def run(source, port):
  make(source, port, target='all')
  make(source, port, target='program')
  make(source, port, target='clean')
  os.remove(source + '.c') # Apaga o código instrumentado

# Executa uma determinada regra ou a regra 'all', caso nada seja informado
def make(source, port, target='all'):
  out = subprocess.Popen(['make', target,'SOURCE=' + source, 'AVRDUDE_PORT=' + port], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))
