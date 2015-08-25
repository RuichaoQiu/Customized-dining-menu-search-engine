import os
import re 
import json 
import timeit
import sys
import MySQLdb
from datetime import datetime
from elasticsearch import Elasticsearch


first = True
city = {}

class rev:
    def __init__(self):
        self.r = {}
        self.d = {}

class reviewdetail:
    def __init__(self,t,r):
        self.text = t
        self.stars = r

def findsmallest(p):
    mini = p[0][0]
    mininum = 0
    for i in xrange(1,len(p)):
        if p[i][0] < mini:
            mini = p[i][0]
            mininum = i
    return mininum

def getcity():
    global city
    conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user="root", # your username
                          passwd="", # your password
                          db="dining", charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    cursor.execute("SELECT business_id,city FROM dm_restaurant")
    li = cursor.fetchall()
    for row in li:
        city[row[0]] = row[1]

def queryresult(mc,loc):
    global first
    global city
    if first:
        getcity()
        first = False
    es = Elasticsearch()
    trainPredictions = rev()
    for it in mc:
        td = {}
        line = it.name
        res = es.search(index="project_index", q=line,size=1000)
        #print("Got %d Hits:" % res['hits']['total'])
        
        for hit in res['hits']['hits']:
            #print(hit["_source"]["doc_id"])
            doc_id = hit["_source"]["business_id"].encode('utf-8').strip()
            score = float(hit["_score"])
            text = hit["_source"]["text"].encode('utf-8').strip()
            stars = float(hit["_source"]["stars"])
            if doc_id not in trainPredictions.r:
                trainPredictions.r[doc_id] = [reviewdetail(text,stars)]
            else:
                trainPredictions.r[doc_id].append(reviewdetail(text,stars))
            if doc_id not in td:
                td[doc_id] = [[score,stars]]
            else:
                td[doc_id].append([score,stars])
        for item in td:
            sc = 0.0
            st = 0.0
            for i in xrange(len(td[item])):
                sc += float(td[item][i][0])
                st += float(td[item][i][1])
            sc = sc / float(len(td[item]))
            st = st / float(len(td[item]))
            if item not in trainPredictions.d:
                trainPredictions.d[item] = [sc*it.fav,st*it.fav]
            else:
                trainPredictions.d[item] = [trainPredictions.d[item][0]+sc*it.fav,trainPredictions.d[item][1]+st*it.fav]
    tt = [[0.0,0.0,""] for i in xrange(10)]
    for item in trainPredictions.d:
        index = findsmallest(tt)
        if trainPredictions.d[item][0] > tt[index][0]:
            if item in city and (loc == "All" or loc == city[item]):
                tt[index][0] = trainPredictions.d[item][0]
                tt[index][1] = trainPredictions.d[item][1]
                tt[index][2] = item
    res = [[0.0,""] for i in xrange(10)]
    for item in tt:
        index = findsmallest(res)
        if item[1] > res[index][0]:
            res[index][0] = item[1]
            res[index][1] = item[2]
    res.sort(key=lambda elem: elem[0], reverse=True)
    tot = 0.0
    for it in mc:
        tot += it.fav
    for it in res:
        it[0] = it[0] / tot
    ans = []
    for item in res:
        ans.append([item[1],item[0],trainPredictions.r[item[1]][:]])
    return ans

