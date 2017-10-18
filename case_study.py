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




    initial_year=1985
    final_year=2005
 
    first_day_history=dt.datetime(1985,1,1)
    last_day_history= dt.datetime(2005,12,31)



    zs_threshold=2.
    string_cohort=""
 
   
    print "reading pickle master dict...."
    dict_micj_dict_dates_aggregate_trans = pickle.load(open("../Results/dict_micj_dict_dates_info_transactions"+string_cohort+".pickle"))                                     # example of dict entry:  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"]
    print "   done"





    print "reading pickle zscore dict...."
    master_dict_year_dict_micj_zscore = pickle.load(open("../Results/dict_year_dict_micj_zscore_error_freq_controlling_year_degree.pickle")) # according to Yifang's randomization of data, preservig year. see Code/read_shuffling_data_add_zscore_to_hazard_file.py  ZSore for how likely it is that a link is infected a given year
    print "   done"



    list_num_trans=[]
    list_lengths=[]
    list_fracc_errors=[]
    for mi_cj in dict_micj_dict_dates_aggregate_trans:

        dicc=sorted(dict_micj_dict_dates_aggregate_trans[mi_cj])  # list of tuples (une per trans. for the current micj)

        flag_zs=0

        num_trans=0

        num_neg=0
        num_pos=0


        for tupla in dict_micj_dict_dates_aggregate_trans[mi_cj]:
           # print tupla,dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]
            # (datetime.datetime(1990, 1, 1, 0, 0), datetime.datetime(1990, 12, 31, 0, 0)) {'accum_num_trans': 0.0, 'cj': 510142, 'tot_neg_gross': 0.0, 'business_asym_ij': 0.7389728642581813, 'MCJ': 1, 'num_trans': 2, 'mi': 2305884, 'length': 365, 'overlap': 1, 'fin_period': 72, 'accum_pos_gross': 0.0, 'num_c_i': 35, 'num_c_j': 0, 'num_j_i': 1, 'num_m_j': 1, 'num_j_j': 0, 'tot_pos_gross': 756021.0, 'year': 1990, 'net_adj_gross': 756021, 'num_m_i': 0, 'p_inf': 0}


            if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['tot_neg_gross'] <0.:
                num_neg +=1
            elif  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['tot_pos_gross'] >0.:
                num_pos +=1



            try:
                fracc_errors=dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['tot_neg_gross'] /dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['tot_pos_gross'] 
                
            except ZeroDivisionError:
                fracc_errors=0.

            list_fracc_errors.append(fracc_errors)

            year=str(dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['year'])

            zs=0.
            try:
                zs= master_dict_year_dict_micj_zscore[year][mi_cj]               

                if zs > 2.0   or zs  <-2.:
                    flag_zs=1
                   
            except KeyError: pass

            num_trans +=dict_micj_dict_dates_aggregate_trans[mi_cj][tupla]['num_trans']




        tupla_dates_first_transaction=dicc[0]
        tupla_dates_last_transaction=dicc[-1]
        transaction_length=(tupla_dates_last_transaction[1]-tupla_dates_first_transaction[0]).days  +1.  

        list_lengths.append(transaction_length)

        #num_trans=float(len(dicc))
        list_num_trans.append(num_trans)


        ##### i select a typical mi_cj
        #if transaction_length <= 270. and transaction_length >= 200. :
        #if num_trans <= 25. and num_trans >= 10. :
        if len(dicc) <= 25 and len(dicc) >= 10 :
                #if flag_zs == 1:

                if num_neg >5  and num_pos >5:
                    print "example of micj with typical(median) life span and avg # trans.:  ", mi_cj, " zs flag:", flag_zs," # entries:", len(dicc)
                    




    print "avg life span for a pair mi_cj:", numpy.mean(list_lengths), "days"    # avg: 475.7   days
    print "median life span for a pair mi_cj:", numpy.median(list_lengths), "days"    # median: 211   days
    print "   max:", max(list_lengths),  " min:", min(list_lengths)    # max: 7091.0  min: 2.0

 



    print
    print 



    print "avg num. trans for a pair mi_cj:", numpy.mean(list_num_trans)   #12.3413188355
    print "median num. trans for a pair mi_cj:", numpy.median(list_num_trans)   # 4.0
    print "   max:", max(list_num_trans),  " min:", min(list_num_trans)    #max: 977  min: 1

 



    print
    print 



    print "avg fract. errors for a pair mi_cj:", numpy.mean(list_fracc_errors) #  -0.0413008322812
    print "median fract. errors for a pair mi_cj:", numpy.median(list_fracc_errors)  #0.0
    print "   max:", max(list_fracc_errors),  " min:", min(list_fracc_errors)    #max: 0.0  min: -1141.4


 


#P_inf	Mi	Cj	Mi_Cj	MCJ	num_trans	start_date_trans	end_date_trans	first_day_trans	last_day_trans	length_trans	period_end	first_date_mi_cj	first_day_mi_cj	net_adj_gross	tot_pos_gross	tot_neg_gross	frac_neg_pos	acumm_pos_gross	accum_num_trans	k_M_fin	k_C_fin	num_M_i	num_C_i	num_J_i	num_M_j	num_C_j	num_J_j	k_M_fin_accum	k_C_fin_accum	artificial_start_date_trans	overlap	year	N	L	CC_m_fin	CC_c_fin	betweenness_m_fin	betweenness_c_fin	max_clique_size_m_fin	max_clique_size_c_fin	kshell_m_fin	kshell_c_fin	p_inf_prev_trans	accum_inf_prev_ij	accum_inf_prev_neighb_i	frac_accum_inf_prev_neighb_i	accum_inf_prev_neighb_j	frac_accum_inf_prev_neighb_j	history_ij	min_dist_i_to_inf	avg_dist_i_to_inf	min_dist_j_to_inf	avg_dist_j_to_inf	degree_asym_ij	business_asym_ij	zs_yearly_error_rate_ij	Dist	zip1	zip2	zs_error_rate_ij_year	zs_error_rate_ij_year_degree


# period_end 12

#num_M_i	23
#num_C_i	24
#num_J_i        25

#num_M_j	26
#num_C_j	27
#num_J_j        28



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
