#!/usr/bin/env python3

import os
import sys
import subprocess
import io
import datetime

# def file_change(output_name : str, res : str):
#     print('func file_change() is started')
#     with open(output_name, 'w') as output_file:
#         output_file.write(res)
#     print("job is done")


leader_file = sys.argv[-1]
del sys.argv[-1]
env_dict = os.environ
env_dict['LEADER_PARAM_FILE']=leader_file
#file_change('AAexp.txt',leader_file)

with open("AAexp_2.txt", 'a+') as my_file:
    my_file.write("\n------------------------------------\n")
    my_file.write("wrapper_bielevel.py:\ntime: {}\n".format(datetime.datetime.now()))

cmd_str=' '.join(sys.argv[1:])
# print(cmd_str)
with open("AAexp_2.txt", 'a+') as my_file:
    my_file.write("cmd_str:\n {}\n\t end_cmd\n".format(cmd_str))
arguments=cmd_str.split(' ')
p = subprocess.run(arguments, env=env_dict, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout_text = io.TextIOWrapper(io.BytesIO(p.stdout), encoding='utf-8') #оборачиваем p.stdout чтобы работал readline()

with open("AAexp_2.txt", 'a+') as my_file:
    my_file.write("stdout_text:\n {}\n\t end_text\n".format(stdout_text))

f = open('AAexp_2.txt','a+')
while True:
    line = stdout_text.readline().strip()
    # print(line)
    f.write(line + '\n')
    if line == '':
        break
    log_line = line

f.write("log_line:\n" + log_line + '\n--------------------------------------------------\n')
f.close()

print(log_line)