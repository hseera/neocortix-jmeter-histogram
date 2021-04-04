# -*- coding: utf-8 -*-
'''
TODO:
Modify the code to display test duration for the scatterplot rather than the count of data points plot. 
'''

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import re
from collections import Counter
import numpy as np

import seaborn as sns


'''
This function filters out all the rows for which the label column does not match a given value (i.e GetDistribution).
And saves "elapsed" value for rows that do match the specified label text(transaction name) into a csv.
'''
LOCATION = os.getcwd()
TRANSACTION_NAME = 'GetDistribution'  #replace the transaction name with your transaction name

def extract_latency_data():

    FILE_TO_WRITE =""       
    for file in os.listdir(LOCATION):
        try: #extract latency data from csv files that begin with TestPlan_
            if file.startswith("TestPlan_") and file.endswith(".csv"):
                substring = re.search('TestPlan_results_(.+?).csv', file).group(1)
                FILE_TO_WRITE = "extracted_"+substring+".csv"
                df = pd.read_csv(file)
                x = []
                x = df.loc[df['label'] == TRANSACTION_NAME] #filter out all the rows for which the label column does not contain value GetDistribution
                with open(FILE_TO_WRITE,'w') as fwrite:
                    fwrite.write('latency_'+substring+',responsecode_'+substring+'\n')
                    for item in range(len(x)):
                       fwrite.write('%s,%s\n' %(x['elapsed'].values[item],x['responseCode'].values[item]))
            else:
                continue
        except Exception as e:
            raise e

'''
Note glob.glob() is not case sensitive in Windows OS. 
Make sure the files that need to be merged have unique names from other file. 
https://jdhao.github.io/2019/06/24/python_glob_case_sensitivity/
'''
def merge_data():
    try:    
        files = glob.glob("./extracted_*.csv") #extract_data function generates csv files that start with new_TestPlan_results
        dataframes = [pd.read_csv(p) for p in files]
        merged_dataframe = pd.concat(dataframes, axis=1)
        merged_dataframe.to_csv("./metrics.csv", index=False)
    except Exception as e:
        raise e


'''
This function iterates through all the columns in the responsetime_histogram file
and generate histogram for all of them. It also plots the average response time for all.

Note: comment out the code that plots mean on the graph if not required.
'''

def generate_graphs():
    FILE = "./metrics.csv" #replace with your file name
     
    try:
        df = pd.read_csv(FILE) # read the file    
    
        fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharey=False) # set 2x2 plots
        
        plt.subplots_adjust(hspace = 0.3)
        
        #generate scatterplot for elapsed time
        hist_df = df.filter(regex='latency_')
        ax = sns.scatterplot(ax=axes[0, 0], data=hist_df, s=2, legend=True)
        ax.set(ylim=(0,4500))
        ax.legend(fontsize='medium')
        ax.set_title('Response Time Over Time')
        ax.set_xlabel('Test Duration (sec)')
        ax.set_ylabel('Response Time (ms)')
        
        #generate response time distribuiton graph
        kwargs = dict(element='step',shrink=.8, alpha=0.6, fill=True, legend=False) 
        ax = sns.histplot(ax=axes[0, 1], data=hist_df,**kwargs)
        ax.set(xlim=(0,4500))
        ax.set_title('Response Time Distribution')
        ax.set_xlabel('Response Time (ms)')
        ax.set_ylabel('Frequency')
        #ax.legend(fontsize='medium')
        
        summary = np.round(hist_df.describe(percentiles=[0.25,0.5,0.75,0.90,0.95],include='all'),2)# show basic statistics as in row
        
        axes[2, 0].axis("off")
        table_result = axes[2, 0].table(cellText=summary.values,
                  rowLabels=summary.index,
                  colLabels=summary.columns,
                  cellLoc = 'right', rowLoc = 'center',
                  loc='center')
        table_result.auto_set_font_size(False)
        table_result.set_fontsize(9)
        axes[2, 0].set_title('Response Time Statistics')
        
       
        
        #generate response code scatterplot
        hist_df = df.filter(regex='responsecode_')
        ax = sns.scatterplot(ax=axes[1, 0], data=hist_df, s=15, legend=True)
        ax.set(ylim=(0,600))
        ax.legend(fontsize='medium')
        ax.set_title('Response Code Over Time')
        ax.set_xlabel('Test Duration (sec)')
        ax.set_ylabel('Response Code')
        
        
        #generate response code distribution graph
        bar_df = pd.DataFrame(columns=['name', 'response_code', 'count'])
                
        for col in hist_df.columns:
            data = Counter(df[col])
            for key,value in data.items():
                data = {'name':col, 'response_code':key, 'count':value}
                bar_df = bar_df.append(data, ignore_index=True)

        grouped_df = bar_df.groupby(['name', 'response_code']).agg({'count': 'sum'})
        percents_df= np.round(grouped_df.groupby('name').apply(lambda x: 100 * x / float(x.sum())),2).reset_index()
        
        #ax = sns.barplot(ax=axes[1, 1],data=bar_df,x='response_code', y='count', hue='name' )
        ax = sns.barplot(ax=axes[1, 1],data=percents_df,x='count', y='response_code', hue='name', orient = 'h' )
        ax.legend_.remove()
        #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='medium')
        ax.set_title('Response Code - % Distribution')
        ax.set_xlabel('% Distribution')
        ax.set_ylabel('Response Code')
        
        
        axes[2, 1].axis("off")
#        table_result = axes[2, 1].table(cellText=bar_df.values,
#                  rowLabels=bar_df.index,
#                  colLabels=bar_df.columns,
#                  cellLoc = 'right', rowLoc = 'center',
#                  loc='center')
#        table_result.auto_set_font_size(False)
#        table_result.set_fontsize(9)
#        axes[2, 1].set_title('Response Code Breakdown')

        
        fig.tight_layout()  

        plt.savefig('graphs.png')
    except Exception as e:
        raise e



def main():
    extract_latency_data()
    merge_data()
    generate_graphs()
    

if __name__ == "__main__":
    main()