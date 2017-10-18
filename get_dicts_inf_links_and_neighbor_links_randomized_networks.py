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



   
    inf_threshold_neg_trans=0.   #min fraction of infected transactions to consider a node or link as infected


    Niter=100

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

    print "reading networks...."

   


    for ii in range(Niter):

      print "iter", ii

      dict_period_num_transactions={}
      dict_period_num_neg_transactions={}
       
      dict_period_list_inf_links={}
       
      dict_period_dict_link_list_neighboring_links={}


      period=initial_period
      while period <= final_period:     

         try:
         ###### i read the actual network structure from the data
          network_filename="../Results/Shuffled_links_networks/Supply_network_slicing_"+slicing+"_period_"+str(period)+"_no_network_metrics_random_"+str(ii)+".pickle"

          G_period = pickle.load(open(network_filename, 'rb'))    


          dict_period_num_transactions[period]=0.
          dict_period_num_neg_transactions[period]=0.
          dict_period_list_inf_links[period]=[]


          dict_period_dict_link_list_neighboring_links[period]={}



          if len(G_period.nodes()) >0 and  len(G_period.edges()) >0:   # there are two empty networks:  Nov and Dec. 1994      

                          
            ############ info coden on links and nodes:
            #print G_period.nodes(data=True)   #example:   (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 2, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0008438954375540839})

            #  print G_period.edges(data=True)  # example: (514603, 2302275, {'pos_weight': 23989, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 1.0, 'link_betweeness': 0.0016097736255839023, 'neg_weight': 0.0})
                               

            for edge in G_period.edges():  
                e1=edge[0]                                 
                e2=edge[1]

              
                dict_period_num_transactions[period] +=1.
                         
                if int(G_period.edge[e1][e2]["num_neg_trans"]) >0:

                    dict_period_num_neg_transactions[period] += 1.

                    if edge not in dict_period_list_inf_links[period]:
                        dict_period_list_inf_links[period].append(edge)



                ####### i get the list of neighboring links of a link (from either side)
                try:
                    dict_period_dict_link_list_neighboring_links[period][edge]
                except KeyError:
                    dict_period_dict_link_list_neighboring_links[period][edge]=[]

                for neighbor in G_period.neighbors(e1):
                    link12=(e1, neighbor)
                    link21=(neighbor, e1)

                    if link12  not in dict_period_dict_link_list_neighboring_links[period][edge]:
                        dict_period_dict_link_list_neighboring_links[period][edge].append(link12)
                    if link21  not in dict_period_dict_link_list_neighboring_links[period][edge]:
                        dict_period_dict_link_list_neighboring_links[period][edge].append(link21)   # i add them both ways, just in case

                for neighbor in G_period.neighbors(e2):
                    link12=(e2, neighbor)
                    link21=(neighbor, e2)

                    if link12  not in dict_period_dict_link_list_neighboring_links[period][edge]:
                        dict_period_dict_link_list_neighboring_links[period][edge].append(link12)
                    if link21  not in dict_period_dict_link_list_neighboring_links[period][edge]:
                        dict_period_dict_link_list_neighboring_links[period][edge].append(link21)   # i add them both ways, just in case





         except IOError: pass  # skip a couple networks missing

         period +=1
         ######### end of current period
      print " done."       



      background_fract_neg_trans={}
      for period in sorted(dict_period_num_neg_transactions):
        try:
            background_fract_neg_trans[period]=dict_period_num_neg_transactions[period] / dict_period_num_transactions[period] 
            
#            print "t:", period, " tot # trans.",dict_period_num_transactions[period], " # neg. trans.:", dict_period_num_neg_transactions[period], " relative fract:",background_fract_neg_trans[period
           # print period, background_fract_neg_trans[period]
        except ZeroDivisionError:pass


      pickle_name="../Results/Shuffled_links_networks/dict_periods_background_prob_inf_link_randomized_"+str(ii)+".pickle"
      pickle.dump(background_fract_neg_trans, open(pickle_name, 'wb'))
      print "written pickle for dict of periods, background fraction of inf.:", pickle_name
      
      
      
      pickle_name="../Results/Shuffled_links_networks/dict_periods_list_inf_links_randomized_"+str(ii)+".pickle"
      pickle.dump(dict_period_list_inf_links, open(pickle_name, 'wb'))
      print "written pickle for dict. period, list inf. links:", pickle_name
      
      
      pickle_name="../Results/Shuffled_links_networks/dict_periods_dict_links_list_neighboring_links_randomized_"+str(ii)+".pickle"
      pickle.dump(dict_period_dict_link_list_neighboring_links, open(pickle_name, 'wb'))
      print "written pickle for dict. period, dict links, list inf. links:", pickle_name
      






######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

