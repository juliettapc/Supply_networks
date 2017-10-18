#!/usr/bin/env python

'''
Created by Julia Poncela, on Feb. 2016

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

    slicing="monthly"    #"monthly"  # or "yearly"


    flag_cohort=1  # to only consider firms from the cohort, or every firm


    string_cohort=""
    if flag_cohort==1:
        string_cohort="_cohort_"



    num_periods=253
    ii=0
    while ii <= num_periods:

      ii+=1
      

      try:

        ####  i read pickles for networks

        #network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(ii)+"_.pickle"
        network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(ii)+string_cohort+".pickle"
        G_period = pickle.load(open(network_period, 'rb'))  
        N_period = len(G_period.nodes())
                       
        #network_accumulate_year="../Results/Simplified_supply_network_yearly_acummlate_until_period_"+str(ii)+"_.pickle"
        network_accumulate_year="../Results/Simplified_supply_network_yearly_acummlate_until_period_"+str(ii)+string_cohort+".pickle"
        G = pickle.load(open(network_accumulate_year, 'rb'))  
        
        
        print ii,"N",N_period
        if N_period >0:  # to avoid the couple of empty networks around period 120
            
         
          list_networks=[(network_period,G_period), (network_accumulate_year,G)]          
          
          for tupla in list_networks:

            Gi= tupla[1]
            network_name= tupla[0]

            dict_clustering=nx.clustering(Gi)                   
            dict_betweenness_nodes=nx.betweenness_centrality(Gi)

            max_k=0
            list_k=[]
            for node in Gi.nodes():  
                k=Gi.degree(node)           
                Gi.node[node]["degree"]=k
                list_k.append(k)
                max_k=max(list_k)            
                
                Gi.node[node]["CC"]=dict_clustering[node]            
                Gi.node[node]["betweeness"]= dict_betweenness_nodes[node]            
                                

            dict_betweenness_edges=nx.edge_betweenness_centrality(Gi, normalized=True, weight=None)   # it returns  dictionary of edges (tuplas as keys) with betweenness centrality as the value.   ### i can also calculate the edges' betweenness taking into account their weight!!


            
            for edge in Gi.edges():  
                try:                
                    Gi.edge[edge[0]][edge[1]]["link_betweeness"]=dict_betweenness_edges[edge]                    
                except TypeError:                             
                    Gi.edge[edge[0]][edge[1]]["link_betweeness"]="NA"
                    print "edge",edge, "not found"
                


            for node in Gi.nodes():              
                maximo=1     
                lista=nx.cliques_containing_node(Gi, node) #list of lists,  ej: [[207925, 203592], [207925, 10500761], [207925, 200554], [207925, 202587]]
            
                for elem in lista:               
                    if len(elem) > maximo:
                        maximo=len(elem)      
                Gi.node[node]['max_clique_size']=maximo                                  
            calculate_kshell(Gi, max_k)






            ########  i (over)write pickles for networks including the new attributes
            pickle.dump(Gi, open(network_name, 'wb'))
            print "  written", network_name


      except IOError: pass   # if network pickle not found











#########################################
#########################################


def  calculate_kshell(G, max_k): ####  k-shell decomposition   
        
    #G_for_kshell = remove_self_loops(G)   # there shouldnt be any self loops already
                    

    for node in G.nodes():
        G.node[node]["kshell"]=0


    cont_zeros=0      
    for i in range(max_k):   # k_max is the absolute upper boundary for max kshell index
        kshell= nx.k_shell(G, k=i, core_number=None)  # it returns the k-shell subgraph
        size_shell=len(kshell)
           # print  "    ",i, size_shell, kshell.nodes()
        for node in kshell.nodes():
            G.node[node]["kshell"]=i


        if size_shell==0:
            cont_zeros +=1       
        if cont_zeros >=7:  # to stop calculating shells after a few ones come back empty 
            break



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

