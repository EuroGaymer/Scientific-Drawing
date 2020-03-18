# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 23:11:58 2019

@author: 王若宇
"""
from FileReader import Reader as rd
from academic_graphics import graph as gp

import pandas as pd
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import os 




def multi_cv(ax,path,title=None,mass=1.0,
                   color_set=['black', 'blue', 'green', 'red', 'pink','brown','yellow'],
                   xlabel=None, ylabel=None,filter_on=False,smooth_range=None, 
                   legend_font=12, **kwargs):
    
    '''Draw multiple cv curves on a single axe\
       Arguments:\
       ax\
       path: the path of the file containing .txt files\
       title\
       mass: mass or surface area or volume of the sample'''
       
    gp.Update_axe(ax,title=title,**kwargs)
    # the list for Dataframe objects
    cv=[]
    for s in os.listdir(path):
        # find the .txt files
        if '.txt' in s:
            f_path=os.path.join(path,s)
            obj=rd.CV(filename=f_path,mass=mass)
                
                
            cv.append(obj)
    # the list for line objects in an axe
    
    for counter,obj in enumerate(cv):
        #  if filter is on
        if filter_on==True and smooth_range is not None:
            gp.MultiLine(smoother_cv(obj,smooth_range),ax,label=obj.scan_rate, color=color_set[counter])
          
        # or not...
        else:
            gp.MultiLine(obj,ax,label=obj.scan_rate, color=color_set[counter])
        
    if xlabel== None:
        
        ax.set_xlabel(cv[0].columns[0])
        
    else:
        ax.set_xlabel(xlabel)
        
    if ylabel==None:
        ax.set_ylabel(cv[0].columns[1])
        
    else:
        ax.set_ylabel(ylabel)
    
    gp.Auto_legend(ax, bbox_to_anchor=(0, 1.03),loc='upper left',fontsize=legend_font)
    
    

def smoother_cv(df,smoother_range):
    '''df: the original data to be smoothed;
        smoother_range: the data point exceed this would be limited
    '''
   
    # create a new DF
    df_n=pd.DataFrame()
    # the index of THE LAST good point
    lgp=0
    for i in df.index:
        if i==0:
            df_n=df_n.append(df.iloc[0])
        
    
        else:
            if abs(df.iloc[i,1]-df.iloc[lgp,1])>(smoother_range*(i-lgp)):
                
                pass 
            else:
                lgp=i
                df_n=df_n.append(df.iloc[i])
                
    # return the filtered data as new DF
    
    return df_n
    
    
    
def multi_c_d(ax,path,title=None ,mass=1.0, unit=' A/g',
              color_set=['black', 'blue', 'green', 'red', 'pink', 'brown','yellow'],
                   xlabel=None, ylabel=None,legend_font=12,b_to_a=(1,0.75),**kwargs):
    '''Draw multiple charge/discharge curves on a single axe\
       Arguments:\
       ax\
       path: the path of the file containing .txt files\
       title\
       mass: mass or surface area or volume of the sample'''
       
    gp.Update_axe(ax,title=title,**kwargs)
    
    # the list for GV objects
    instances=[]
    
    
    for s in os.listdir(path):
        # find the .txt files
        if '.txt' in s:
            f_path=os.path.join(path,s)
            inst=rd.GV(filename=f_path,mass=mass)
            instances.append(inst)
            
    
            
            
    # the list for line objects in an axe
    handles=[]
    
    for counter,inst in enumerate(instances):
        
        l_char=gp.MultiLine(inst.charge_curve(),ax,label=str(inst.current)+unit, color=color_set[counter])
        
        gp.MultiLine(inst.discharge_curve(),ax,label=str(inst.current)+unit, color=color_set[counter])
        # line object is a list
        handles+=l_char
       
        
    if xlabel==None:
        
        ax.set_xlabel(instances[0].columns[0])
        
    else:
        ax.set_xlabel(xlabel)
        
    if ylabel==None:
        ax.set_ylabel(instances[0].columns[1])
        
    else:
        ax.set_ylabel(ylabel)   
        
    
    ax.set_xlim(left=0)
    ax.set_ylim(top= 0.8,bottom=0)
   
    ax.legend(handles=handles, bbox_to_anchor=b_to_a, loc='upper right', frameon=False,fontsize=legend_font)


def multi_cap(ax,path,cap_df=None, handles=None,labels=None, title=None,mass=1.0,legend_on=True,
              legend_label='label', marker='o',linewidth='2',
              xunit='A/g',yunit='F/g', color='black',**kwargs):
    
    '''Draw multiple charge/discharge curves on a single axe\
       Arguments:\
       ax\
       path: the path of the file containing .txt files\
       title\
       handles,labels: two empty lists created as global variable.\
       mass: mass or surface area or volume of the sample'''
    
    gp.Update_axe(ax,title=title,**kwargs)
  
    
    # get the value of capacitance
    if cap_df is None:    
        capacitance= list_cap(path,mass)
        
    else:
        capacitance= cap_df
    
    
    # draw the graph
    gp.MultiLine(capacitance,ax,marker,color=color,linewidth=linewidth)
    if legend_on==True and handles!=None and labels != None:
        
        handles.append(mlines.Line2D([], [], color=color, markersize=2))
        labels.append( legend_label)
        
        
    
    ax.set_xlabel(capacitance.columns[0]+ ' (' + xunit +')')
    ax.set_ylabel(capacitance.columns[1]+' (' + yunit +')')
    
    ax.set_xlim(left=0)
    
    
    
    
    
    
def multi_cap_cv(ax,path,cap_df=None,handles=None,labels=None, title=None,mass=1.0,massfactor=1.0,
                 legend_on=True,
              legend_label='label', marker='o',
              xunit='A/g',yunit='C/g', color='black',**kwargs):
    
    '''Draw multiple charge/discharge curves on a single axe\
       Arguments:\
       ax\
       path: the path of the file containing .txt files\
       title\
       handles,labels: two empty lists created as global variable.\
       mass: mass or surface area or volume of the sample'''
    
    gp.Update_axe(ax,title=title,**kwargs)
    
    
    # the list for GV objects    
    if cap_df is None:
        capacitance= list_cap_cv(path,mass,massfactor=massfactor)
        
    else:
        capacitance=cap_df
    
    
    gp.MultiLine(capacitance,ax,marker,color=color)
    if legend_on==True and handles!=None and labels != None:
        
        handles.append(mlines.Line2D([], [], color=color, markersize=2))
        labels.append( legend_label)
        
        
    
    ax.set_xlabel(capacitance.columns[0]+ ' (' + xunit +')')
    ax.set_ylabel(capacitance.columns[1]+' (' + yunit +')')
    
    ax.set_xlim(left=0)
    
    
    
    
    
def stability_cap(ax,path, *args, interval=100.0, title=None,mass=1.0,color='black', **kwargs):
    '''Return a list of stability data caculated from\
       the .txt files within the path.\
       Argument:\
       interval: the number of GV cycles between two checkpoints.\
       mass: mass or surface area or volume of the sample'''
       
    gp.Update_axe(ax,title=title,**kwargs)
    
    capacitance= list_cap(path,mass)
    stability=[]
   
    
    first_cap=capacitance.iloc[0,1]
    # return a list of stability value
    
   
    
    for i in capacitance.index:
        
        stability.append([i*interval, capacitance.iloc[i,1]*100/first_cap ])
    
    
    stability=pd.DataFrame(data=stability, columns=['Cycle number', 'Capacitance (%)'])
        
    
    gp.MultiLine(stability,ax,*args,color=color)
    
    
    ax.set_xlabel(stability.columns[0])
    ax.set_ylabel(stability.columns[1])
    
    ax.set_ylim(bottom=0)













def list_cap(path,mass):
    '''Return a list of capacitance(or something else~*) caculated from\
       the .txt files within the path.\
       Argument:\
       mass: mass or surface area or volume of the sample'''
       
    
    
    def object_generator(path,mass):
        for s in os.listdir(path):
        # find the .txt files
            if '.txt' in s:
                f_path=os.path.join(path,s)
                yield rd.GV(filename=f_path,mass=mass)
                



    # the list for line objects in an axe
    capacitance=pd.DataFrame()
    
    for inst in object_generator(path,mass):
        capacitance=capacitance.append(inst.Capacitance())
        
    print(capacitance)
        
        
    return capacitance.reset_index(drop=True)




def list_cap_cv(path,mass,**kwargs):
    '''Return a list of capacitance(or something else~*) caculated from\
       the .txt files within the path.\
       Argument:\
       mass: mass or surface area or volume of the sample'''
       
    
    
    def object_generator(path,mass):
        for s in os.listdir(path):
        # find the .txt files
            if '.txt' in s:
                f_path=os.path.join(path,s)
                yield rd.CV(filename=f_path,mass=mass)
                



    # the list for line objects in an axe
    capacitance=pd.DataFrame()
    
    
    for inst in object_generator(path,mass):
        capacitance=capacitance.append(inst.Capacitance(**kwargs))
        
        
    return capacitance.reset_index(drop=True)




def list_w_p(path,mass):
    '''Return a list of work-power datas caculated from\
       the .txt files within the path.\
       Argument:\
       mass: mass or surface area or volume of the sample'''
       
    instances=[]
    
    for s in os.listdir(path):
        # find the .txt files
        if '.txt' in s:
            f_path=os.path.join(path,s)
            inst=rd.GV(filename=f_path,mass=mass)
            instances.append(inst)

    # the list for line objects in an axe
    w_p=pd.DataFrame()
    for counter,inst in enumerate(instances):
        
        w_p=w_p.append(inst.work_power())
        
        
    return w_p.reset_index(drop=True)







def ragone_plot(ax,path,handles,labels,*args, title=None,mass=1.0, legend_on=True,
              legend_label='label',xunit=r'Wh/cm$^{3}$',yunit=r'W/cm$^{3}$',color='black',marker='o',
              **kwargs):
    
    '''Draw multiple work-power curves on a single axe\
       Arguments:\
       ax\
       path: the path of the file containing .txt files\
       title\
       handles,labels: two empty lists created as global variable.\
       mass: mass or surface area or volume of the sample.\
       legend_on: bool, add current data set on legend.\
       legend_label: str, the legend label for current data set. '''
    
    gp.Update_axe(ax,title=title,labelpad=3,**kwargs)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # the list for GV objects    
    w_p= list_w_p(path,mass)
 
    
    gp.MultiLine(w_p,ax,marker,*args, color=color)
    
    
    if legend_on==True:
        handles.append(mlines.Line2D([], [], color=color, markersize=2))
        labels.append(legend_label)
        
    
    ax.set_xlabel(w_p.columns[0]+ ' (' + xunit+')')
    ax.set_ylabel(w_p.columns[1]+' (' + yunit+')')
   
    
