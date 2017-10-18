#!/usr/bin/env python

'''
Code to read multiple network files (pickle or gml) and do basic analysis

Created by Julia Poncela, May 2016

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

  
    initial_period=1
    final_period=250

    filename3="../Results/Time_evol_network_metrics_monthly___.dat"
    file3 = open(filename3,'wt')
    file3.close()


  #header:  period N L GC avg_degree std_degree max_k avg_pos_w std_pos_w avg_neg_w std_neg_w max_pos_w min_pos_w max_neg_w min_neg_w 
##           1     2 3  4  5            6         7    8          9        10         11       12        13         14        15
#    max_shell  avg_shortest_path max_clique avg_betweenness std_betweenness
#       16        17               18              19           20


    list_network_month_files=[]
    period=initial_period
    while period  <= final_period:

        list_network_month_files.append("../Results/Supply_network_slicing_monthly_period_"+str(period)+"_no_network_metrics.pickle")
        period +=1

    list_network_month_files.append("../Results/Supply_network_1985_2005_no_network_metrics.pickle")



    ########## i read input pickle network
    for filename in list_network_month_files:  
      G=pickle.load(open(filename, 'rb'))  

      if len(G.nodes()) > 1: 
        print "\n\nloaded pickle file for the network:", filename
 
        try:
            period=filename.split("period_")[1].split(".pickle")[0].split("_no_network_metrics")[0]
        except IndexError:
            period=filename.split("Supply_network_")[1].split("_no_network_metrics.pickle")[0]



       # print G.nodes(data=True)
        #raw_input()



        N= len(G.nodes())
        L=len(G.edges())    

        GC = nx.connected_component_subgraphs(G)[0] 

   
        print "period", period
        print "  N:", N,  "L:", L, "GC:", len(GC.nodes())
        



        ####### degree
        print "degrees:"
        
        list_k=[]
        for node in G.nodes():
            #list_k.append(len(G.neighbors(node)))
            list_k.append(G.degree(node))
                        
        avg_degree= numpy.mean(list_k)
        std_degree=numpy.std(list_k)

        print "  <k>:",  avg_degree, "+/-", std_degree

        path_name_h="../Results/degree_distribution_period"+str(period)+".dat"
        histograma_gral.histogram(list_k, path_name_h)
        
        max_k=max(list_k)        
        print "  max_k:", max_k
 



       ######### weights
        print "weights:" 

        list_pos_w=[]
        list_neg_w=[]
        for edge in G.edges():
            list_pos_w.append(G.edge[edge[0]][edge[1]]["pos_weight"])
            list_neg_w.append(-1.*(G.edge[edge[0]][edge[1]]["neg_weight"]))


        avg_pos_w = numpy.mean(list_pos_w)
        std_pos_w = numpy.std(list_pos_w)
            
        print "  pos. weight:",  avg_pos_w, "+/-", std_pos_w
                #        print >> file3, numpy.mean(list_pos_w), numpy.std(list_pos_w),
                
        avg_neg_w = numpy.mean(list_neg_w)
        std_neg_w = numpy.std(list_neg_w)


        print "  neg. weight:",  numpy.mean(list_neg_w), "+/-", numpy.std(list_neg_w)

        path_name_h="../Results/weight_pos_trans_distribution_period"+str(period)+".dat"
        histograma_gral.histogram(list_pos_w, path_name_h)


        path_name_h="../Results/weight_neg_trans_distribution_period"+str(period)+".dat"
        histograma_gral.histogram(list_neg_w, path_name_h)

        
        max_pos_w=max(list_pos_w)  
        min_pos_w=min(list_pos_w)  

        max_neg_w=max(list_neg_w)  
        min_neg_w=min(list_neg_w)  


      
        print "  max_pos_w:", max_pos_w,"    min_pos_w:", min_pos_w
        print "  max_neg_w:", -1.*max_neg_w,"    min_neg_w:", -1.*min_neg_w




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
            


        max_shell=0
        cont_zeros=0      
        for i in range(max_k):        
            size_shell=len(nx.k_shell(G_for_kshell, k=i, core_number=None))
            print  "  ",i, size_shell
            
            if size_shell==0:
                 cont_zeros +=1       
            else:
                 max_shell =i
            if cont_zeros >=10:
               
                break

        print "max shell:", max_shell 





        #########  connected components
        print "connected components:"    
        max_con_comp=0       
        list_sizes=[]
        for item in  sorted(nx.connected_components(G), key = len, reverse=True):
            size=len(item)
            list_sizes.append(size)
            if size >max_con_comp:
                max_con_comp=size


        # print "list sizes of connected components:",list_sizes
        path_name_h="../Results/connected_components_distribution_period"+str(period)+".dat"
        histograma_gral.histogram(list_sizes, path_name_h)

      


        ##########  avg. path lenght
        avg_shortest_path=nx.average_shortest_path_length(GC)
        print "average shortest path within GC:", avg_shortest_path





        ########  max. clique size
        absolute_max=1
        for i in G.nodes():        
       
            maximo=1     
            list2=nx.cliques_containing_node(G, i)
                 # print i, list2
       
            for elem in list2:
                   # print elem,len(elem,)
                if len(elem) > maximo:
                    maximo=len(elem)
                         # print "\n",maximo
            G.node[i]['max_clique_size']=maximo
       
            if absolute_max < maximo:
                absolute_max = maximo
  

        lista=list(nx.find_cliques(G)) # crea una lista de cliques (lista de listas)
        max_clique=nx.graph_clique_number(G)  #finds out max size clique
        num_tot_clique=nx.graph_number_of_cliques(G) #finds out total number of cliques

        print "max. clique size:", max_clique
     



        print "calculating betweenness centrality..."
        #for item in  nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None):
        dict_betweenness=nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
        
        list_betweenness=[]
        for node in G.nodes():
            betw=dict_betweenness[node]       
            list_betweenness.append(betw)
           

        avg_betweenness = numpy.mean(list_betweenness)
        std_betweenness = numpy.std(list_betweenness)

        print  "avg centrality:", avg_betweenness, std_betweenness


        path_name_h="../Results/betweenness_distribution_period"+str(period)+".dat"
        histograma_bines_gral.histograma_bins_norm(list_betweenness,10, path_name_h)
    

        print 
        print 



        file3 = open(filename3,'at')
        print >> file3,  period, N, L, len(GC.nodes()), avg_degree, std_degree, max_k, avg_pos_w, std_pos_w, -1.*avg_neg_w, std_neg_w, max_pos_w, min_pos_w, -1.*max_neg_w, -1.*min_neg_w, max_shell, avg_shortest_path, max_clique, avg_betweenness, std_betweenness

    file3.close()
    print "written:",filename3




######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

