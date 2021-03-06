# InterLied 1.0

InterLied is a set of python GUI (interface) and python notebook, both designed for computational music analysis. Although it is adapted for analysing vocal pieces only, lieder in particular, a majority of its tools can be useful for other purposes as well. 
The notebook is appropriate for both, computationally advanced and beginner users. If you assume, you belong to the latter, please go through these instructions first and then open the GUI. The notebook does not require any coding experience; however, you are strongly encouraged to not only utilise the GUI, but also the InterLied
notebook. All parameters are described in the notebook itself, thus, in order to get to it, scroll through the instructions bellow and first install Python3, install all the (missing) prerequisite dependencies and MuseScore or any other software for symbolic notation.

------
## 1. INSTALL DEPENDENCIES:

To use GUI or the notebook, first install all prerequired dependencies. You can do that automatically by opening terminal (Linux / Mac OS) or prompt command (NOT SHELL!) (Windows) and type in:
 "cd your/path/to/interface/Interlied_1.0"

When you successfully enter the folder, type this command into terminal: 
"python interlied_dependencies.py"

If you run into some errors, install the required packages manually (find list just below) by following instructions in the INTERLIED_USER_MANUAL.
Also, it is strongly advised to first create a new python environment (https://docs.python.org/3/library/venv.html, if you haven't already, and then either install the dependencies manually or through Anaconda Navigator (https://docs.anaconda.com/anaconda/navigator/index.html) or miniconda (https://docs.conda.io/en/latest/miniconda.html).

*The list of required packages:*
 - pip install music21
 - pip install pandas
 - pip install numpy
 - pip install os-sys
 - pip install more-itertools
 - pip install pyoperators
 - pip install nltk
 - pip install heapq_max
 - pip install regex
 - pip install python-csv
 - pip install matplotlib
 - pip install glob2
 - pip install IPython
 - pip install random2
 - pip install pandastable

*So far, the errors on different computers showed difficulties installing pandastable, pyoperators and os-sys.*

------
## 2. ACCESS THE INTERLIED TOOLS:

The Interlied offers 2 different types of accessing the codes:

### 2.1 Jupyter notebook + scripts
To use this option, install jupyter notebook (https://jupyter.org/install). The notebook includes all of the basic code explanations and execution commands.

### 2.2 GUI
If you do not wish to interact with code, simply download the interface part above, enter the folder through terminal / prompt command and then run "python interlied_interface.py".

-------

## 3. DATA PREPARATION:

Although the tools are made to read a variety of different musicXML files, it must be noted that non-organised and not well prepared data will cause issues.

Below, find some pointers on where to pay extra attention when preparing your corpus.
1. All files should be converted to musicXML formats ONLY. Sibelius original format, MEI and other formats are not readable by these tools.
2. Most of music notational softwares (Musescore, Finale, Sibelius) offer an option of filling out all different types of information about the score. When it is converted to musicXML (if you use another format first), please check if it translated the fields correctly. The InterLied can so far read the fields of composer, title, lyricist and lyric (but many others can easily be added if you wish to do so, so fill out as much information as you can gather per score).
3. If there are multiple composers, titles or lyricists, my method was to separate them by this symbol ";" (e.g., Mozart; Beethoven). However, you can apply your own rule to this - but note that you must be consistent with the chosen method throughout your entire corpus, as it will be easier for you to adapt it.
4. Parts: When it comes to parts, InterLied's algorithms are pre-set to reading part[0], where they expect a single voice music line (no chords, etc.) to be stored in the first part. Should your single voice line fall under another part, please adjust this in the scripts. You can also analyse multiple lines of a single score, by adapting the number of the part each time (for example, if you chose to analyse all four of the SATB voices, run the code 4 times by changing x in the part[x]).
5. InterLied CANNOT analyse multiple voice streams. 
6. If some data was misread, change it manually in the output csv files you gather.
7. "year" parameter always remains as "None" and always requires a manual input as it can indicate various things (from the date of manuscript, first edition, the chosen edition, composer's date of birth etc.), which may be confusing for it to be generalised. Thus, each user is allowed to define this parameter as they please.


-------
## 4. PACKAGE INTRODUCTION:

### CONTENT OVERVIEW:
- interface folder: Includes all neccessary codes to run GUI.
- jupyter_notebooks folder: Includes all neccessary codes to run Interlied Jupyter Notebook.
- example_scores_and_csvs: Includes 18 open source score (and processed csvs) examples (extracted from: https://musescore.com/openscore-lieder-corpus).
- "interlied_dependencies.py" allow you to run a single script and download all neccessary packages / dependencies.
- "INTERLIED_USER_MANUAL.pdf" is a manual adapted for computational beginners, but is nonetheless suggested to be run through by all users.

### CODE DESCRIPTIONS:

The codes are separated into 3 categories:

### 3.1 ANALYSIS
- The first group of 3 alogrithms processes your scores and prepares dataframes (in csv form) for further data exploring.
- !Beware - two of the three algorithms need language as the input prior to starting the function. If your function has not passed the test scores, this may be the issue.
### 3.2 VISUALISATIONS 
- Plots and other visual representations allow for your data to be refined and visually represented by graphs, as music notation and / or midi.
### 3.3 EXPLORATION 
- This section offers an easy access to refined data by your desired keywords.

![Screenshot 2021-08-07 at 16 47 43](https://user-images.githubusercontent.com/76003382/128604082-0da9c24a-bddd-4e26-a02a-83608b040699.png)

------
## ANALYSIS:
The three basic algorithms that serve for data preparation, separately focusing on melodic intervals, music patterns and lyric. 

### - INTERVALS (interlied_intervals):

The function called [interlied_intervals] turns a MusicXML file to a pandas data frame that is purposefully saved to user???s computer as CSV. From each score, it extracts metadata information and information related to the music analysis. Algorithm only observes the first, assuming vocal, part (e.g., score.parts[0])). With music21 function of ???segmentByRests???, the algorithm ignores the relationships between two consecutive notes divided by breaks. From that, a complete interval sequence list is created within the loop for each composition. Each interval element includes the ascending (plus), descending (minus) or oblique (underscore) symbol, thus M-2 and M+2 is not considered to be the same interval. This is useful especially when trying to grasp the vocal contours, to observe the score???s peaks and to explore lyrics semantics. Intervals are described as follows, 
- *P5 = Perfect (fifth)*
- *A4 = Augmented (fourth)*
- *D4 = Diminished (fourth)*
- *M3 = Major (third)*
- *m2 = minor (second)*

The algorithm first defines the interval and appends the metadata information (e.g., title, composer, lyricist, and year ) to each. If metadata information is missing form the score, the field is marked with ???None???. This can later be substituted or filled in manually. All interval elements also come with the following music analysis parameters, mainly supported by music21 algorithms:

- *Start and end measure of the interval.*
- *Rhythm values consist of a tuple of both rhythmic note values of the interval, (example: M+2 = (0.5, 1.0), where 0.5 equals one eight note and 1.0 equals one quarter note).*
- *Key is predicted with The Krumhansl-Schmuckler Key-Finding Algorithm, a built-in option with music21.*
- *In addition to the most probable key, the function offers alternative keys, writing down the top three most feasible guesses, also supported by music21 algorithm.*
- *Voice range is computed between the lowest and highest note value in the vocal part and is expressed as an interval (for example, M9).*
- *Meter change confirms whether the score has a meter change by YES/NO, and exact meter or meters are computed and written down afterwards, in format of a dictionary.*
- *The first method for lyrics extracts the ???assembled lyrics??? per interval. This means that the system takes all words at least partially connected to each note of the interval to make the process of lyrics segmentation / exploration.
- *Second method tokenizes the lyric words per interval.*
- *The last method removes any stopwords we have set in advance.*
- *The final parameter is the language of the lyric.*

This algorithm is using NLTK packages, so if the language is included in their repository a user can access it through inserting the desired language (as a string) to the second input. The first input of this algorithm expects a folder of musicXML files. As an output, it writes all the information presented above in both, csv file, which is saved to user???s computer and pandas data frame, which can be further used in the code itself.

### - PATTERNS (interlied_pattern_analysis):

The intervals data tables, produced by the first function, can serve as an input to the next function, called [interlied_pattern_analysis]. What this particular algorithm does is to compute all n-grams (2<n<30) or patterns from the interval sequence obtained through the [interlied_intervals] function. Some data is collected for the first of the two grams only, assuming the information will inevitably be identical for the next gram as well. This is true for the metadata (title, composer, lyricist), score key, alternative score key(s), score meter(s), score???s voice range and lyric language. Start measure number is retrieved from the first note of the first gram, and end measure is retrieved from the last note of the last interval of selected pattern. The lyrics elements represent a gathered bundle of words from all grams. Additionally, the user is also offered the information about pattern length. Since pattern is considered to be a repeated event, the function erases all grams that are unique. The user is informed about the quantity of patterns that were excluded from consideration. The output is the same as in intervals data table, thus data frame written onto the user???s computer as CSV file, but also remains as a pandas data frame variable, that can be further referenced in the code.

### - LYRIC:

The [interlied_lyric] function includes less meta and musical data, but rather focuses on preparing the lyric in whole per score. The first two functions only deliver short excerpts of the lyric or tokens connected to much smaller pieces (e.g., interval or repeated pattern), while this, on the other hand, prepares the lyric with an aid of NLTK  Python package. It first extracts the lyric form the musicXML score, then tokenizes it and in the end, removes the stopwords. The collection of the latter is already provided with the NLTK package in many languages, among them English, Italian, French, Spanish, etc. You can find the available options listed in the interface. For the purpose of my own research, I extended the provided list of words for slovenian language. The rest of the offered language lists remain unchanged.  The extension was done especially for the purpose of my targeted corpus as I have noticed that the articulations and other text marks in the score occasionally find their way to the lyric transcription, thus I have removed words such as rall., allegro, andante, and so on. The transcribed and processed text of three described types is accompanied by the data about the lyricist, composer, and tonality, but can easily be extended should the user require more information. The inputs of this algorithm are first, a folder of musicXML scores and second, the chosen language. The outputs are a pandas dataframe and five text strings, providing some statistical information about the corpus. As the other two functions, this one stores a csv file to your computer as well.

![Screenshot 2021-08-07 at 16 48 32](https://user-images.githubusercontent.com/76003382/128604107-df0ba480-1ac7-4a59-a0f2-18655fe1a879.png)

-------
## VISUALISATIONS:

There are four types of plots. 

*If you wish to explore the whole corpus and not separate scores, I suggest you merge your csvs. This is one of the ways on how to do it computationally: https://extendsclass.com/merge-csv.html or https://serp.co/blog/combine-merge-csv-files-mac/. You can, ofcourse, also do it manually, but it will be a very time consuming process.*

### *1. interlied_pitch_plot:*
It realises the music21 score plot in the form of piano roll and pitch representation. It requires a single musicXML score to run and returns two colourful plots, which can be, as any other plots in this sub-chapter, downloaded onto the user???s computer. As the music21 presents a larger issue to be incorporated into the interface, this plot is for now only accessible through the Jupyter notebook. 

### *2. interlied_top_10_plot:*
It accepts any type of csv and a query, which should be the name of one column in the chosen csv. The algorithm returns a plot of ten most frequently fully repeated elements in that query and csv. To get more accurate representation results, the code in GUI also saves a txt file with the exact values of the top 10.

### *3. interlied_word_freq_q_plot:* 
It takes one csv (or directly the pandas data frame if we slightly modify the code) and two queries. Its pre-set function accepts a type of interval (e.g., M+3) as the query 1 and a score???s title as query 2. Based on the user???s input it delivers a plot of word frequency of all tokens that appear in the combination with the queries. Mind that this code is very easily modified and can explore word tokens through other parameters as well, replacing the ???interval??? and ???title??? with desired alternatives. 

### *4. interlied_lyric_freq_plot:* 
This one also explores the lyric, but instead of the pattern or an interval, utilises the lyric data frame. It takes one csv file in which it plots the frequency of words for chosen first key in chosen column 1 and chosen second key in chosen column 2, for example Franz Schubert in composer column plus C major in key/tonality column.

### SCORE PART AND MIDI VISUALISATION:
The visualisation of the score is somewhat unreliable when done in Jupyter notebook. It does not mean it delivers wrong note values; however, the actual measure numbers can get lost or be misplaced alongside the other information (as articulation and other marks). Nonetheless, it serves its general purpose of rapidly visualising the data the user is interested in. This is done by [ interlied-view-midi-and-score ], which also delivers a midi excerpt of the same visualised piece. As an input, the user inserts the path to score, start and end measure. This function is supported by any software that can (re)produce musicXML format, but the preferred program must be set in the music21 package. If the user does not wish to interact with music21 code, the algorithms will automatically run it on a free software called MuseScore 2.0.  This InterLied???s algorithm is much more efficient in the interface as it opens the excerpt directly in the software, where a user can correct the possible faults, save it to their computer, plays and saves the midi etc. The [ interlied-save-midi ] option, which allows the user to download the midi file, is thus only available in Jupyter notebook. 

![Screenshot 2021-08-07 at 16 49 09](https://user-images.githubusercontent.com/76003382/128604121-fdeb8600-aa4a-42f2-ab48-dfdba154551c.png)


-------
## EXPLORATION:
This category of codes helps the user to further explore their acquired data or the pre-composed database that comes with the InterLied package. For more experienced programmers, these can be modified or rewritten, as they only provide a glimpse of what exploring data with Python can offer. These are also incorporated into the interface, although due to GUI???s performance, several functions may have a somewhat different structure from the ones offered in the notebook. In general, you can find the following in the notebook:

### *1. interlied_int_explore_lyric* 
It requires a dataframe acquired by one of the analysis function and returns a dictionary (e.g., info text) with the most common intervals and lyric words combinations in explored score. From this, we can explore in detail each instance where the interval and a specific word co-exist. The funciton is preset to explore the intervals dataframe, but can be easily adapted by changing one of the search parameters.

### *2. interlied_int_explore_lyric_token*
It requires the data frame of your choice, composer???s name, lyric token entry and interval entry. It returns a text with all information about these instances (from music parameters to metadata). We can notice that the data frame also requires composer information. This was added, assuming we may want to explore the same combinations within different corpora, or we have several composers stored in the same data frame. With slight modification this function can return a query of any desired parameters??? combination (for example replacing the composer for the lyricist, interval for rhythm pattern etc.). 

### *3. interlied_search_pattern_lyric_composer & interlied_search_melody_rhythm_composer*
It explores the relationship between lyric, rhythmic and melodic patterns, second of which replaces the lyric parameter with the rhythm. It returns all instances of the score where both patterns match. While the functions above deal with data from either intervals or patterns data, the last explore option concerns itself with the interlied_lyric output. It returns a list of most frequent words per score, alongside score???s title, composer, lyricist, and key.

### *4. interlied_words_count*
This funcion requires a single lyric csv file path as an input and computes the word instances per score, returning a dataframe with composer, title, key and most common words per row (e.g., score).

![Screenshot 2021-08-17 at 16 25 57](https://user-images.githubusercontent.com/76003382/129744511-49c5f51f-e2b7-4bd0-9cba-e6fe119d89b0.png)


-------
## TUTORIALS:

*This project will eventually offer a series of tutorials adapted to the computational beginners as well. After the full project will be published in September, you will find there a first tutorial - a case study on Slovenian 20th century Lieder using InterLied's tools.*

-------
InterLied is my master's thesis project, defended at the Pompeu Fabra University (SMC) under the mentorship of Dr Rafael Caro Repetto.

For more information about the project and the citation, click here: https://zenodo.org/record/5554859#.YXV6fdlBw-Q.
