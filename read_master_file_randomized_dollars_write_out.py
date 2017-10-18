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
    new_name="../Results/new_file.dat"#name0.strip(".dat")+"_added_random_dollars.dat"
    file_new=open(new_name,'wt')




    list_p_inf=[]
    for list_row in reader:                
        p_inf=int(list_row[0])
        list_p_inf.append(p_inf)



    print sum(list_p_inf), numpy.mean(list_p_inf)

    random.shuffle(list_p_inf)


    print sum(list_p_inf), numpy.mean(list_p_inf)






    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
    next(reader, None)   # to skip the header
    cont =0

    dict_micj_list_previous_failures_randomized={}
    for list_row in reader:     # OJO!!!! the original file has been manually sorted: first by micj and then my start_date !!!!!!!


        micj=str(list_row[3])        

        try:
            dict_micj_list_previous_failures_randomized[micj]
        except KeyError:
            dict_micj_list_previous_failures_randomized[micj]=[]



        #print micj, dict_micj_list_previous_failures_randomized[micj]


        num_prev_errors_ij=sum(dict_micj_list_previous_failures_randomized[micj])   # sum of empty list =0

        if len(dict_micj_list_previous_failures_randomized[micj])>0:
            fract_errors_ij=float(sum( dict_micj_list_previous_failures_randomized[micj]))/len(dict_micj_list_previous_failures_randomized[micj])
        else:
            fract_errors_ij=0.



        for item in list_row:            
            print >> file_new, item,


        p_inf_new=list_p_inf[cont]

        prev_p_inf=0
        try:
           prev_p_inf= dict_micj_list_previous_failures_randomized[micj][-1]
        except IndexError:pass


        print >> file_new,  p_inf_new, num_prev_errors_ij , fract_errors_ij,prev_p_inf



        #### for next time
        dict_micj_list_previous_failures_randomized[micj].append(p_inf_new)


        cont +=1








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
