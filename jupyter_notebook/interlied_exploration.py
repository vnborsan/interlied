import collections
from collections import OrderedDict
from collections import Counter
import copy
import csv
import glob
from heapq import nlargest
import itertools
from itertools import chain
from IPython.display import clear_output
from IPython.display import HTML
import matplotlib
import matplotlib.pyplot as plt
from music21 import*
from music21 import text, stream
import pandas as pd
import nltk as nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import ngrams
import numpy as np
import operator
from operator import itemgetter
import os
import random
import re 
import string
import warnings
warnings.simplefilter('ignore')

def interlied_int_explore_lyric(csv):
    df_intervals=pd.read_csv(csv)
    tpls=[]
    for i,r in df_intervals.iterrows():
        idx=i
        itr=r["interval"]
        lyrc=r["lyric_tokens"]
        l=re.sub("[']",'', lyrc)
        tpl=(idx, (str(l)+" / "+str(itr)))
        tpls.append(tpl)

    dct = Counter(j for i,j in tpls)

    kys=[]
    vls=[]

    for k in dct.keys():
        kys.append(str(k))

    for v in dct.values():
        vls.append(int(v))

    res = {}

    for key in kys:
        for value in vls:
            res[key] = value
            vls.remove(value)
            break

    new_dict={ky:vl for (ky,vl) in res.items() if vl > 1}
    return new_dict

#######################################
#######################################
#######################################

def interlied_int_explore_lyric_token(csv, c_name, l_entry, intr_entry):
    instance=0
    df=pd.read_csv(csv)
    for i,r in df.iterrows():
        idx=i
        #PARAMETERS / COLUMNS
        itr=r["interval"]
        lyrc=r["lyric_tokens"]
        cmp=r["composer"]
        
        #INPUTS
        c= str(c_name)
        q = str(l_entry)
        intr=str(intr_entry)
        
        if (itr == intr) and (q in lyrc) and (c in cmp):
            instance=instance+1
            print("**INSTANCE NUMBER",instance)
            display(df.iloc[int(idx)])
        else:
            continue
    print("Done.")

#######################################
#######################################
#######################################


def interlied_search_pattern_lyric_composer(csv, pattern_string, composer_name, lyric_query):
    instance=0
    df_ngrams=pd.read_csv(csv)
    for i1,r in df_ngrams.iterrows():
        idx1=i1
        ptrn=r["pattern"]
        lyrc=r["lyric_tokens"]
        cmp=r["composer"]
        p = str(pattern_string)
        c=str(composer_name)
        q =str(lyric_query)
        if (p == ptrn) and (q in lyrc):
            instance=instance+1
            print("**INSTANCE NUMBER",instance)
            display(df_ngrams.iloc[int(idx1)])
        else:
            continue
    print("Done.")


#######################################
#######################################
#######################################


def interlied_search_melody_rhythm_composer(csv, pattern_string, rhythm_pattern, composer_name):
    instance=0
    df_ngrams=pd.read_csv(csv)
    for i1,r in df_ngrams.iterrows():
        idx1=i1
        ptrn=r["pattern"]
        rhythm=r["duration"]
        cmp=r["composer"]
        p = str(pattern_string)
        c=str(composer_name)
        q =str(rhythm_pattern)
        if (p == ptrn) and (q == rhythm):
            instance=instance+1
            print("**INSTANCE NUMBER",instance)
            display(df_ngrams.iloc[int(idx1)])
        else:
            continue
    print("Done.")

#######################################
#######################################
#######################################


def interlied_words_count(csv):
    df_lyric=pd.read_csv(csv)
    wrds_l = []
    composer_l = []
    title_l = []
    tonality_l= []
    word_count_l=[]
    words_df={}

    for i in range(0, len(df_lyric)):
        composer_l.append(df_lyric.composer[i])
        title_l.append(df_lyric.title[i])
        tonality_l.append(df_lyric.score_key_s[i])
        list_of_lyric=df_lyric.lyric_tokens[i]
        list_of_lyric=list_of_lyric.split()
        wrds_l.append(collections.Counter(list_of_lyric).most_common(5))


    for m in range (len(title_l)):
        word_count_l+=[[composer_l[m], title_l[m], tonality_l[m], (wrds_l)[m]]]

    words_df=pd.DataFrame(word_count_l)
    words_df=words_df.rename(columns={0: "composer", 1: "title", 2:"key", 3: "most common words"})

    with pd.option_context('display.max_rows', 100, 'display.max_columns', 10, 'max_colwidth', 100):
        display(words_df)

