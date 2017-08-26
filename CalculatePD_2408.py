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
    
def cal_super(repo_id,UPDATEDFINAL_CSV):
    """ Calculate Average idle time taken for two consecutive tasks by different authors (superposed work) """
    repo_found = 0
    idletime_hrs = 0
    prev_row = []
    tot_idletime = 0
    tot_cnt = 0
    avg_idletime = 0
    with open(UPDATEDFINAL_CSV, 'rt', encoding = 'utf-8') as UPDATEDFINAL_read:    
        UPDATEDFINAL_handle = csv.reader(UPDATEDFINAL_read) 
        for row in UPDATEDFINAL_handle:
            if row[0] != "PullRequestEvent" and row[0] != "PushEvent" and row[0] != "":                
                if repo_found == 1:
                    """If the repo was already found we have reached the end, Calculate avg idle time and return results"""
                    if tot_idletime != 0:
                        avg_idletime = tot_idletime/tot_cnt
                    else: 
                        avg_idletime = 0
                    return avg_idletime
                if row[0] == repo_id:
                    repo_found = 1 
            elif repo_found == 1 and (row[0] == "PullRequestEvent" or row[0] == "PushEvent") and (prev_row[0] == "PullRequestEvent" or prev_row[0] == "PushEvent"):
                if row[2] != prev_row[2]:
                    idletime_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%d %H:%M:%S')
                    if tot_idletime < 0:
                        tot_idletime = tot_idletime * -1
                    tot_idletime = tot_idletime + idletime_hrs
                    tot_cnt = tot_cnt  + 1
            prev_row = row    
        return 0


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
                        avg_super = cal_super(repo_id,UPDATEDFINAL_CSV)
                        if avg_super != 0:   
                            pd1 = avg_super / avg_cowork
                        else:
                            pd1 = ""
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
        return None
#step 2 

   
def PD2(repo_id,UPDATEDFINAL_CSV):
    """ PD2 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken between any two consecutive tasks in the project"""
    repo_found = 0 
    prev_row = []
    nidletime_hrs = 0
    didletime_hrs = 0
    ntot_idletime = 0
    dtot_idletime = 0
    ntot_cnt = 0
    dtot_cnt = 0
    navg_idletime = 0
    davg_idletime = 0
    pd2 = 0
    with open(UPDATEDFINAL_CSV, 'rt', encoding = 'utf-8') as updated_read:    
        updated_handle = csv.reader(updated_read)  
        for row in updated_handle:
            if row[0] != "PullRequestEvent" and row[0] != "PushEvent" and row[0] != "":                
                if repo_found == 1:
                    """If the repo was already found we have reached the end, Calculate PD2 and return results"""
                    if ntot_idletime != 0 and dtot_idletime != 0 :
                        navg_idletime = ntot_idletime/ntot_cnt
                        davg_idletime = dtot_idletime/dtot_cnt
                        pd2 = navg_idletime/davg_idletime
                        print(repo_id,"  ",navg_idletime,"   ",davg_idletime)
                    else: 
                        pd2 = ""
                    return pd2
                if row[0] == repo_id:
                    repo_found = 1 
            elif repo_found == 1 and (row[0] == "PullRequestEvent" or row[0] == "PushEvent") and (prev_row[0] == "PullRequestEvent" or prev_row[0] == "PushEvent"):
                if row[2] != prev_row[2]:
                    nidletime_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%d %H:%M:%S')
                    if nidletime_hrs < 0:
                        nidletime_hrs = nidletime_hrs * -1
                    ntot_idletime = ntot_idletime + nidletime_hrs
                    ntot_cnt = ntot_cnt  + 1

                didletime_hrs = timediff_hrs(row[4],prev_row[4],'%Y-%m-%d %H:%M:%S')
                if didletime_hrs < 0:
                    didletime_hrs = didletime_hrs * -1
                dtot_idletime = dtot_idletime + didletime_hrs
                dtot_cnt = dtot_cnt  + 1                    
            prev_row = row    
        return ""
            
""" 
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
                row.append(PD2(repo_id,UPDATEDFINAL_CSV))
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