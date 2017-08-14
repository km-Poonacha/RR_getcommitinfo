from __future__ import division
import csv

def addnewrepodata(intsup_row,NEW_REPO_CSV):
    """Update the repo details with some additional details stores in newRepoList2014 csv file """
    with open(NEW_REPO_CSV, 'rt',encoding = 'utf-8' ) as New_Repo_read:    
        New_Repo_analysis = csv.reader(New_Repo_read) 
        new_index = 0
        for repo_row in New_Repo_analysis:
            found_flag = 0
            if str(intsup_row[0]) == str(repo_row[0]):
                intsup_row.append(repo_row[19])
                intsup_row.append(repo_row[20])
                intsup_row.append(repo_row[21])
                intsup_row.append(repo_row[22])
                intsup_row.append(repo_row[23])
                intsup_row.append(repo_row[24])
                intsup_row.append(repo_row[25])
                intsup_row.append(repo_row[26])
                intsup_row.append(repo_row[27])
                found_flag = 1
                return intsup_row
            else:
                new_index = new_index + 1   
                    
        if found_flag == 0:
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            intsup_row.append('Not Found')
            print ("**********************No match found while searching for new repo deatils")
            return intsup_row

def findSDflag(current_repo,INT_SD_CSV):
    """Include SD flag details into the repository """ 
    found_flag = 0
    with open(INT_SD_CSV, 'rt',encoding = 'utf-8' ) as SD_Read:    
        SD_analysis = csv.reader(SD_Read) 
        new_index = 0
        for SD_row in SD_analysis:
            found_flag = 0
            if str(current_repo[0]) == str(SD_row[1]):
                current_repo.append(SD_row[57])

                found_flag = 1
                return current_repo
            else:
                new_index = new_index + 1   
                    
        if found_flag == 0:
            current_repo.append('Not Found')
            print ("**********************No match found while searching for SD_FLAG")
            return current_repo

    
def create_super(UPDATEDFINAL_CSV,SUPER_CSV,NEW_REPO_CSV,INT_SD_CSV):
    
    with open(SUPER_CSV, 'wt',encoding = 'utf-8', newline='' ) as super_append:    
        super_handle = csv.writer(super_append)   
        deg_super = float 
        push_no = 0 
        pull_no = 0 
        current_repo = []
# Write the column headings
        super_handle.writerow(["REPO_ID","NAME","OWNER","OWNER_TYPE","SIZE","CREATE_DATE","PUSHED_DATE","MAIN_LANGUAGE","NO_LANGUAGES","SCRIPT_SIZE","STARS", "WATCHERS", "SUBSCRIPTIONS","OPEN_ISSUES","FORKS", "LICENCE_NAME","URL", "DESCRIPTION","LANG_JSON","NO_CONTRIBUTORS", "NO_PUSHES", "NO_PULLS", "NO_TASKS", "NO_NODES", "DEG_SUPER","AVG_COMMITS_PULLREQ","OWNER_PUBLICREPO" ,"OWNER_FOLLOWERS","OWNER_FOLLOWING","OWNER_CREATED","OWNER_HIREABLE","OWNER_EMAIL","TOTAL_CONTRIBUTORS","CONTRIBUTORS_PRE2015","AVG_COMMITS_COMMITTER","SD_FLAG"])        
        
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
                        first_row_flag = first_row_flag+1                        
                        current_repo = row
                        prev_row = row
                        continue
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
                    
                    #print ('Degree of superposition for repo no -', current_repo[0],contributor_no, push_no, pull_no, task_count, node_count, deg_super) 
                    #print ('**Total commit**', tot_commit, 'Avg commit', avg_commit)
                    #print ('')
                    """Append super details"""
                    current_repo.append(contributor_no)
                    current_repo.append(push_no)
                    current_repo.append(pull_no)
                    current_repo.append(task_count)
                    current_repo.append(node_count)
                    current_repo.append(deg_super)
                    current_repo.append(avg_commit)

                    """ Get additional repo details from NEW_REPO_CSV"""
                    current_repo = addnewrepodata(current_repo,NEW_REPO_CSV)
                    
                    """To overcoem the problems dealing with the first repo """

                    
                                        
                    """ Add SD_FLAG to the super repo """
                    current_repo = findSDflag(current_repo, INT_SD_CSV)
                    super_handle.writerow(current_repo)
                    
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
    
    UPDATEDFINAL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-2/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    SUPER_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-2/UpdateCommit/UpCommitSuper2014_24.csv'    
    NEW_REPO_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 5-2/RepoList2014_New.csv'
    INT_SD_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/New IntegratedSuper/FULLDATAIntegratedSuper2014_June_UPV2.csv'
    create_super(UPDATEDFINAL_CSV,SUPER_CSV,NEW_REPO_CSV,INT_SD_CSV)
    

if __name__ == '__main__':
  main()