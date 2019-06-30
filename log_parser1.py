# -*- coding: utf-8 -*-
"""
Created on Thu May 30 09:42:15 2019

@author: Aneeshaa11
"""

import sys
import re
import datetime
import json 
import collections


def get_parts_of_log(line):
    split_line = line.split()
    match = re.search(r'(\d+/\d+/\d+)',str(split_line)) # search for date format
    d = datetime.datetime.strptime(str(match.group(1)),"%d/%m/%Y") #get month
    y = d.year
    lang = split_line[6].split('/')[1]
    #print(lang)
 
    return {'month': d.strftime("%B"), # get name of month corresponding to number
            'apache_status': split_line[8],
            'data':split_line[-1],
            'year': y,
            'language': lang
            }

def log_parser(directory,output_path):
    log_dict ={}
    #data_dict ={}

    infile = open(directory, 'r')

    for line in infile:
        line_dict = get_parts_of_log(line)
        
        # add entry if doesn't exist already
        if not(log_dict.__contains__(line_dict['year'])):
            log_dict[line_dict['year']] = {}
            
        if not(log_dict[line_dict['year']].__contains__(line_dict['month'])):
            log_dict[line_dict['year']][line_dict['month']] = {'non_ascii': 0,'total':0,'success':0,'percent':0,'language':{}}
        
        if line_dict['language'] not in log_dict[line_dict['year']][line_dict['month']]['language']:
            log_dict[line_dict['year']][line_dict['month']]['language'][line_dict['language']]={'mean_MB':0,'stddev_MB':0,'total_GB':0}
        else:
 
            log_dict[line_dict['year']][line_dict['month']]['language'][line_dict['language']]['total_GB'] += int(line_dict['data'])
            log_dict[line_dict['year']][line_dict['month']]['language'][line_dict['language']]['mean_MB'] += int(line_dict['data'])
        
        # encoding unicode into ascii fails. use that exception to count number of nonascii filenames
        try:
            line.encode('ascii')
        except UnicodeEncodeError:
            log_dict[line_dict['year']][line_dict['month']]['non_ascii'] += 1  
        
        #success codes are 2xx, count how many start with 2
        if line_dict['apache_status'].startswith('2'):
            log_dict[line_dict['year']][line_dict['month']]['success'] += 1  
    
        log_dict[line_dict['year']][line_dict['month']]['total'] += 1
        
 
    
    # calculat success %, total_GB,mean_MB
    
    for i,j in log_dict.items():
        for j in log_dict[i].keys():
            log_dict[i][j]['percent'] = log_dict[i][j]['success']/log_dict[i][j]['total'] *100
            for l in log_dict[i][j]['language']:
                log_dict[i][j]['language'][l]['total_GB'] /= float(1<<30)
                log_dict[i][j]['language'][l]['mean_MB'] /= float(1<<20)
                log_dict[i][j]['language'][l]['mean_MB'] /= log_dict[i][j]['total']
            
    
 
    sorted_x=collections.OrderedDict(sorted(log_dict.items(), key=lambda t: t[0]))
 
    
    with open('json_data.json', 'w') as fp:
        json.dump(sorted_x, fp,indent=2)           
        
    
if __name__ == "__main__":

    directory = sys.argv[1]
    output_path = sys.argv[2]
    log_parser(directory ,output_path)