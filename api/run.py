import subprocess
import json

venv_python = '/usr/local/bin/python3.10'

script_path = '/Users/macbookpro/nigeb_server/api/test_import.py'

input_value = 'testscopy3.csv'

# completed_process = subprocess.run([venv_python,script_path,input_value],capture_output=True,text=True)
subprocess.run([venv_python,script_path,input_value])

# output = json.loads(completed_process.stdout.strip())

# print(output["surname"])



# completed_process.stdout.strip().split('/n')
# print(output[1] + "wddwdwd")