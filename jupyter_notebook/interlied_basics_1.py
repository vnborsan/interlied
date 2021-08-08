#IMPORT REQUIREMENTS
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

warnings.simplefilter('ignore')
from interlied_stopwords import interlied_sw


def interlied_intervals(path, lang):
    from interlied_stopwords import interlied_sw

    """
    This is one of the basic functions by InterLied. 

    Input: path to musicXML folder (string), language of corpus (string)*
    *for full list of languages available, please type print(stopwords.fileids()).
    ** "slovene" list of stopwords is updated and includes more words than the ones offered in NLTK package.

    Output: pandas dataframe.
    *The score also saves separate csv files for each score in the folder "intervals" where this code is stored. 

    Available columns of dataframe: 
    ["interval", "durations", "measure_start", "measure_end" , "title", "composer", "year", "lyricist", "score_key_s", 
     "alternative_key(s)", "voice_range", "meter_change", "meter(s)", "lyric_string", "lyric_tokens", "lyric_language"]

    For more information visit detailed algorithm descriptions in the repository @https://github.com/vnborsan/interlied.

    """
    
    sw=interlied_sw(lang)
    

    try:
        lied_directory=os.scandir(str(path))

        for i in lied_directory:

            try:
                print("_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
                print("file:", i.name, "is seleced.")
                print("_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")

                #Includes _ per interval:
                #msr_start = start measure of the first note in interval. 
                msr_start_list=[]
                #msr_end = end measure of the last note in interval. 
                msr_end_list=[]
                #intList = interval list.          
                intList_1=[]
                #lyric_combined = string of lyric per interval, including stopwords.                 
                lyric_combined=[]
                #duration = list of durations per interval, including stopwords.                             
                dur_combined=[]
                #reduced_token = list of lyric words, excluding the stopwords.
                reduced_token_list=[]
                #composer = composer of the score in which the interval is.
                composers=[]
                #title = title of the score in which the interval is.
                titles=[]
                #lyricist = lyricist of the score in which the interval is.
                lyricsts=[]
                #years = year of origin of the score in which the interval is. Has to be added manually afterwards! Only returns empty fields.
                years=[]
                #tonalities = tonalities of the score in which the interval is.
                tonalities=[]
                #alternative tonalities, which could substitute the one computed.
                alternatives=[]
                #voiceranges = voice range of the score in which the interval is.
                voiceranges=[]
                #meters = meters of the score in which the interval is.
                meters=[]
                #meter_changes = meter changes of the score in which the interval is.
                meter_changes=[]
                #lang_list=language of the score
                lang_list=[]

                intList=[]

                i_1=i.name
                i=i.path
                score=converter.parse(i)
                voice=score.parts[0]
                voice_2=score.parts[0]
                intList = analysis.segmentByRests.Segmenter.getIntervalList(voice)

                #COMPOSER
                comp=score.metadata.composer
                #TITLE
                title=score.metadata.title
                #YEAR
                year="None"
                #LYRICIST
                metadt=score.metadata.all()
                for element in metadt:
                    if(element[0]=='lyricist'):
                        lyricist=element[1]
                #KEY
                tonality=score.analyze('key')
                #ALTERNATIVE TOP 3 KEYS
                alt_t=[str(score) for score in tonality.alternateInterpretations[0:3]]
                #RANGE
                amb=analysis.discrete.analyzeStream(voice, 'ambitus')
                ambitus=amb.diatonic.name
                #METER CHANGE
                metChange = features.jSymbolic.ChangesOfMeterFeature(score)
                m_c = metChange.extract().vector
                for y in m_c:
                    if y == 0:
                        m_c='NO'
                    elif y ==1:
                        m_c='YES'
                #METERS
                y= []
                lastTimeSignature=None
                for n in score.recurse().getElementsByClass('Note'):
                    thisTimeSignature = n.getContextByClass('TimeSignature')
                    if thisTimeSignature is not lastTimeSignature:
                        lastTimeSignature = thisTimeSignature
                        y.append(thisTimeSignature.ratioString)
                meter = set(y)

                for x in intList:
                    voice=score.parts[0]
                    voice_2=score.parts[0]
                    intList=[]
                    intList = analysis.segmentByRests.Segmenter.getIntervalList(voice)
                    print("Next up interval:", x.name)
                    lyric_int=[]

                    #START MEASURE
                    pos1=x.noteStart.containerHierarchy()
                    msr_start=str(pos1[0])
                    msr_start=re.split("[_.]", msr_start)[-2]
                    msr_start = re.search(r"\d+", msr_start)
                    msr_start=msr_start.group(0)
                    msr_start_list.append(msr_start)

                    #END MEASURE
                    pos2=x.noteEnd.containerHierarchy()
                    msr_end=str(pos2[0])
                    msr_end=re.split("[_.]", msr_end)[-2]
                    msr_end = re.search(r"\d+", msr_end)
                    msr_end=msr_end.group(0)
                    msr_end_list.append(msr_end)

                    #COMPOSER
                    composers.append(str(comp))
                    #TITLE
                    titles.append(str(title))
                    #YEAR
                    years.append(str(year))
                    #LYRICIST
                    lyricsts.append(str(lyricist))
                    #KEY
                    tonalities.append(str(tonality))
                    #ALTERNATIVE TOP 3 KEYS
                    alternatives.append(str(alt_t))
                    #RANGE
                    voiceranges.append(str(ambitus))
                    #METER CHANGE
                    meter_changes.append(str(m_c))
                    #METERS
                    meters.append(str(meter))
                    lang_list.append(str(lang))

                    try:
                        #MAKE DEEP COPY
                        voice_1=voice.measures(msr_start,msr_end)
                        voice_copy=copy.deepcopy(voice_1)
                        text_copy=copy.deepcopy(voice_copy)
                        bb=text.assembleLyrics(text_copy)

                    except:
                        bb="/"
                        comp="not specified"
                        composers.append(comp)
                        title="not specified"
                        titles.append(title)
                        lyricst="not specified"
                        lyricsts.append(lyricst)
                        tonality="not specified"
                        tonalities.append(tonality)
                        alt_t="not specified"
                        alternatives.append(alt_t)
                        ambitus="not specified"
                        voiceranges.append(ambitus)
                        meter = "not specified"
                        meters.append(meter)
                        m_c="not specified"
                        meter_changes.append(m_c)
                        lang_list.append("not specified")

                    #Combined lyric for each interval.
                    lyric=bb
                    s_lyric_1ist=[]
                    s_lyric_lower_list=[]

                    #Delete unneccessary symbols and make all lower caps.
                    s_lyric_1=re.sub("[,-?,.!@#$:;/*']", '', lyric)
                    s_lyric_1=re.sub('[_]',' ', s_lyric_1)
                    s_lyric_1ist+=s_lyric_1
                    s_lyric_lower=str(s_lyric_1).lower()
                    s_lyric_lower_list+=s_lyric_lower

                    #Tokenize the lyric.
                    tokens=nltk.word_tokenize(str(s_lyric_lower))
                    lyric_combined+=[s_lyric_1]
                    #Apply stopwords and filter them out.
                    reduced_tokens = [w.lower() for w in tokens if w.lower() not in sw]
                    reduced_token_list+=[reduced_tokens]

                    #Duration start and end for each interval.
                    lyric_start=x.noteStart
                    lyric_end=x.noteEnd
                    dur_start=lyric_start.duration.quarterLength
                    dur_end=lyric_end.duration.quarterLength
                    duration=(dur_start, dur_end)
                    dur_combined.append(duration)

                    #Retrieve the name of each interval and assign to each a symbol which indicates its direction. 
                    #"+" means ascending; "-" means descending (is already established in music21); "_" means neither up nor down (e.g. P_1 - perfect unison).
                    x_1=x.name
                    x_2=x.direction.name
                    if x_2=="ASCENDING":
                        x_2="+"
                    elif x_2 == "DESCENDING":
                        x_2="-"
                    else:
                        x_2 = "_"

                    interval_1=str(x_1[0]+ x_2+ x_1[1])

                    (intList_1).append(interval_1)
                    print("All features appended to dataframe.")
                    NewList=[]

                #CREATE COMBINED LIST
                print("Creating a file...")   
                for m in range (len(intList_1)):
                    NewList+=[[intList_1[m], dur_combined[m], msr_start_list[m], msr_end_list[m], titles[m], composers[m], 
                               years[m], lyricsts[m], tonalities[m], alternatives[m], voiceranges[m], meter_changes[0],
                               meters[m], lyric_combined[m], reduced_token_list[m], lang_list[m]]]

                #CREATE DATAFRAME
                df_intervals=pd.DataFrame(NewList)
                df_intervals = df_intervals.rename(columns=({0:"interval", 1:"duration", 2:"measure_start", 3:"measure_end", 4:"title" , 5:"composer", 
                                       6:"year", 7:"lyricist", 8:"score_key_s", 9:"alternative_key(s)", 10: "voice_range",
                                        11:"meter_change", 12:"meter(s)", 13:"lyric_string", 14:"lyric_tokens", 15:"lyric_language"}))

                df_intervals = df_intervals[["interval", "duration", "measure_start", "measure_end" , "title", "composer", "year", "lyricist", 
                                             "score_key_s", "alternative_key(s)", "voice_range", "meter_change", "meter(s)", "lyric_string", "lyric_tokens", "lyric_language"]]

                df_intervals.to_csv("intervals/_intervals_"+str(i_1) + "_combined"+".csv")

                print("---------------------------------------------------------------------------------------")
                print("***", i_1, "IS DONE***")
                print("---------------------------------------------------------------------------------------")

            except Exception as e: 
                print(e)
                print("-----------------------------------------!!!-------------------------------------------")
                print("ERROR occured.", i_1, "cannot be parsed.")
                print("-----------------------------------------!!!-------------------------------------------")

        print("*******************************************************************")
        print("******************A*L*L*********D*O*N*E****************************")
        print("*******************************************************************")

    except Exception as e:
        print(e)
        print("Directory cannot be found or is not compatible with the algorithms format. Check for possible errors in your database and try again.")
    
#######################################################

#######################################################

#######################################################

