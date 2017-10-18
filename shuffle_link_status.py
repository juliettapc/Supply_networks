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

  
    period=initial_period
    while period <= final_period:

        print period

        ###### i read the actual network structure from the data
        network_filename="../Results/Supply_network_slicing_"+slicing+"_period_"+str(period)+"_no_network_metrics.pickle"
        G_period = pickle.load(open(network_filename, 'rb'))    

        

                
            ############ info coden on links and nodes:
        #print G_period.nodes(data=True)   #example:   (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 2, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0008438954375540839})

      #  print G_period.edges(data=True)  # example: (514603, 2302275, {'pos_weight': 23989, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 1.0, 'link_betweeness': 0.0016097736255839023, 'neg_weight': 0.0})
         


        if len(G_period.nodes()) >0 and  len(G_period.edges()) >0:   # there are two empty networks:  Nov and Dec. 1994      

            for ii in range(Niter):
                                 
                print "  ", ii
                #### i collect all the link values (num neg. trans) for reshuffling later
                list_dict_links=[]
                for edge in G_period.edges():  
                    e1=edge[0]     # the ends of the current link                            
                    e2=edge[1]
                
                    dict_link={}
                    dict_link["pos_weight"]=G_period.edge[e1][e2]["pos_weight"]
                    dict_link["num_neg_trans"]=G_period.edge[e1][e2]["num_neg_trans"]
                    dict_link["fract_neg_trans"]=G_period.edge[e1][e2]["fract_neg_trans"]
                    dict_link["num_pos_trans"]=G_period.edge[e1][e2]["num_pos_trans"]
                    dict_link["neg_weight"]=G_period.edge[e1][e2]["neg_weight"]
                    
                    list_dict_links.append(dict_link)   # i preserve coherently all link's attributes for the randomization
                    

                H_period_aux=nx.Graph()  # to make sure i clear the previous one
                H_period_aux = G_period.copy()   # make a copy to randomized its link attributes
    
                for edge in H_period_aux.edges():  
                    e1=edge[0]   
                    e2=edge[1]

                    random_dict=random.choice(list_dict_links)

                    # i rewrite link attributes with randomized values from the same network
                    H_period_aux.edge[e1][e2]["pos_weight"]=random_dict["pos_weight"]
                    H_period_aux.edge[e1][e2]["num_neg_trans"]=random_dict["num_neg_trans"]
                    H_period_aux.edge[e1][e2]["fract_neg_trans"]=random_dict["fract_neg_trans"]
                    H_period_aux.edge[e1][e2]["num_pos_trans"]=random_dict["num_pos_trans"]
                    H_period_aux.edge[e1][e2]["neg_weight"]=random_dict["neg_weight"]


                                
                pickle_name_random_network=network_filename.replace("Results/","Results/Shuffled_links_networks/").replace(".pickle","")+"_random_"+str(ii)+".pickle"
                pickle.dump(H_period_aux, open(pickle_name_random_network, 'wb'))
                print "written:", pickle_name_random_network



        period +=1
        ######### end of current period
  





######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

