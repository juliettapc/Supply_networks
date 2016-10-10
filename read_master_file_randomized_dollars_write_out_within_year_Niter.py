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



    Niter=3
    existing=998   # as not to overwrite existing random files

  



    for ii in range(Niter):

        print ii



        ####### original file :
        name0="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_monthly_slicing_dropped_overlaps_randomly_from_list.dat"   
        csvfile=open(name0, 'rb')
        reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
        next(reader, None)   # to skip the header
  




        ####### new file that will include a randomized value for the dollars field
        new_name="../Results/Pinf_vs_mulitiple_variables_pinf_rand"+str(ii+existing)+"_within_year.csv"
        file_new=open(new_name,'wt')



        print >> file_new,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans",  "start_date_trans","start_time_trans", "end_date_trans","end_time_trans", "first_day_trans","last_day_trans",  "length_trans", "period_end",  "first_date_mi_cj", "first_time_mi_cj", "first_day_mi_cj", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "acumm_pos_gross","accum_num_trans","k_M_fin", "k_C_fin", "num_M_i","num_C_i","num_J_i", "num_M_j","num_C_j","num_J_j" ,  "k_M_fin_accum",  "k_C_fin_accum" , "artificial_start_date_trans","artificial_start_time_trans", "overlap", "year", "N", "L", "CC_m_fin","CC_c_fin","betweenness_m_fin","betweenness_c_fin","max_clique_size_m_fin","max_clique_size_c_fin","kshell_m_fin","kshell_c_fin","p_inf_prev_trans","accum_inf_prev_ij", "accum_inf_prev_neighb_i","frac_accum_inf_prev_neighb_i","accum_inf_prev_neighb_j","frac_accum_inf_prev_neighb_j","history_ij", "min_dist_i_to_inf", "avg_dist_i_to_inf", "min_dist_j_to_inf", "avg_dist_j_to_inf", "degree_asym_ij","business_asym_ij","zs_error_rate_ij_year_degree", "Dist","zip1", "zip2", "core_score_year_i", "core_score_year_j","p_inf_rand","num_prev_errors_ij_rand" , "fract_errors_ij_rand","prev_p_inf_rand"
                                     


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
