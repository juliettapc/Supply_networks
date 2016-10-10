#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept. 2016

'''

import datetime as dt
import csv
import pickle
import histogram_bins_increasing
import histograma_bines_gral
import histograma_gral
import numpy 
import networkx as nx
import random
import sys
import datetime as dt
import Herfindahl_index
import itertools
import random
import operator



def main():




##  ONLY MANUFACTURERS:
#list high core score nodes: [100389, 101047, 101059, 102817, 105338, 106483, 112604, 116191, 117201, 151853, 152146, 153443, 201789, 207639, 260599, 504506, 507787, 508861, 700198, 2000398, 2003685, 2100265, 2302780, 2305884, 2312359, 2314526, 2322791, 2322894, 2325081, 2366131, 2391375, 6203152, 6203279, 10500321]


#list low core score nodes: [101722, 105491, 105764, 107141, 107578, 109861, 109964, 110671, 112057, 113827, 114030, 115307, 115411, 115769, 116270, 116348, 116749, 117080, 120042, 150198, 150460, 150502, 150851, 200323, 203592, 260174, 260290, 501803, 2001937, 2003341, 2300151, 2300205, 2300783, 2301325, 2301805, 2301994, 2302408, 2302639, 2302640, 2303474, 2303528, 2303701, 2303711, 2304284, 2305069, 2305197, 2305811, 2306487, 2306529, 2306670, 2307182, 2307261, 2307364, 2308770, 2314770, 2315993, 2317451, 2320216, 2321506, 2323709, 2362922, 2363380, 2390206, 2390590, 2393591, 2394169, 2395320, 2701078, 6203620, 10500175, 10500527, 10500576, 10500621, 10503450, 12200420, 12201953, 12202213, 12203421, 20593568]




    focus_node=str(2303701)

    


    dict_id_list_scores={}
    dict_id_list_degrees={}

    threshold_high_core_score=.75
    threshold_low_core_score=.5

    dict_year_dict_firmID_core_score={}

    list_m_high_core_scores=[]
    list_m_low_core_scores=[]

    zs_threshold=2.
    string_cohort=""
    slicing="monthly"  
   
    max_period=250


    list_time_cuts=[]
    dict_index_tuple_times={}
    ii=1
    time_window=12   # months to observe core-fluctuating layer
    aux=0
    while aux <= max_period:
        tupla=(aux+1, aux +time_window)
        list_time_cuts.append(tupla)
        aux += time_window

        dict_index_tuple_times[ii]=tupla
        ii +=1


         
    year= 1984
    for ii in sorted(dict_index_tuple_times): 

        dict_node_months_present_over_time_window={}   # it can be smaller than time-window! (i use it to norm. the core score)       
        dict_node_dict_neigh_times_with_each={}   # number of distinct neighbors over the time window (of 12 months)      


        list_core_scores=[]
        print 

        cont_periods_aux=dict_index_tuple_times[ii][0]-1
        max_period=dict_index_tuple_times[ii][1]


        year +=1
        dict_year_dict_firmID_core_score[year]={}

        while  cont_periods_aux < max_period: 
            
           
           cont_periods_aux +=1
           

           network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(cont_periods_aux)+string_cohort+"_.pickle"
           G_period = pickle.load(open(network_period, 'rb'))  
            
            
           for node in G_period.nodes():
                

             #if G_period.node[node]["type"]=="manuf":


                try:
                     dict_id_list_scores[node]
                     dict_id_list_degrees[node]
                except KeyError:
                     dict_id_list_scores[node]=[]
                     dict_id_list_degrees[node]=[]


                try:
                    dict_node_dict_neigh_times_with_each[node]
                except KeyError:
                    dict_node_dict_neigh_times_with_each[node]={}


                try:
                    dict_node_months_present_over_time_window[node] +=1.
                except KeyError:
                    dict_node_months_present_over_time_window[node] =1.




                for neigh in G_period.neighbors(node): 

                    try:
                        dict_node_dict_neigh_times_with_each[node][neigh] +=1.
                    except KeyError:
                        dict_node_dict_neigh_times_with_each[node][neigh] =1.

                      


                #if str(node)  == focus_node:


                   # print "\nt:",cont_periods_aux, "  node:",node, "k:",G_period.degree(node), " tot. # diff. partners so far in time window:", len(dict_node_dict_neigh_times_with_each[node])    #G_period.node[node]["type"], G_period.node[node]['num_m'], G_period.node[node]['num_c'], G_period.node[node]['num_j']
                    
                    
                    #sorted_x = sorted(dict_node_dict_neigh_times_with_each[node].items(), key=operator.itemgetter(1))
                    
                  
                    
                    #for item in sorted_x:
                       # print item




        ############ i get the core score for each node  for the current time window
        for node in dict_node_dict_neigh_times_with_each:
            #if str(node)  == focus_node:  
                core_score=0.
                for neigh in dict_node_dict_neigh_times_with_each[node]:
                    core_score += dict_node_dict_neigh_times_with_each[node][neigh]                   
                core_score = core_score/(len(dict_node_dict_neigh_times_with_each[node])*dict_node_months_present_over_time_window[node])

                    
                #print "core score:", core_score  #, "  min. 1/all_k:", 1./time_window#len(dict_node_dict_neigh_times_with_each[node])

              

                list_core_scores.append(core_score)

                dict_year_dict_firmID_core_score[year][node]=core_score

                dict_id_list_scores[node].append(core_score)
                dict_id_list_degrees[node].append(float(len(dict_node_dict_neigh_times_with_each[node])))





        #raw_input()



    for node in dict_id_list_scores:
        
        
        avg_score=numpy.mean(dict_id_list_scores[node])
        avg_k=numpy.mean(dict_id_list_degrees[node])


        if avg_score > threshold_high_core_score  and avg_k >5.:
            list_m_high_core_scores.append(node)
        elif  avg_score < threshold_low_core_score  and  avg_k > 5:
            list_m_low_core_scores.append(node)
            


       # Nbins=50
        #name_h="../Results/histogram_core_score_period"+str(cont_periods_aux)+".dat"
        #histogram_bins_increasing.histogram(list_core_scores,Nbins, name_h)
        #histograma_bines_gral.histograma_bins_norm(list_core_scores,Nbins, name_h)


   
    #list1=sorted(list(set(list_m_high_core_scores)))
        
    #print "list high core score nodes:", list1

    #print 

    #list2=sorted(list(set(list_m_low_core_scores)))
    #print "list low core score nodes:", list2




    pickle_name="../Results/dict_year_dict_firmID_core_score.pickle"   # firm id is an int and so is year!!
    pickle.dump(dict_year_dict_firmID_core_score, open(pickle_name, 'wb'))

    print "written:",pickle_name

    list_firms=[]
    for year in sorted(dict_year_dict_firmID_core_score):
       
        for firm_id in dict_year_dict_firmID_core_score[year]:
            print year,type(year)," " , firm_id,type(firm_id),dict_year_dict_firmID_core_score[year][firm_id] 
            if firm_id not in list_firms:
                list_firms.append(firm_id)
        raw_input()
    print "# firms in dict:",len(list_firms)

       








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
