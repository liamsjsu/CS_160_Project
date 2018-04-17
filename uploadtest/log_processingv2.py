'''

INFO and ERROR can be two separate dictionaries. So far, the script parses each line and takes classifiable components out
of each line (date, time, type, description, etc) but does not yet store them.

INFO can be stored in the following format:
{ processname:
          threadname: {month:
                        day:
                        year:
                        time:
                        description:
        }
    * processname is extracted as proc_name in process_info_line
This allows entries in INFO to be search/sorted by thread or processname.

ERROR can be stored as:
{       types: [keywords defined in the below list 'errors']
        month:
        day:
        year:
        time:
        line:
}
or maybe as a set
[[types], month, day, year, time, line]

This allows entries in ERROR to be searched/sorted by error keywords. Note that error lines are not processed like INFO lines

'''
#TODO: INFO and ERROR entries are not stored in dictionaries yet. Is there a better way to store them?

import sys
from collections import Counter, defaultdict
#import plotly
#plotly.tools.set_credentials_file(username='cs160teameggplant', api_key='ILajujL06lsyqJjLjur9')

errors = ['exception', 'warn', 'WARN ', '[warn]', 'fail', 'unauthorized', 'AUTHORIZATION_FAILURE', 'timeout', 'refused', 'nosuchpageexception', ' 401 ', ' 401\n'] # error
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun':6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec': 12}

log_file = sys.argv[1]

lines = 0 # counting lines for test purposes
info = 0 # test purposes
error = 0 # test purposes
info_dict = {}
info_list = []
error_dict = {}
error_list = []
runtime_data = {} # section off runtime by seconds, put error/info statistics in here

list_threads = set() # FOR TESTING; DELETE LATER?
list_names = set() # FOR TESTING; DELETE LATER?

# ================ PARSING FUNCTIONS

def has_error(line):
    line = line.replace('0 connect failure, 0 send limit, 0 transport error', '') # eliminate this as it is not an error
    if any(i in line.lower() for i in errors):
        #print("error found")
        #print(line)
        return True
    else:
        return False

def process_date(line):
    date = line.split(' ')
    date[0] = months[date[0]] # convert month to number
    #print(date[2])
    return date[0:3] # only the first three elements

# find the components of each usage/info
def process_info_line(line):
    #print(line)
    if "INFO " and " --- " in line: # INFO 1 --- [TaskExecutor-17] ontainerStatusNotificationMessageHandler : Received container status for [1]
        line_split = line.split(' --- ')
        line_split = line_split[1].split(' ')
        #print(line_split)
        thread = line_split[0].strip()
        list_threads.add(thread) ######## FOR TESTING; DELETE LATER
        proc_name = line_split[1].strip()
        list_names.add(proc_name) ######## FOR TESTING; DELETE LATER
        desc = ' '.join(line_split[3:]).strip()
        desc = desc.replace(':','').strip() # get rid of extra colons
        #print([thread, proc_name, desc])
        if has_error(line):
            process_error_line(line) # if the line has info and error (such as authorization_failure) then the line is saved to both the info and error lists
        return [thread, proc_name, desc]
    elif "INFO " in line: # INFO  org.apache.solr.update.UpdateHandler  – end_commit_flush
        line_split = line.split('INFO')
        thread_name = line_split[0].strip().split(' ')[-1]
        #print(thread_name)
        line_split = line_split[1].split('–')
        proc_name = line_split[0].strip()
        desc = ' - '.join(line_split[1:]).strip()
        #print([proc_name, desc])
        if has_error(line):
            process_error_line(line)  # if the line has info and error (such as authorization_failure) then the line is saved to both the info and error lists
        return [thread_name, proc_name, desc]

# find the components of each error
def process_error_line(line):
    error_types = []
    for i in errors:
        if i.lower() in line.lower():
            error_types.append(i.strip());
    #print(error_types, line)
    return [error_types, line]


# ================ TODO: ADD SEARCH FUNCTIONS (search by timeframe, type, etc?)

# param for start/end [mm, dd, yyyy, tt:tt:tt]
def narrow_by_time(start, end, line_list):
    pass

def search_errors_by_keyword(keywords, error_list):
    pass

def search_info_by_name(name, info_dict):
    results = []
    for proc in info_dict:
        #print(proc) ####TESTING
        if name in proc:
            pass # add to results
    return results

def search_info_by_thread(thread, info_dict):
    for proc in info_dict:
        if thread in info_dict[proc]:
            pass #add to results

def get_error_keywords():
    pass

#returns duplicates
def get_info_names():
    results = []
    for month in info_dict:
        for day in info_dict[month]:
            for time in info_dict[month][day]:
                for proc_name in info_dict[month][day][time]:
                    results.append(proc_name)
    return results

#returns duplicates
def get_info_threads():
    results = []
    for month in info_dict:
        for day in info_dict[month]:
            for time in info_dict[month][day]:
                for proc_name in info_dict[month][day][time]:
                    for thread in info_dict[month][day][time][proc_name]:
                        results.append(thread)
    return results

# keywords is a list
def count_totals(keywords, result_list):
    return Counter(result_list)

# ================ MAIN FILE OPENER



with open(log_file, "r") as infile:
    #print("Reading %s\n" % (infile))
    for line in infile:
        lines = lines + 1 # test purposes

        # separate date information ?
        # split_line = line.split('hfvm')

        # if entire line has INFO
        # split line, find info type
        # might be followed by number and dash 1 -
        # might be followed by type
        # send to error processor afterwards
        if "info " in line.lower():
            date = process_date(line)
            info_details = process_info_line(line)

            #sort by [month][day][time][proc_name]:[threads]
            if date[0] not in info_dict:
                #print(date)
                info_dict[date[0]] = {}
            if date[1] not in info_dict[date[0]]:
                info_dict[date[0]][date[1]]={}
                #print(date)
            if date[2] not in info_dict[date[0]][date[1]]:
                #print(date)
                info_dict[date[0]][date[1]][date[2]]={}
            if info_details[1] not in info_dict[date[0]][date[1]][date[2]]:
                info_dict[date[0]][date[1]][date[2]][info_details[1]]=[]
            info_dict[date[0]][date[1]][date[2]][info_details[1]].append(info_details[0])
            #info_list.append(line)
            info = info + 1

        # if entire line has error (do NOT count the lines that have INFO already)
            # split line, find error type
        elif has_error(line):
            date = process_date(line)
            err_details = process_error_line(line)
            error = error + 1
            # print(line);

            #error_line_reader(split_line.split(' '))




        # store error type in date slot


####### FOR TESTING
print("%d unique threadnames<br>%d unique process names<br>" % (len(list_threads), len(list_names))) ######## FOR TESTING; DELETE LATER
print("%d lines read<br>%d info<br>%d errors<br>" % (lines, info, error))
info_names = set(get_info_names())
#all_proc = ""
all_proc = len(info_names)
print("All processes:")
#for proc in info_names:
#    all_proc = all_proc + proc + "\n"
print(all_proc)
