# %%
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:38:28 2017

@author: Jamie Johns
Program to log process (tasks) with established (connected)
outgoing ip address and list their;
internal ip, foreign (outgoing ip) , Pid and process name

logging of a new process is performed on basis that it's
PID or process name is unique to previously printed logs

"""
# KEEP AN EYE ON IP TRAFFIC
import re #import module which provides support for "regular expressions" used to obtain column data from cmd output
import os #operating system module - allows for execution of cmd commands in python code (and obtain output)
import datetime #imports module used to obtain exact (current) date and time
import subprocess # module allows to spawn multiple (cmd) outputs and connect input/output values and obtain return code


os.system('color C')  #set text color to bright red [only works in final produced .exe (cmd type prompt)]
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '$$$$$$$$$$$$$$$$$$$$$  IP TRAFFIC LOGGER $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '                     Program Created by Jamie Johns                    '
print '                              2017                                     '
print '                          version 1.00                                 '
print ' [code created in python 2.7 and then converted to .exe using pyinstaller]'
print 'This program logs foriegn IP address and related details of any proces-'
print 'that make established connections outside of your computer.            '
print '\n'
print 'This program performs continous logging and produces information for new'
print 'connections that are made.                                             '
print 'The format of the output is: '
print '(internal/local ip) || (foriegn ip address) || PID (process ID) || related process'
print '\n'
print 'The scan is continous and only logs unique processes'
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print '\n\n'
nothin=raw_input('<Press enter to start scanning>') #wait for user input
running=1 #parameter which controls below while loop 
scannum=1 #parameter which counts how many scan logs have been printed
PID_LIST=[] #list of PID (related to running task) which have been listed in a scan log
PROCESS_LIST=[] # list of processes (by image name, i.e "chrome.exe) which have been listed in at least one scan log
# MAIN SECTION OF CODE [CONTINOUS SCANNING] ####################################################################################
while running == 1: #Continous scanning of outgoing/ingoing ip related to running processes [whilst running=1]   
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
        print ' Internal IP || Foreign IP || PID || Process name' #header names of printed data
        for x in nw: #for each element of list of newly establish (connect) process to be logged
            print x[1]+' || '+x[2]+' || '+x[3]+' || '+x[4]   
            #(above) print; Internal IP + Foreign IP + PID + Process name 
        print '######################################################################\n'
        print 'ACTIVELY SCANNING, NEW RESULTS WILL BE DISPLAYED.......'
        scannum += 1 #update parameter which indicates a new scanlog has just been printed (count of logs printed)
    #[return to beggining of while loop to perform new scans]