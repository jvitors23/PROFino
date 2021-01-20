import subprocess

def find_functions(): 
  out = subprocess.Popen(['ctags-universal', '--c-types=f','-o', '-', '--fields=+ne', 'main.c'], 
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
      'start_line': int(elts[4].split(':')[1]),
      'end_line': int(elts[6].split(':')[1])
    })

  with open('main.sym') as f: 
    lines = f.readlines()
    for line in lines: 
      name = line.replace('\n', '').split(' ')[2]
      address = line.replace('\n', '').split(' ')[0]
      for f in functions_list:       
        if f['name'] == name: 
          f['address'] = address

  return functions_list

def instrument():
  functions = find_functions()
  print(functions)

