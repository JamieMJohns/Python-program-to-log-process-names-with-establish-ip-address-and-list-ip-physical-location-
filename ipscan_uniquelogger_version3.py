# %%
# -*- coding: utf-8 -*-
"""
@author: Jamie Johns

Created on Fri Jun 02 16:38:28 2017 (version 1)
Updated on Fri Jun 10 02:00:00 2018 (version 2)
Updated on Thu Aug 22 06:30:12 2019 (version 3.0.1: checkpoint commit, program functionality finalised; code comments to be added and code to be further tidied up)

Github repository: https://github.com/JamieMJohns/Python-program-to-log-process-names-with-establish-ip-address-and-list-ip-physical-location-

NEW IN VERSION 3 (rough detail); !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

The functionality of the code is finalised version 3, the only major changes to be made for the final commit (post-checkpoint commit) is;
 -> add further comments to python code for context (where further contenxt is need or comments missing)
 -> tidy up code [remove anything unsused/redundant]

[some details below will be eventually move to repository readme]
as mentioned, this is a checkpoint commit (more details[comments for context] to be added and code to be tidied)

 >added second api [for look up geolocation dat of ip], if first original API times-out; (a check is made in the program)
     >> API 1 (original used in version 1 and 2); ip-api.com
         > unlimited ip-lookups (requests) over time but limited to 150 requests per minute otherwise your ip is temporarily 
             blocked by website [as per their terms and policies]; you can unblock your ip earlier by submitting to http://ip-api.com/docs/unban
             [note to self: add limiter to code to avoid 150 request in a minute (a very rare scenario)]
             
     >> API 2; ipapi.co
         > API (website) comes with free and registered accounts, free account is limited to 1000 lookups per day
           [note to self: add parameter to count requests]
           
     Further note: current code will always use API 1 over API 2, if available (when timeout-connect test is done).
             
> in addition showing to country/state/city for associated ip {obtained using [above API]} ... 
   "organisation" associated with the ip is now listed
   
 > [if found] program reads "excluded" ip(outgoing),pid,process_name from      
   textfile named "exclude_process.txt" which should be located (placed) in same directory as
    the code/program .... (more details to add but example .txt file found on github repository)
    { between scans - the program will search for and read .txt (if found) and determine if new exclusion conditions are applied;
      the user is alerted if there is a change to exclusion conditions}
    Exclusion conditions = exclude printing and ip look (geo-loc data with API) for processes of particular process_name,PID,ip(outgoing)
      [look at example .txt file on github repository]
    >> program has wont crash and handles for scenarios;
        > text file is missing
        > text file is empty (no text)
        > text file is empty but on multiple lines (white spaces with no character) = handled as empty text file
        > "comments" can be made in text file for which lines are completely ignored as exclusion condition (if "##" appears anywhere in that line)

  few smaller details to note in final commit, soon to come, of version 3.00

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


[below here is description from version 2 of program (to be update)]
Program to log process (tasks) with established (connected)
outgoing ip address and list their;
internal ip, foreign (outgoing ip) , Pid and process name as well
as physical location related to outgoing ip address

The difference from version 1 is;
-> added catch/exception to code such that .exe does not suddenly
   exit in event of an unexpected error (also prints error message)
-> using website: http://ip-api.com
   details about an in ip address is obtained (in csv) by applying, for
   example of arbitrary ip address '153.177.97.188' the csv output is obtained
   from reading html output of "http://ip-api.com/csv/153.177.97.188"
   
   From this html (and hence output csv), can obtain; country/state/city
   of ip address.
   
   Other than that, no significant changes from version1

printed logging of a new process is performed on basis that it's
PID or process name is unique to previously printed logs
in a later version of this program; unique outgoing ip will result in
previous pid and process name being printed in log


"""
# KEEP AN EYE ON IP TRAFFIC
import re #import module which provides support for "regular expressions" used to obtain column data from cmd output
import os #operating system module - allows for execution of cmd commands in python code (and obtain output)
import datetime #imports module used to obtain exact (current) date and time
import subprocess # module allows to spawn multiple (cmd) outputs and connect input/output values and obtain return code
import urllib #urllib module is used for reading a website and obtaining it's html code
import requests # requests module applied to test connnection for if time with API (requires internet)
os.system('color 0c')  #set text color to bright red [only works in final produced .exe (cmd type prompt)]
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' # Introduction%%%%%%%%%%%%%%%%%%%%%%%%%
print '$$$$$$$$$$$$$$$$$$$$$  IP TRAFFIC LOGGER $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '                     Program Created by Jamie Johns                    '
print '                              2018                                   '
print '                          version 3.0.0 [2019 update]                  '
print ' [code created in python 2.7 and then converted to .exe using pyinstaller]'
print '  (description to below be updated.. [mostly version 2 descript below])'
print ' '
print 'This .exe is converted from code of a checkpoint commit for version3;'
print ' \t-> the program [.exe] functionality is finalised  for version 3'
print 'Only changes for final commit is to update description (below) and finish'
print 'off final comments [in code] which are both part of the source code of this .exe'
print ''
print 'The final commit of version 3 (incl. .exe and source .py) will soon be '
print 'uploaded to github repository of this same .exe file, which is: '
print 'https://github.com/JamieMJohns/Python-program-to-log-process-names-with-establish-ip-address-and-list-ip-physical-location-'
print ''
print 'PROGRAM DESCRIPTION (to be updated)=================================='
print 'This program logs foriegn IP address and related details of any proces-'
print 'that make established connections outside of your computer.            '
print '\n'
print 'This program performs continous logging and produces information for new'
print 'connections that are made.                                             '
print 'The format of the output is: '
print '(internal/local ip) || (foriegn ip address) || PID (process ID) || related process'
print 'In addition, a country,state, city and organistation is provided for'
print 'each foriegn Ip address [if obtainable] through the use of either API:'
print '\t\t>ip-api.com [if available]'
print '\t\t>ipapi.co [if first not available]\n\n'
print 'The scan is continous and only logs unique processes over entire program run'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print '(scroll up to read full details)\n\n'
nothin=raw_input('<Press enter to start scanning>') #wait for user input
running=1 #parameter which controls below while loop 
scannum=1 #parameter which counts how many scan logs have been printed
first_run = 1
Unique_LIST=[] #list of unqiue strings <outgoing_ip>_<PID>_<process_name> from processes



# Functions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def process_exclude_obtain(excludes,error_param,echo): # timeout and connection test to see if API are available
    excluded0=excludes[:]
    excludes=[]
    try: # will cause error if related text file unavailable
        path=os.getcwd()
        fid=open(path+'\\exclude_process.txt','r')
        excludes = fid.read().split("\n") # Create a list containing all lines
        excludes = [j for j in excludes if "##" not in j] # remove lines which are comments (contain '##' anywhere in line)
        fid.close() # Close file
        if (echo ==1) and ((set(excluded0)!=set(excludes)) or error_param ==1): # if echo text is on and new list is different (text file was modified)
            exl='|'.join(excludes)
            exl_nws = exl.replace('|','') # excl with | repclaced with empty space
            exl_nws = exl_nws.replace(' ','') # excl with white spaces repclaced with empty space [exl-nws considers if text file multiple blank lines]
            print '\n@@@@@@@@@@@@@@@@@@@@ "exclude_process.txt" read @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
            if exl!='' and exl_nws!='': # if textfile not empty
                print 'New exclusion list:'+exl
            else:
                print 'New exclusion list: <none specified in file>'
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
            error_param = 0
    except: # if  problem reading file: return blank list { most like due to missing .txt file}
        excludes=[]
        if echo ==1 and error_param==0 :
            print '\n@@@@@@@@@@@@@@@@@@@@ "exclude_process.txt" READ ERROR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
            print 'Could not succesfully located and read required text file (exclude_process.txt);'
            print ' Hence, New exclusion list:  <none specified>'
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
            error_param = 1
    return excludes,error_param

def timeouttest(api1T,api2T,timeout_input,echo_text): # timeout and connection test to see if API are available
    api1T=0
    api2T=0
    if echo_text==1:
        print '\t Performing connection test for API .....'
        print '\t   [geo-location of ip-address]'
    try: #test timeout on main ip-detail grab api [best]
        r = requests.get('http://ip-api.com/', timeout=timeout_input) # limited to 1000 IP lookups in a day for free account
    except requests.Timeout:
        api1T=1
    except: 
        api1T=1
    try: #test timeout on secondary ip-detail grab api
        r = requests.get('https://ipapi.co/', timeout=timeout_input) # limited to 1000 IP lookups in a day for free account
    except requests.Timeout:
        api2T=1
    except: 
        api2T=1
    if echo_text==1:
        print '\t ...Test complete!\n'
    return api1T, api2T
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Exclud_process=[]
api1_timeout=0
api2_timeout=0
txtfile_err=0;
# MAIN SECTION OF CODE [CONTINOUS SCANNING until program close or error] ####################################################################################
while running == 1: #Continous scanning of outgoing/ingoing ip related to running processes [whilst running=1]
    try: #Try running main section of code $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        api_connect_attempt=0
        api_timeout_persist=0
        Exclud_process,txtfile_err=process_exclude_obtain(Exclud_process,txtfile_err,1)
        if first_run == 1 :
            api1_timeout,api2_timeout=timeouttest(api1_timeout,api2_timeout,2,1) # timeoutctest
            if api1_timeout == 1 and api2_timeout == 1:  # if both connections timed out
                print '\n None of the two Api ARE available to obtain locational data for ip-addresses [all had time-out connection]'
                print 'Connection will be retested before next scan.......\n'
            first_run = 0 
        profilesNEW=[] #initialize (empty) list of profiles (tasks and details) picked up in scan
        tasks=[] #initialize (empty) list of tasknames picked up in scan
        now=datetime.datetime.now() #current date and time
        k=subprocess.Popen(['netstat','-ano'],stdout=subprocess.PIPE) #record (and connect) data of running cmd command 'netstat -ano'
        #"netstat -ano" cmd command is a list of detected running processes and their respective;
        # outgoing/ingoing ip address, PID and Image name        
        profilesNEW=re.findall('(.*)ESTABLISHED(.+)\r',k.communicate()[0]) #gets list of processes for which ip connection has been established
        tasks = os.popen("tasklist").readlines()  #get list of processes detected as currently running (cmd)
        del tasks[0] #removes(deletes) first row from "tasks" (which is just a blank line)
        del tasks[0] #removes(deletes) next row from "tasks" (which is just column headers of output from tasklist command)
        del tasks[0] #removes(deletes) next row from "tasks" (which is seperator of column header from data in columns)
        # final "tasks" is just tasklist data; image name
        #[below] cur=parameter which keeps track of current process being seperated into distinct data (start cur=0)
        for cur,x in enumerate(tasks,start=0): #enumerate through each element of "tasks"
            tasks[cur]=tasks[cur].split() #split each element (sentence) of "tasks" into distinc element
        r=[] #initialise list of established connections which will be complete collection of imname,PID, out/in IP etc... (for each process)
        y=[] #initialise list which will be collection of ip address and PID which has made "established connection
        for x in profilesNEW : #iterate through each element of "profilesNEW" (which are list of tasks with establish connection to external ip)
            #each x has form  ('  TCP    192.168.0.18:54914     54.230.245.51:443      ', '     5548')
            # which is        (' {con. type} {ingoing ip}:{port} {outgoing ip}:{port}   ', '    PID ')          
            y=x[0]+x[1] #y is =(' {con. type} {ingoing ip}:{port} {outgoing ip}:{port}  PID')   [x combined]
            y=y.split() #get elements of y which are disinct by seperation of ' ' that is y=[{con. type},{ingoing ip}:{port},{outgoing ip}:{port},PID]
            y[1]=y[1].split(':')[0] #y[1]={ingoing ip}  (remove ":{port}")
            y[2]=y[2].split(':')[0] #y[2]={outgoing ip}   (remove ":{port}")  
            #y is now =[{con. type},{ingoing ip},{outgoing ip},PID]            
            pf=0 #parameter which indicates if at least one PID of "tasks"
            for z in tasks: #for each row,z= imagename,PID,etc... for "tasks"
                if z[1] in y[3] and '.exe' in z[0]: #if PID z[1] in PID of y and is image name is .exe (not something else due to error)
                    y.append(z[0]) #apprend image name to to related y (by PID between tasks and y)
                    pf=1 #set parameter to 1 which indicates at least one "Established" connection has been found
            if pf == 0: #if not at least one relation of PID between tasks and y
                y.append('Process Unkown/dead') #apped string that 'process is dead/unknown' (used later in code)
            r.append(y) #append final y to r (data in y was found to have relation to a running process listed in "tasks")
        newscan=0 #initialise parameter which, if =1, indicates at least one new establish ip connection and currently running process has been found
        nw=[] #list of these new processes 
        for x in r: #for each element of r (list of running process (PID,imname,ip) with an established connection)
            if x[2]+'_'+x[3]+'_'+x[4] not in Unique_LIST and x[2] != '127.0.0.1': #if this element of r has PID or image name (process name) unique to previously logged establish connecitons                
                if not Exclud_process: # if exclude list is empty , print all; regardless []
                    nw.append(x) #append to list of unique establish process
                    Unique_LIST.append(x[2]+'_'+x[3]+'_'+x[4]) #add <outgoing_ip>_<PID>_<process_name> to unique list
                    newscan=1 #set newscan parameter to 1 to indicate a new printout of at least one unique established process will be printed
                else: #else if list is not empty
                    excluded=0 # exclude "unique process" (0=no 1=yes)
                    for Y in Exclud_process: # check for excludes
                        if x[2] == Y or x[3] == Y or x[4] == Y:
                            excluded=1
                    if excluded==0: #if at least not found
                        nw.append(x) #append to list of unique establish process
                        Unique_LIST.append(x[2]+'_'+x[3]+'_'+x[4]) #add <outgoing_ip>_<PID>_<process_name> to unique list
                        newscan=1 #set newscan parameter to 1 to indicate a new printout of at least one unique established process will be printed
        if newscan == 1: #if new scan =1 [if newscan=0, no new log is to printed and "while loop" starts again with new scan]
            Exclud_process,txtfile_err=process_exclude_obtain(Exclud_process,txtfile_err,1) # re-read text-file to see if new excludes added
            print 'Scan number '+str(scannum)+'##########################################' #indicate number scan log being printed
            print ' time performed: '+str(now)+'\n'   #indicate time that this scan was performed at (will be give or take ~10 seconds)
            api1_timeout,api2_timeout=timeouttest(api1_timeout,api2_timeout,2,0) # timeoutctest
            print ' Internal IP || Foreign IP (country,state;city - organisation) || PID || Process name' #header names of printed data
            for x in nw: #for each element of list of newly establish (connect) process to be logged
                    if api1_timeout ==0: # if primary api did not time out
                        try: #try to obtain country,state,city of outgoing (foriegn) ip address [if error, go to "catch"]               
                            ip_details=urllib.urlopen('http://ip-api.com/csv/'+x[2]).read().split(',') #read html of ip details from website
                            country=ip_details[1] #record country name related to foreign ip address
                            state=ip_details[3] #record state name related to foreign ip address
                            city=ip_details[5] #record city name related to foreign ip address
                            org=ip_details[11] #record organisation name related to foreign ip address 
                        except: #if error with recording details of interest in "try:"
                            if x[2] in '127.0.0.1': #assess wether "foreign" ip is just local (internal) ip address
                                country='local_host' #set "country name"
                                state='[internal]' #set "sity name"
                                city='' #leave city name blank
                                org =''
                            else: #else if country,state,city could not be obtain (for other circumstances)
                                country='N/A' #set country name to 'N/A' ('Not available)
                                state='' #leave state name blank
                                city='' #leave city name blank
                                org =''
                    else: #if primary api timed out
                        if api2_timeout ==0: # if secondary api did not time out
                            country=''
                            state=''
                            city=''
                            org =''
                            if x[2] in '127.0.0.1': #assess wether "foreign" ip is just local (internal) ip address
                                country='local_host' #set "country name"
                                state='[internal]' #set "sity name"
                                city='' #leave city name blank
                                org =''
                            else: #else if country,state,city could not be obtain (for other circumstances)
                                try:
                                    ip_details=urllib.urlopen('https://ipapi.co/'+x[2]+'/csv/').read().split('\r\n')[1]  
                                    country=ip_details[5] #record country name related to foreign ip address
                                    state=ip_details[3] #record state name related to foreign ip address
                                    city=ip_details[1] #record city name related to foreign ip address
                                    org =ip_details[12] #record organisation name related to foreign ip address 
                                except:
                                    country='N/A'
                                    state='N/A'
                                    city='N/A'     
                                    org='N/A'   
                        else:
                            country='N/A'
                            state='N/A'
                            city='N/A'
                            org='N/A'
                            if api_connect_attempt < 5: # if 5 or more consecutive timoute for all api / skip connect test on current scan to save time
                                api1_timeout,api2_timeout=timeouttest(api1_timeout,api2_timeout,1,0) # timeoutctest
                                if api1_timeout == 1 and api2_timeout == 1:
                                    api_connect_attempt += 1
                                else:
                                    api_connect_attempt = 0   
                            else:
                                api_timeout_persist=1 #
                    print x[1]+' || '+x[2]+'('+country+','+state+';'+city+'-'+org+') || '+x[3]+' || '+x[4]            
                    #(above) print; Internal IP + Foreign IP (country,state;city) + PID + Process name
                    
            print '######################################################################\n'
            if api_timeout_persist==1: # if api timeout persistent
                print '\n Both API, used to obtain locational data for ip-addresses, were found to'
                print 'have persist time-out issues on this scan (note: require internet connection)\n'
            print 'ACTIVELY SCANNING, NEW RESULTS WILL BE DISPLAYED.......'
            scannum += 1 #update parameter which indicates a new scanlog has just been printed (count of logs printed)
            #running=0
            Exclud_process,txtfile_err=process_exclude_obtain(Exclud_process,txtfile_err,1) # re-read text-file to see if new excludes added
    except Exception as er2:#If error was experience in main code section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
       running=0  #above (related error is recorded as 'er2') and while loop param (running) set 0 to break scanning
       
###################################################################################################################################
# Code below, is outside of while loop which is only exited due an unexpected error
# [else it should continously run until program is closed]       
try:#If error message (er2) was recorded in main section of code@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    print '' #then print error message er2
    print 'ERROR!!!!'
    print 'the program has stopped due to an unexpected error, this error is'
    print '(most likely python related), the error message is: '
    print er2
except:# otherwise, if er2 not recorded@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    print '' # then tell user unkown error was encountered
    print 'ERROR!!!'
    print 'Program has halted due to an unknown error.....'
print '\nThe program must be closed and reopened if you wish to run it again....'
raw_input('<PRESS ENTER TO EXIT THE PROGRAM>') #wait for user keypress [following which program is finished]