
import collections
from collections import OrderedDict
from collections import Counter
from interlied_stopwords import interlied_sw
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

def interlied_view_midi_and_score(score, msr_start, msr_end ):
    score_1=converter.parse(score)
    s_title=score_1.metadata.title
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    msr_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key_name = voice_key.analyze('key')
    msr_key_name=msr_key.analyze('key')
    print("**** The predicted key of chosen exerpt of score '",s_title, "' is: ", str(msr_key_name),'****')
    print("**** The predicted key of vocal part excerpt of score '",s_title, "' is: ", str(voice_key_name),'****')
    v.show()
    v.show('midi')

def interlied_save_midi(score, msr_start, msr_end):
    score_1=converter.parse(score)
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    mf = midi.translate.streamToMidiFile(v)
    fp = v.write('midi', fp='midi_files/'+score_1+".mid")
