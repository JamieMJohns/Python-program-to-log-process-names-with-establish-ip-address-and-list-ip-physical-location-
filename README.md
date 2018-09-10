# Python-program-to-log-process-names-with-establish-ip-address-and-list-ip-physical-location-
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
 


