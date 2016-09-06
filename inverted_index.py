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

def tokenizer(text):
    text = re.sub("[^a-zA-Z]+", " ", text)
    tokens = nltk.tokenize.word_tokenize(text)
    return tokens        

def preprocessing_txt(text):
    
    tokens = tokenizer(text)
    stemmer = nltk.stem.porter.PorterStemmer()
    stopwords = nltk.corpus.stopwords.words('english')
    new_text = ""
    for token in tokens:
        token = token.lower()
        if token not in stopwords:
#             print token
            new_text += stemmer.stem(token)
            new_text += " "
        
    return new_text

def inverted_index():
    """
    Creates a dictionary of words as key and name of the documents as items
    """
    inverted = {}
    docs_indexed = 0
    list_doc = os.listdir("./alldocs")
    total = len(list_doc)
    point = total / 100
    increment = total / 100
    indexer = {}
    for doc in list_doc:
#         sys.stdout.write('\r')
        doc_loc = "./alldocs/" + str(doc)
        file_doc = open(doc_loc, "r")
        file_doc = preprocessing_txt(file_doc.read())
        tokens = tokenizer(file_doc)
        for word in tokens:
            if not inverted.__contains__(word):
                count = 1
                doclist = {}
                doclist[doc] = 1
                inverted[word] = doclist
            else:
                if doc in inverted[word]:
                    doclist = inverted[word]
                    doclist[doc] += 1
                    inverted[word] = doclist
                else:
                    count = 1
                    doclist = inverted[word]
                    doclist[doc] = count
                    inverted[word] = doclist
                    
        docs_indexed += 1
        i = docs_indexed
        if(i % (point) == 0):
            sys.stdout.write("\r[" + "=" * (i / increment) + ">" +  " " * ((total - i)/ increment) + "]" +  str(100*i / float(len(list_doc))) + "%")
            sys.stdout.flush()
    return inverted
                
                
if __name__ == "__main__":
    with open("indexed_docs.p","wb") as handle:
        indexed_docs = inverted_index()
        pkl.dump(indexed_docs, handle)

              
        
        
        
        