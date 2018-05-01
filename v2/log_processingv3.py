'''
WEEK OF 4/28:
    added graphs + prints grouped to bottom of code

WEEK OF 4/22:
    make get_info_name and get_thread_names faster
    info has two dictionaries --  one for sorting by time, other for retrieving all infos

INFO storage:

{   month:
        day:
            time:
                process:
                    [threads]
}



VVVVVVVVVVV IGNORE

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
[[types], [month, day, year, time]]

This allows entries in ERROR to be searched/sorted by error keywords. Note that error lines are not processed like INFO lines

'''

import sys
from collections import Counter, defaultdict
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='cs160teameggplant', api_key='ILajujL06lsyqJjLjur9')

errors = ['exception', 'WARN ', '[warn]', 'fail', 'unauthorized', 'AUTHORIZATION_FAILURE', 'timeout', 'refused', 'nosuchpageexception', ' 401 ', ' 401\n', ' 500 '] # error
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun':6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec': 12}

# intended for printing
err_categories = {'exception':0, 'warn':0, 'fail':0, 'unauthorized':0, 'AUTHORIZATION_FAILURE':0, 'timeout':0, 'refused':0 , 'nosuchpageexception':0 , '401': 0, '500': 0}

log_file = sys.argv[1]

lines = 0 # counting lines for test purposes
info = 0 # test purposes
error = 0 # test purposes
info_dict = {} #sort by month:day:time:proc_name:[threads]   used for narrowing down by time
info_all_dict = {} # sort by proc_name:[threads]
info_all_proc = [] # just the process names
error_list = [] # [[error types], [month, day, time]] used for narrowing down by time
error_all = [] # list of all errors, includes duplicates
runtime_data = {} # section off runtime by seconds, put error/info statistics in here

list_threads = set() # FOR TESTING; DELETE LATER?
list_names = set() # FOR TESTING; DELETE LATER?

# ================ PARSING FUNCTIONS

def has_error(line):
    line = line.replace('0 connect failure, 0 send limit, 0 transport error', '') # eliminate this as it is not an error
    if any(i in line for i in errors):
        #print(line)
        #print("error found")
        #print(line)
        return True
    else:
        return False

def process_date(line):
    date = line.split(' ')
    date[0] = months[date[0]] # convert month to number
    date[1] = int(date[1])
    #print(date[2])
    return date[0:3] # only the first three elements

# find the components of each usage/info
# return [thread, proc]
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
        #if has_error(line):
        #   process_error_line(line) # if the line has info and error (such as authorization_failure) then the line is saved to both the info and error lists
        return [thread, proc_name, desc]
    elif "INFO " in line: # INFO  org.apache.solr.update.UpdateHandler  – end_commit_flush
        line_split = line.split('INFO')
        thread_name = line_split[0].strip().split(' ')[-1]
        #print(thread_name)
        line_split = line_split[1].split('–')
        proc_name = line_split[0].strip()
        proc_name = proc_name.split('-')[0] # sometimes cannot detect hyphens?
        #desc = ' - '.join(line_split[1:]).strip()
        #print([proc_name, desc])
        if has_error(line):
            process_error_line(line)  # if the line has info and error (such as authorization_failure) then the line is saved to both the info and error lists
        return [thread_name, proc_name]

# find the components of each error
def process_error_line(line):
    error_types = []
    for i in errors:
        if i.lower() in line.lower():
            error_types.append(i.strip())
            error_all.append(i)
    #print(error_types, line)
    return set(error_types)


# ================ TODO: ADD SEARCH FUNCTIONS (search by timeframe, type, etc?)

# param for start/end [mm, dd, hh, mm , ss]
# assumes everything is in chronological order
# returns {process:[thread]}
def info_narrow_by_time(start, end, this_list):
    return_list = dict(this_list)
    if len(start) > 0:
        return_list = info_truncate_from_start(start, return_list)
        print("after start: ")
        print(len(return_list))
    if len(end) > 0:
        return_list = info_truncate_from_end(end, return_list)
        print("after end: ")
        print(len(return_list))
    print(len(return_list))
    if len(return_list) > 0:
        print("printing return list")
        return return_list # returns all proc:[threads]
    else:
        print("printing all infos")
        return info_all_dict

def info_truncate_from_end(end, line_list):
    return_list = {}
    for month in line_list:
        if int(month) <= end[0] or end[0] is None:
            for day in line_list[month]:
                if day <= end[1] or end[1] is None:
                    for time in line_list[month][day]:
                        print(time)
                        timeArr = time.split(':')
                        if int(timeArr[0]) <= end[2] or end[2] is None:
                            if int(timeArr[1]) <= end[3] or end[3] is None:
                                if int(timeArr[2]) <= end[4] or end[4] is None:
                                    #print("adding from end")
                                    for proc in line_list[month][day][time]:
                                        if month not in return_list:
                                            return_list[month] = {}
                                            if day not in return_list:
                                                return_list[month][day] = {}
                                                if time not in return_list[month][day]:
                                                    return_list[month][day][time] = {}
                                                    if proc not in return_list[month][day][time]:
                                                        return_list[month][day][time][proc] = line_list[month][day][time][proc]
    return return_list

def info_truncate_from_start(start, line_list):
    return_list = {}
    for month in line_list:
        if int(month) >= start[0] or start[0] is None:
            for day in line_list[month]:
                if day >= start[1] or start[1] is None:
                    for time in line_list[month][day]:
                        timeArr = time.split(':')
                        if int(timeArr[0]) >= start[2]:
                            if int(timeArr[1]) >= start[3]:
                                if int(timeArr[2]) >= start[4]:
                                    #print("adding from start")
                                    for proc in line_list[month][day][time]:
                                        if month not in return_list:
                                            return_list[month] = {}
                                            if day not in return_list:
                                                return_list[month][day] = {}
                                                if time not in return_list[month][day]:
                                                    return_list[month][day][time] = {}
                                                    if proc not in return_list[month][day][time]:
                                                        return_list[month][day][time][proc] = line_list[month][day][time][proc]
    return return_list

#==================== SEARCH FUNCTIONS AND ANALYTICS

def search_errors_by_keyword(keywords, error_list):
    for line in error_list:
        for k in keywords:
            if k in line:
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
    for proc in info_all_dict:
        results.append(proc)
    return results

#returns duplicates
def get_info_threads():
    results = []
    for proc in info_all_dict:
        results.append(info_all_dict[proc])
    return results

# return top 5, 6, etc recurring names in a list
# param keywords: narrow down by type of name
# param retnum: how many names to return
# param name_list: 1-dimensional array
def get_most(keywords, retnum, name_list):
    new_list = []
    if len(keywords) > 0:
        for n in name_list:
            for k in keywords:
                if k.lower() in n.lower():
                    #print("%s matches %s" % (n, k))
                    new_list.append(n)
    else:
        new_list = name_list
    results = Counter(new_list)
    return results.most_common(retnum)

# dockerservercontroller, volumes, provisions, blueprints
# param proc_dict: sorted by process:[threads]
# return [volume, docker, controller, handler] count
def count_info_by_type(proc_dict):
    dockerservercontroller = 0
    volume = 0
    provision = 0
    blueprint = 0
    handler = 0
    for proc in proc_dict:
        if 'dockerservercontroller' in proc.lower():
            dockerservercontroller = dockerservercontroller + 1
        if 'volume' in proc.lower():
            volume = volume + 1
        if 'provision' in proc.lower():
            provision = provision + 1
        if 'blueprint' in proc.lower():
            blueprint = blueprint + 1
        if 'handler' in proc.lower():
            handler = handler + 1
    return [dockerservercontroller, volume, provision, blueprint, handler]

def count_error_by_type(err_list):
    errCount = dict(Counter(err_list))

    for type in err_categories:
        for typ in errCount:
            if type.lower() in typ.lower():
                err_categories[type] = err_categories[type] + errCount[typ]
    return err_categories

# keywords is a list
def count_totals(keywords, result_list):
    return Counter(result_list)

# ========================================= MAKING THE GRAPH

def makeGraphFromArr(labels, stats):
    data = [go.Bar(
        x = labels,
        y = stats
    )]

def makeGraphFromDict(diction):
    my_plot_div = plot([go.Bar(
        x=list(diction.keys()),
        y=list(diction.values()))],
        output_type='div',show_link=False,include_plotlyjs=False)
    return my_plot_div

# ================ MAIN FILE OPENER


# Specified encoding to 'utf8' so that it works with all the log files
with open(log_file, "r", encoding='utf8') as infile:
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
            info_details = process_info_line(line) # [thread, proc]

            # sort by [month][day][time][proc_name]:[threads]
            # if timeframe given, narrow it down further
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

            # saving to info_all {proc: [threads]}
            if info_details[1] not in info_all_dict:
                info_all_dict[info_details[1]] = []
            info_all_dict[info_details[1]].append(info_details[0])

            # add to total proc names
            info_all_proc.append(info_details[1])

            # if at least one timeframe (start or end) is given, call info_narrow by time on info_dict
            #info_narrow_by_time(start, end, info_dict)


            info = info + 1

        # split line, find error type
        if has_error(line):
            date = process_date(line)
            err_details = process_error_line(line)
            error = error + 1
            error_all.extend(err_details)
            error_list.append([err_details, date])
            #print(err_details);

            #error_line_reader(split_line.split(' '))




        # store error type in date slot


# ================ PRINTING THE OUTPUT

######### TESTING PROCESS RETRIEVAL #######

#print("All processes:")
#info_names = set(get_info_names())
#print(len(info_names))
#print(len(set(get_info_names())))
#all_proc = ""
#for proc in info_names:
#    all_proc = all_proc + proc + "\n"
#print(all_proc)
#print(get_most('',0,get_info_names()))

########## DOCKER/ VOLUME/ CONTROLLER STATS ##########

stats = count_info_by_type(info_all_proc)
total_stats = sum(stats)
dsc = float(stats[0]/total_stats*100.0)
vol = float(stats[1]/total_stats*100.0)
prov = float(stats[2]/total_stats*100.0)
blue = float(stats[3]/total_stats*100.0)
han = float(stats[4]/total_stats*100.0)
total_stats_print = "<h4>DockerServerController usage: %d %% </h4><h4>Volume usage: %d %% </h4><h4>Provision usage: %d %% </h4><h4>Blueprint usage: %d %% </h4><h4>Handler usage: %d %%</h4>" % (dsc, vol, prov, blue, han)

########## RETURNING MOST FREQUENT OCCURENCES + GRAPH ##########

freq_proc_5 = get_most('', 5, info_all_proc)
freq_proc_print = "<h4>Most frequent processes:</h4>"
for proc in freq_proc_5:
    freq_proc_print = freq_proc_print + "<li>- " + str(proc[0]) + ": "+ str(proc[1]) +" occurrences</li>"
freq_proc_10 = dict(get_most('', 10, info_all_proc))
infoGraph = makeGraphFromDict(freq_proc_10) # INFO GRAPH

#print("\nMost frequent processes (docker only): This is just to demonstrate that keywords can be implemented in the search") ## this is just to demonstrate
#print(get_most(['docker'], 5, info_all_proc))

################## ERROR COUNT + GRAPH #############################

error_print = "<h4>Error count: %d </h4><h4>Errors by type: </h4>" % len(error_all)
#print(error_all)
errorsdataset = count_error_by_type(error_all)
errorGraph = makeGraphFromDict(errorsdataset) # ERROR GRAPH

########## TESTING NARROW TIME ##########

#print("Narrow by time:")
#print(info_all_dict.keys())
#time_dict = info_narrow_by_time([8, 21, 6,17,25], [8,21,6,29,16], info_dict) ##NEED TO FIX
#print(time_dict[8][21].keyset())

################### CONCATENATE + PRINT ALL STRINGS

#print("%d unique threadnames, %d unique process names" % (len(list_threads), len(list_names))) ######## FOR TESTING; DELETE LATER
#print("%d lines read\n%d info\n%d errors" % (lines, info, error))
print(total_stats_print)
print(freq_proc_print)
print(infoGraph)
print(error_print)
print(errorGraph)
