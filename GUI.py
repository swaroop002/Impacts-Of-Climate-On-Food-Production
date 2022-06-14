import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import unknown_support
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import isfile, join
import datapackage
from numpy import mean
from numpy import std
from scipy.stats import pearsonr
from matplotlib import pyplot
import xlsxwriter
def rel(data):
    rel=""
    if data>=-1 and data<=-0.5:
        rel="negative"
    elif data>=-0.5 and data<=-0.2:
        rel="slight negative"
    elif data>=-0.2 and data<=0.2:
        rel="zero"
    elif data>=0.2 and data<=0.5:
        rel="slight positive"
    elif data>=0.5 and data<=1:
        rel="positive"
    return rel
def prod_wrt_rain(data):
    status="Conclusion W.R.T Rainfall\n"
    if data>=-1 and data<=-0.2:
        status=status+"1) Production is Likely to Increase if The Rainfall Decreases On which the Price Decreases\n2) Production is Likely to Decrease if The Rainfall Increases On which the Price Increases"
    elif data>=-0.2 and data<=0.2:
        status=status+"1) Production remains Unaffected unless there is a Drastic Change in The Rainfall. The Price remains Unchanged"
    elif data>=0.2 and data<=1:
        status=status+"1) Production is Likely to Increase if The Rainfall Increases On which the Price Decreases\n2) Production is Likely to Decrease if The Rainfall Decreases On which the Price Increases"
    return status        
def prod_wrt_temp(data):
    status="Conclusion W.R.T Temperature\n"
    if data>=-1 and data<=-0.2:
        status=status+"1) Production is Likely to Increase if The Temperature Decreases On which the Price Decreases\n2) Production is Likely to Decrease if The Temperature Increases On which the Price Increases"
    elif data>=-0.2 and data<=0.2:
        status=status+"1) Production remains Unaffected unless there is a Drastic Change in The Temperature The Price remains Unchanged"
    elif data>=0.2 and data<=1:
        status=status+"1) Production is Likely to Increase if The Temperature Increases On which the Price Decreases\n2) Production is Likely to Decrease if The Temperature Decreases On which the Price Increases"
    return status

files = [f for f in listdir("data/Crops") if isfile(join("data/Crops",f))]
crops=[]
for  file in files:
    cr=file.split(".")
    cr=cr[0]
    cr=cr.capitalize()
    crops.append(cr)
workbook = xlsxwriter.Workbook('Output/Overview.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Crops')
worksheet.write('B1', 'Yield & Rainfall')
worksheet.write('C1', 'Area Harvested & Rainfall')
worksheet.write('D1', 'Production & Rainfall')
worksheet.write('E1', 'Rainfall Average')
worksheet.write('F1', 'Yield & Temperature')
worksheet.write('G1', 'Area Harvested & Temperature')
worksheet.write('H1', 'Production & Temperature')
worksheet.write('I1', 'Temperature Average')

df_temp = pd.read_csv("data/temperature.csv")
df_rain = pd.read_csv("data/rainfall.csv")
r=1
c=0
for file in files:
    cr=file.split(".")
    
    
    cr=cr[0]
    cr=cr.capitalize()
    worksheet.write(r, c, cr)
    c=c+1
    sum=0
    df_crop = pd.read_csv("data/Crops/"+file)
    df_yields=df_crop[df_crop['Element']=='Yield']
    df_area=df_crop[df_crop['Element']=='Area harvested']
    df_prod=df_crop[df_crop['Element']=='Production']
    corr, _ = pearsonr(df_prod['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1

    corr, _ = pearsonr(df_area['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1

    corr, _ = pearsonr(df_yields['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1
    worksheet.write(r, c, rel(sum/3))
    c=c+1
    sum=0
    corr, _ = pearsonr(df_prod['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1

    corr, _ = pearsonr(df_area['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1

    corr, _ = pearsonr(df_yields['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, rel(corr))
    c=c+1
    worksheet.write(r, c, rel(sum/3))
    c=c+1
    r=r+1
    c=0
workbook.close()
workbook = xlsxwriter.Workbook('Output/Detailed.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Crops')
worksheet.write('B1', 'Yield & Rainfall')
worksheet.write('C1', 'Area Harvested & Rainfall')
worksheet.write('D1', 'Production & Rainfall')
worksheet.write('E1', 'Rainfall Average')
worksheet.write('F1', 'Yield & Temperature')
worksheet.write('G1', 'Area Harvested & Temperature')
worksheet.write('H1', 'Production & Temperature')
worksheet.write('I1', 'Temperature Average')

df_temp = pd.read_csv("data/temperature.csv")
df_rain = pd.read_csv("data/rainfall.csv")
r=1
c=0
for file in files:

    cr=file.split(".")
    
    sum=0
    cr=cr[0]
    cr=cr.capitalize()
    worksheet.write(r, c, cr)
    c=c+1
    df_crop = pd.read_csv("data/Crops/"+file)
    df_yields=df_crop[df_crop['Element']=='Yield']
    df_area=df_crop[df_crop['Element']=='Area harvested']
    df_prod=df_crop[df_crop['Element']=='Production']
    corr, _ = pearsonr(df_prod['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    c=c+1

    corr, _ = pearsonr(df_area['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    c=c+1

    corr, _ = pearsonr(df_yields['Value'], df_rain['ANN'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    c=c+1
    worksheet.write(r, c, (sum/3))
    c=c+1
    sum=0
    
    corr, _ = pearsonr(df_prod['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    c=c+1

    corr, _ = pearsonr(df_area['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    c=c+1

    corr, _ = pearsonr(df_yields['Value'], df_temp['ANNUAL'])
    sum=sum+corr
    worksheet.write(r, c, corr)
    
    c=c+1
    worksheet.write(r, c, (sum/3))
    c=c+1
    r=r+1
    c=0
workbook.close()
avg_temp=df_temp['ANNUAL'].mean()
avg_rain=df_rain['ANN'].mean()

def realtime_prod_wrt_temp(avg_wrt_temp,r_temp):
    status=""
    global avg_temp
    bw=avg_temp*0.40
    low=avg_temp-bw
    high=avg_temp+bw
    status="Conclusion W.R.T Temperature\n"
    if(not(r_temp>high or r_temp<low)):
        if avg_wrt_temp>=-1 and avg_wrt_temp<=-0.1:
            if(r_temp<(avg_temp-(avg_temp*0.05))):
                status=status+"Production is Likely to Increase as The Temperature Is Below Average which will cause the Price to Decreases"
            
            elif(r_temp>(avg_temp+(avg_temp*0.05))):
                status=status+"Production is Likely to Decrease as The Temperature Is Above Average Causing the Price to Increase"
            
            else:
                status=status+"Production would be Slightly affected.\n This will cause The Price to remain Unchanged"
                
        elif avg_wrt_temp>=0.2 and avg_wrt_temp<=1:
            if(r_temp<(avg_temp-(avg_temp*0.10))):
                status=status+"Production is Likely to Decrease as The Temperature Is Below Average which will cause the Price to Increases"
            
            elif(r_temp>(avg_temp+(avg_temp*0.10))):
                status=status+"Production is Likely to Increase as The Temperature Is Above Average Causing the Price to Decrease"
            
            else:
                status=status+"Production would be Slightly affected.\n This will cause The Price to remain Unchanged"
            
        else:
            status=status+"Production would be Slightly affected.\n This will cause The Price to Slightly Change"
            
    else:
        status=status+"This will Diversly affect the production and price aswell"
    return status

def realtime_prod_wrt_rain(avg_wrt_rain,r_rain):
    status="\nConclusion W.R.T Rainfall\n"
    global avg_rain
    bw=avg_rain*0.70
    low=avg_rain-bw
    high=avg_rain+bw
    if(not(r_rain>high or r_rain<low)):
        if avg_wrt_rain>=-1 and avg_wrt_rain<=-0.1:
            if(r_rain<(avg_rain-(avg_rain*0.1))):
                status=status+"Production is Likely to Increase as The Rainfall Is Below Average which will cause the Price to Decreases"
            
            elif(r_rain>(avg_rain+(avg_rain*0.1))):
                status=status+"Production is Likely to Decrease as The Rainfall Is Above Average Causing the Price to Increase"
            
            else:
                status=status+"Production would be Slightly affected.\n This will cause The Price to remain Unchanged"
                
        elif avg_wrt_rain>=0.2 and avg_wrt_rain<=1:
            if(r_rain<(avg_rain-(avg_rain*0.1))):
                status=status+"Production is Likely to Decrease as The Rainfall Is Below Average which will cause the Price to Increases"
            
            elif(r_rain>(avg_rain+(avg_rain*0.1))):
                status=status+"Production is Likely to Increase as The Rainfall Is Above Average Causing the Price to Decrease"
            
            else:
                status=status+"Production would be Slightly affected.\n This will cause The Price to remain Unchanged"
            
        else:
            status=status+"Production would be Slightly affected.\n This will cause The Price to Slightly Change"
            
    else:
        status=status+"This will Diversly affect the production and price aswell"
    return status


crop=""
crop1=""
#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 7.2
#  in conjunction with Tcl version 8.6
#    Feb 06, 2022 11:44:05 AM IST  platform: Windows NT




class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("1280x720+128+18")
        top.minsize(120, 1)
        top.maxsize(3204, 853)
        top.resizable(width=False, height=False)
        top.title("Agrigultural Data Analysis")
        top.configure(background="#ffffff")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top
        self.combobox = tk.StringVar()
        self.combobox1 = tk.StringVar()
        
        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.0, rely=-0.014, height=90, width=1277)
        self.Label1.configure(activebackground="#ffffff")
        self.Label1.configure(activeforeground="#7d8280")
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(borderwidth="0")
        self.Label1.configure(compound='center')
        self.Label1.configure(disabledforeground="#7d8280")
        self.Label1.configure(font="-family {Sitka Heading} -size 32 -weight bold")
        self.Label1.configure(foreground="#000040")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Impacts Of Climate on Food Production And Supply''')

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.102, rely=0.097, height=40, width=120)
        self.Button1.configure(activebackground="#ffffff")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#ffffff")
        self.Button1.configure(borderwidth="3")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief="solid")
        self.Button1.configure(state='active')
        self.Button1.configure(text='''Overview''')
        self.Button1["command"] = self.Button1_command

        self.Button1_1 = tk.Button(self.top)
        self.Button1_1.place(relx=0.438, rely=0.097,height=40, width=120)
        self.Button1_1.configure(activebackground="#ffffff")
        self.Button1_1.configure(activeforeground="#000000")
        self.Button1_1.configure(background="#ffffff")
        self.Button1_1.configure(borderwidth="3")
        self.Button1_1.configure(compound='left')
        self.Button1_1.configure(disabledforeground="#a3a3a3")
        self.Button1_1.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Button1_1.configure(foreground="#000000")
        self.Button1_1.configure(highlightbackground="#d9d9d9")
        self.Button1_1.configure(highlightcolor="black")
        self.Button1_1.configure(pady="0")
        self.Button1_1.configure(relief="solid")
        self.Button1_1.configure(text='''Detailed Result''')
        self.Button1_1["command"] = self.Button1_1command

        self.Button1_1_1 = tk.Button(self.top)
        self.Button1_1_1.place(relx=0.758, rely=0.097, height=40, width=120)
        self.Button1_1_1.configure(activebackground="#ffffff")
        self.Button1_1_1.configure(activeforeground="#000000")
        self.Button1_1_1.configure(background="#ffffff")
        self.Button1_1_1.configure(borderwidth="3")
        self.Button1_1_1.configure(compound='left')
        self.Button1_1_1.configure(disabledforeground="#a3a3a3")
        self.Button1_1_1.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Button1_1_1.configure(foreground="#000000")
        self.Button1_1_1.configure(highlightbackground="#d9d9d9")
        self.Button1_1_1.configure(highlightcolor="black")
        self.Button1_1_1.configure(pady="0")
        self.Button1_1_1.configure(relief="solid")
        self.Button1_1_1.configure(text='''Real-Time Data''')
        self.Button1_1_1["command"] = self.Button1_1_1command

        
        self.Labelframe1_1 = tk.LabelFrame(self.top)
        self.Label2 = tk.Label(self.Labelframe1_1)
        self.Label2.place(relx=0.452, rely=0.05, height=30, width=94
                , bordermode='ignore')
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''OVERVIEW''')
        self.Label2_1 = tk.Label(self.Labelframe1_1)
        self.Label2_1.place(relx=0.46, rely=0.518, height=30, width=84
                , bordermode='ignore')
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(anchor='w')
        self.Label2_1.configure(background="#ffffff")
        self.Label2_1.configure(compound='left')
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''DETAILED''')
        # Create a Treeview widget
        tree = ttk.Treeview(self.Labelframe1_1)
        df = pd.read_excel("Output/Overview.xlsx")
        # Clear all the previous data in tree
        tree.delete(*tree.get_children())
        # Add new data in Treeview widget
        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        # For Headings iterate over the columns
        for col in tree["column"]:
           tree.heading(col, text=col)
           tree.column(col,width=100,anchor=tk.CENTER)
        # Put Data in Rows
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
              tree.insert("", "end", values=row)
        tree.place(relx=0.016, rely=0.1, relheight=0.409, relwidth=0.972, bordermode='ignore')
        tree2 = ttk.Treeview(self.Labelframe1_1)
        df = pd.read_excel("C:/Users/swaro/Project/Output/Detailed.xlsx")
        # Clear all the previous data in tree
        tree2.delete(*tree2.get_children())
        # Add new data in Treeview widget
        tree2["column"] = list(df.columns)
        tree2["show"] = "headings"
        # For Headings iterate over the columns
        for col in tree["column"]:
           tree2.heading(col, text=col)
           tree2.column(col,width=100,anchor=tk.CENTER)
        # Put Data in Rows
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
              tree2.insert("", "end", values=row)
        tree2.place(relx=0.016, rely=0.568, relheight=0.409, relwidth=0.971, bordermode='ignore')
        self.Labelframe1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)
        self.Labelframe1_1.configure(relief='groove')
        self.Labelframe1_1.configure(borderwidth="3")
        self.Labelframe1_1.configure(font="-family {Sitka Heading} -size 20 -weight bold")
        self.Labelframe1_1.configure(foreground="black")
        self.Labelframe1_1.configure(text='''Overview''')
        self.Labelframe1_1.configure(background="#ffffff")
        self.Labelframe1_1.configure(highlightbackground="#060606")
        self.Labelframe1_1.configure(highlightcolor="#060606")

        
        self.Labelframe1_1_1 = tk.LabelFrame(self.top)
        self.Label2 = tk.Label(self.Labelframe1_1_1)
        self.Label2.place(relx=0.016, rely=0.067, height=31, width=86, bordermode='ignore')
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Select Crop''')

        self.TCombobox1 = ttk.Combobox(self.Labelframe1_1_1)
        self.TCombobox1.place(relx=0.095, rely=0.067, relheight=0.052, relwidth=0.129, bordermode='ignore')
        self.TCombobox1.configure(font="-family {Segoe UI} -size 11")
        self.TCombobox1.configure(textvariable=self.combobox)
        self.TCombobox1['values']=crops
        self.combobox.set('''Select one''')
        self.TCombobox1.configure(takefocus="")

        self.Label3 = tk.Label(self.Labelframe1_1_1)
        self.Label3.place(relx=0.024, rely=0.15, height=51, width=187, bordermode='ignore')
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Segoe UI} -size 22 -weight bold")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''''')

        self.Button1_1_1_1 = tk.Button(self.Labelframe1_1_1)
        self.Button1_1_1_1.place(relx=0.278, rely=0.067, height=30, width=110, bordermode='ignore')
        self.Button1_1_1_1.configure(activebackground="#ffffff")
        self.Button1_1_1_1.configure(activeforeground="#000000")
        self.Button1_1_1_1.configure(background="#ffffff")
        self.Button1_1_1_1.configure(borderwidth="3")
        self.Button1_1_1_1.configure(compound='left')
        self.Button1_1_1_1.configure(disabledforeground="#a3a3a3")
        self.Button1_1_1_1.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Button1_1_1_1.configure(foreground="#000000")
        self.Button1_1_1_1.configure(highlightbackground="#d9d9d9")
        self.Button1_1_1_1.configure(highlightcolor="black")
        self.Button1_1_1_1.configure(pady="0")
        self.Button1_1_1_1.configure(relief="solid")
        self.Button1_1_1_1.configure(text='''Update''')
        self.Button1_1_1_1["command"] = self.Button1_1_1_1command



        self.Labelframe1_1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)
        self.Labelframe1_1_1.configure(relief='groove')
        self.Labelframe1_1_1.configure(borderwidth="3")
        self.Labelframe1_1_1.configure(font="-family {Sitka Heading} -size 20 -weight bold")
        self.Labelframe1_1_1.configure(foreground="black")
        self.Labelframe1_1_1.configure(text='''Detailed View''')
        self.Labelframe1_1_1.configure(background="#ffffff")
        self.Labelframe1_1_1.configure(highlightbackground="#060606")
        self.Labelframe1_1_1.configure(highlightcolor="#060606")
        self.Labelframe1_1_1.place_forget()
        



        self.Labelframe1_1_1_1 = tk.LabelFrame(self.top)
        df_temp = pd.read_csv("data/temperature.csv")
        df_rain = pd.read_csv("data/rainfall.csv")
        fig = Figure(figsize=(5, 5), dpi=50)
        fig.add_subplot(111).plot(df_temp["ANNUAL"])
        fig1 = Figure(figsize=(5, 5), dpi=50)
        fig1.add_subplot(111).plot(df_rain["ANN"])
        # A tk.DrawingArea.
        canvas = FigureCanvasTkAgg(fig, master=self.Labelframe1_1_1_1)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.476, rely=0.117, relheight=0.426,relwidth=0.223, bordermode='ignore')

        # A tk.DrawingArea.
        canvas1 = FigureCanvasTkAgg(fig1, master=self.Labelframe1_1_1_1)
        canvas1.draw()
        canvas1.get_tk_widget().place(relx=0.738, rely=0.117, relheight=0.426,relwidth=0.225, bordermode='ignore')

        
        self.Label2 = tk.Label(self.Labelframe1_1_1_1)
        self.Label2.place(relx=0.016, rely=0.067, height=31, width=86, bordermode='ignore')
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Select Crop''')

        self.TCombobox11 = ttk.Combobox(self.Labelframe1_1_1_1)
        self.TCombobox11.place(relx=0.095, rely=0.067, relheight=0.052, relwidth=0.129, bordermode='ignore')
        self.TCombobox11.configure(font="-family {Segoe UI} -size 11")
        self.TCombobox11.configure(textvariable=self.combobox1)
        self.TCombobox11['values']=crops
        self.combobox1.set('''Select one''')
        self.TCombobox11.configure(takefocus="")
        
        self.Label31 = tk.Label(self.Labelframe1_1_1_1)
        self.Label31.place(relx=0.024, rely=0.15, height=41, width=96
                , bordermode='ignore')
        self.Label31.configure(activebackground="#f9f9f9")
        self.Label31.configure(activeforeground="black")
        self.Label31.configure(background="#ffffff")
        self.Label31.configure(compound='left')
        self.Label31.configure(disabledforeground="#a3a3a3")
        self.Label31.configure(font="-family {Segoe UI} -size 16 -weight bold")
        self.Label31.configure(foreground="#000000")
        self.Label31.configure(highlightbackground="#d9d9d9")
        self.Label31.configure(highlightcolor="black")
        self.Label31.configure(text='''Rainfall''')

        self.Label3_1 = tk.Label(self.Labelframe1_1_1_1)
        self.Label3_1.place(relx=0.024, rely=0.217, height=51, width=145
                , bordermode='ignore')
        self.Label3_1.configure(activebackground="#f9f9f9")
        self.Label3_1.configure(activeforeground="black")
        self.Label3_1.configure(background="#ffffff")
        self.Label3_1.configure(compound='left')
        self.Label3_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1.configure(font="-family {Segoe UI} -size 16 -weight bold")
        self.Label3_1.configure(foreground="#000000")
        self.Label3_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1.configure(highlightcolor="black")
        self.Label3_1.configure(text='''Temperature''')

        self.Entry1 = tk.Entry(self.Labelframe1_1_1_1)
        self.Entry1.place(relx=0.214, rely=0.15, height=30, relwidth=0.162
                , bordermode='ignore')
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Entry1_1 = tk.Entry(self.Labelframe1_1_1_1)
        self.Entry1_1.place(relx=0.214, rely=0.234, height=30, relwidth=0.162
                , bordermode='ignore')
        self.Entry1_1.configure(background="white")
        self.Entry1_1.configure(disabledforeground="#a3a3a3")
        self.Entry1_1.configure(font="TkFixedFont")
        self.Entry1_1.configure(foreground="#000000")
        self.Entry1_1.configure(highlightbackground="#d9d9d9")
        self.Entry1_1.configure(highlightcolor="black")
        self.Entry1_1.configure(insertbackground="black")
        self.Entry1_1.configure(selectbackground="blue")
        self.Entry1_1.configure(selectforeground="white")

        self.Button1_1_2 = tk.Button(self.Labelframe1_1_1_1)
        self.Button1_1_2.place(relx=0.278, rely=0.067, height=30, width=110, bordermode='ignore')
        self.Button1_1_2.configure(activebackground="#ffffff")
        self.Button1_1_2.configure(activeforeground="#000000")
        self.Button1_1_2.configure(background="#ffffff")
        self.Button1_1_2.configure(borderwidth="3")
        self.Button1_1_2.configure(compound='left')
        self.Button1_1_2.configure(disabledforeground="#a3a3a3")
        self.Button1_1_2.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Button1_1_2.configure(foreground="#000000")
        self.Button1_1_2.configure(highlightbackground="#d9d9d9")
        self.Button1_1_2.configure(highlightcolor="black")
        self.Button1_1_2.configure(pady="0")
        self.Button1_1_2.configure(relief="solid")
        self.Button1_1_2.configure(text='''Get Results''')
        self.Button1_1_2["command"] = self.Button1_1_2command
        self.Label4 = tk.Label(self.Labelframe1_1_1_1)
        self.Label4.place(relx=0.516, rely=0.067, height=21, width=184
                , bordermode='ignore')
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(anchor='w')
        self.Label4.configure(background="#ffffff")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Segoe UI} -size 10")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Annual Average  Temperature''')

        self.Label4_1 = tk.Label(self.Labelframe1_1_1_1)
        self.Label4_1.place(relx=0.786, rely=0.067, height=21, width=184
                , bordermode='ignore')
        self.Label4_1.configure(activebackground="#f9f9f9")
        self.Label4_1.configure(activeforeground="black")
        self.Label4_1.configure(anchor='w')
        self.Label4_1.configure(background="#ffffff")
        self.Label4_1.configure(compound='left')
        self.Label4_1.configure(disabledforeground="#a3a3a3")
        self.Label4_1.configure(font="-family {Segoe UI} -size 10")
        self.Label4_1.configure(foreground="#000000")
        self.Label4_1.configure(highlightbackground="#d9d9d9")
        self.Label4_1.configure(highlightcolor="black")
        self.Label4_1.configure(text='''Annual Average Rainfall''')
        self.Labelframe1_1_1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)
        self.Labelframe1_1_1_1.configure(relief='groove')
        self.Labelframe1_1_1_1.configure(borderwidth="3")
        self.Labelframe1_1_1_1.configure(font="-family {Sitka Heading} -size 20 -weight bold")
        self.Labelframe1_1_1_1.configure(foreground="black")
        self.Labelframe1_1_1_1.configure(text='''Real-Time Data''')
        self.Labelframe1_1_1_1.configure(background="#ffffff")
        self.Labelframe1_1_1_1.configure(highlightbackground="#060606")
        self.Labelframe1_1_1_1.configure(highlightcolor="#060606")
        self.Labelframe1_1_1_1.place_forget()
        
    def Button1_1_2command(self):
        

        self.Label3_1_1 = tk.Label(self.Labelframe1_1_1_1)
        self.Label3_1_1.place(relx=0.024, rely=0.534, height=31, width=208
                , bordermode='ignore')
        self.Label3_1_1.configure(activebackground="#f9f9f9")
        self.Label3_1_1.configure(activeforeground="black")
        self.Label3_1_1.configure(anchor='w')
        self.Label3_1_1.configure(background="#ffffff")
        self.Label3_1_1.configure(compound='left')
        self.Label3_1_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1_1.configure(font="-family {Segoe UI} -size 16 -weight bold")
        self.Label3_1_1.configure(foreground="#000000")
        self.Label3_1_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1_1.configure(highlightcolor="black")
        self.Label3_1_1.configure(text='''Real-time Analysis''')
        r_temp=self.Entry1_1.get()
        r_rain=self.Entry1.get()
        crop1 = self.TCombobox11.get()
        self.Label3.configure(text=crop)
        crop1=crop1.lower()
        df_temp = pd.read_csv("data/temperature.csv")
        df_crop = pd.read_csv("data/Crops/"+crop1+".csv")
        df_rain = pd.read_csv("data/rainfall.csv")
        df_yields=df_crop[df_crop['Element']=='Yield']
        df_area=df_crop[df_crop['Element']=='Area harvested']
        df_prod=df_crop[df_crop['Element']=='Production']
        sum=0
        d1=0
        d2=0
        workbook1 = xlsxwriter.Workbook('output/Temp.xlsx')
        worksheet = workbook1.add_worksheet()
        worksheet.write('A1', "OVERVIEW")
        worksheet.write('B1', 'Tempreature')
        worksheet.write('C1', 'Rainfall')
        worksheet.write('A2', 'Production')
        worksheet.write('A3', 'Area Harvested')
        worksheet.write('A4', 'Yields')
        worksheet.write('A5', 'Average')
        worksheet.write('A6', 'Relation')
        corr, _ = pearsonr(df_prod['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C2', corr)

        corr, _ = pearsonr(df_area['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C3', corr)

        corr, _ = pearsonr(df_yields['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C4', corr)

        worksheet.write('C5', (sum/3))
        d1=(sum/3)
        worksheet.write('C6', rel(sum/3))

        sum=0
        corr, _ = pearsonr(df_prod['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B2', corr)

        corr, _ = pearsonr(df_area['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B3',corr)

        corr, _ = pearsonr(df_yields['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B4', corr)
        worksheet.write('B5', (sum/3))
        d2=(sum/3)
        worksheet.write('B6', rel(sum/3))
        workbook1.close()
        # Create a Treeview widget
        tree = ttk.Treeview(self.Labelframe1_1_1_1)
        df = pd.read_excel("output/Temp.xlsx")
        # Clear all the previous data in tree
        tree.delete(*tree.get_children())
        # Add new data in Treeview widget
        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        # For Headings iterate over the columns
        for col in tree["column"]:
           tree.heading(col, text=col)
           tree.column(col,width=100,anchor=tk.CENTER)
        # Put Data in Rows
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
              tree.insert("", "end", values=row)
        tree.place(relx=0.024, rely=0.317, relheight=0.225, relwidth=0.433
                , bordermode='ignore')
        ans=realtime_prod_wrt_temp(float(d2),float(r_temp))
        ans=ans+realtime_prod_wrt_rain(float(d1),float(r_rain))
        self.Labell = tk.Label(self.Labelframe1_1_1_1)

        
        self.Labell.place(relx=0.024, rely=0.584, relheight=0.392, relwidth=0.941, bordermode='ignore')
        self.Labell.configure(activebackground="#f9f9f9")
        self.Labell.configure(activeforeground="black")
        self.Labell.configure(anchor='center')
        self.Labell.configure(background="#ffffff")
        self.Labell.configure(compound='center')
        self.Labell.configure(disabledforeground="#a3a3a3")
        self.Labell.configure(font="-family {Segoe UI} -size 14 -weight normal")
        self.Labell.configure(foreground="#000000")
        self.Labell.configure(highlightbackground="#d9d9d9")
        self.Labell.configure(highlightcolor="black")
        self.Labell.configure(text=ans)
        
    def Button1_1_1_1command(self):
        crop = self.TCombobox1.get()
        self.Label3.configure(text=crop)
        crop=crop.lower()
        df_temp = pd.read_csv("data/temperature.csv")
        df_crop = pd.read_csv("data/Crops/"+crop+".csv")
        df_rain = pd.read_csv("data/rainfall.csv")
        df_yields=df_crop[df_crop['Element']=='Yield']
        df_area=df_crop[df_crop['Element']=='Area harvested']
        df_prod=df_crop[df_crop['Element']=='Production']
        
        fig = Figure(figsize=(5, 5), dpi=50)
        fig.add_subplot(111).scatter(df_prod['Value'], df_temp["ANNUAL"],color='green')

        fig1 = Figure(figsize=(5, 5), dpi=50)
        fig1.add_subplot(111).scatter(df_area['Value'], df_temp["ANNUAL"],color='green')

        fig2 = Figure(figsize=(5, 5), dpi=50)
        fig2.add_subplot(111).scatter(df_yields['Value'], df_temp["ANNUAL"],color='green')

        fig3 = Figure(figsize=(5, 5), dpi=50)
        fig3.add_subplot(111).scatter(df_prod['Value'], df_rain["ANN"],color='orange')

        fig4 = Figure(figsize=(5, 5), dpi=50)
        fig4.add_subplot(111).scatter(df_area['Value'], df_rain["ANN"],color='orange')

        fig5 = Figure(figsize=(5, 5), dpi=50)
        fig5.add_subplot(111).scatter(df_yields['Value'], df_rain["ANN"],color='orange')


        canvas = FigureCanvasTkAgg(fig, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.476, rely=0.1, relheight=0.259, relwidth=0.128, bordermode='ignore')

        canvas1 = FigureCanvasTkAgg(fig1, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas1.draw()
        canvas1.get_tk_widget().place(relx=0.643, rely=0.1, relheight=0.259, relwidth=0.129, bordermode='ignore')
        

        canvas2 = FigureCanvasTkAgg(fig2, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas2.draw()
        canvas2.get_tk_widget().place(relx=0.81, rely=0.1, relheight=0.259, relwidth=0.129, bordermode='ignore')

        canvas3 = FigureCanvasTkAgg(fig3, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas3.draw()
        canvas3.get_tk_widget().place(relx=0.476, rely=0.417, relheight=0.259, relwidth=0.129, bordermode='ignore')

        canvas4 = FigureCanvasTkAgg(fig4, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas4.draw()
        canvas4.get_tk_widget().place(relx=0.643, rely=0.417, relheight=0.259, relwidth=0.129, bordermode='ignore')

        canvas5 = FigureCanvasTkAgg(fig5, master=self.Labelframe1_1_1)  # A tk.DrawingArea.
        canvas5.draw()
        canvas5.get_tk_widget().place(relx=0.81, rely=0.417, relheight=0.259, relwidth=0.129, bordermode='ignore')
        sum=0
        d1=0
        d2=0
        workbook1 = xlsxwriter.Workbook('output/Temp.xlsx')
        worksheet = workbook1.add_worksheet()
        worksheet.write('A1', "  ")
        worksheet.write('B1', 'Tempreature')
        worksheet.write('C1', 'Rainfall')
        worksheet.write('A2', 'Production')
        worksheet.write('A3', 'Area Harvested')
        worksheet.write('A4', 'Yields')
        worksheet.write('A5', 'Average')
        worksheet.write('A6', 'Relation')
        corr, _ = pearsonr(df_prod['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C2', corr)

        corr, _ = pearsonr(df_area['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C3', corr)

        corr, _ = pearsonr(df_yields['Value'], df_rain['ANN'])
        sum=sum+corr
        worksheet.write('C4', corr)

        worksheet.write('C5', (sum/3))
        d1=(sum/3)
        worksheet.write('C6', rel(sum/3))

        sum=0
        corr, _ = pearsonr(df_prod['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B2', corr)

        corr, _ = pearsonr(df_area['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B3',corr)

        corr, _ = pearsonr(df_yields['Value'], df_temp['ANNUAL'])
        sum=sum+corr
        worksheet.write('B4', corr)
        worksheet.write('B5', (sum/3))
        d2=(sum/3)
        worksheet.write('B6', rel(sum/3))
        workbook1.close()
        # Create a Treeview widget
        tree = ttk.Treeview(self.Labelframe1_1_1)
        df = pd.read_excel("output/Temp.xlsx")
        # Clear all the previous data in tree
        tree.delete(*tree.get_children())
        # Add new data in Treeview widget
        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        # For Headings iterate over the columns
        for col in tree["column"]:
           tree.heading(col, text=col)
           tree.column(col,width=100,anchor=tk.CENTER)
        # Put Data in Rows
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
              tree.insert("", "end", values=row)
        tree.place(relx=0.024, rely=0.334, relheight=0.225, relwidth=0.417, bordermode='ignore')
        res=prod_wrt_rain(d1)
        res=res+"\n"+prod_wrt_temp(d2)
        self.Label4 = tk.Label(self.Labelframe1_1_1)
        self.Label4.place(relx=0.571, rely=0.05, height=21, width=366
                , bordermode='ignore')
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#ffffff")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Segoe UI} -size 11")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Correlation with Temperature''')

        self.Label4_1 = tk.Label(self.Labelframe1_1_1)
        self.Label4_1.place(relx=0.556, rely=0.367, height=21, width=394
                , bordermode='ignore')
        self.Label4_1.configure(activebackground="#f9f9f9")
        self.Label4_1.configure(activeforeground="black")
        self.Label4_1.configure(background="#ffffff")
        self.Label4_1.configure(compound='left')
        self.Label4_1.configure(disabledforeground="#a3a3a3")
        self.Label4_1.configure(font="-family {Segoe UI} -size 11")
        self.Label4_1.configure(foreground="#000000")
        self.Label4_1.configure(highlightbackground="#d9d9d9")
        self.Label4_1.configure(highlightcolor="black")
        self.Label4_1.configure(text='''Correlation with Rainfall''')

        self.Label3_1 = tk.Label(self.Labelframe1_1_1)
        self.Label3_1.place(relx=0.197, rely=0.25, height=40, width=139
                , bordermode='ignore')
        self.Label3_1.configure(activebackground="#f9f9f9")
        self.Label3_1.configure(activeforeground="black")
        self.Label3_1.configure(background="#ffffff")
        self.Label3_1.configure(compound='left')
        self.Label3_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1.configure(font="-family {Segoe UI} -size 20")
        self.Label3_1.configure(foreground="#000000")
        self.Label3_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1.configure(highlightcolor="black")
        self.Label3_1.configure(text='''Overview''')

        self.Label3_1_1 = tk.Label(self.Labelframe1_1_1)
        self.Label3_1_1.place(relx=0.032, rely=0.618, height=40, width=202
                , bordermode='ignore')
        self.Label3_1_1.configure(activebackground="#f9f9f9")
        self.Label3_1_1.configure(activeforeground="black")
        self.Label3_1_1.configure(anchor='w')
        self.Label3_1_1.configure(background="#ffffff")
        self.Label3_1_1.configure(compound='left')
        self.Label3_1_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1_1.configure(font="-family {Segoe UI} -size 20")
        self.Label3_1_1.configure(foreground="#000000")
        self.Label3_1_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1_1.configure(highlightcolor="black")
        self.Label3_1_1.configure(text='''Result Analysis''')
        
        self.Labell = tk.Label(self.Labelframe1_1_1)

        
        self.Labell.place(relx=0.024, rely=0.718, relheight=0.225, relwidth=0.941, bordermode='ignore')
        self.Labell.configure(activebackground="#f9f9f9")
        self.Labell.configure(activeforeground="black")
        self.Labell.configure(anchor='center')
        self.Labell.configure(background="#ffffff")
        self.Labell.configure(compound='center')
        self.Labell.configure(disabledforeground="#a3a3a3")
        self.Labell.configure(font="-family {Segoe UI} -size 14 -weight normal")
        self.Labell.configure(foreground="#000000")
        self.Labell.configure(highlightbackground="#d9d9d9")
        self.Labell.configure(highlightcolor="black")
        self.Labell.configure(text=res)

        
    def Button1_command(self):
        
        self.Labelframe1_1_1_1.place_forget()
        self.Labelframe1_1_1.place_forget()
        self.Labelframe1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)

    def Button1_1command(self):
        
        self.Button1_1.configure(state='active')
        self.Labelframe1_1_1_1.place_forget()
        self.Labelframe1_1.place_forget()
        self.Labelframe1_1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)

    def Button1_1_1command(self):
        
        self.Labelframe1_1_1.place_forget()
        self.Labelframe1_1.place_forget()
        self.Button1_1_1.configure(state='active')
        self.Labelframe1_1_1_1.place(relx=0.008, rely=0.153, relheight=0.832, relwidth=0.984)
        
    


def start_up():
    unknown_support.main()


if __name__ == '__main__':
    unknown_support.main()
