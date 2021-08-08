
from music21 import*
from collections import OrderedDict
from pathlib import Path

def view_score(score, msr_start, msr_end ):
    score_1=converter.parse(score)
    s_title=score_1.metadata.title
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    msr_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key_name = voice_key.analyze('key')
    msr_key_name=msr_key.analyze('key')
    info1='The predicted key of chosen excerpt of score '+str(s_title)+' is: '+ str(msr_key_name)
    info2='The predicted key of VOCAL part excerpt of score '+str(s_title)+' is: '+str(voice_key_name)
    return v, info1, info2


def play_midi(score, msr_start, msr_end):
    score_1=converter.parse(score)
    s_title=score_1.metadata.title
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    msr_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key = score_1.measures(msr_start_1, msr_end_1)
    voice_key_name = voice_key.analyze('key')
    msr_key_name=msr_key.analyze('key')
    print("**** The predicted key of chosen exerpt of score '"+(str(s_title))+"' is: "+str(msr_key_name)+'****')
    print("**** The predicted key of vocal part excerpt of score '",s_title, "' is: ", str(voice_key_name),'****')
    return v.show('midi')