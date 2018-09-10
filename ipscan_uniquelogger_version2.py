# %%
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:38:28 2017 (version 1)
Updated on Fri Jun 10 02:00:00 2018 (version 2)

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


@author: Jamie Johns
"""
# KEEP AN EYE ON IP TRAFFIC
import re #import module which provides support for "regular expressions" used to obtain column data from cmd output
import os #operating system module - allows for execution of cmd commands in python code (and obtain output)
import datetime #imports module used to obtain exact (current) date and time
import subprocess # module allows to spawn multiple (cmd) outputs and connect input/output values and obtain return code
import urllib #urllib module is used for reading a website and obtaining it's html code
os.system('color C')  #set text color to bright red [only works in final produced .exe (cmd type prompt)]
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' # Introduction%%%%%%%%%%%%%%%%%%%%%%%%%
print '$$$$$$$$$$$$$$$$$$$$$  IP TRAFFIC LOGGER $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '                     Program Created by Jamie Johns                    '
print '                              2018                                   '
print '                          version 2.00                                 '
print ' [code created in python 2.7 and then converted to .exe using pyinstaller]'
print 'This program logs foriegn IP address and related details of any proces-'
print 'that make established connections outside of your computer.            '
print '\n'
print 'This program performs continous logging and produces information for new'
print 'connections that are made.                                             '
print 'The format of the output is: '
print '(internal/local ip) || (foriegn ip address) || PID (process ID) || related process'
print 'In addition, a country,state and city is provided for each foriegn Ip address'
print '\n'
print 'The scan is continous and only logs unique processes'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print '\n\n'
nothin=raw_input('<Press enter to start scanning>') #wait for user input
running=1 #parameter which controls below while loop 
scannum=1 #parameter which counts how many scan logs have been printed
PID_LIST=[] #list of PID (related to running task) which have been listed in a scan log
PROCESS_LIST=[] # list of processes (by image name, i.e "chrome.exe) which have been listed in at least one scan log
# MAIN SECTION OF CODE [CONTINOUS SCANNING] ####################################################################################
while running == 1: #Continous scanning of outgoing/ingoing ip related to running processes [whilst running=1]
    try: #Try running main section of code $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
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
            if x[3] not in PID_LIST or x[4] not in PROCESS_LIST: #if this element of r has PID or image name (process name) unique to previously logged establish connecitons
                nw.append(x) #append to list of unique establish process
                PID_LIST.append(x[3]) #add PID to list of all unique PID (with established connection)
                PROCESS_LIST.append(x[4]) #add image (process) name to list of all unique process name(with established connection)
                newscan=1 #set newscan parameter to 1 to indicate a new printout of at least one unique established process will be printed
        if newscan == 1: #if new scan =1 [if newscan=0, no new log is to printed and "while loop" starts again with new scan]
            print 'Scan number '+str(scannum)+'##########################################' #indicate number scan log being printed
            print ' time performed: '+str(now)+'\n'   #indicate time that this scan was performed at (will be give or take ~10 seconds)
            print ' Internal IP || Foreign IP (country,state;city) || PID || Process name' #header names of printed data
            for x in nw: #for each element of list of newly establish (connect) process to be logged
                    try: #try to obtain country,state,city of outgoing (foriegn) ip address [if error, go to "catch"]               
                        ip_details=urllib.urlopen('http://ip-api.com/csv/'+x[2]).read().split(',') #read html of ip details from website
                        country=ip_details[1] #record country name related to foreign ip address
                        state=ip_details[3] #record state name related to foreign ip address
                        city=ip_details[5] #record city name related to foreign ip address
                    except: #if error with recording details of interest in "try:"
                        if x[2] in '127.0.0.1': #assess wether "foreign" ip is just local (internal) ip address
                            country='local_host' #set "country name"
                            state='[internal]' #set "sity name"
                            city='' #leave city name blank
                        else: #else if country,state,city could not be obtain (for other circumstances)
                            country='N/A' #set country name to 'N/A' ('Not available)
                            state='' #leave state name blank
                            city='' #leave city name blank
                    print x[1]+' || '+x[2]+'('+country+','+state+';'+city+') || '+x[3]+' || '+x[4]
                    #(above) print; Internal IP + Foreign IP (country,state;city) + PID + Process name 
            print '######################################################################\n'
            print 'ACTIVELY SCANNING, NEW RESULTS WILL BE DISPLAYED.......'
            scannum += 1 #update parameter which indicates a new scanlog has just been printed (count of logs printed)
            #running=0
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