#IMPORT REQUIREMENTS
import collections
from collections import OrderedDict
from collections import Counter
import copy
import csv
import glob
from heapq import nlargest
from interlied_stopwords import interlied_sw
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

def interlied_intervals(path, lang):
    from interlied_stopwords import interlied_sw

    """
    This one of the basic functions by InterLied. 

    Input1 and Input2: path to musicXML folder (string), language of corpus (string)
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
    #             intList_1=[]
    #             token_lyric=[]
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
    #                     print([bb])

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
    #             break

        print("*******************************************************************")
        print("******************A*L*L*********D*O*N*E****************************")
        print("*******************************************************************")

    except Exception as e:
        print(e)
        print("Directory cannot be found or is not compatible with the algorithms format. Check for possible errors in your database and try again.")
    
###################################
###################################
###################################

def interlied_pattern_analysis(csv_folder_path):
    """
    This is one of the basic functions by InterLied, constructed to analyse music patterns of vocal or any other SINGLE voice score.

    - Input: path to interval csv folder (string)

    - Output: pandas dataframe.
    *The score also saves separate csv files for each score in the folder "patterns" where this code is stored. 

    - Available columns of dataframe: 
    ["pattern","pattern_length","duration","measure_start", "measure_end", "title", "composer", "year","lyricist", 
    "score_key_s", "alternative_keys", "range", "meter_change", "meter_s", "lyric_tokens", "lyric_language"]]

    *For more information visit detailed algorithm descriptions in the repository @https://github.com/vnborsan/interlied. 

    """
   
    def convert_list_to_string(org_list, seperator=' '):
        return seperator.join(org_list)

    folder=os.scandir(csv_folder_path)
    txt=[]
    
    for csv in folder:
        try:
            csv1=open(csv)
            name=os.path.basename(csv1.name)
            interval_csv = pd.read_csv(csv1)
            interval_csv.shape[0]
            temporary_ngrams=[]
            ngrams_final=[]

 
            for indx in range (interval_csv.shape[0]):
                all_attributes=interval_csv.iloc[indx,:]
                int_ints=[interval_csv.iloc[indx,1]]
                int_durations=[interval_csv.iloc[indx,2]]
                int_s_measure=[interval_csv.iloc[indx,3]]
                int_e_measure=[interval_csv.iloc[indx,4]]
                int_title=[interval_csv.iloc[indx,5]]
                int_composer=[interval_csv.iloc[indx,6]]
                int_year=[interval_csv.iloc[indx,7]]
                int_lyricist=[interval_csv.iloc[indx,8]]
                int_keys=[interval_csv.iloc[indx,9]]
                int_alt_keys=[interval_csv.iloc[indx,10]]
                int_range=[interval_csv.iloc[indx,11]]
                int_meter_chng=[interval_csv.iloc[indx,12]]
                int_meter=[interval_csv.iloc[indx,13]]
                int_l_string=[interval_csv.iloc[indx,14]]
                int_l_tokens=[str(interval_csv.iloc[indx,15])]
                lyric_lang=[str(interval_csv.iloc[indx,16])]
                ngram_len=[]

                for ngram_length in range(2,30):
                    joinedlist=[]
                    templist=[]
                    if indx+ngram_length>=interval_csv.shape[0]:
                        break
                    int_ints+=[interval_csv.iloc[indx+ngram_length,1]]
                    int_durations+=[interval_csv.iloc[indx+ngram_length,2]]
                    int_e_measure=[interval_csv.iloc[indx+ngram_length,4]]
                    tkn=str(interval_csv.iloc[indx+ngram_length,15])         
                    int_l_tokens+=[tkn]
                    int_l_tokens=list(set(int_l_tokens))
                    final_l_tokens=','.join(int_l_tokens)
                    final_l_tokens=final_l_tokens.replace(" ", "")
                    final_l_tokens=final_l_tokens.replace(" ,", "")
                    final_l_tokens=final_l_tokens.replace("]", "")
                    final_l_tokens=final_l_tokens.replace("[", "")
                    final_l_tokens=final_l_tokens.replace(",", ", ")

                    ngram_len=[str(int(len(int_ints)))]
                    current_ngram=[str(int_ints)[1:-1], str(ngram_len)[1:-1], str(int_durations)[1:-1],
                                   str(int_s_measure)[1:-1], str(int_e_measure)[1:-1], str(int_title)[1:-1],
                                   str(int_composer)[1:-1],str(int_year)[1:-1], str(int_lyricist)[1:-1],
                                   str(int_keys)[1:-1],str(int_alt_keys)[1:-1],str(int_range)[1:-1],
                                   str(int_meter_chng)[1:-1],str(int_meter)[1:-1], str(final_l_tokens)[1:-1], str(lyric_lang)[1:-1]]
                    ngrams_final+=[current_ngram]



            df_ngrams=pd.DataFrame(ngrams_final)
            df_ngrams=df_ngrams.rename(columns={0: "pattern", 1: "pattern_length", 2: "duration", 3: "measure_start", 
                                                4: "measure_end", 5: "title", 6: "composer", 7: "year", 8:"lyricist", 
                                                9: "score_key_s",10: "alternative_keys", 11:"range", 
                                                12:"meter_change", 13:"meter_s", 14:"lyric_tokens", 15:"lyric_language"})
            number= len(df_ngrams)
            allGramDict=dict()
            grams_list=df_ngrams['pattern']

            for gram in grams_list:
                if(gram not in allGramDict.keys()):
                    allGramDict[gram]=1
                else:
                    allGramDict[gram]=allGramDict[gram]+1

            for gram in list(allGramDict):
                if allGramDict[gram] > 1:
                    del allGramDict[gram]

            for gram in allGramDict.keys():
                for i in df_ngrams['pattern']: 
                    if (gram == i) : 
                        ind=int(df_ngrams[df_ngrams["pattern"]==i].index.values)
                        df_ngrams=df_ngrams.drop(ind)

                inter_len=len(df_ngrams)
            
            temp_txt=[]
            t0=str("-----------------------------------------INFO-----------------------------------------")
            temp_txt+=[t0]
            t1=str("All n-grams in score:  "+str(name)+"  "+str(len(df_ngrams)))
            temp_txt+=[t1]
            t2=str("Repeated patterns of length >= 2 in score: "+str(len(df_ngrams)))
            temp_txt+=[t2]
            t3=str("Dropped  "+str(int(number)-(int(len(df_ngrams))))+"  unique patterns.")
            temp_txt+=[t3]
            column = df_ngrams["pattern_length"]
            max_value = column.max()
            t4=str("The longest repeated pattern in corpus consists of:  "+str(column.max())+"  grams.")
            temp_txt+=[t4]
            txt.extend(temp_txt)

            df_ngrams = df_ngrams[["pattern","pattern_length","duration","measure_start", 
                                "measure_end", "title", "composer", "year","lyricist", 
                                "score_key_s", "alternative_keys", "range", 
                                "meter_change", "meter_s", "lyric_tokens", "lyric_language"]]
            df_ngrams=df_ngrams.reset_index(drop=True)

            df_ngrams.to_csv("patterns/patterns_"+str(name))
            print("*******", "Done with processing n-grams of: ", (name), "********")

            print("---------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------")

            print(" ")
            print("---------------------------------------------------------------------------------------")
            print("------------------------------------------NEW------------------------------------------")
            print("---------------------------------------------------------------------------------------")
            print(" ")
        
        except Exception as e:
            print(e)
            print("Could not parse this file:",csv)
            print("---------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------")
    
    with open('patterns/info_patterns.txt', 'w') as f:
        for t in txt:
            f.write(t)
            f.write('\n')
            
    print("*******************************************************************")
    print("*****************************D*O*N*E*******************************")
    print("*******************************************************************")

    print("---------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------")

    return df_ngrams

###################################
###################################
###################################


def interlied_lyric(corpus_folder, lang):
    from interlied_stopwords import interlied_sw

    """
    This is one of the basic functions by InterLied, constructed to analyse music patterns of vocal or any other SINGLE voice score.

    - Input1: path to musicXML scores folder (string)

    - Input2: language of text (e.g., lyric)
    *for full list of languages available, please type print(stopwords.fileids()).
    ** "slovene" list of stopwords is updated and includes more words than the ones offered in NLTK package.

    - Output: pandas dataframe & 5 text strings*
    *The score also saves separate csv files for each score in the folder "lyric" where this code is stored and txt file with basic data information.

    - Available columns of dataframe: [0: "composer", 1: "title", 2:"lyric", 3: "tokenized_lyric",  4: "lyric_tokens", 5: "score_key_s"]

    *For more information visit detailed algorithm descriptions in the repository, Interlied notebook or master's thesis.

    """
    
    sw=interlied_sw(str(lang))

    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer() 

    df={}
    txt_l=[]

    corpus=os.scandir(str(corpus_folder))
    lyric_list=[]
    title_list=[]
    composer_list=[]
    key_list=[]
    l_c_list=[]
    lyricists_list=[]
    token_lyric=[]
    reduced_token_list=[]
    lyricist_list=[]
    lyric_language=[]
    

    print("-------------------------------------------------------------------------------------")
    print(corpus,"folder is in")
    print("-------------------------------------------------------------------------------------")
    l_c_list=[]

    for c in corpus:
        try:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(c,"score is in.")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            #Parse each score in the folder, then retrieve the title, composer and key.
            score_1=converter.parse(c.path)
            #title
            s_title=score_1.metadata.title
            title_list+=[s_title]
            #composer
            s_composer=score_1.metadata.composer
            composer_list+=[s_composer]
            
            #lyricist
            metadt=score_1.metadata.all()
            for element in metadt:
                if(element[0]=='lyricist'):
                    lyricist=element[1]
                    

            #language
            l=str(lang)
            lyric_language+=[l]

            #key
            s_key=score_1.analyze("key")
            key_list+=[str(s_key)]
            
            #Assemble lyric from score.
            s_lyric=text.assembleLyrics(score_1)
            lyric_list+=[str(s_lyric)]
            
            #Delete unneccessary symbols and make all lower caps.
            s_lyric_1=re.sub("[,-?,.!@#$:;/*']", '', s_lyric)
            s_lyric_1=re.sub('[_]',' ', s_lyric_1)
            s_lyric_lower=str(s_lyric_1).lower()
            
            #Tokenize the lyric.
            tokens=nltk.word_tokenize(str(s_lyric_lower))
            token_lyric+=[tokens]
            
            #Apply stopwords and filter them out.
            reduced_tokens = [w.lower() for w in tokens if w.lower() not in sw]
            reduced_token_list+=[reduced_tokens]
            lyricist_list+=[str(lyricist)]


        except Exception as e: 
            print(e)
            print("!!!! Did not proccess !!!! :", c)
    
            continue

    for m in range (len(lyric_language)):
         l_c_list+=[[composer_list[m], title_list[m], lyric_list[m], token_lyric[m], reduced_token_list[m], lyricist_list[m], lyric_language[m],  key_list[m]]]
    df_lyric_only=pd.DataFrame(l_c_list)

    #Make titles for columns in dataframe.
    df_lyric_only=df_lyric_only.rename(columns={0: "composer", 1: "title", 2:"lyric", 3: "tokenized_lyric",  4: "lyric_tokens", 5:"lyricist", 6:"lyric_language", 7: "score_key_s"})

    #INFO ABOUT DATASET
    print("------------------------------------------------------------------------------------------------------------")
    t1=str("There are {} entries and {} feature type(s) in this dataset.".format(df_lyric_only.shape[0],df_lyric_only.shape[1]))
    print(t1)
    print("------------------------------------------------------------------------------------------------------------")

    t2=str("There is/are {} composer(s) in this dataset such as {}...".format(len(df_lyric_only.composer.unique()),
                                                                                          ", ".join(df_lyric_only.composer.unique()[0:1])))
    print(t2)
    print("------------------------------------------------------------------------------------------------------------")
    t3=str("There are {} tonalities in this dataset such as {}...".format(len(df_lyric_only.score_key_s.unique()),
                                                                                          ", ".join(df_lyric_only.score_key_s.unique()[0:3])))
    print(t3)
    print("------------------------------------------------------------------------------------------------------------")
    

    t4=str("There is/are {} title(s) in this dataset such as {}...".format(len(df_lyric_only.title.unique()),
                                                                               ", ".join(df_lyric_only.title.unique()[0:5])))
    print(t4)
    print("------------------------------------------------------------------------------------------------------------")

    name=os.path.basename(corpus_folder)
    df_lyric_only.to_csv("lyric/lyric_"+str(name)+".csv")


    #Count the words in tokenized column.
    txt_1=''

    for t in df_lyric_only.lyric_tokens:
        tx = ' '.join(map(str, t))
        txt_1+=str(tx)

    t5=str("There are {} tokenized words in all lyrics.".format(len(txt_1)))
    separator=("------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------")
    

    txt_l+=[t1]
    txt_l+=[t2]
    txt_l+=[t3]
    txt_l+=[t4]
    txt_l+=[t5]
    txt_l+=[separator]

    with open('lyric/info_lyric_'+(str(s_composer))+'_.txt', 'w') as f:
        for t in txt_l:
            f.write(t)
            f.write('\n')


    
    print("***************************")
    print("************DONE***********")
    print("***************************")
