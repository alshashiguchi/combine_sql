import sys
import re

arg = sys.argv
branch_target = arg[1]
branch_origin = arg[2]

new_file = len(arg) > 3 and arg[3] or ''

import subprocess

def command_diff():
  return f'git diff --name-only {branch_target} $(git merge-base {branch_target} {branch_origin}) | grep -e .*SQL$ -e .*sql'

def command_set_branch():
  return f'git checkout {branch_target}'

def validate_path(path):
  expression = '^(\.\.\/(?:\.\.\/)*)?(?!.*?\/\/)(?!(?:.*\/)?\.+(?:\/|$)).+sql$'

  if re.compile(expression).match(path) == None:
    return False
  
  return True;

def subprocess_cmd(command):
  process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
  proc_stdout = process.communicate()[0].strip()  
  return proc_stdout.splitlines()
  
def concat_files():
  if validate_path(new_file) == False:    
    print('Path invalid')
    return 

  subprocess_cmd(command_set_branch())
  files = subprocess_cmd(command_diff())  
  with open(new_file, 'w') as outfile:
    for fname in files:    
      print(f'Read: {fname}')
      with open(fname, encoding="ISO-8859-1") as infile:
        for line in infile:
          outfile.write(line)
  print(f'Created file: {new_file}')
  


concat_files()
