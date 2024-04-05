#!/bin/python3
import re
import sys
import os

def text_lines():
    with  open("test-input-01.txt", "r") as file:
        res = [sub.replace('.', ', .') for sub in file]
        list_val0 = []
        for i in res:
            list_val0.append(i)

    list_val1 = []
    for line in list_val0:
        list_val1.append(" ".join(line.split()[1:]) + "\n")

    list_of_lines = list_val1
    number = 1
    num_lines = []
    for i in list_of_lines:
        numbered_lines = "{0:0>2}".format(number) + ", " + i
        num_lines.append(numbered_lines)
        number += 1
    contents = num_lines
    contents.sort(key=sort_lines)
    f = open("fixed_text.txt", "w")
    for j in contents:
        f.write(j)
    f.close()

def sort_lines(line):
    line_fields = line.strip().split(',')
    count = str(line_fields[3])
    return count

def sort_fixes(line):
    line_fields = line.strip().split(',')
    amount = str(line_fields[1])
    return amount

def citi_map():
    list1 = []
    num = 1
    with open("fixed_text.txt", 'r') as file:
        for k in file:
            if re.search("War", str(k)):
                num_lines = "{0:0>2}".format(num) + ", " + k
                list1.append(num_lines)
                num +=1
    num = 1
    with open("fixed_text.txt", 'r') as file:
        for k in file:
            if re.search("Par", str(k)):
                num_lines = "{0:0>1}".format(num) + ", " + k
                list1.append(num_lines)
                num +=1
    num = 1
    with open("fixed_text.txt", 'r') as file:
        for k in file:
            if re.search("Lon", str(k)):
                num_lines = "{0:0>1}".format(num) + ", " + k
                list1.append(num_lines)
                num +=1
    contents = list1
    contents.sort(key=sort_fixes)
    ordered_list = []
    for i in contents:
        ordered_list.append(i)

    data = ordered_list
    fix_line = []
    for line in data:
        line_fields = line.strip().split(',')
        citi = str(line_fields[3])
        num = str(line_fields[0])
        photo = str(line_fields[2])
        sn = str(line_fields[1])
        fix_line.append(citi)
        fix_line.append(num)
        fix_line.append(photo)
        fix_line.append('\n')
    f = open("final_text.txt", "w")
    for j in fix_line:
        f.write(j)
    f = open("final_text.txt")
    filedata = f.read()
    filedata = filedata.replace(' ', '')
    f = open("final_text.txt", "w")
    f.write(filedata)
    print(filedata)
    f.close()

    filelist = ['final_text.txt', 'fixed_text.txt']
    for f in filelist:
        os.remove(f) 

text_lines()
citi_map()
