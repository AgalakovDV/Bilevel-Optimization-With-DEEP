#!/usr/bin/python

import os
import sys
import subprocess
import io

leader_file = sys.argv[-1]
del sys.argv[-1]
env_dict = os.environ
env_dict['LEADER_PARAM_FILE']=leader_file
cmd_str=' '.join(sys.argv[1:])
# print(cmd_str)
arguments=cmd_str.split(' ')
p = subprocess.run(arguments, env=env_dict, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout_text = io.TextIOWrapper(io.BytesIO(p.stdout), encoding='utf-8') #оборачиваем p.stdout чтобы работал readline()

while True:
    line = stdout_text.readline().strip()
    # print(line)
    if line == '':
        break
    log_line = line

print(log_line)
