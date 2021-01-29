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
def extract_data():

    FILE_TO_WRITE =""       
    for file in os.listdir(LOCATION):
        try:
            if file.startswith("TestPlan_") and file.endswith(".csv"):
                FILE_TO_WRITE = "result_"+os.path.basename(file)
                df = pd.read_csv(file)
                x = []
                x = df.loc[df['label'] == 'GetDistribution'] #filter out all the rows for which the label column does not contain value GetDistribution
                with open(FILE_TO_WRITE,'w') as fwrite:
                    fwrite.write('elapsed_time_'+FILE_TO_WRITE+'\n')
                    for item in range(len(x)):
                       fwrite.write('%s\n' %x['elapsed'].values[item])
        except Exception as e:
            raise e

'''
note glob.glob() is not case sensitive in Windows OS. 
Make sure the files that needs to be merged have unique names from other file. 
https://jdhao.github.io/2019/06/24/python_glob_case_sensitivity/
'''

def merge_files():
    try:    
        files = glob.glob("./result_TestPlan_results_*.csv")
        dataframes = [pd.read_csv(p) for p in files]
        merged_dataframe = pd.concat(dataframes, axis=1)
        merged_dataframe.to_csv("./responsetime_histogram.csv", index=False)
    except Exception as e:
        raise e


'''
This function iterates through all the columns in the responsetime_histogram file
and generate histogram for all of them. It also plots the average response time for all.
'''
def generate_histogram():
    #for testing purpose use the file responsetime_histogram provided
    FILE = "./responsetime_histogram.csv" #replace with your file name
    try:
        df = pd.read_csv(FILE) # read the file
        
        plt.figure(figsize=(10,10))
        kwargs = dict(histtype='stepfilled', stacked=False, alpha=0.7, fill=True, bins=7000)
        plt.xlim(0,4000)
        plt.xlabel('Response Time (ms)')
        plt.ylabel('Total Count/Bin')
        
        y_upper=0.4
        x_upper=1
        for col in df.columns:
            plt.hist(df[col],**kwargs)
            plt.axvline(np.mean(df[col]), color='r', linestyle='dashed', linewidth=0.5)
            min_ylim, max_ylim = plt.ylim()
            plt.text(np.mean(df[col])*x_upper, max_ylim*y_upper, 'Mean: {:.3f}'.format(np.mean(df[col])))
            y_upper=y_upper + 0.05
            x_upper=x_upper+ 0.002
    except Exception as e:
        raise e

def main():
    extract_data()
    merge_files()
    generate_histogram()
    
    

if __name__ == "__main__":
    main()
