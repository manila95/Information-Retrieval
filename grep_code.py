"""

__file__

    grep_search.py

__description__

    This file contains the method of using grep to search for queries using python

__author__

    Kaustubh Mani <kaustubh3095@gmail.com>

"""

import time
from subprocess import Popen, PIPE

Query = open('query.txt','r')

for lines in Query :
    final_set = set()
    Start = time.time()
    query_id = lines[0:3]
    lines = lines[4:]
    words = lines.split(' ')
    final_set = set()
    count = 0
    
    for word in words:
        process=Popen(["grep",'-lr',word,'alldocs'],stdout=PIPE)
        s=str(process.stdout.read())
        temp=s.split("\n")
        if count == 0:
            final_set=set(temp)
            count = 1
        else:
            final_set = final_set & set(temp)
    final_answer = list(final_set)
    print len(final_answer)
    
    file = open('output_grep.txt','a')
    for answers in final_answer :
        if answers == "":
            continue
        file.write(str(query_id)+"  "+str(answers.split("/")[-1])+"\n")
    file.close()
    
    file = open('Time_grep.txt','a')
    file.write(str(query_id)+"  "+str(time.time()-Start)+"\n")
    file.close()