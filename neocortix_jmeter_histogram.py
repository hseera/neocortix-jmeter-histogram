# -*- coding: utf-8 -*-

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import os

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
                FILE_TO_WRITE = "new_"+os.path.basename(file)
                df = pd.read_csv(file)
                x = []
                x = df.loc[df['label'] == TRANSACTION_NAME] #filter out all the rows for which the label column does not contain value GetDistribution
                with open(FILE_TO_WRITE,'w') as fwrite:
                    fwrite.write('elapsed_time_'+FILE_TO_WRITE+'\n')
                    for item in range(len(x)):
                       fwrite.write('%s\n' %x['elapsed'].values[item])
            else:
                continue
        except Exception as e:
            raise e

'''
Note glob.glob() is not case sensitive in Windows OS. 
Make sure the files that need to be merged have unique names from other file. 
https://jdhao.github.io/2019/06/24/python_glob_case_sensitivity/
'''
def merge_latency_data():
    try:    
        files = glob.glob("./new_TestPlan_results_*.csv") #extract_data function generates csv files that start with new_TestPlan_results
        dataframes = [pd.read_csv(p) for p in files]
        merged_dataframe = pd.concat(dataframes, axis=1)
        merged_dataframe.to_csv("./responsetime_histogram.csv", index=False)
    except Exception as e:
        raise e


'''
This function iterates through all the columns in the responsetime_histogram file
and generate histogram for all of them. It also plots the average response time for all.

Note: comment out the code that plots mean on the graph if not required.
'''
def generate_histogram():
    #for testing purpose use the file responsetime_histogram provided
    FILE = "./responsetime_histogram.csv" #replace with your file name
    try:
        df = pd.read_csv(FILE) # read the file
        
        #default histogram settings
        plt.figure(figsize=(12,8))
        kwargs = dict(histtype='step', stacked=False, alpha=0.6, fill=True, bins=20000)
        plt.xlim(0,3000)
        plt.xlabel('Response Time (ms)')
        plt.ylabel('Frequency')
        plt.grid(axis="x", color="black", alpha=.8, linewidth=0.2, linestyle=":")
        plt.grid(axis="y", color="black", alpha=.8, linewidth=0.2, linestyle=":")
        
        y_upper=0.1 # set the default y distance for the text for mean 
        x_upper=1 # set the default x distance for the text for mean
        
        for col in df.columns:
            plt.hist(df[col],**kwargs)
            '''Disable the below code if you don't want to display mean value for each chart. 
            '''
            plt.axvline(np.mean(df[col]), color='r', linestyle='dashed', linewidth=0.5)
            min_ylim, max_ylim = plt.ylim()
            plt.text(np.mean(df[col])*x_upper, max_ylim*y_upper, 'μ: {:.2f}'.format(np.mean(df[col])))
            y_upper=y_upper + 0.05
            x_upper=x_upper+ 0.002
        plt.savefig('histogram.png')
    except Exception as e:
        raise e

def main():
    extract_latency_data()
    merge_latency_data()
    generate_histogram()
    
    

if __name__ == "__main__":
    main()
