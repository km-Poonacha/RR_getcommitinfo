
import csv

def PDappendsuper(UPDATEDFINAL_CSV,SUPER_CSV,PDSUPER_CSV):
    """Update the PD details into the super csv file - C_IDLETIME, S_IDLETIME, T_IDLETIME,S_SDCNT, T_SDCNT,SCNT, TCNT"""
    with open(PDSUPER_CSV, 'wt',encoding = 'utf-8', newline='' ) as pdsuper_append:    
        pdsuper_handle = csv.writer(pdsuper_append) 
        pdsuper_handle.writerow(["REPO_ID","NAME","OWNER","OWNER_TYPE","SIZE","CREATE_DATE","PUSHED_DATE","MAIN_LANGUAGE","NO_LANGUAGES","SCRIPT_SIZE","STARS", "WATCHERS", "SUBSCRIPTIONS","OPEN_ISSUES","FORKS", "LICENCE_NAME","URL", "DESCRIPTION","LANG_JSON","NO_CONTRIBUTORS", "NO_PUSHES", "NO_PULLS", "NO_TASKS", "NO_NODES", "DEG_SUPER","AVG_COMMITS_PULLREQ","OWNER_PUBLICREPO" ,"OWNER_FOLLOWERS","OWNER_FOLLOWING","OWNER_CREATED","OWNER_HIREABLE","OWNER_EMAIL","TOTAL_CONTRIBUTORS","CONTRIBUTORS_PRE2015","AVG_COMMITS_COMMITTER","SD_FLAG","C_IDLETIME","S_IDLETIME","T_IDLETIME","S_SDCNT","T_SDCNT","SCNT","TCNT"])        
 
        with open(SUPER_CSV, 'rt',encoding = 'utf-8') as super_append:    
            super_handle = csv.reader(super_append) 
            for repo_row in super_handle:
                found_flag = 0
                with open(UPDATEDFINAL_CSV, 'rt',encoding = 'utf-8' ) as New_Repo_read:    
                    New_Repo_analysis = csv.reader(New_Repo_read) 
                    for row in New_Repo_analysis:
                        if str(repo_row[0]) ==  str(row[0]):
                            repo_row.append(row[19])
                            repo_row.append(row[20])
                            repo_row.append(row[21])
                            repo_row.append(row[22])
                            repo_row.append(row[23])
                            repo_row.append(row[24])
                            repo_row.append(row[25])
                            found_flag = 1
                            pdsuper_handle.writerow(repo_row) 
                            break
                    if found_flag == 0 and repo_row[0] != "REPO_ID":
                        repo_row.append("")
                        repo_row.append("")
                        repo_row.append("")
                        repo_row.append("")
                        repo_row.append("")
                        repo_row.append("")
                        pdsuper_handle.writerow(repo_row) 
                        #print ("**********************No match found while searching for new repo deatils - ",repo_row[0] )

def main():


    UPDATEDFINAL_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/UpdateCommitFinal2014V2_24.csv'
    SUPER_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/UpCommitSuper2014_24.csv'    
    PDSUPER_CSV = '/Users/medapa/Dropbox/HEC/Data GitHub/2014/Run 1000/UpdateCommit/PDUpCommitSuper2014_24.csv'    

    PDappendsuper(UPDATEDFINAL_CSV,SUPER_CSV,PDSUPER_CSV)
    print("Completed ", PDSUPER_CSV )

if __name__ == '__main__':
  main()