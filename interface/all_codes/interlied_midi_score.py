#THESE FUNCTIONS DEAL WITH MIDI AND SCORE REPRESENTATION, ANALYSE THE KEY OF THE CHOSEN SCORE PART AND SAVE MIDI TO YOUR COMPUTER.


def view_midi_and_score(score, msr_start, msr_end ):
    score_1=converter.parse(score)
    s_title=score_1.metadata.title
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    msr_key = score_1.measures(msr_start_1, msr_end_1)
    msr_key_name=msr_key.analyze('key')
    print("**** The key of chosen part in a score '",s_title, "' is: ", str(msr_key_name),'****')
    v.show()
    v.show('midi')

def save_midi(score, msr_start, msr_end):
    score_1=converter.parse(score)
    msr_start_1=int(msr_start)
    msr_end_1=int(msr_end)
    v=score_1.parts[0].measures(msr_start_1, msr_end_1)
    mf = midi.translate.streamToMidiFile(v)
    fp = v.write('midi', fp=score_1+".mid")