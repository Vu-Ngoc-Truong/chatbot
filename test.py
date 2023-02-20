#!/usr/bin/env python3
# -*-coding:utf-8-*-

# abc = "12.34"
# index = abc.rfind(".")
# print(abc[index-1])
# print(abc[index+1])
# digit1 = abc[index - 1]
# digit2 = abc[index + 1]

# print(digit1.isdigit())
# print(digit2.isdigit())

# import subprocess

# subprocess.run(["ls", "-l"])

import subprocess

result = subprocess.run(["ls"], stdout=subprocess.PIPE)
output = result.stdout.decode("utf-8")
print(output)