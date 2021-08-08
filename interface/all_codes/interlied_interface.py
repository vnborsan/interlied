from imp import reload
from music21 import*
from tkinter import * 
import os
import sys 
import numpy as np
from tkinter import filedialog
import tkinter.font as font
from interlied_basics import interlied_intervals, interlied_pattern_analysis, interlied_lyric
from interlied_plots import interlied_pitch_plot, interlied_top_10_plot, interlied_word_freq_q_plot, interlied_lyric_freq_plot
from interlied_visualise import view_score
from interlied_explore import interlied_int_explore_lyric, interlied_int_explore_lyric_token, interlied_search_pattern_lyric_composer, interlied_words_count
import pandas as pd
import pandastable as pt
from pandastable import Table, TableModel
import itertools
from collections import OrderedDict
from operator import itemgetter
from nltk import ngrams
import operator
import re 
import csv
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter.messagebox import showinfo
from interlied_explore_intervals_patterns import intervals_lyric
from interiled_explore_lyric_only import lyric_only

#BASE STUFF

base = Tk()
base.title("INTERLIED - START MENU")
# H V
base.geometry("545x360")
base.configure(bg='#EBDDDC')

#FONTS
global titles
titles=font.Font(family = "Helvetica",size = 34, weight = "bold")
sub_titles=font.Font(family = "Helvetica",size = 24, weight = "bold")


#INSTRUCTION POP-UPS
def instruction_popup():	
		instrtk =Tk()
		instrtk.title("General instructions")
		instrtk.geometry("980x600")	
		with open("instructions.txt", "r") as f:
			Label(instrtk, text=f.read()).pack()

		instrtk.mainloop()



##BASICS##
def analysis_functions():

	def langs_popup():
		langtk =Tk()
		langtk.title("Available Languages")
		langtk.geometry("310x210")	
		with open("langs.txt", "r") as f:
			Label(langtk, text=f.read()).pack()

		langtk.mainloop()

	root =Tk()
	root.title("ANALYSIS")
	root.geometry("660x530")
	root.configure(bg='#FEF9E7')

	lang_label = Label(root, text="Insert Language Of Your Corpus", bg="#FEF9E7", font=('Helvetica', '16', 'bold'))
	lang_label.grid(row=4, column=0, columnspan=1, pady=10, padx=10, ipadx=143)
	lang_entry=Entry(root, width=15, borderwidth=5, text="Insert The Language")
	lang_entry.grid(row=6, column=0, columnspan=1, pady=10, padx=10, ipadx=143)
	lang_btn=Button(root, text="Check Available Languages",font=('Helvetica', '15', 'bold'), command=langs_popup)
	lang_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

	def run_intervals():
		my_xml_folder = filedialog.askdirectory()
		lang=lang_entry.get()
		print(my_xml_folder)
		intervals=interlied_intervals(str(my_xml_folder), lang)

	def run_ngrams():
		my_csv_folder = filedialog.askdirectory()
		print(my_csv_folder)
		ngram_f=interlied_pattern_analysis(str(my_csv_folder))

	def run_lyric():
		my_corpus = filedialog.askdirectory()
		lang=lang_entry.get()
		print(my_corpus)
		lyrics_f=interlied_lyric(str(my_corpus), lang)
			

	# xml_btn = Button(root, text="Upload CSV",command=pick_xml)
	# xml_btn.grid(row=1, column=3, columnspan=2, pady=10, padx=10, ipadx=143)
	# csv_btn = Button(root, text="Upload XML",command=pick_csv)
	# csv_btn.grid(row=2, column=3, columnspan=2, pady=10, padx=10, ipadx=143)

	label=Label(root, text="ANALYSIS TOOLS",font=('Helvetica', '20', 'bold'))
	label.grid(row=0, rowspan=4, column=0, columnspan=4, padx=5, pady=5)
	
	intervals_label = Label(root, text="Press the button below to run intervals function", bg="#FEF9E7", font=('Helvetica', '16', 'bold'))
	intervals_label.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=143)
	intervals_btn = Button(root, text="Run intervals function",font=('Helvetica', '20', 'bold'), command=run_intervals)
	intervals_btn.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=143)
	
	ngrams_label = Label(root, text="Press the button below to run patterns function", bg="#FEF9E7", font=('Helvetica', '16', 'bold'))
	ngrams_label.grid(row=16, column=0, columnspan=2, pady=10, padx=10, ipadx=143)
	ngrams_btn = Button(root, text="Run patterns function",font=('Helvetica', '20', 'bold'), command=run_ngrams) 
	ngrams_btn.grid(row=18, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

	lyric_label = Label(root, text="Press the button to run lyric function", bg="#FEF9E7", font=('Helvetica', '16', 'bold'))
	lyric_label.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=143)
	lyric_btn = Button(root, text="Run lyric function",font=('Helvetica', '20', 'bold'),command=run_lyric)
	lyric_btn.grid(row=23, column=0, columnspan=2, pady=10, padx=10, ipadx=143)


	exit_btn = Button(root, text = "Exit", font=('Helvetica', '20', 'bold'),command = root.destroy) 
	exit_btn.grid(row=24, rowspan=1, column=0, columnspan=4)

	
	root.mainloop()


def plots():
	plts =Tk()
	plts.title("CORPUS VISUALISATION")
	plts.geometry("1060x800")
	plts.configure(bg='#D4E6F1')


###RUN PLOTS	
	def run_top_10_plots(): #see top 10 parameters  in score
		try:
			my_csv = filedialog.askopenfilename(title="Select CSV File")
			interlied_top_10_plot(my_csv, str(e.get()))
			plt.tight_layout()
			plt.show()
			
		except Exception as r:
			print(r)
			print("Something went wrong. Check that your file is in csv format and your input is the actual name of a column.")
			
	def run_pitch_plots(): #plot freq of pitch in a score
			try:
				my_csv = filedialog.askopenfilename(title="Select XML File")
				interlied_pitch_plot(my_csv, str(e.get()))
				plt.tight_layout()
				plt.show()
			except:
				print("Something went wrong. Check that your file is in csv format and your input is the actual name of a column.")
				
	def run_f_q_plots(): #plot word freq per certain interval in certain score
		try:
			q1=f_q_1.get()
			q2=f_q_2.get()
			my_csv = filedialog.askopenfilename(title="Select CSV File")
			interlied_word_freq_q_plot(str(my_csv), q1, q2)
			plt.tight_layout()
			plt.show()
		except Exception as e:
			print (e)
			print("Something went wrong. Check that your file is in csv format and your input is the actual name of a column.")
				
	def run_lyric_freq_plots():
			# try:
		my_csv = filedialog.askopenfilename(title="Select !LYRIC! CSV File")
		qu1=k1.get()
		qu2=k2.get()
		qu3=k3.get()
		qu4=k4.get()
		interlied_lyric_freq_plot(str(my_csv), qu1, qu2, qu3, qu4)
		plt.tight_layout()
		plt.show()
			# except:
			# 	print("Something went wrong. Check that your file is in csv format and your input is the actual name of a column.")
				
	###RUN SCORE	
	def run_view_score():
		# try:
		my_xml = filedialog.askopenfilename(title="Select XML File")
		
		global info1
		global info2

		x, info1, info2=view_score(my_xml,msr1.get(),msr2.get())

		toplevel = Toplevel()
		label1 = Label(toplevel, text=info1, height=0, width=100)
		label1.pack()
		label2 = Label(toplevel, text=info2, height=0, width=100)
		label2.pack()

		return x.show()


	#BUTTONS AND LABELS FOR PLOTS

	title_plots = Label(plts, text="DATA AND SCORE VISUALISATIONS", bg="#D4E6F1", font=('Helvetica', '34', 'bold'))
	title_plots.grid(row=0, column=0, rowspan=1, columnspan=2, pady=1, padx=10, ipadx=120)

	empty1 = Label(plts, bg="#D4E6F1", font=('Helvetica', '16', 'bold'))
	empty1.grid(row=2, column=0, rowspan=2, columnspan=3, pady=1, padx=10, ipadx=120)
	
	
	#Score
	see_score_lbl = Label(plts, text="Insert desired START and END measures, press the button, chose your score and wait for the pre-set software to open.", bg="#FFFFFF", font=('Helvetica', '16', 'bold'))
	see_score_lbl.grid(row=6, column=0, rowspan=1, columnspan=2, pady=1, padx=10, ipadx=120)
	msr1 = Entry(plts, width=15, borderwidth = 5)
	msr1.insert(0, 'Insert Start Measure')
	msr1.grid(row=8, column=0)
	msr2 = Entry(plts, width=15, borderwidth = 5)
	msr2.insert(0, 'Insert END Measure')
	msr2.grid(row=8, column=1)
	see_score = Button(plts, text='SHOW SCORE', font=('Helvetica', '20', 'bold'), command=run_view_score)
	see_score.grid(row=9, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)
	
	empty2 = Label(plts, bg="#D4E6F1", font=('Helvetica', '16', 'bold'))
	empty2.grid(row=11, column=0, rowspan=2, columnspan=3, pady=1, padx=10, ipadx=120)
	
	#Top 10
	see_10_lbl = Label(plts, text="Insert desired QUERY, press the button, chose your CSV and wait for the plot.", bg="#FFFFFF", font=('Helvetica', '16', 'bold'))
	see_10_lbl.grid(row=14, column=0, rowspan=2, columnspan=2, pady=1, padx=10, ipadx=120)
	e = Entry(plts, width=30, borderwidth = 5)
	e.insert(0, 'Insert CSV Column Name')
	e.grid(row=16, column=0, columnspan=3)
	see_10 = Button(plts, text='PLOT TOP 10', font=('Helvetica', '20', 'bold'), command=run_top_10_plots)
	see_10.grid(row=17, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)

	empty3 = Label(plts, bg="#D4E6F1", font=('Helvetica', '16', 'bold'))
	empty3.grid(row=19, column=0, rowspan=2, columnspan=3, pady=1, padx=10, ipadx=120)
	

	#Freq - 2 Queries
	see_2q_lbl = Label(plts, text="Insert desired 2 QUERIES, press the button, chose your CSV and wait for the plot.", bg="#FFFFFF", font=('Helvetica', '16', 'bold'))
	see_2q_lbl.grid(row=22, column=0, rowspan=2, columnspan=2, pady=1, padx=10, ipadx=120)
	f_q_1=Entry(plts, width=30, borderwidth = 5)
	f_q_1.insert(0, 'Insert CSV Column Name')
	f_q_1.grid(row=24, column=0)
	f_q_2=Entry(plts, width=30, borderwidth=5)
	f_q_2.insert(0, 'Insert CSV Column Value')
	f_q_2.grid(row=24, column=1)
	see_2q = Button(plts, text='PLOT YOUR 2 QUERIES', font=('Helvetica', '20', 'bold'), command=run_f_q_plots)
	see_2q.grid(row=26, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)


	empty4 =Label(plts, bg="#D4E6F1", font=('Helvetica', '16', 'bold'))
	empty4.grid(row=28, column=0, rowspan=2, columnspan=3, pady=1, padx=10, ipadx=120)
	
	#Freq - 4 Queries	
	see_4q_lbl = Label(plts, text="Insert desired 4 QUERIES, press the button, chose your CSV and wait for the plot.", bg="#FFFFFF", font=('Helvetica', '16', 'bold'))
	see_4q_lbl.grid(row=31, column=0, rowspan=2, columnspan=2, pady=1, padx=10, ipadx=120)
	k1=Entry(plts, width=30, borderwidth = 5)
	k1.insert(0, 'Insert CSV Column Name 1')
	k1.grid(row=33, column=0)
	k2=Entry(plts, width=30, borderwidth = 5)
	k2.insert(0, 'Insert CSV Column Value 1')	
	k2.grid(row=34, column=0)
	k3=Entry(plts, width=30, borderwidth = 5)
	k3.insert(0, 'Insert CSV Column Name 2')	
	k3.grid(row=33, column=1)
	k4=Entry(plts, width=30, borderwidth = 5)
	k4.insert(0, 'Insert CSV Column Value 2')	
	k4.grid(row=34, column=1)
	see_4q = Button(plts, text='PLOT YOUR 4 QUERIES', font=('Helvetica', '20', 'bold'), command=run_lyric_freq_plots)
	see_4q.grid(row=36, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)

	#EXIT BUTTON
	exit_btn = Button(plts, text = "EXIT",font=('Helvetica', '15', 'bold'), command = plts.destroy) 
	# exit_btn.pack()
	exit_btn.grid(row=40, rowspan=1, column=0, columnspan=3, padx=10, pady=10)

	plts.mainloop()

##############################################################################################
##############################################################################################

def explore_corpus():
	b_f=font.Font(family='Courier', size = 33)
	exp =Tk()
	exp.title("EXPLORE CORPUS")
	exp.geometry("530x200")
	exp.configure(bg='#C0FF9A')
	
#FUNCTIONS
	def run_intervals_lyic():
	        return intervals_lyric()

	def run_lyric_only():
	        return lyric_only()

#Label
	label=Label(exp, text="Explore Your Corpus", font=('Helvetica', '20', 'bold'))
	label.grid(row=1,rowspan=2, column=0, columnspan=4, padx=5, pady=5)

# BUTTONS
	first_btn = Button(exp, text=" Intervals or Patterns & Lyric", font=('Helvetica', '18', 'bold'), command=run_intervals_lyic)
	first_btn.grid(row=6, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)
	
	second_btn = Button(exp, text='Lyric Only', font=('Helvetica', '18', 'bold'), command=run_lyric_only)
	second_btn.grid(row=9, column=0, rowspan=1, columnspan=2, pady=10, padx=10, ipadx=120)


	exit_btn = Button(exp, text = "Exit",font=('Helvetica', '15', 'bold'), command = exp.destroy) 
	exit_btn.grid(row=11, rowspan=1, column=0, columnspan=3, padx=10, pady=10)

	exp.mainloop()

##############################################################################################
##############################################################################################

#BASE STUFF
label=Label(base, text="Welcome to InterLied", font=titles)
label.grid(row=1,rowspan=4, column=0, columnspan=4, padx=5, pady=5)

instructions_btn=Button(base, text="1. INSTRUCTIONS",font=sub_titles,command=instruction_popup)
instructions_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=138)

functions_btn = Button(base, text="2. DATA ANALYSIS",font=sub_titles,command=analysis_functions)
functions_btn.grid(row=6, column=0, columnspan=2, pady=5, padx=5, ipadx=120)

other_btn = Button(base, text="3. DATA VISUALISATON",font=sub_titles,command=plots)
other_btn.grid(row=7, column=0, columnspan=2, pady=5, padx=5, ipadx=117)

other_btn = Button(base, text="4. EXPLORE DATA",font=sub_titles,command=explore_corpus)
other_btn.grid(row=8, column=0, columnspan=2, pady=5, padx=5, ipadx=117)

exit_btn = Button(base, text = "EXIT", font=sub_titles, command = base.destroy) 
exit_btn.grid(row=12, rowspan=1, column=0, columnspan=4, padx=15, pady=15)

base.mainloop()

# root.mainloop()
