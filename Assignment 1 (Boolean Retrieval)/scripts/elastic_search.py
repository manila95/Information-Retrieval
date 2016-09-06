"""

__file__

    elastic_search.py

__description__

    This file contains Elastic Search implementation for boolean retrieval

__author__

    Kaustubh Mani <kaustubh3095@gmail.com>

"""




import os
from datetime import datetime
import elasticsearch
import time

es = elasticsearch.Elasticsearch('http://localhost:9200/',timeout=30,max_retries=10,retry_on_timeout=True)
request={
    "settings":{
    "number_of_shards":"1",
    "number_of_replicas":"0",
    "analysis": {
      "analyzer": {
        "full_name": {
          "filter": [
            "standard",
            "lowercase",
            "asciifolding"
          ],
            "type": "custom",
            "tokenizer": "standard"
                }
              }
        }
    }
}

try:
    es.delete_index('doc')
except:
    pass
res=es.create(index='doc',doc_type='text',body=request)
print(res)

file_paths=[]
directory_path = 'alldocs'
for root,dirs,files in os.walk(directory_path):
        for f in files:
            file_paths.append(os.path.join(root,f))
            
count=1
for file in file_paths:
    f=open(file,'rb')
    s=str(f.read())
    res=es.create(index='doc',doc_type='text',body={'content':s,'name':file})
    print(count)
    print(res)
    count=count+1

t0=time.time()
List=[]
Dist={}
query_file_path = 'query.txt'
f=open(query_file_path)
for line in f:
    print(line)
    line=line.strip()
    words=line.split(" ")
    #print(words)
    index=words[0]
    try:
        query=words[2]
        line=words[3:]
    except:
        continue
    for x in words:
        query=query+" "+x
    print(query)
    res=es.search(index='doc',doc_type='text',body={"from":0,"size":300,"query":{"match":{"content":query}}})
    print(index)
    List.append(index)
    print(res['hits']['total'])
    rest=[]
    for doc in res['hits']['hits']:
        if (doc['_source']['name']) not in rest:
            rest.append(doc['_source']['name'])
        if len(rest)>60:
            break
    Dist[index]=rest
f.close()

t1=time.time()
f2=open('output_elastic.txt','a')
f2.write(str(t1-t0))
f2.write('\n')
for x in List:
    f2.write(x)
    f2.write('\n')
    for z in Dist[x]:
        f2.write(z)
        f2.write('\n')
    f2.write('\n')
f2.close()