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



    # real data for the infection:  p"../Results/Time_evol_tot_num_infected_links_nodes_GC_monthly_slicing.dat" u 1:3 w lp  3:fract_links,  5:fract_nodes, 6: size Gc of infection



    name1="../Results/Prob_inf_link_for_previously_inf_and_not.dat"
    file1= open(name1, 'wt')       
    
   
    inf_threshold_neg_trans=0.   #min fraction of infected transactions to consider a node or link as infected


    slicing="monthly"    #"monthly"  # or "yearly"

    if slicing =="yearly":
        initial_period=1
        final_period=21
    elif slicing =="monthly":
        initial_period=1
        final_period=252
    else:
        print "wrong slicing"
        exit()




    print "reading dicts...."

    pickle_name="../Results/dict_periods_background_prob_inf_link.pickle"
    dict_period_background_fract_neg_trans = pickle.load(open(pickle_name, 'rb')) 



    pickle_name="../Results/dict_periods_list_inf_links.pickle"
    dict_period_list_inf_links = pickle.load(open(pickle_name, 'rb')) 


    pickle_name="../Results/dict_periods_dict_links_list_neighboring_links.pickle"
    dict_period_dict_link_list_neighboring_links= pickle.load(open(pickle_name, 'rb')) 




    print "reading networks...."

    dict_period_tot_num_trans={}
    dict_period_tot_num_neg_trans={}

    dict_period_num_neg_trans_with_previous_inf_link={}
    dict_period_num_neg_trans_without_previous_inf_link={}


    dict_period_num_neg_trans_with_previous_neighboring_inf_link ={}
    dict_period_num_neg_trans_without_previous_neighboring_inf_link ={}


    period=initial_period
    while period <= final_period:

       # print period

        ###### i read the actual network structure from the data
        network_filename="../Results/Supply_network_slicing_"+slicing+"_period_"+str(period)+"_no_network_metrics.pickle"
        G_period = pickle.load(open(network_filename, 'rb'))    


        dict_period_tot_num_trans[period]=0.
        dict_period_tot_num_neg_trans[period]=0.
        dict_period_num_neg_trans_with_previous_inf_link[period] =0.        
        dict_period_num_neg_trans_without_previous_inf_link[period]  =0.        

        dict_period_num_neg_trans_with_previous_neighboring_inf_link[period] =0.        
        dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]  =0.        


        previous_period=period-1
                  
        if len(G_period.nodes()) >0 and  len(G_period.edges()) >0:   # there are two empty networks:  Nov and Dec. 1994      

                           
            ############ info coden on links and nodes:
            #print G_period.nodes(data=True)   #example:   (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 2, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0008438954375540839})

            #  print G_period.edges(data=True)  # example: (514603, 2302275, {'pos_weight': 23989, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 1.0, 'link_betweeness': 0.0016097736255839023, 'neg_weight': 0.0})
                               

                for edge in G_period.edges():  
                    e1=edge[0]     # the ends of the current link                            
                    e2=edge[1]

                    dict_period_tot_num_trans[period] +=1.

                                                      
                    if int(G_period.edge[e1][e2]["num_neg_trans"]) >0:

                        dict_period_tot_num_neg_trans[period] +=1.

                        if period >1:

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
                                






        period +=1
        ######### end of current period
    print "done."       





   
    for period in sorted(dict_period_tot_num_trans):
      
        try:
            fract_neg_trans=  dict_period_tot_num_neg_trans[period] / dict_period_tot_num_trans[period]
        except ZeroDivisionError:      
            fract_neg_trans= "NA"



        try:
            fract_inf_previously_inf=   dict_period_num_neg_trans_with_previous_inf_link[period] /  dict_period_tot_num_neg_trans[period]# fraction of infected links als infected in the previous time step

            fract_inf_previously_inf_norm_by_all= dict_period_num_neg_trans_with_previous_inf_link[period] /  dict_period_tot_num_trans[period]
        except ZeroDivisionError:           
            fract_inf_previously_inf= "NA"




        try:
            fract_inf_previously_NON_inf=   dict_period_num_neg_trans_without_previous_inf_link[period] /  dict_period_tot_num_neg_trans[period]# fraction of infected links that weren't infected in the previous time step

            fract_inf_previously_NON_inf_norm_by_all= dict_period_num_neg_trans_without_previous_inf_link[period] / dict_period_tot_num_trans[period]
        except ZeroDivisionError:           
            fract_inf_previously_NON_inf= "NA"





        try:
            fract_neg_tr_with_prev_inf_neigh =   dict_period_num_neg_trans_with_previous_neighboring_inf_link[period]   /  dict_period_tot_num_neg_trans[period]

            fract_neg_tr_with_prev_inf_neigh_norm_by_all =  dict_period_num_neg_trans_with_previous_neighboring_inf_link[period]   /  dict_period_tot_num_trans[period]

        except ZeroDivisionError:    
            fract_neg_tr_with_prev_inf_neigh = "NA"





        try:
            fract_neg_tr_without_prev_inf_neigh =   dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]   /  dict_period_tot_num_neg_trans[period]

            fract_neg_tr_without_prev_inf_neigh_norm_by_all =  dict_period_num_neg_trans_without_previous_neighboring_inf_link[period]   /  dict_period_tot_num_trans[period]

        except ZeroDivisionError:    
            fract_neg_tr_without_prev_inf_neigh = "NA"

             
        print >> file1, period, fract_neg_trans, fract_inf_previously_inf, fract_inf_previously_inf_norm_by_all, fract_inf_previously_NON_inf, fract_inf_previously_NON_inf_norm_by_all, fract_inf_previously_inf + fract_inf_previously_NON_inf,  fract_neg_tr_with_prev_inf_neigh, fract_neg_tr_with_prev_inf_neigh_norm_by_all, fract_neg_tr_without_prev_inf_neigh, fract_neg_tr_without_prev_inf_neigh_norm_by_all, fract_neg_tr_with_prev_inf_neigh + fract_neg_tr_without_prev_inf_neigh


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

