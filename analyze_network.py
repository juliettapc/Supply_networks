#!/usr/bin/env python

'''
Code to read multiple network files (pickle or gml) and do basic analysis

Created by Julia Poncela, January 2016

'''

import pickle
import datetime as dt
import histograma_gral
import histograma_bines_gral
import numpy
from  scipy import stats
import networkx as nx
from random import shuffle


def main():

  

    ####### time window i am currently looking at
    initial_year=85
    final_year=95


    list_network_year_files=[]
    y=initial_year
    while y <= final_year:

        list_network_year_files.append("../Results/Supply_network_year_"+str(y)+".pickle")
        y +=1

    list_network_year_files.append("../Results/Supply_network_85_95.pickle")


    ########## i read input pickle network
  
    for filename in list_network_year_files:  
        G=pickle.load(open(filename, 'rb'))   
        print "\n\nloaded pickle file for the network:", filename
 
        try:
            y=filename.split("year_")[1].split(".pickle")[0]
        except IndexError:
            y=filename.split("network_")[1].split(".pickle")[0]


        N= len(G.nodes())
        L=len(G.edges())       
        print "N:", N,  "L:", L
        


        ####### degree
        print "degrees:"
        
        list_k=[]
        for node in G.nodes():
            #list_k.append(len(G.neighbors(node)))
            list_k.append(G.degree(node))
                        
        print "    <k>:",  numpy.mean(list_k), "+/-", numpy.std(list_k)
        
        path_name_h="../Results/degree_distribution_y"+str(y)+".dat"
        histograma_gral.histogram(list_k, path_name_h)
        
        max_k=max(list_k)        
        print "    max_k:", max_k
        




       ######### weights
        print "weights:" 

        list_w=[]
        for edge in G.edges():
            list_w.append(G.edge[edge[0]][edge[1]]["weight"])

        print "    w:",  numpy.mean(list_w), "+/-", numpy.std(list_w)

        #path_name_h="../Results/weight_distribution_"+str(y)+".dat"
       # histograma_gral.histogram(list_w, path_name_h)
        
        max_w=max(list_w)  
        min_w=min(list_w)  
      
        print "    max_w:", max_w,"    min_w:", min_w



        #########  k-shell decomposition
        print "k-shell structure:"   


         # i need to make a copy and remove the self-loops from that before i can proceed
        G_for_kshell = nx.Graph(G.subgraph(G.nodes()))
        
        list_edges_to_remove=[]
        for edge in G_for_kshell.edges():
            if edge[0] == edge[1]:
                list_edges_to_remove.append(edge)


        for edge in  list_edges_to_remove:
            G_for_kshell.remove_edge(edge[0], edge[1])
            



        cont_zeros=0      
        for i in range(max_k):        
            size_shell=len(nx.k_shell(G_for_kshell, k=i, core_number=None))
            print  "    ",i, size_shell
            
            if size_shell==0:
                cont_zeros +=1
       
            if cont_zeros >=10:
                break




        ######### connected components
        print "connected components:"           
        list_sizes=[]
        for item in  sorted(nx.connected_components(G), key = len, reverse=True):
            list_sizes.append(len(item))
       
        # print "list sizes of connected components:",list_sizes
        path_name_h="../Results/connected_components_distribution_y"+str(y)+".dat"
        histograma_gral.histogram(list_sizes, path_name_h)
























    exit()





















    exit()
















    print 
    print "calculating betweenness centrality..."
    #for item in  nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None):
    dict_betweenness=nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    
    list_betweenness=[]
    for node in G.nodes():
        betw=dict_betweenness[node]       
        list_betweenness.append(betw)

    print  "avg centrality:",  numpy.mean(list_betweenness)


    path_name_h="../Results/betweenness_distribution"+file_info+"_"+name+".dat"
    histograma_bines_gral.histograma_bins_norm(list_betweenness,10, path_name_h)
    



    ##### for comparison with ER and SF, same size
    print "\n\nk-shell structure of the BA synthetic with:"
    p=2.*L/(N*N*(N-1))
    m=2   #int(L/(N*(N-1)))+1
    print "p:",p, " m:", m,"\n"
    graph=nx.barabasi_albert_graph(N, m)#ER_graph=nx.erdos_renyi_graph(N, p)


    #########  k-shell decomposition
    cont_zeros=0   
    for i in range(max_k):        
        size_shell=len(nx.k_shell(graph, k=i, core_number=None))
        print  i, size_shell

        if size_shell==0:
            cont_zeros +=1
       
        if cont_zeros >=10:
            break



 
    ######## I separate into subgraphs for drs with mostly controlled or uncontrolled patients ### to create subgraph :   H = G.subgraph([0,1,2])
  
    G_high_ratio = nx.Graph(G.subgraph(list_high_rate_drs)) # this way i make sure their attributes are indepented from the original!!!!
    G_low_ratio = nx.Graph(G.subgraph(list_low_rate_drs))

    print "Subgraphs:"
    

    gml_filename="../Results/Physician_referral_network_by_dr_rates_HIGH_dates_"+str(initial_date).split(" ")[0]+"_to_"+str(final_date).split(" ")[0]+"_"+num_lines+"lines.gml"
    nx.write_gml(G_high_ratio,gml_filename)
    print "   written:",gml_filename 
    print "   high ratio:  N:",len(G_high_ratio.nodes()), " L:",len(G_high_ratio.edges())
    

    filename_network_pickle="../Results/Physician_referral_network_by_dr_rates_HIGH_dates_"+str(initial_date).split(" ")[0]+"_to_"+str(final_date).split(" ")[0]+"_"+num_lines+"lines.pickle"
    pickle.dump(G_high_ratio, open(filename_network_pickle, 'wb'))
    print "   written", filename_network_pickle

 


    
    gml_filename="../Results/Physician_referral_network_by_dr_rates_LOW_dates_"+str(initial_date).split(" ")[0]+"_to_"+str(final_date).split(" ")[0]+"_"+num_lines+"lines.gml"
    nx.write_gml(G_low_ratio,gml_filename)
    print "   written:",gml_filename 
    print "   low ratio:  N:",len(G_low_ratio.nodes()), " L:",len(G_low_ratio.edges())
  

    filename_network_pickle="../Results/Physician_referral_network_by_dr_rates_LOW_dates_"+str(initial_date).split(" ")[0]+"_to_"+str(final_date).split(" ")[0]+"_"+num_lines+"lines.pickle"
    pickle.dump(G_low_ratio, open(filename_network_pickle, 'wb'))
    print "   written", filename_network_pickle



#######################################
#######################################
#######################################
#######################################


def randomizar_nodes(G, name):


    G_for_random = nx.Graph(G.subgraph(G.nodes()))  # auxiliary copy of the network
   # this way i make sure their attributes are indepented from the original!!!!



    empty=0
    list_dr_ratios=[]
    for node in G_for_random.nodes(data=True):
            #node is a <type 'tuple'>  for example: (1913372578, {'ratio': 1.0})

        list_dr_ratios.append(node[1]["ratio"])
       
        if node[1]["ratio"] == "":
               empty +=1

  #  print "# empty", empty, len(list_dr_ratios)
 #   list_dr_ratios=filter(None, list_dr_ratios)

   # print len(list_dr_ratios)
    #raw_input()

    shuffle(list_dr_ratios)

    cont=0
    for node in G_for_random.nodes():
        #print "  len nodes rand:",len(G_for_random.nodes()), node,  G_for_random.node[node]["ratio"],
        G_for_random.node[node]["ratio"]=list_dr_ratios[cont]
        #print G_for_random.node[node]["ratio"],"  len nodes rand:",len(G_for_random.nodes()), "  len. ratios",len(list_dr_ratios), name
        
        cont +=1
   

    return G_for_random




#######################################
#######################################
#######################################
#######################################

def   count_num_links_types(G,dr_ratio):

    num_links_contr_contr=0.
    num_links_contr_uncontr=0.
    num_links_uncontr_uncontr=0.
    for edge in G.edges(data=True):          

        dr1=edge[0]
        dr2=edge[1]
        
        ratio1 = G.node[dr1]["ratio"]
        ratio2 = G.node[dr2]["ratio"]
        
        
        if ratio1 >= dr_ratio:   # dr1's patients mostly controlled
            if ratio2  >= dr_ratio:
                num_links_contr_contr +=1
            else:
                num_links_contr_uncontr +=1
                
        else: # dr1's patients mostly uncontrolled
            
            if ratio2  >= dr_ratio:
                num_links_contr_uncontr +=1
            else:
                num_links_uncontr_uncontr +=1


    return  num_links_contr_contr,  num_links_contr_uncontr,  num_links_uncontr_uncontr


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

