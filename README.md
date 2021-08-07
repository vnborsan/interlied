# InterLied 1.0

InterLied is a set of python GUI (interface) and python notebook, both designed for computational music analysis. Although it is adapted for analysing vocal pieces only, lieder in particular, a majority of its tools can be useful for other purposes as well. 
The notebook is appropriate for both, computationally advanced and beginner users. If you assume, you belong to the latter, please go through these instructions first and then open the GUI. The notebook does not require any coding experience; however, you are strongly encouraged to not only utilise the GUI, but also the InterLied
notebook. All parameters are described in the notebook itself, thus, in order to get to it, scroll through the instructions bellow and first install Python3, install all the (missing) prerequisite dependencies and MuseScore or any other software for symbolic notation.

------
## 1. INSTALL DEPENDENCIES:

To use GUI or the notebook, first install all prerequired dependencies. You can do that automatically by opening terminal (Linux / Mac OS) or prompt command (Windows) and type in:
 "cd your/path/to/interface/Interlied_1.0"

When you successfully enter the folder, type this command into terminal: 
"python interlied_dependencies.py"

If you run into some errors, install the required packages manually by following instructions in the INTERLIED_USER_MANUAL.

------
## 2. ACCESS THE INTERLIED TOOLS:

The Interlied offers 2 different types of accessing the codes:

### 2.1 Jupyter notebook + scripts
To use this option, install jupyter notebook (https://jupyter.org/install). The notebook includes all of the basic code explanations and execution commands.

### 2.2 GUI
If you do not wish to interact with code, simply download the interface part above, enter the folder through terminal / prompt command and then run "python interlied_interface.py".

-------
## 3. PACKAGE INTRODUCTION:

The codes are separated into 3 categories:

### 3.1 ANALYSIS
- The first group of 3 alogrithms processes your scores and prepares dataframes (in csv form) for further data exploring.
### 3.2 VISUALISATIONS 
- Plots and other visual representations allow for your data to be refined and visually represented by graphs, as music notation and / or midi.
### 3.3 EXPLORATION 
- This section offers an easy access to refined data by your desired keywords.

![Screenshot 2021-08-07 at 16 47 43](https://user-images.githubusercontent.com/76003382/128604082-0da9c24a-bddd-4e26-a02a-83608b040699.png)

------
## ANALYSIS:
The three basic algorithms that serve for data preparation, separately focusing on melodic intervals, music patterns and lyric. 

### - INTERVALS (interlied_intervals):

The function called [interlied_intervals] turns a MusicXML file to a pandas data frame that is purposefully saved to user’s computer as CSV. From each score, it extracts metadata information and information related to the music analysis. Algorithm only observes the first, assuming vocal, part (e.g., score.parts[0])). With music21 function of ‘segmentByRests’, the algorithm ignores the relationships between two consecutive notes divided by breaks. From that, a complete interval sequence list is created within the loop for each composition. Each interval element includes the ascending (plus), descending (minus) or oblique (underscore) symbol, thus M-2 and M+2 is not considered to be the same interval. This is useful especially when trying to grasp the vocal contours, to observe the score’s peaks and to explore lyrics semantics. Intervals are described as follows, 
- *P5 = Perfect (fifth)*
- *A4 = Augmented (fourth)*
- *D4 = Diminished (fourth)*
- *M3 = Major (third)*
- *m2 = minor (second)*

The algorithm first defines the interval and appends the metadata information (e.g., title, composer, lyricist, and year ) to each. If metadata information is missing form the score, the field is marked with “None”. This can later be substituted or filled in manually. All interval elements also come with the following music analysis parameters, mainly supported by music21 algorithms:

- *Start and end measure of the interval.*
- *Rhythm values consist of a tuple of both rhythmic note values of the interval, (example: M+2 = (0.5, 1.0), where 0.5 equals one eight note and 1.0 equals one quarter note).*
- *Key is predicted with The Krumhansl-Schmuckler Key-Finding Algorithm, a built-in option with music21.*
- *In addition to the most probable key, the function offers alternative keys, writing down the top three most feasible guesses, also supported by music21 algorithm.*
- *Voice range is computed between the lowest and highest note value in the vocal part and is expressed as an interval (for example, M9).*
- *Meter change confirms whether the score has a meter change by YES/NO, and exact meter or meters are computed and written down afterwards, in format of a dictionary.*
- *The first method for lyrics extracts the ‘assembled lyrics’ per interval. This means that the system takes all words at least partially connected to each note of the interval to make the process of lyrics segmentation / exploration.
- *Second method tokenizes the lyric words per interval.*
- *The last method removes any stopwords we have set in advance.*
- *The final parameter is the language of the lyric.*

This algorithm is using NLTK packages, so if the language is included in their repository a user can access it through inserting the desired language (as a string) to the second input. The first input of this algorithm expects a folder of musicXML files. As an output, it writes all the information presented above in both, csv file, which is saved to user’s computer and pandas data frame, which can be further used in the code itself.

### - PATTERNS (interlied_pattern_analysis):

The intervals data tables, produced by the first function, can serve as an input to the next function, called [interlied_pattern_analysis]. What this particular algorithm does is to compute all n-grams (2<n<30) or patterns from the interval sequence obtained through the [interlied_intervals] function. Some data is collected for the first of the two grams only, assuming the information will inevitably be identical for the next gram as well. This is true for the metadata (title, composer, lyricist), score key, alternative score key(s), score meter(s), score’s voice range and lyric language. Start measure number is retrieved from the first note of the first gram, and end measure is retrieved from the last note of the last interval of selected pattern. The lyrics elements represent a gathered bundle of words from all grams. Additionally, the user is also offered the information about pattern length. Since pattern is considered to be a repeated event, the function erases all grams that are unique. The user is informed about the quantity of patterns that were excluded from consideration. The output is the same as in intervals data table, thus data frame written onto the user’s computer as CSV file, but also remains as a pandas data frame variable, that can be further referenced in the code.

### - LYRIC:

The [interlied_lyric] function includes less meta and musical data, but rather focuses on preparing the lyric in whole per score. The first two functions only deliver short excerpts of the lyric or tokens connected to much smaller pieces (e.g., interval or repeated pattern), while this, on the other hand, prepares the lyric with an aid of NLTK  Python package. It first extracts the lyric form the musicXML score, then tokenizes it and in the end, removes the stopwords. The collection of the latter is already provided with the NLTK package in many languages, among them English, Italian, French, Spanish, etc. You can find the available options listed in the interface. For the purpose of my own research, I extended the provided list of words for slovenian language. The rest of the offered language lists remain unchanged.  The extension was done especially for the purpose of my targeted corpus as I have noticed that the articulations and other text marks in the score occasionally find their way to the lyric transcription, thus I have removed words such as rall., allegro, andante, and so on. The transcribed and processed text of three described types is accompanied by the data about the lyricist, composer, and tonality, but can easily be extended should the user require more information. The inputs of this algorithm are first, a folder of musicXML scores and second, the chosen language. The outputs are a pandas dataframe and five text strings, providing some statistical information about the corpus. As the other two functions, this one stores a csv file to your computer as well.

![Screenshot 2021-08-07 at 16 48 32](https://user-images.githubusercontent.com/76003382/128604107-df0ba480-1ac7-4a59-a0f2-18655fe1a879.png)

-------
## VISUALISATIONS:

There are four types of plots. 
### *1. interlied_pitch_plot:*
It realises the music21 score plot in the form of piano roll and pitch representation. It requires a single musicXML score to run and returns two colourful plots, which can be, as any other plots in this sub-chapter, downloaded onto the user’s computer. As the music21 presents a larger issue to be incorporated into the interface, this plot is for now only accessible through the Jupyter notebook. 

### *2. interlied_top_10_plot:*
It accepts any type of csv and a query, which should be the name of one column in the chosen csv. The algorithm returns a plot of ten most frequently fully repeated elements in that query and csv.

### *3. interlied_word_freq_q_plot:* 
It takes one csv (or directly the pandas data frame if we slightly modify the code) and two queries. Its pre-set function accepts a type of interval (e.g., M+3) as the query 1 and a score’s title as query 2. Based on the user’s input it delivers a plot of word frequency of all tokens that appear in the combination with the queries. Mind that this code is very easily modified and can explore word tokens through other parameters as well, replacing the ‘interval’ and ‘title’ with desired alternatives. 

### *4. interlied_lyric_freq_plot:* 
This one also explores the lyric, but instead of the pattern or an interval, utilises the lyric data frame. It takes one csv file in which it plots the frequency of words for chosen first key in chosen column 1 and chosen second key in chosen column 2, for example Franz Schubert in composer column plus C major in key/tonality column.

### SCORE PART AND MIDI VISUALISATION:
The visualisation of the score is somewhat unreliable when done in Jupyter notebook. It does not mean it delivers wrong note values; however, the actual measure numbers can get lost or be misplaced alongside the other information (as articulation and other marks). Nonetheless, it serves its general purpose of rapidly visualising the data the user is interested in. This is done by [ interlied-view-midi-and-score ], which also delivers a midi excerpt of the same visualised piece. As an input, the user inserts the path to score, start and end measure. This function is supported by any software that can (re)produce musicXML format, but the preferred program must be set in the music21 package. If the user does not wish to interact with music21 code, the algorithms will automatically run it on a free software called MuseScore 2.0.  This InterLied’s algorithm is much more efficient in the interface as it opens the excerpt directly in the software, where a user can correct the possible faults, save it to their computer, plays and saves the midi etc. The [ interlied-save-midi ] option, which allows the user to download the midi file, is thus only available in Jupyter notebook. 

![Screenshot 2021-08-07 at 16 49 09](https://user-images.githubusercontent.com/76003382/128604121-fdeb8600-aa4a-42f2-ab48-dfdba154551c.png)


-------
## EXPLORATION:

![Screenshot 2021-08-07 at 16 50 55](https://user-images.githubusercontent.com/76003382/128604197-f707101c-2a9e-4992-9873-fd066da4e40c.png)


-------

