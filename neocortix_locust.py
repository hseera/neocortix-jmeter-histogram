# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import numpy as np


import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

'''
This function filters out all the rows for which the label column does not match a given value (i.e GetDistribution).
And saves "elapsed", "responsecode" & "timestamp" value for rows that do match the specified label text(transaction name) into a csv.
'''

outputDir= './sample/locust/locust_test'


def find_files(): 
    resultFiles = []
    for root, dirs, files in os.walk(outputDir, topdown=False):
        for name in files:
            if  name.endswith("_results_good.csv"):
                Path = os.path.join(root, name)
                m = re.search(r'worker_(.+?)_results_good.*$', str(Path))
                resultFiles.append({'fileNumber': str(m.group(1)), 'filePath': Path})
    return resultFiles

def extract_data(resultFiles):
    FILE_TO_WRITE ="./sample/locust/merged.csv"
    lookup_df = pd.read_csv('./sample/locust/mapConfig.csv')
    if os.path.exists(FILE_TO_WRITE):
        os.remove(FILE_TO_WRITE)
    df=pd.DataFrame(columns=['timestamp','method','elapsed','URL','Location']) 
    df.to_csv(FILE_TO_WRITE, mode='a', header=["timeStamp", "method", "elapsed","URL", "Location"], index = False)
    for files in resultFiles:
        y = lookup_df.loc[lookup_df[' Filename'].str.contains(files['fileNumber'])][' Region']
        y = y.values.tolist()
        df = pd.read_csv(files['filePath'], usecols = ['timeStamp','method','elapsed','URL'])
        df['Location']=y[0]
        df.to_csv(FILE_TO_WRITE, mode='a',  index = False, header=False)

def generate_graphs():
    FILE = "./sample/locust/merged.csv" #replace with your file name
     
    try:
        df = pd.read_csv(FILE, dtype={'Location':'str'}) # read the file
        df['timeStamp'] = df['timeStamp']*1000

        '''
        This code generates the percentile graph
        '''

        #base subplot setup
        res = df.pivot(columns='Location', values='elapsed')
        fig, axes = plt.subplots(2, 2, figsize=(16, 8), sharey=False) # set 2x2 plots 
        fig.patch.set_facecolor('#bbe5f9')
        plt.subplots_adjust(hspace = 0.4)
        color = {' USA':'#0000FF',' Russia':'#FF0000',' Other':'#00FF00' }

        #generate scatterplot for elapsed time
        ax = sns.scatterplot(ax=axes[0,0], data=df,x=df['timeStamp'],y=df['elapsed'], hue=df['Location'],  s=7,palette=color, legend=True ) #legend=True
        ax.set(ylim=(0,3000))
        xticks = ax.get_xticks()
        ax.set_xticklabels([pd.to_datetime(tm, unit='ms').strftime('%d/%m/%y\n%H:%M:%S') for tm in xticks], rotation = 45) #, rotation = 45
        ax.legend(fontsize='medium')
        ax.set_title('Response Time Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Response Time (ms)')
        
        #generate response time distribuiton graph
        kwargs = dict(element='step',shrink=.8, alpha=0.3, fill=True, legend=True, palette=color)  #, palette=color
        ax = sns.histplot(ax=axes[0, 1], data=res,**kwargs)
        ax.set(xlim=(0,3000))
        ax.legend([' USA',' Russia', ' Other']).set_title('')
        ax.set_title('Response Time Distribution')
        ax.set_xlabel('Response Time (ms)')
        ax.set_ylabel('Frequency')

        #Generate percentile distribution                 
        summary = np.round(res.describe(percentiles=[0.0, 0.1, 0.2,
                                                         0.3, 0.4, 0.5,
                                                         0.6, 0.7, 0.8,  
                                                         0.9, 0.95, 0.99, 1]),2) # add 1 in the percentile
        dropping = ['count', 'mean', 'std', 'min','max'] #remove metrics not needed for percentile graph
        for drop in dropping:
            summary = summary.drop(drop)        
        ax = sns.lineplot(ax=axes[1, 1],data=summary,dashes=False,  legend=True,palette=color) #palette=color,
        ax.legend(fontsize='medium')
        ax.set(ylim=(0,3000))
        ax.set_title('Percentile Distribution')
        ax.set_xlabel('Percentile')
        ax.set_ylabel('Response Time (ms)')
        
        #Basic statistics
        axes[1, 0].axis("off")
        df['loc_url'] = df['Location'].astype(str) +'_'+ df['URL']
        res = df.pivot(columns='loc_url', values='elapsed')
        full_summary = np.round(res.describe(percentiles=[0.25,0.5,0.75,0.90,0.95],include='all'),2)# show basic statistics as in row
        table_result = axes[1, 0].table(cellText=full_summary.values,
                  rowLabels=full_summary.index,
                  colLabels=full_summary.columns,
                  rowColours =["#bbe5f9"] * 10,  #xkcd:mint green
                  colColours =["#bbe5f9"] * 10,  #palegreen
                  cellLoc = 'right', rowLoc = 'center',
                  loc='upper center')
        table_result.auto_set_font_size(False)
        table_result.set_fontsize(8)
        axes[1, 0].set_title('Response Time Statistics')
                        

        fig.tight_layout(pad=1)
        
        plt.savefig('./sample/locust/graphs.png',facecolor=fig.get_facecolor(), edgecolor='none')

    except Exception as e:
        raise e  

def main():
   resultFiles = find_files()
   extract_data(resultFiles)  
   generate_graphs()

if __name__ == "__main__":
    main()