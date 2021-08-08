def interlied_int_explore_lyric(intervals_file):
    
    csv1=open(intervals_file)
    name=os.path.basename(csv1.name)
    df_intervals = pd.read_csv(csv1)
    df_intervals.shape[0]
    
    tpls=[]
    for i,r in df_intervals.iterrows():
        idx=i
        itr=r["interval"]
        lyrc=r["reduced_lyric_token(s)"]
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
    return str(new_dict)
    
#############

def interlied_int_explore_lyric_token(df, c_name, l_entry, intr_entry):
    instance=0
    for i,r in df.iterrows():
        idx=i
        #PARAMETERS / COLUMNS
        itr=r["interval"]
        lyrc=r["reduced_lyric_token(s)"]
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

################

def interlied_search_pattern_lyric_composer(df_ngrams, pattern_string, composer_name, lyric_query):
    instance=0
    df_ngrams=df_ngrams
    for i1,r in df_ngrams.iterrows():
        idx1=i1
    #     print(idx1)
        ptrn=r["pattern"]
    #     print(ptrn)
        lyrc=r["lyric_tokens"]
        cmp=r["composer"]
    #     print(lyrc)
        p = str(pattern_string)
        c=str(composer_name)
        q =str(lyric_query)
        if (p == ptrn) and (q in lyrc):
            instance=instance+1
            print("**INSTANCE NUMBER",instance)
    #         print(idx1)
            display(df_ngrams.iloc[int(idx1)])
        else:
            continue
    print("Done.")

################

def interlied_words_count(df_lyric):
    df_lyric=df_lyric
    wrds_l = []
    composer_l = []
    title_l = []
    tonality_l= []
    word_count_l=[]
    words_df={}

    for i in range(0, len(df_lyric)):
        composer_l.append(df_lyric.composer[i])
        title_l.append(df_lyric.title[i])
        tonality_l.append(df_lyric.key[i])
        wrds_l.append(collections.Counter(df_lyric["reduced_tokens"][i]).most_common(300))
    # print(wrds_l)

    for m in range (len(composer_l)):
        word_count_l+=[[composer_l[m], title_l[m], tonality_l[m], (wrds_l)[m]]]
    # word_count_l
    # print(word_count_l)
    words_df=pd.DataFrame(word_count_l)
    words_df=words_df.rename(columns={0: "composer", 1: "title", 2:"key", 3: "most common words"})

    return words_df
