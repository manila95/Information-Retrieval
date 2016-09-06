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


def precision_and_recall(output_file,filename):
    """
    Args:
        output_file: file containing result for queries
    """
    
    output = open("output.txt",'r')
    query = open("query.txt","r")
    est_output = open(output_file)
    query_ID = []
    prerec = open(filename,"a")
    prerec.write("queryID" + " " + "precision" + " " + "recall" + "\n")
    for line in query:
        query_ID.append(line.split()[0])
    e_out = pd.DataFrame(columns = ["q_ID","Doc"])
    o_out = pd.DataFrame(columns=["q_ID","Doc"])
    query = []
    docs = []
    for line in est_output:
        query.append(line.split()[0])
        docs.append(line.split()[1])
    e_out['q_ID'] = query
    e_out["Doc"] = docs
    query = []
    docs = []
    for line in output:
        query.append(line.split()[0])
        docs.append(line.split()[1])
    o_out['q_ID'] = query
    o_out["Doc"] = docs
        
    for q_ID in query_ID:
        estimated = list(e_out[e_out['q_ID'] == q_ID]["Doc"])
#         print len(estimated)
        true = list(o_out[o_out["q_ID"] == q_ID]["Doc"])
#         print len(true)
        precision = len(list(set(estimated).intersection(set(true))))/float(len(estimated))
        recall = len(list(set(estimated).intersection(set(true))))/float(len(true))
        prerec.write(str(q_ID) + " " + str(precision) + " " + str(recall) + "\n")
    prerec.close()
    output.close()
    est_output.close()

if __name__ == "__main__":
	precision_and_recall("output_inverted_index.txt","inverted_index_precision_and_recall.txt")
	precision_and_recall("output_grep.txt","grep_precision_and_recall.txt")
	precision_and_recall("output_elastic.txt","elastic_search_precision_and_recall.txt")