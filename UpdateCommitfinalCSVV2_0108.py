import csv
from datetime import datetime

def timediff_hrs(sdatetime1, sdatetime2, dtformat):
    """Calculate the time difference between two string objects """ 
    hrdiff = 0
    datetimediff = datetime.strptime(sdatetime1, dtformat) - datetime.strptime(sdatetime2, dtformat)
    hrdiff = datetimediff.total_seconds()/(60*60)
    return hrdiff
    
def matchcommit_final_2(FINAL2_CSV, COMMITS_CSV, NEW_CSV,MISSINGPR_CSV):
    """Match commit information of PRs in CommitPullRequestList2014.csv with the PRs in Final2014V2_24.csv """    
    with open(NEW_CSV, 'wt', encoding = 'utf-8', newline='' ) as new_append:    
        new_handle = csv.writer(new_append)     
        PR_list = []
        del PR_list[:]
        with open(FINAL2_CSV, 'rt', encoding = 'utf-8' ) as final_read:
            final_analysis = csv.reader(final_read) 
            PR_found_list= []
            for row in final_analysis:
                """If it is a new repo then find the commit information from the Commit_Csv and store in a multi list """
                if (row[0] != 'PullRequestEvent') and (row[0] != 'PushEvent'):
                    repo_id = row[0]
                    repo_found = 0
                    """Find the PRs that are missing from BQ results and store in a seperate MISSINGPR_CSV"""

                    for row_element in PR_list:
                        if row_element[0] != "PullRequestEvent":
                            continue
                        elif row_element[9] in PR_found_list:
                            continue
                        else: 
                            if str(row_element[14]) == "TRUE" :
                                """ If the PR is not found in BQ and it is merged, then append it to the missing csv file """
                                #print("PR not found - ", row_element[9] )
                                with open(MISSINGPR_CSV, 'at', encoding = 'utf-8', newline='' ) as missing_append:    
                                    missing_handle = csv.writer(missing_append)  
                                    missing_handle.writerow(row_element)
                    
                    with open(MISSINGPR_CSV, 'at', encoding = 'utf-8', newline='' ) as missing_append:    
                        missing_handle = csv.writer(missing_append) 
                        missing_handle.writerow(row) 
                    """ Write the repo details into the NEW_CSV file"""
                    new_handle.writerow(row)
                    del PR_list[:]                    
                    del PR_found_list[:]
                    with open(COMMITS_CSV, 'rt' , encoding = 'utf-8') as commits_read:
                        commits_analysis = csv.reader(commits_read) 
                        for commit_row in commits_analysis:
                            if(commit_row[0] == repo_id ):
                                repo_found = 1
                                print("Repo found - ",repo_id)
                                continue
                            if(repo_found == 1):
                                if(commit_row[0]=="" or commit_row[0]=="PullRequestEvent" ):
                                    PR_list.append(commit_row)
                                else:
                                    repo_found = 0
                                    break
                elif(row[0] == 'PullRequestEvent'):
                    """ Use PR_list to find commit information for the pull requests"""    
                    """If it is a new repo then find the commit information from the Commit_Csv and store in a multi list """
                    PR_id = row[1]
                    PR_found = 0
                    author_found =0 
                    author_list = []
                    no_authors = 0
                    del author_list[:]
                    #print("Searching for PR - ", PR_id)
                    for element in PR_list:
                        """Find the PR from the PR_list """
                        if PR_id in element:
                           # print("PR found - ", PR_id)
                            PR_found = 1
                            PR_found_list.append(PR_id)
                            continue
                        elif element[0] == "" and PR_found == 1:
                            """ Populate the authors list"""
                            author_found = 0
                            for author in author_list:
                                """The name and emailidhas to be different to be considered as different contributors """
                                if author[1] == element[3] or author[0] == element[2]:
                                    author_found = 1
                                    break
                            if author_found == 0:
                                author_list.append([element[2],element[3]])
                                no_authors = no_authors + 1
                        else:
                            PR_found = 0
                
                    row.append(no_authors)
                    """Calculate time duration of the task for productive deferrel """
                    prod_deferrel  = timediff_hrs(row[4],row[3],'%Y-%m-%d %H:%M:%S')
                    row.append(prod_deferrel)
                    new_handle.writerow(row)       
                elif(row[0] == 'PushEvent'): 
                    """Do nothing """
                    new_handle.writerow(row)  
  
def main():

    FINAL2_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/Final 2/Final2014V2_24.csv'
    COMMITS_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/CommitPullRequestList2014.csv'
    NEW_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    MISSINGPR_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/MISSINGPR.csv'
    matchcommit_final_2(FINAL2_CSV, COMMITS_CSV,NEW_CSV,MISSINGPR_CSV)
    
if __name__ == '__main__':
  main()