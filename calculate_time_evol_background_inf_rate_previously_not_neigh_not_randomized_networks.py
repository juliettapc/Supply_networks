#!/usr/bin/env python

'''
Created by Julia Poncela, on April 2016

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


def main():




   

    Niter=100



    ######  output file
    name1="../Results/Prob_inf_link_for_previously_inf_and_not_with_randomized_links_"+str(Niter)+"iter.dat"
    file1= open(name1, 'wt')           
    file1.close()


    slicing="monthly"    #"monthly"  # or "yearly"

    if slicing =="yearly":
        initial_period=1
        final_period=21
    elif slicing =="monthly":
        initial_period=1
        final_period=250
    else:
        print "wrong slicing"
        exit()




    dict_period_tot_num_trans={}
    dict_period_tot_num_neg_trans={}

    dict_period_num_neg_trans_with_previous_inf_link={}
    dict_period_num_neg_trans_without_previous_inf_link={}


    dict_period_num_neg_trans_with_previous_neighboring_inf_link ={}
    dict_period_num_neg_trans_without_previous_neighboring_inf_link ={}



    for ii in range(Niter):

       print ii
       pickle_name="../Results/Shuffled_links_networks/dict_periods_list_inf_links_randomized_"+str(ii)+".pickle"
       dict_period_list_inf_links = pickle.load(open(pickle_name, 'rb')) 
          
          
       pickle_name="../Results/Shuffled_links_networks/dict_periods_dict_links_list_neighboring_links_randomized_"+str(ii)+".pickle"
       dict_period_dict_link_list_neighboring_links= pickle.load(open(pickle_name, 'rb')) 
          



       period=initial_period
       while period <= final_period:
           try:
               print " ", period
               dict_period_tot_num_trans[period]=0.
               dict_period_tot_num_neg_trans[period]=0.
               dict_period_num_neg_trans_with_previous_inf_link[period] =0.        
               dict_period_num_neg_trans_without_previous_inf_link[period]  =0.        
               
               dict_period_num_neg_trans_with_previous_neighboring_inf_link[period] =0.        
               dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]  =0.        
               
               previous_period=period-1
               
               
               ###### i read the actual network structure from the data
               rand_network_filename="../Results/Shuffled_links_networks/Supply_network_slicing_"+slicing+"_period_"+str(period)+"_no_network_metrics_random_"+str(ii)+".pickle"
               
               G_period = pickle.load(open(rand_network_filename, 'rb'))    
               
               
               for edge in G_period.edges():  
                   e1=edge[0]     # the ends of the current link                            
                   e2=edge[1]
                   
                   dict_period_tot_num_trans[period] +=1.
                   
                   if int(G_period.edge[e1][e2]["num_neg_trans"]) >0:

                        dict_period_tot_num_neg_trans[period] +=1.

                        if period >1:

                            try:
                                dict_period_list_inf_links[previous_period]
                            except KeyError:# to skip missing networks  119 and 120
                                previous_period = 118
                              



                            if edge in dict_period_list_inf_links[previous_period]:         
                                dict_period_num_neg_trans_with_previous_inf_link[period] +=1.
                            else:
                                dict_period_num_neg_trans_without_previous_inf_link[period] +=1.
                          

                            ###### i check all neighboring links of the current link
                            flag_inf_neigh=0
                            for neighboring_link in dict_period_dict_link_list_neighboring_links[period][edge]:
                                neighboring_e1 = neighboring_link[0]  # the ends of the neighboring link
                                neighboring_e2 = neighboring_link[1]
                                
                                same_link=(neighboring_e2, neighboring_e1)
                                if (neighboring_link in dict_period_list_inf_links[previous_period])  or (same_link in dict_period_list_inf_links[previous_period]):      
                                    
                                    if (neighboring_e1 == e1 and  neighboring_e2 == e2): # i dont wanna include the current link as one of the neighboring links                                       
                                        pass

                                    elif (neighboring_e2 == e1 and  neighboring_e1 == e2 ) :  # i dont wanna include the current link as one of the neighboring links                                       
                                        pass
                                    else:
                                        flag_inf_neigh=1




                            if flag_inf_neigh==1:
                                dict_period_num_neg_trans_with_previous_neighboring_inf_link[period]  +=1.
                            else:
                                dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]   +=1.     
                                



           except IOError: pass 

           period +=1

  
      
    for period in dict_period_tot_num_neg_trans:

          try:
              fract_neg_trans=  dict_period_tot_num_neg_trans[period] / dict_period_tot_num_trans[period]
          except ZeroDivisionError:      
              fract_neg_trans= "NA"




          try:
              fract_inf_previously_inf= dict_period_num_neg_trans_with_previous_inf_link[period] /  dict_period_tot_num_neg_trans[period]#dict_period_tot_num_trans[period]
              
              fract_inf_previously_inf_norm_by_all= dict_period_num_neg_trans_with_previous_inf_link[period] /  dict_period_tot_num_trans[period]
          except ZeroDivisionError:           
              fract_inf_previously_inf= "NA"


          try:
              fract_inf_previously_NON_inf= dict_period_num_neg_trans_without_previous_inf_link[period] /  dict_period_tot_num_neg_trans[period]#dict_period_tot_num_trans[period]

              fract_inf_previously_NON_inf_norm_by_all= dict_period_num_neg_trans_without_previous_inf_link[period] / dict_period_tot_num_trans[period]
          except ZeroDivisionError:           
              fract_inf_previously_NON_inf= "NA"



          try:
              fract_neg_tr_with_prev_inf_neigh =  dict_period_num_neg_trans_with_previous_neighboring_inf_link[period]   /  dict_period_tot_num_neg_trans[period]

              fract_neg_tr_with_prev_inf_neigh_norm_by_all =  dict_period_num_neg_trans_with_previous_neighboring_inf_link[period]   /  dict_period_tot_num_trans[period]

          except ZeroDivisionError:    
              fract_neg_tr_with_prev_inf_neigh = "NA"



          try:
              fract_neg_tr_without_prev_inf_neigh =  dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]   /  dict_period_tot_num_neg_trans[period]

              fract_neg_tr_without_prev_inf_neigh_norm_by_all =  dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]   /  dict_period_tot_num_trans[period]

          except ZeroDivisionError:    
              fract_neg_tr_without_prev_inf_neigh = "NA"





          file1= open(name1, 'at')           
          print >> file1, period, fract_neg_trans, fract_inf_previously_inf, fract_inf_previously_inf_norm_by_all, fract_inf_previously_NON_inf, fract_inf_previously_NON_inf_norm_by_all, fract_inf_previously_inf + fract_inf_previously_NON_inf,  fract_neg_tr_with_prev_inf_neigh, fract_neg_tr_with_prev_inf_neigh_norm_by_all, fract_neg_tr_without_prev_inf_neigh, fract_neg_tr_without_prev_inf_neigh_norm_by_all, fract_neg_tr_with_prev_inf_neigh + fract_neg_tr_without_prev_inf_neigh
          file1.close()



          print  period, fract_neg_trans, fract_inf_previously_inf, fract_inf_previously_inf_norm_by_all, fract_inf_previously_NON_inf, fract_inf_previously_NON_inf_norm_by_all, fract_inf_previously_inf + fract_inf_previously_NON_inf,  fract_neg_tr_with_prev_inf_neigh, fract_neg_tr_with_prev_inf_neigh_norm_by_all, fract_neg_tr_without_prev_inf_neigh, fract_neg_tr_without_prev_inf_neigh_norm_by_all, fract_neg_tr_with_prev_inf_neigh + fract_neg_tr_without_prev_inf_neigh




      

    file1.close()
    print "writen:", name1
       
      





######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

