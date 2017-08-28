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
import numpy as np

def timediff_hrs(sdatetime1, sdatetime2, dtformat):
    """Calculate the time difference between two string objects """ 
    hrdiff = 0
    datetimediff = datetime.strptime(sdatetime1, dtformat) - datetime.strptime(sdatetime2, dtformat)
    hrdiff = datetimediff.total_seconds()/(60*60)
    return hrdiff

def PD1(repo_id,NEWPULL_CSV,UPDATEDFINAL_CSV):
    """ Calculates PD using the measure PD1 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken by two consecutive contributions by different authors within a task/pullrequest (co-work) """
    co_idletime = []
    repo_found = 0
    prev_row = []
#step 1 find the repo
    with open(NEWPULL_CSV, 'rt', encoding = 'utf-8') as newpull_read:    
        newpulll_handle = csv.reader(newpull_read) 
        for row in newpulll_handle:
            if row[0] != "PullRequestEvent" and row[0] != "":                
                if repo_found == 1:
                    """If the repo was already found we have reached the end, Calculate pd1 and return results"""  
                    return co_idletime

                if row[0] == repo_id:
                    repo_found = 1 
            elif repo_found == 1 and row[0] == "" and prev_row[0] == "":
                if row[2] != prev_row[2] and row[3] != prev_row[3]:
                    cowork_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%dT%H:%M:%SZ')
                    if cowork_hrs < 0: cowork_hrs=cowork_hrs*-1
                    co_idletime.append(cowork_hrs)
            prev_row = row
        return co_idletime
#step 2 

   
def PD2(repo_id,UPDATEDFINAL_CSV):
    """ PD2 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken between any two consecutive tasks in the project"""
    repo_found = 0 
    prev_row = []
    nidletime_hrs = 0
    didletime_hrs = 0
    didletime = []
    nidletime = []
    with open(UPDATEDFINAL_CSV, 'rt', encoding = 'utf-8') as updated_read:    
        updated_handle = csv.reader(updated_read)  
        for row in updated_handle:
            if row[0] != "PullRequestEvent" and row[0] != "PushEvent" and row[0] != "":                
                if repo_found == 1:
                    """If the repo was already found we have reached the end, Calculate PD2 and return results"""
                    return nidletime,didletime

                if row[0] == repo_id:
                    repo_found = 1 
            elif repo_found == 1 and (row[0] == "PullRequestEvent" or row[0] == "PushEvent") and (prev_row[0] == "PullRequestEvent" or prev_row[0] == "PushEvent"):
                if row[2] != prev_row[2]:
                    nidletime_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%d %H:%M:%S')
                    if nidletime_hrs < 0:
                        nidletime_hrs = nidletime_hrs * -1
                    nidletime.append(nidletime_hrs)

                didletime_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%d %H:%M:%S')
                if didletime_hrs < 0:
                    didletime_hrs = didletime_hrs * -1
                didletime.append(didletime_hrs)                    
            prev_row = row    
        return nidletime,didletime
            
def PD3(nidletime,didletime):
    """PD3 = Assess the proportion of tasks with atypical idle time (e.g., 2 standard deviations from the mean). 
    The time diff is already calculated is already calculated as the task duration of of PR. """
    ncnt = 0
    dcnt = 0
    SD = np.std(didletime)
    #print("SD = ", SD)
    for ele in nidletime:
        if ele >= 2*SD:
            ncnt = ncnt +1
    for ele in didletime:
        if ele >=  2*SD:
            dcnt = dcnt + 1
    return ncnt, dcnt    
  
    
def cal_PD(NEWPULL_CSV ,UPDATEDFINAL_CSV):
    """ This function finds the repo and the details for collecting PD"""
    final_list = []
    avg_super = 0
    avg_cowork = 0
    nidletime = []
    didletime = []
    del final_list[:]
    with open(UPDATEDFINAL_CSV, 'rt', encoding = 'utf-8') as final_append:    
        final_handle = csv.reader(final_append) 
        for row in final_handle:
            
            if row[0] != "PushEvent" and row[0] != "PullRequestEvent":
                repo_id = row[0]
                #print("repo = ", repo_id)
                
                """New colums added to excel - C_IDLETIME, S_IDLETIME, T_IDLETIME,S_SDCNT, T_SDCNT,SCNT, TCNT"""
                co_idletime = PD1(repo_id,NEWPULL_CSV,UPDATEDFINAL_CSV)
                if co_idletime:
                    row.append(np.mean(co_idletime))
                else: row.append("")
                nidletime,didletime = PD2(repo_id,UPDATEDFINAL_CSV)
                if nidletime:
                    row.append(np.mean(nidletime))
                else: row.append("")
                if didletime:
                    row.append(np.mean(didletime))
                else: row.append("")
                ncnt, dcnt = PD3(nidletime,didletime)
                row.append(ncnt)
                row.append(dcnt) 
                row.append(len(nidletime))
                row.append(len(didletime))
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
"""
    NEWPULL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-2/UpdateCommit/CommitPullRequestList2014.csv'    
    UPDATEDFINAL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-2/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    cal_PD( NEWPULL_CSV ,UPDATEDFINAL_CSV)    
"""    
if __name__ == '__main__':
  main()