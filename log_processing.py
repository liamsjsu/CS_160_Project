import sys
import csv

'''
to do:
look into argparse later (QoL)

how to run:
python log_processing.py syslogClassShare.5 sess_rel

requirements:
https://docs.google.com/viewer?a=v&pid=forums&srcid=MTYxMjQ4NDg1NzIwMDk1MDMzMzQBMTYyNTIxNjYyMzM3MjUzNjAzMzYBUlE2Wm54b2pBUUFKATAuMQEBdjI&authuser=0
'''
errors = ['excepion', 'warn', 'error', 'fail', 'unauthorized', 'timeout', 'refused', 'nosuchpageexception']#, '404', '401', '500']

def req_rel(): # request reliability
    num_rows = 0
    num_errors = 0

    for line in reader:
        line = line[0]
        num_rows += 1
        error_found = False
        for error in errors: # checks data value for each error word in the list
            if error in line.lower():
                error_found = True
                break # error found, no need to check for other error words
        if error_found:
            num_errors += 1
    print('% errors: ', end='')
    return num_errors/num_rows

def sess_rel(): # session reliability
    error_found = False
    total_sessions = 0
    sessions_with_error = 0

    for line in reader:
        line = line[0]
        if 'sessionid' in line.lower():
            total_sessions += 1
            if error_found:
                sessions_with_error += 1
            error_found = False
        else:
            if error_found:
                continue # error already found in session, keep going until next session
            for error in errors:
                if error in line.lower():
                    error_found = True
                    break # no need to check for other errors in the same line
    print(session_length)
    print('total sessions:',total_sessions,'\nsessions with error:',sessions_with_error)
    print('session reliability: ', end='')
    return (total_sessions - sessions_with_error) / total_sessions


def mtff(): # mean transactions to first failure
    pass

def term_fail_prob(): # terminal failure probability
    pass

def avg_sess_len_req(): # average session length (requests)
    pass

def avg_sess_len_byte(): # average session length (bytes)
    pass

def avg_sess_len_time(): # average session length (time)
    pass



log_file = sys.argv[1]
infile = open(log_file)
reader = csv.reader(infile)

test_type = sys.argv[2]
print('{:.2%}'.format(eval(test_type + '()'))) # should probably change the eval() later