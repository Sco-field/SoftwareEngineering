#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Enoch time:2018/10/22 0031
 
import time
import re
import operator
from string import punctuation           
import sys
from collections import Counter

def ProcessLine0(line,counts):
    
 
    line = re.sub('[^a-z]', '', line)
    for ch in line:
        counts[ch] = counts.get(ch, 0) + 1
    return counts
 
def CountLetter(path):
    file = open(path, 'r')
    wordsCount = 0
    alphabetCounts = {}
    for line in file:
        alphabetCounts = ProcessLine0(line.lower(), alphabetCounts)
    wordsCount = sum(alphabetCounts.values())
    alphabetCounts = sorted(alphabetCounts.items(), key=lambda k: k[0])
    alphabetCounts = sorted(alphabetCounts, key=lambda k: k[1], reverse=True)
    for letter, fre in alphabetCounts:
    	print("|\t{:15}|{:<11.2%}|".format(letter, fre / wordsCount))
 
    file.close()
   

    
def CountWords1(file_name,n,stopName,verbName):
    print("File name:" + sys.path[0] + "\\" + file_name)
    if (stopName != None):
        stopflag = True
    else:
        stopflag = False
    if(verbName != None):
        verbflag = True
    else:
        verbflag = False
    
    with open(file_name) as f:
        txt = f.read()
    txt = txt.lower()
    if(stopflag == True):
        with open(stopName) as f:
            stoplist = f.readlines()
    pattern = r"[a-z][a-z0-9]*"
    wordList = re.findall(pattern,txt)
    totalNum = len(wordList)
    tempc = Counter(wordList)
    if (stopflag == True):
        for word in stoplist:
            word = word.replace('\n','')
            del tempc[word]
    dicNum = dict(tempc.most_common(n))
    if (verbflag == True):
        totalNum = 0
        verbDic = {}
        verbDicNum = {}
        with open(verbName) as f:
            for line in f.readlines():
                key,value = line.split('')
                verbDic[key] = value.replace('\n','').split(',')
                verbDicNum[key] = tempc[key]
                for word in verbDic[key]:
                    verbDicNum[key] += tempc[word]
                totalNum += verbDicNum[key]
        verbDicNum = sorted(verbDicNum.items(), key=lambda k: k[0])
        verbDicNum = sorted(verbDicNum, key=lambda k: k[1], reverse=True)
    dicNum = sorted(dicNum.items(), key=lambda k:k[0])
    dicNum = sorted(dicNum, key=lambda k:k[1], reverse=True)

    if (verbflag == True):
        print(verbDicNum[:n])
    else:
        print(dicNum)



def CountPhrases(file_name,n,stopName,verbName,k):
    print("File name:" + sys.path[0] + "\\" + file_name)
    totalNum = 0
    if (stopName != None):
        stopflag = True
    else:
        stopflag = False
    if(verbName != None):
        verbflag = True
    else:
        verbflag = False

    with open(file_name) as f:
        txt = f.read()
    txt = txt.lower()
    txt = re.sub(r'[\s|\']+',' ',txt)
    pword = r'(([a-z]+ )+[a-z]+)'  # extract sentence
    pattern = re.compile(pword)
    sentence = pattern.findall(txt)
    txt = ','.join([sentence[m][0] for m in range(len(sentence))])
    if(stopflag == True):
        with open(stopName) as f:
            stoplist = f.readlines()
    pattern = "[a-z]+[0-9]*"
    for i in range(k-1):
        pattern += "[\s|,][a-z]+[0-9]*"
    wordList = []
    for i in range(k):
        if( i == 0 ):
            tempList = re.findall(pattern, txt)
        else:
            wordpattern = "[a-z]+[0-9]*"
            txt = re.sub(wordpattern, '', txt, 1).strip()
            tempList = re.findall(pattern, txt)
        wordList += tempList
    tempc = Counter(wordList)
    if (stopflag == True):
        for word in stoplist:
            word = word.replace('\n','')
            del tempc[word]
    dicNum = {}
    if (verbflag == True):
        verbDic = {}
        with open(verbName) as f:
            for line in f.readlines():
                key,value = line.split(' -> ')
                for tverb in value.replace('\n', '').split(','):
                    verbDic[tverb] = key
                verbDic[key] = key
        for phrase in tempc.keys():
            if (',' not in phrase):
                totalNum += 1
                verbList = phrase.split(' ')
                normPhrase = verbList[0]
                for verb in verbList[1:]:
                    if verb in verbDic.keys():
                        verb = verbDic[verb]
                    normPhrase += ' ' + verb
                if (normPhrase in dicNum.keys()):
                    dicNum[normPhrase] += tempc[phrase]
                else:
                    dicNum[normPhrase] = tempc[phrase]
    else:
        phrases = tempc.keys()
        for phrase in phrases:
            if (',' not in phrase):
                dicNum[phrase] = tempc[phrase]
                totalNum += tempc[phrase]
    dicNum = sorted(dicNum.items(), key=lambda k: k[0])
    dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
   
    print(dicNum[:n])
    
