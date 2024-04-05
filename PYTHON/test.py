#!/bin/python3
import re
import sys

def text_lines():
    c = open('test-input-01.txt', 'r')
    list_of_lines = c.readlines()
    c.close()
    number = 1
    numbered_list_of_lines = []
    for i in list_of_lines:
        numbered_lines = "{0:0>2}".format(number) + ", " + i
        numbered_list_of_lines.append(numbered_lines)
        number += 1
    f = open("numerated_text.txt", "w")
    for i in numbered_list_of_lines:
        f.write(i)
    f.close()
    with  open("numerated_text.txt", "r") as file:
        filedata = file.read()

    filedata = filedata.replace('.', ',.')
    with  open("numerated_text.txt", "w") as file:
         file.write(filedata)


def sort_lines(line):
    line_fields = line.strip().split(',') 
    amount = str(line_fields[4]) 
    return amount 

with  open("numerated_text.txt", "r") as f:

#f = open('numerated_text.txt') 
    contents = f.readlines() 
    contents.sort(key=sort_lines) 
    filedata = str(contents)
#f.close() 
with  open("sorted_text.txt", "w") as file:
    for i in contents:
        file.write(i)
  
  
def ord_lines():
    fp = open('sorted_text.txt')
    data = fp.readlines()
    fix_line = []
    for line in data:
        line_fields = line.strip().split(',')
        timestm = str(line_fields[4])
        citi = str(line_fields[3])
        photo = str(line_fields[2])
        num = str(line_fields[0])
        #fix_line.append(timestm)
        fix_line.append(citi)
        fix_line.append(',')
        fix_line.append(photo)
        fix_line.append(',')
        fix_line.append(num)
        fix_line.append('\n')
        #print(citi,photo,num)
    #print(fix_line)
    with  open("sorted_text.txt", "w") as file:
        for i in fix_line:
            file.write(i)
    fp.close()

text_lines()
ord_lines()
#sort_lines()
