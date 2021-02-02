import subprocess
import os

def compile_and_upload_to_arduino(target):
  
  out = subprocess.Popen(['make', 'TARGET='+target], 
          stdout=subprocess.PIPE, 
          stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))

  #upload to arduino
  out = subprocess.Popen(['make', 'program', 'TARGET='+target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))

  out = subprocess.Popen(['make', 'clean', 'TARGET='+target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))
  os.remove(target+'.c')
