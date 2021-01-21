import subprocess

def find_functions(filename): 
  out = subprocess.Popen(['ctags-universal', '--c-types=f','-o', '-', '--fields=+ne', filename], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()

  functions = stdout.decode("utf-8").split('\n')
  functions.remove('')
  functions_list = []
  
  for f in functions: 
    elts = f.split('\t')
    functions_list.append({
      'name': elts[0], 
      'start_line': int(elts[4].split(':')[1]) - 1,
      'end_line': int(elts[6].split(':')[1]) - 1
    })

  with open(filename, 'r') as file: 
    lines = file.readlines()
    for func in functions_list:
      if '{' in lines[func['start_line']]: 
        continue
      else: 
        for i in range(func['start_line'], len(lines)):
          if '{' in lines[i]:
            func['start_line'] = i 
            break

  # with open(filename.replace(".c", ".sym")) as f: 
  #   lines = f.readlines()
  #   for line in lines: 
  #     name = line.replace('\n', '').split(' ')[2]
  #     address = line.replace('\n', '').split(' ')[0]
  #     for f in functions_list:       
  #       if f['name'] == name: 
  #         f['address'] = address

  return functions_list

def getEntryFunctionCode(): 
  code = 'printf("Entrando na funcao: %s'+'\\'+'n"'+', __func__);'
  return code

def getExitFunctionCode(): 
  code = 'printf("Saindo da funcao: %s'+'\\'+'n"'+', __func__);'
  return code

def instrument(filename):  
  functions = find_functions(filename)
  instrumented_filename = filename.split('.')[0]+'inst.c'
  instf = open(instrumented_filename, 'w')
  instf.write('#include <util/delay.h>\n')
  instf.write('#include <stdio.h>\n')
  instf.write('#include "comm/uart.h"\n')
  instf.write('#include "comm/send.h"\n')
  with open(filename, 'r') as file: 
    lines = file.readlines()
    for i in range(len(lines)): 
      change = False
      pos = None
      main = False
      for func in functions:
        if i == func['start_line']:
          if func['name'] == 'main': 
            main = True
          change = True
          pos = 'start'
        if i == func['end_line']:
          change = True
          pos = 'end'
      if change: 
        if pos == 'start': 
          if main: 
            prepare_comm = 'uart_init();\nstdout = &uart_output;\n_delay_ms(2000);\nputs("inicio");\nputs("inicio");\nputs("inicio");'
            lines [i] = lines[i] + prepare_comm + '\n' + getEntryFunctionCode() + '\n'
          else:  
            lines [i] = lines[i] + getEntryFunctionCode() + '\n'
        if pos == 'end': 
          lines [i] = getExitFunctionCode() + '\n' + lines[i]
    
    for func in functions:      
      for i in range(func['start_line'], func['end_line']):
        if 'return' in lines[i] :
          lines [i] = getExitFunctionCode() + '\n' + lines[i]
    
    instf.writelines(lines)
  instf.close()

  # compile instrumented file
  inst_target = instrumented_filename.split('.')[0]
  out = subprocess.Popen(['make', 'TARGET='+inst_target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))

  #upload to arduino
  out = subprocess.Popen(['make', 'program', 'TARGET='+inst_target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  print(stdout.decode("utf-8"))

