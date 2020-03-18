# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:54:17 2019

@author: 王若宇
"""


import matplotlib as mpl

import matplotlib.pyplot as plt

# The module to build gridspec
import matplotlib.gridspec as gridspec

from matplotlib.legend_handler import HandlerLine2D

from matplotlib import collections as matcoll

import matplotlib.lines as mlines

    
    
mpl.rcParams['axes.linewidth'] = 2
  


def CVgraph(**kwarg):
    '''return the fig & ax objects of CV graph formatting'''
    return Create_sfig(**kwarg)
    


def XRDgraph(fig,left=False, labelleft=False,**kwarg):
    '''return the fig & ax objects of XRD graph formatting'''
    return Create_sfig(fig, left=False, labelleft=False,**kwarg)





def Create_multifig(x,y,**kwargs):
    '''Create a figure of multiple axes'''
    fig, axes = plt.subplots(x, y, **kwargs)
    
    return fig, axes


def Update_axe(ax,top=False, left=True, right=False, labelleft=True,
                xlabel=None, ylabel=None,title=None,tick_label_size=12,label_size=18, labelpad=10, **kwargs):
    '''Update an axe'''
    
    
    
# Set the ticks
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(tick_label_size) 
    
    
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(tick_label_size)  
        
    ax.tick_params(top=top, left=left, right=right, labelleft=labelleft,**kwargs)

    ax.set_ylabel(ylabel,labelpad=labelpad,fontsize=label_size)
    ax.set_xlabel(xlabel,labelpad=labelpad,fontsize=label_size)
    ax.set_title(title, fontsize=18,pad=10)
    
    

def Create_sfig(top=False, left=True, right=False, labelleft=True,
                xlabel='X', ylabel='Y',title='Title'):
    
    fig,ax=plt.subplots()
    
    
# Set the ticks
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(12) 
        
    
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(12)  
        
    ax.tick_params(top=top, left=left, right=right, labelleft=labelleft)

    ax.set_ylabel(ylabel,labelpad=10,fontsize=18)
    ax.set_xlabel(xlabel,labelpad=10,fontsize=18)
    ax.set_title(title, fontsize=15,pad=10)
    
    return fig, ax
    
    


def MultiLine(df,ax,*args,x=0,y=1,color='blue',label='label',linewidth='1',**kwarg):
    '''Add lines'''
    signals=df.columns
    l=ax.plot(df[signals[x]],df[signals[y]],*args, color=color, linewidth=linewidth,label=label,
              **kwarg)
   

    return l



def Scatter(df,ax,x=0,y=1,color='black',marker='o'):
    '''Scatter plot'''
    sc=ax.scatter(df[df.columns[x]],df[df.columns[y]],color=color,
                  marker=marker)
    return sc


def ScatterLine(df,ax,x=0,y=1,color='black',marker='-ok'):
    '''Scatter plot with line'''
    sc=ax.scatter(df[df.columns[x]],df[df.columns[y]],color=color,
                  marker=marker)
    return sc


def Auto_legend(ax, *args, loc='upper right', bbox_to_anchor=(1, 1),markerscale=None, frameon=False,**kwargs):
    '''Update legend'''
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,*args, loc=loc, bbox_to_anchor=bbox_to_anchor, markerscale=markerscale,frameon=False, **kwargs)
    
    
    
    
    
    
def Costomize_legendL(color='black', label='legend', *kwargs, tpl=()):
    '''proxy artist'''
    line_legend = mlines.Line2D([], [], color=color, markersize=5, label=label)
    tpl=tpl+(line_legend,)
    return tpl


def PDF_line(cl1,cl2):
    '''Draw the drop line'''
    lines=[]
    for l in range(len(cl1)):
        pair=[(cl1[l],0),(cl1[l],cl2[l])]
        lines.append(pair)
      
    dpL=matcoll.LineCollection(lines)
    
      
    return dpL





# ax.set_xlim(20,80)
# ax.set_ylim(4000,15000)





# Create a 'proxy artist': 

# import matplotlib.lines as mlines

# black_line = mlines.Line2D([], [], color='black', marker='o',
  #                        markersize=5, label='Ni-CAT')

#plt.legend(handles=[black_line],loc='upper left', bbox_to_anchor=(0.1, 0.9))



#fig.savefig('C:/Users/王若宇/Desktop/The tatami galaxy.png')
