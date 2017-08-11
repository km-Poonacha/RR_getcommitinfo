from __future__ import division
import csv
import time
from datetime import date
from datetime import datetime


def create_super(UPDATEDFINAL_CSV,SUPER_CSV):
    
    with open(SUPER_CSV, 'wt',encoding = 'utf-8', newline='' ) as super_append:    
        super_handle = csv.writer(super_append)   
        deg_super = float 
        push_no = 0 
        pull_no = 0 
        current_repo = []
# Write the column headings
        super_handle.writerow(["REPO_ID","NAME","OWNER","OWNER_TYPE","SIZE","CREATE_DATE","PUSHED_DATE","MAIN_LANGUAGE","NO_LANGUAGES","SCRIPT_SIZE","STARS", "WATCHERS", "SUBSCRIPTIONS","OPEN_ISSUES","FORKS", "LICENCE_NAME","URL", "DESCRIPTION","LANG_JSON","NO_CONTRIBUTORS", "NO_PUSHES", "NO_PULLS", "NO_TASKS", "NO_NODES", "DEG_SUPER","AVG_COMMIT"])        
        
        with open(UPDATEDFINAL_CSV, 'rt',encoding = 'utf-8' ) as new_read:    
            new_analysis = csv.reader(new_read)     
            node_count = 0
            deg_super = 0.0
            task_count = 0
            first_row_flag = 0
            contributor_no = 0
            tot_commit = 0
            avg_commit = 1
            for row in new_analysis:
                if (row[0] != 'PullRequestEvent') and (row[0] != 'PushEvent'):

                    if first_row_flag == 0: 
                        current_repo = row
                        prev_row = row
                    first_row_flag = first_row_flag+1
#append contributor no                    
                    if prev_row[0] != 'PushEvent' and prev_row[0] != 'PullRequestEvent':
                        contributor_no = 0
                    else: 
                        contributor_no = prev_row[14]
                        

                    if node_count == 0: deg_super = 0.0
                    
                    else: 
                        deg_super = float( node_count / task_count)
                    
                    if pull_no == 0: avg_commit = 1.0
                    
                    else:                         
                        
                        avg_commit = tot_commit / pull_no
                    
                    print ('Degree of superposition for repo no -', current_repo[0],contributor_no, push_no, pull_no, task_count, node_count, deg_super) 
                    print ('**Total commit**', tot_commit, 'Avg commit', avg_commit)
                    print ('')
                  
                    super_handle.writerow([current_repo[0],current_repo[1],current_repo[2],current_repo[3],current_repo[4],current_repo[5],current_repo[6],current_repo[7],current_repo[8],current_repo[9],current_repo[10], current_repo[11], current_repo[12],current_repo[13],current_repo[14], current_repo[15], current_repo[16], current_repo[17], current_repo[18],contributor_no, push_no, pull_no, task_count, node_count, deg_super,avg_commit])
                    current_repo = row
                    node_count = 0
                    task_count = 0 
                    push_no = 0 
                    pull_no = 0 
                    contributor_no = 0
                    tot_commit = 0
                
                elif (prev_row[0] != 'PullRequestEvent') and (prev_row[0] != 'PushEvent'):  
                    node_count = 1
                    task_count = 1 

                    if row[0] == 'PullRequestEvent':
                        pull_no = pull_no + 1
                        """ Increase task count by number of authors in PR - 1 """
                        if int(row[16]) > 1:
                            task_count= task_count + int(row[16])-1
                        tot_commit = tot_commit + int(row[13])
                    else:
                        push_no = push_no + 1
       
                else: 
                    if row[15] == prev_row[15]:
                        task_count = task_count + 1
                        if row[0] == 'PullRequestEvent':
                            pull_no = pull_no + 1
                            tot_commit = tot_commit + int(row[13])
                            """ Increase task count by number of authors in PR - 1 """
                            if int(row[16]) > 1:
                                task_count= task_count + int(row[16])-1
                        else:
                            push_no = push_no + 1
                    else: 
                        task_count = task_count + 1
                        node_count = node_count + 1
                        if row[0] == 'PullRequestEvent':
                            pull_no = pull_no + 1
                            tot_commit = tot_commit + int(row[13])
                            """ Increase task count by number of authors in PR - 1 """
                            if int(row[16]) > 1:
                                task_count= task_count + int(row[16])-1
                        else:
                            push_no = push_no + 1
                prev_row = row
                
                
    print ('No of repos processed = ', first_row_flag)                          

def main():
    
    UPDATEDFINAL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-1/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    SUPER_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-1/UpdateCommit/UpCommitSuper2014_24.csv'
    create_super(UPDATEDFINAL_CSV,SUPER_CSV)
    

if __name__ == '__main__':
  main()