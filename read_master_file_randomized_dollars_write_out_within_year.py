#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept. 2016

'''

import datetime as dt
import csv
import pickle
import histogram_bins_increasing
import histograma_gral
import numpy 
import networkx as nx
import random
import sys
import datetime as dt
import Herfindahl_index
import itertools
import random

def main():

    ####### original file :
    name0="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_monthly_slicing_dropped_overlaps_randomly_from_list.dat"   
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
    next(reader, None)   # to skip the header
    

    ####### new file that will include a randomized value for the dollars field
    new_name="../Results/new_file_rand_within_year.dat"#name0.strip(".dat")+"_added_random_dollars.dat"
    file_new=open(new_name,'wt')




    dict_year_list_p_inf={}
    for list_row in reader:                
        p_inf=int(list_row[0])
        year=int(list_row[36])

        try:
            dict_year_list_p_inf[year]
        except KeyError:
            dict_year_list_p_inf[year]=[]

        dict_year_list_p_inf[year].append(p_inf)



    ####### i reshuffle errors within each year
    for year in  dict_year_list_p_inf:
        #print year, numpy.mean(dict_year_list_p_inf[year])
        random.shuffle(dict_year_list_p_inf[year])
        #print year, numpy.mean(dict_year_list_p_inf[year]),"\n\n"









    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
    next(reader, None)   # to skip the header
    dict_year_cont={}


    dict_micj_list_previous_failures_randomized={}
    for list_row in reader:     # OJO!!!! the original file has been manually sorted: first by micj and then my start_date !!!!!!!

        micj=str(list_row[3])        
        year=int(list_row[36])

        try:
            dict_micj_list_previous_failures_randomized[micj]
        except KeyError:
            dict_micj_list_previous_failures_randomized[micj]=[]


        try:
            dict_year_cont[year]
        except KeyError:
            dict_year_cont[year]=0

       

        num_prev_errors_ij=sum(dict_micj_list_previous_failures_randomized[micj])   # sum of empty list =0


        if len(dict_micj_list_previous_failures_randomized[micj])>0:
            fract_errors_ij=numpy.mean(dict_micj_list_previous_failures_randomized[micj])
        else:
            fract_errors_ij=0.



        for item in list_row:            
            print >> file_new, item,



        cont=dict_year_cont[year]
        p_inf_new=dict_year_list_p_inf[year][cont]

        prev_p_inf=0
        try:
           prev_p_inf= dict_micj_list_previous_failures_randomized[micj][-1]
        except IndexError:pass


        print >> file_new,  p_inf_new, num_prev_errors_ij , fract_errors_ij,prev_p_inf



        #### for next time
        dict_micj_list_previous_failures_randomized[micj].append(p_inf_new)



        dict_year_cont[year] +=1







    file_new.close()
    print "written:", new_name






######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



############################3
#################################
