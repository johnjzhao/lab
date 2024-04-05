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

f = open('numerated_text.txt')
fp = open('res_text.txt', 'w')
contents = f.readlines()
contents.sort(key=sort_lines)
for i in contents:
    fp.write(i)
f.close()
fp.close()


def citi_map():
    list1 = []
    num = 1
    with open("numerated_text.txt", 'r') as file:
        for k in file:
            if re.search("War", str(k)):
                num_lines = "{0:0>2}".format(num) + "," + k
                list1.append(num_lines)
                num +=1
    num = 1
    with open("numerated_text.txt", 'r') as file:
        for k in file:
            if re.search("Par", str(k)):
                num_lines = "{0:0>1}".format(num) + "," + k
                list1.append(num_lines)
                num +=1
    num = 1
    with open("numerated_text.txt", 'r') as file:
        for k in file:
            if re.search("Lon", str(k)):
                num_lines = "{0:0>1}".format(num) + "," + k
                list1.append(num_lines)
                num +=1
    with  open("numerated_text.txt", "w") as file:
        for i in list1:
            file.write(i)

def sort1_lines(line):
    fields = line.strip().split(',')
    amount = str(fields[3])
    return amount

f = open('res_text.txt')
fp = open('res1_text.txt', 'w')
contents = f.readlines()
contents.sort(key=sort1_lines)
fixed_col = []
for i in contents:
    #fp.write(i)
    fields = i.strip().split(',')
    seqno = str(fields[3])
    num = str(fields[0])
    citi = str(fields[1])
    photo = str(fields[2])
    fixed_col.append(citi)
    fixed_col.append(num)
    fixed_col.append(photo)
    fixed_col.append("\n")
#print (fixed_col)
for j in fixed_col:
    fp.write(j)
    #print (seqno,citi,num,photo)
f.close()
fp.close()

text_lines()
#citi_map()
