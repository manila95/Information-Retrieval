"""

__file__

    Query_processing_inverted_index.py

__description__

    This file contains the code for processing queries using inverted index

__author__

    Kaustubh Mani <kaustubh3095@gmail.com>

"""


import os
import sys
import re
import nltk
import operator
import pickle as pkl
import progressbar
import time
import numpy as np
import pandas as pd
from inverted_index import *

with open("indexed_docs.p","r") as dict_file:
    dictionary = pkl.load(dict_file)

def process_query(query_file):
    
    f = open(query_file,"r")
    query_ID = []
    query_result = []
    Time = []
    q_res = pd.DataFrame(columns = ["queryID","Time"])
    for j,query in enumerate(f):
        result = []
        q_ID = query.split()[0]
        query_ID.append(q_ID)
        query = preprocessing_txt(query)
        query = query.split()
        START = time.time()
        for i,word in enumerate(query):
            
            if i == 0:
                for i in dictionary[word].items():
                    result.append(i[0])
            else:
                temp = []
                for i in dictionary[word].items():
                    temp.append(i[0])
                result = list(set(result).intersection(set(temp)))
        END = time.time()
        f1 = open("output_inverted_index.txt",'a')
#         print str(q_ID) + "%d" % len(result)
        for res in result:
            f1.write(str(q_ID) + " " + str(res) + "\n")
        f1.close() 
        Time.append(float(END - START))
        query_result.append(result)
    q_res["queryID"] = query_ID
    q_res["Time"] = Time
    q_res.to_csv("inverted_index.csv",encoding='utf-8')
    result = pd.DataFrame(columns = ["query_ID","relevant_docs"])
    result["query_ID"] = query_ID
    result["relevant_docs"] = query_result
    return result

if __name__ == "__main__":
    query_file = "query.txt"
    process_query(query_file)
