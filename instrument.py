import subprocess

out = subprocess.Popen(['ctags', '-x', '--c-types=f', 'main.c'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
stdout, stderr = out.communicate()
functions = stdout.decode("utf-8").split('\n')
functions.remove('')
functions_list = []

for f in functions: 
  elts = f.split(' ')
  out = []
  for elt in elts: 
    if elt != '':
      out.append(elt)
  functions_list.append({
    'name': out[0], 
    'line': int(out[2])
  })

with open('main.sym') as f: 
  lines = f.readlines()
  for line in lines: 
    name = line.replace('\n', '').split(' ')[2]
    address = line.replace('\n', '').split(' ')[0]
    for f in functions_list:       
      if f['name'] == name: 
        f['address'] = address

print(functions_list)

