# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:01:05 2016

@author: test

"""
import os
import numpy

size_list=[]
index_list=[]
for i in range(0,100):
    size_list.append(-1)
    index_list.append(-1)

for i in range(1,2000000):
    if i<=9:
        size=os.path.getsize("./dataset_HTML/AA/wiki_0"+str(i)+".html")
    else:
        size=os.path.getsize("./dataset_HTML/AA/wiki_"+str(i)+".html")
    for j in range(0,100):
        if(size>=size_list[j]):
            size_list[j]=size
            index_list[j]=i
            sorted_index=numpy.argsort(size_list)
            newlist=[index_list[sorted_index[i]] for i in range(0,100)]
            index_list=newlist
            size_list=sorted(size_list)
            break
        
outfile=open("./dataset_HTML/topic_indexes1.txt","w")
for i in range(0,100):
    outfile.write(str(index_list[i])+"\n")

outfile.close()
