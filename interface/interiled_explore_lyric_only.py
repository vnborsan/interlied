"""
This function explores lyric patterns with some complimentary data, such as composer, title, lyricist and tonality. The data acqired by function interlied_lyric is structured as a prerequisit text for further text analysis or natural language processing.
*Input: dataframe obtained by interlied_lyric function.
*Queries input: Define the keywords by which you wish to refine your data as indicated above the frames.
*Output: Refined dataframe.

Note: If nothing appears, your dataframe does not contain the searches you have input.

If you wish to adapt the search queries, go to the "row iteration" code (e.g., "for row in rows:") and adjust the row element number you wish to observe.
For easier usage, find the defined rows by numbers below (e.g. row[0]):
    0= row index
    1= composer
    2= title
    3= lyric
    4= tokenized_lyric
    5= reduced_tokens
    6=lyricist _ADD
    7= lyric_language _ADD
    8= key
    
"""

def lyric_only():
    
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk, Entry

    import pandas as pd

    # initalise the tkinter GUI
    root = tk.Tk()

    root.geometry("700x720") # set the root dimensions
    root.configure(bg='#EFFFE6')
    root.title("Explore Lyric Only")
    root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
    root.resizable(0, 0) # makes the root window fixed in size.

    # Frame for TreeView
    frame1 = tk.LabelFrame(root, text="Excel Data")
    frame1.place(height=250, width=660)

    # Frame for open file dialog
    file_frame = tk.LabelFrame(root, text="Open File")
    file_frame.place(height=100, width=700, rely=0.35, relx=0)
    
    #Frame for Queries
    q_frame = tk.LabelFrame(root, text="Input Queries")
    q_frame.place(height=300, width=700, rely=0.50, relx=0)

    # Buttons
    button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
    button1.place(rely=0.65, relx=0.50)

    button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
    button2.place(rely=0.65, relx=0.30)

    # The file/file path text
    label_file = ttk.Label(file_frame, text="No File Selected")
    label_file.place(rely=0, relx=0)

    label_q1 = ttk.Label(q_frame, text="Insert Composer")
    label_q1.place(rely=0.30, relx=0.05)

    label_q2 = ttk.Label(q_frame, text="Title")
    label_q2.place(rely=0.30, relx=0.35)

    label_q3 = ttk.Label(q_frame, text="Lyric token")
    label_q3.place(rely=0.30, relx=0.65)

    label_q4 = ttk.Label(q_frame, text="Lyricist")
    label_q4.place(rely=0.60, relx=0.05)

    label_q5 = ttk.Label(q_frame, text="Insert Language")
    label_q5.place(rely=0.60, relx=0.35)

    label_q6 = ttk.Label(q_frame, text="Insert Key")
    label_q6.place(rely=0.60, relx=0.65)

    #Entries
    q1= Entry(q_frame) #Composer
    q1.place(rely=0.40, relx=0.05)

    q2= Entry(q_frame) #Title
    q2.place(rely=0.40, relx=0.35)

    q3= Entry(q_frame) #Reduced Tokens
    q3.place(rely=0.40, relx=0.65)

    q4= Entry(q_frame) #Lyricist
    q4.place(rely=0.70, relx=0.05)

    q5= Entry(q_frame) #Language
    q5.place(rely=0.70, relx=0.35)

    q6= Entry(q_frame) #Key
    q6.place(rely=0.70, relx=0.65)


    ## Treeview Widget
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


    def File_dialog():
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetypes=(("csv files", "*.csv"),("All Files", "*.*")))
        label_file["text"] = filename
        return None


    def Load_excel_data():
        """If the file selected is valid this will load the file into the Treeview"""
        file_path = label_file["text"]

        #Get Queries from Entries

        composer_q=str(q1.get())
        title_q=str(q2.get())
        token_q=str(q3.get())
        lyricist_q=str(q4.get())
        lang_q=str(q5.get())
        key_q=str(q6.get())

        
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                df = pd.read_csv(excel_filename)
            else:
                df = pd.read_excel(excel_filename)

        except ValueError:
            tk.messagebox.showerror("Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information", f"No such file as {file_path}")
            return None

        clear_data()

        tv1["column"] = list(df.columns)
        tv1["show"] = "headings"

        for column in tv1["columns"]:
            tv1.heading(column, text=column) # let the column heading = column name

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists

        for row in df_rows:
            if (composer_q in str(row[1])) and (title_q in str(row[2])) and (token_q in row[4]) and (lyricist_q in str(row[6])) and (lang_q in str(row[7])) and (key_q in str(row[8])):
                tv1.insert("", "end", values=row) # inserts each list into the treeview. 
            else:
                # for row in df_rows:
                #     tv1.insert("", "end", values=row) # inserts each list into the treeview. 
                continue

        return None

    def search_excel_data():
        tv1["column"] = list(df.columns)
        return list(df.columns)


    def clear_data():
        tv1.delete(*tv1.get_children())
        return None


    root.mainloop()
