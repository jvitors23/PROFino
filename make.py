import os, subprocess

# Executa um source especificado do Makefile
def all(source):
  compile(source)
  upload(source)
  clean(source)


def compile(source):
  out = subprocess.Popen(['make', 'SOURCE=' + source], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))


def upload(source):
  out = subprocess.Popen(['make', 'program', 'SOURCE=' + source], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))


def clean(source):
  out = subprocess.Popen(['make', 'clean', 'SOURCE=' + source], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))
  os.remove(source+'.c')
