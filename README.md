# Python-program-to-log-process-names-with-establish-ip-address-and-list-ip-physical-location-
<pre>
Note: 
A checkpoint commit has just been made for version 3.. the only difference from the final commit in the
final commit is that comments will be finished for the source code (.py) and hence finalised program description
inside version 3 .exe file .... the funcationality of version 3 has been finalised as commited.

The finalised commit for version3 (including; .exe , .py and 'exclude_process.txt' file)

Furthermore this readme will be updated when the final commit is made.
   - Jamie 22/08/19
<pre />
Program description (VERSION 1 and VERSION 2  [Version 3 description (rough) at the end])#########################  
A Program to log process (tasks) with established (connected) outgoing ip address and list process;  
internal ip, foreign (outgoing ip) , Pid and process name as well as physical location related to outgoing ip address.    
  
This program logs foriegn IP address and related details of any running process-  
that make established connections outside of your computer. 
  
This program performs continous logging and produces information for new  
connections that are made                                            '
The format of the output is:  
 (internal/local ip) || (foriegn ip address) || PID (process ID) || related process  
   
 {in version 2 of the code, physical location (country,state and city name) is printed    
 in the output, if it can be determined.  
   
The scan is continous and only logs unique processes.    
  
Files of this repository are;  
-> ipscan_uniquelogger_version1.py - version 1 [2017] of the code  
-> ipscan_uniquelogger_version2.py - version 2 [2018] of the code  
-> ipscan_uniquelogger_version1.exe - a standalone .exe of ipscan_uniquelogger_version1.py (and related modules)  
-> ipscan_uniquelogger_version2.exe - a standalone .exe of ipscan_uniquelogger_version2.py (and related modules)  
  
The difference of version 2 from version 1 is;  
-> added catch/exception to code such that .exe does not suddenly  
   exit in event of an unexpected error (also prints error message)  
-> using website: http://ip-api.com  
   details about an in ip address is obtained (in csv) by applying, for  
   example of arbitrary ip address '153.177.97.188' the csv output is obtained  
   from reading html output of "http://ip-api.com/csv/153.177.97.188"  
     
   From this html (and hence output csv), can obtain; country/state/city  
   of ip address.  
     
   Other than that, no significant changes from version1  
     
  I won't go into further detail about the code as the  
 .py files have been commented in detail.  
   
 However, I will note that this code (and .exe) has only been tested on limited  
 computers of OS windows7 and windows10; so I am unsure how the code (and .exe)  
 wil behave on other computers and opterating systems [in regard to if there is  
 a difference in used cmd commands (within .py) and their related outputs].  
 ####################################################################################################################  
 <pre>
 Version 3 DESCRIPTION (ROUGH DETAILS [to be update]) @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
The functionality of the code is finalised version 3, the only major changes to be made for the final commit (post-checkpoint commit) is;
 -> add further comments to python code for context (where further contenxt is need or comments missing)
 -> finalise program (text) description in .exe [description is defined in source code (.py) by print functions]
 -> tidy up code [remove anything unsused/redundant]


VERSION 3 follows the same funcationality as Version 2, with the following differences to version 3:

DIFFERENCE BETWEEN VERSION 2 AND VERSION 3 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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

  [few smaller details to note when updading readme in final commit final commit]

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
<pre />
