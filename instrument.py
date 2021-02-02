import subprocess
import os

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
  code = 'printf("========:%d:%d:%s:%d:========' + '\\' + 'n", timer_overflow_count, timer_overflow_count_overflow, __func__, 1);'

  # code = 'printf("Entrando na funcao: %s'+'\\'+'n"'+', __func__);'
  return code

def getExitFunctionCode(): 
  code = 'printf("========:%d:%d:%s:%d:========' + '\\' + 'n", timer_overflow_count, timer_overflow_count_overflow, __func__, 0);'
  # code = 'printf("Saindo da funcao: %s'+'\\'+'n"'+', __func__);'
  return code

def instrument(filename):  
  functions = find_functions(filename)
  instrumented_filename = filename.split('.')[0]+'inst.c'
  instf = open(instrumented_filename, 'w')
  instf.write('#include <util/delay.h>\n')
  instf.write('#include <stdio.h>\n')
  instf.write('#include "comm/uart.h"\n')
  instf.write('#include <avr/io.h>\n')
  instf.write('#include <avr/interrupt.h>\n\n')
  instf.write('volatile uint16_t timer_overflow_count;\n')
  instf.write('volatile uint16_t timer_overflow_count_overflow;\n\n')
  instf.write('void timer0_init(){\n')
  instf.write('\tTCCR0B |= (1 << CS02);\n')
  instf.write('\tTCNT0 = 0;\n')
  instf.write('\tTIMSK0 |= (1 << TOIE0);\n')
  instf.write('\tsei();\n')
  instf.write('\ttimer_overflow_count = 0;\n')
  instf.write('\ttimer_overflow_count_overflow = 0;\n')
  instf.write('}\n\n')
  instf.write('ISR(TIMER0_OVF_vect){\n')
  instf.write('\ttimer_overflow_count++;\n')
  instf.write('\tif (timer_overflow_count >= 32000){\n')
  instf.write('\t\ttimer_overflow_count_overflow++;\n')
  instf.write('\t\ttimer_overflow_count = 0;\n')
  instf.write('\t}\n')
  instf.write('}\n')

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
            prepare_comm = 'uart_init();\nstdout = &uart_output;\n_delay_ms(3000);\nputs("=======:inicio:=======");\nputs("=======:inicio:=======");\nputs("=======:inicio:=======");\ntimer0_init();\n'
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

  return functions



