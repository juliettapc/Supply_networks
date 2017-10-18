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




   

    Niter=20
    Num_periods=240
    threshold_neg_tran=0.


    ######  output file
    name1="../Results/Time_evol_tot_num_inf_links_nodes_GC_randomized_network_"+str(Niter)+"iter.dat"
    file1= open(name1, 'wt')           
   


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





    for period in range(Num_periods):
        period +=1
      #  print  period        


        list_num_inf_links=[]
        list_num_inf_nodes=[]

        list_fract_inf_links=[]
        list_fract_inf_nodes=[]

        list_GC=[]
        list_L=[]
        list_N=[]

        for ii in range(Niter):            
           # print " ",ii

           


            try:
                       
                ###### i read the randomized  networks
                rand_network_filename="../Results/Shuffled_links_networks/Supply_network_slicing_"+slicing+"_period_"+str(period)+"_no_network_metrics_random_"+str(ii)+".pickle"
               
                G_period = pickle.load(open(rand_network_filename, 'rb'))                   
                H_period_aux = G_period.copy()   # copy to get only the infected links and nodes (for cluster distribution)    


                list_L.append(len(G_period.edges()))
                list_N.append(len(G_period.nodes()))


                num_inf_links=0.
                list_inf_nodes=[]


                for edge in G_period.edges():
            
                    manufacturer=edge[0]
                    contractor=edge[1]

                    ########## infected nodes 
                    if G_period[manufacturer][contractor]['fract_neg_trans'] > threshold_neg_tran:
                        num_inf_links  +=1.                      
                        
                        if manufacturer not in list_inf_nodes:
                            list_inf_nodes.append(manufacturer)
                        if contractor  not in list_inf_nodes:
                            list_inf_nodes.append(contractor)

                    else:  # i remove non-infected links from the aux_graph
                        H_period_aux.remove_edge(manufacturer,contractor)



                try:
                    list_num_inf_links.append(num_inf_links)
                    fract_inf_links = num_inf_links / float(len(G_period.edges()))
                    list_fract_inf_links.append(fract_inf_links)
                        
                    list_num_inf_nodes.append(len(list_inf_nodes))
                    fract_inf_nodes = len(list_inf_nodes) / float(len(G_period.nodes()))
                    list_fract_inf_nodes.append(fract_inf_nodes)

                except ZeroDivisionError:pass  #if empty network
                   

          

                ##### i remove the isolates from aux graph:
                list_to_remove=[]
                for node in H_period_aux.nodes():
                    if H_period_aux.degree(node)==0:
                        list_to_remove.append(node)
                H_period_aux.remove_nodes_from(list_to_remove)
               

          
                try:
                    GC = len(max(nx.connected_component_subgraphs(H_period_aux), key=len))
                    list_GC.append(GC)
                    #print "GC:", GC, "\n"
                except ValueError: 
                    GC="NA"

            except IOError: pass 

        print >> file1, period, numpy.mean(list_num_inf_links),  numpy.mean(list_fract_inf_links), numpy.mean(list_num_inf_nodes),  numpy.mean(list_fract_inf_nodes), numpy.mean(list_GC), numpy.mean(list_L), numpy.mean(list_N)

        print period, numpy.mean(list_num_inf_links),  numpy.mean(list_fract_inf_links), numpy.mean(list_num_inf_nodes),  numpy.mean(list_fract_inf_nodes), numpy.mean(list_GC), numpy.mean(list_L), numpy.mean(list_N)
                
      

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

