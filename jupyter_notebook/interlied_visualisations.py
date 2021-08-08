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

def interlied_pitch_plot(mxl):
    
    """
This is one of the interlied plot functions that operates under music21 pianoroll and pitch plot visualisation.

- Input: path to musicXML score

- Output: Two plots - pianoroll & pitch frequency

    """

    score = converter.parse(mxl)
    score = score.parts[0]

    pianoroll_plot=score.plot('pianoroll')
    pitch_plot=score.plot('pitch')
    plt.title('Pitch frequency in the chosen score:')
    return pitch_plot

######################################################################################################################

def interlied_int_explore_lyric_token(csv_path, c_name, l_entry, intr_entry):
    """
        This is one of the interlied plot functions that operates under music21 pianoroll and pitch plot visualisation.

        - Input1: path to csv dataframe
        - Input2: composer's name (string)
        - Input3: lyric token (string)
        - Input4: interval (string)

        - Output: All refined entries (in text).

    """
    
    instance=0
    df=pd.read_csv(csv_path)
    for i,r in df.iterrows():
        idx=i
        #PARAMETERS / COLUMNS
        itr=r["interval"]
        lyrc=r["lyric_tokens"]
        cmps=r["composer"]
        
        #INPUTS
        c= str(c_name)
        q = str(l_entry)
        intr=str(intr_entry)
        
        if (itr == intr) and (q in lyrc) and (c in cmps):
            instance=instance+1
            print("**INSTANCE NUMBER",instance)
            display(df.iloc[int(idx)])
        else:
            continue
    print("Done.")
    
######################################################################################################################

def interlied_top_10_plot(csv,q):
    """
    This is one of the interlied plot functions that explores frequency of keys in a single column query searches, for example composer+composer name and interval.

    - Input1: path to csv dataframe
    - Input2: column name, e.g. "composer"

    - Output: Plot of key frequency per chosen column.

    """
        
    name=os.path.basename(csv)
    grams=pd.read_csv(csv)
    return grams[(str(q))].value_counts()[:10].plot.bar(color='lime', title="Top 10 "+str(q)+" values in "+str(name))

########################################################################################################################

def interlied_word_freq_q_plot(csv, q1, q2): #Plot word frequency per certain interval in certain score.
    
    """
This is one of the interlied plot functions that explores frequency of word tokens by one query search, for example composer+composer name.

- Input1: path to csv dataframe
- Input2: column name, e.g. "composer"
- Input3: column value, e.g. "Franz Schubert"

- Output: Plot of word frequency per chosen keywords.

    """
    
    df=pd.read_csv(csv)
    q1=str(q1)
    q2=str(q2)
    
    m=df[df[str(q1)]==str(q2)]

    for xy in m.iterrows():
        wrds=[]
        for w in m['lyric_tokens']:
            wrds.append(str(w))
        pd.Series(wrds).value_counts().sort_values(ascending=True).plot(kind = 'barh', title='Words: '+str(q1)+"_"+str(q2))


########################################################################################################################

def interlied_lyric_freq_plot(csv, chosen_key_1, key_1, chosen_key_2, key_2): #Plots word freqency from lyric per two queries (e.g. composer + key).
    """
This is one of the interlied plot functions that explores frequency of word tokens by two queries search, especially in lyric dataframes, for example composer+composer name and interval+interval name.

- Input1: path to csv dataframe
- Input2: column name, e.g. "composer"
- Input3: column value, e.g. "Franz Schubert"
- Input4: second column name, e.g. "key"
- Input5: second column value, e.g. "C major"

- Output: Plot of word frequency per chosen keywords.

    """
    df_lyric=pd.read_csv(csv)
    
    chosen_key_1=str(chosen_key_1)
    key_1=str(key_1)
    chosen_key_2=str(chosen_key_2)
    key_2=str(key_2)

    allCombinations=[]

    temp=df_lyric[df_lyric[chosen_key_1].str.contains(key_1)] #.iloc[:,-2:]
    temp=temp[temp[chosen_key_2]==key_2] #.iloc[:,-2:]

    allWords=""
    
    for i in temp.lyric_tokens:
        allWords+=str(i).replace('[','').replace(']',', ')
    wd = collections.Counter(re.split(r"',",allWords)).most_common(200)

    key_list=[]
    val_list=[]

    for i in wd:
        x=str(i).replace('"','').replace("'",'').replace(")",'').replace("(",'')
        x=x.split(",")
        key_list.append(x[0])
        val_list.append(int(x[1]))

    wrds_dict=dict(zip(key_list, val_list))
    wrds_df=pd.DataFrame(wrds_dict.items(), columns=['word', 'frequency'])
    print("The frequency of words in "+chosen_key_1+": _"+key_1+"_ & "+chosen_key_2+": _"+key_2)
    w_plt=wrds_df.head(10)
    w_plt.plot(kind='bar',x='word',y='frequency', color="#BAE682", title="The frequency of words in "+str(chosen_key_1)+": _"+str(key_1)+"_ & "+str(chosen_key_2)+": _"+str(key_2)+"_")    
