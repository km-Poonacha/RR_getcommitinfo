#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 12:19:18 2017

@author: medapa

This calculates the productive deferrel using three different measures:
    PD1 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken by two consecutive contributions by different authors within a task/pullrequest (co-work) 
    
    PD2 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken between any two consecutive tasks in the project
    
    PD3 = Assess the proportion of tasks with atypical idle time (e.g., 2 standard deviations from the mean). 
    The time diff is already calculated is already calculated as the task duration of of PR. 
"""
import csv
from datetime import datetime

def timediff_hrs(sdatetime1, sdatetime2, dtformat):
    """Calculate the time difference between two string objects """ 
    hrdiff = 0
    datetimediff = datetime.strptime(sdatetime1, dtformat) - datetime.strptime(sdatetime2, dtformat)
    hrdiff = datetimediff.total_seconds()/(60*60)
    return hrdiff
def avg_super(repo_id,UPDATEDFINAL_CSV):
    """ Calculate Average idle time taken for two consecutive tasks by different authors (superposed work) """
    return 1
    
def PD1(repo_id,NEWPULL_CSV,UPDATEDFINAL_CSV):
    """ Calculates PD using the measure PD1 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken by two consecutive contributions by different authors within a task/pullrequest (co-work) """
    pd1 = 0
    cowork_hrs = 0
    tot_cowork = 0
    cowork_cnt = 0
    repo_found = 0
    avg_cowork = 0
    avg_super = 0
    prev_row = []
#step 1 find the repo
    with open(NEWPULL_CSV, 'rt', encoding = 'utf-8') as newpull_read:    
        newpulll_handle = csv.reader(newpull_read) 
        for row in newpulll_handle:
            if row[0] != "PullRequestEvent" and row[0] != "":                
                if repo_found == 1:
                    """If the repo was already found we have reached the end, Calculate pd1 and return results"""
                    if tot_cowork != 0:
                        avg_cowork = tot_cowork/cowork_cnt
                        """Call avg_super to calculate the idle time involved in superpsoed work and calulate tehe pd1  """
                        #pd1 = int(avg_super(repo_id,UPDATEDFINAL_CSV)) / avg_cowork
                        pd1 = avg_cowork
                    else: 
                        pd1 = ""
                    return pd1
                if row[0] == repo_id:
                    repo_found = 1 
            elif repo_found == 1 and row[0] == "" and prev_row[0] == "":
                if row[2] != prev_row[2] and row[3] != prev_row[3]:
                    cowork_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%dT%H:%M:%SZ')
                    tot_cowork = tot_cowork + cowork_hrs
                    cowork_cnt = cowork_cnt  + 1
            prev_row = row    
#step 2 

"""    
def PD2:
    
def PD3:
"""    
    
def cal_PD(NEWPULL_CSV ,UPDATEDFINAL_CSV):
    """ This function finds the repo and the details for collecting PD"""
    final_list = []
    del final_list[:]
    with open(UPDATEDFINAL_CSV, 'rt', encoding = 'utf-8') as final_append:    
        final_handle = csv.reader(final_append) 
        for row in final_handle:
            
            if row[0] != "PushEvent" and row[0] != "PullRequestEvent":
                repo_id = row[0]
                row.append(PD1(repo_id,NEWPULL_CSV,UPDATEDFINAL_CSV))
                final_list.append(row)
  
                
    """Finally update the PD information i nthe same file by re-writing its contents with the new appended data"""        
    with open(UPDATEDFINAL_CSV, 'wt', encoding = 'utf-8', newline='') as PD_append:
        PD_handle = csv.writer(PD_append)
        print("Writing to file .......")
        for row in final_list:
            PD_handle.writerow(row)  
        
        


def main():
    
    NEWPULL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-1/UpdateCommit/CommitPullRequestList2014.csv'    
    UPDATEDFINAL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-1/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    cal_PD( NEWPULL_CSV ,UPDATEDFINAL_CSV)
    
    
if __name__ == '__main__':
  main()