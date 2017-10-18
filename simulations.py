#!/usr/bin/env python

'''
Created by Julia Poncela, on April 2016

'''

import datetime as dt
import csv
import histogram_bins_increasing
import histograma_gral
import numpy 
import networkx as nx
import random
import pickle



def main():



    # real data for the infection:  p"../Results/Time_evol_tot_num_infected_links_nodes_GC_monthly_slicing.dat" u 1:3 w lp  3:fract_links,  5:fract_nodes, 6: size Gc of infection



  


    list_prob_spontaneous= [0.05,0.2,0.4,0.6,0.8,1.]#[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]
  
    list_prob_inf=[0.,0.05,0.2,0.4,0.6,0.8,1.]#[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]

    list_prob_recovery=[0.05,0.2,0.4,0.6,0.8,1.]#[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]


   
  #  inf_threshold=0.0   #min fraction of infected transactions to consider a node as infected




    Niter=2      # iterations for a given set of parameters



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


    for  prob_spontaneous in list_prob_spontaneous:
        print "prob_spontaneous:", prob_spontaneous

        for  prob_inf in list_prob_inf:             
            print " prob_inf:", prob_inf

            for  prob_recovery in list_prob_recovery:                
                print "  prob_recovery:", prob_recovery


                ######## output files from the AVG time evol. 
                name2="../Results/Simulations/Avg_time_evol_num_infected_links_and_nodes_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                file2= open(name2, 'wt')



                dict_period_list_sizes_inf_conn_comp={}
                for tt in range(final_period):
                    tt +=1
                    dict_period_list_sizes_inf_conn_comp[tt]=[]


                list_sizes_inf_components_tot=[]
                list_lists_fract_inf_links=[]
                list_lists_fract_inf_nodes=[]     
                list_lists_GC_inf=[]     
               
                for iteration  in range(Niter):
                    print "   iter:", iteration
                                   

                    list_evol_fract_inf_links=[]
                    list_evol_fract_inf_nodes=[]
                    list_evol_fract_GC_inf=[]

                    list_all_nodes=[]
                    period = initial_period
                    dict_node_previous_status={}
                    while period <= final_period:
                        #print "    ",period

                       
                        #### i read the actual network structure from the data                                                
                        network_filename="../Results/Supply_network_slicing_"+slicing+"_period_"+str(period)+".pickle"
                        G_period=pickle.load(open(network_filename, 'rb'))
                      

                        if len(G_period.nodes()) >0 and  len(G_period.edges()) >0:   # there are two empty networks:  Nov and Dec. 1994
                           
                            ###########  i get the nodes infected initially from the data (the rest of the periods, i only simulate the infection)
                            if period ==1:                                                                               

                                for node in G_period.nodes():                                   
                                    dict_node_previous_status[node]="S"       
                                    G_period.node[node]["status"] ="S"    
                            
                                    if G_period.node[node]["fract_neg_transct"] > 0.:  # > inf_threshold:      
                                        dict_node_previous_status[node]="I"
                                        G_period.node[node]["status"] ="I"


                                lista_components=[]
                                fract_inf_links, fract_inf_nodes, GC ,lista_components  = count_inf_links_nodes_GC(G_period)

                                list_sizes_inf_components_tot.extend(lista_components)
                                dict_period_list_sizes_inf_conn_comp[period].extend(lista_components)

                            ########### i simulate the rest of the periods:     
                            else:
                                list_all_nodes= sorted(G_period.nodes())

                                for node in G_period.nodes():     # initialize for the dynamic with the previous status (simulated status if t >1)
                                    try:                     
                                        G_period.node[node]["status"] =dict_node_previous_status[node]   
                                    except KeyError:
                                        G_period.node[node]["status"] ="S"  # if the node was not present in the previous period


                                ##### one step of the infection dynamics, then spontanous, then recount                     
                                infection_dyn(G_period, dict_node_previous_status, prob_inf, prob_recovery)
                                spontaneous_dyn(G_period, dict_node_previous_status, prob_spontaneous)
                               
                                lista_components=[]
                                fract_inf_links, fract_inf_nodes, GC ,lista_components  = count_inf_links_nodes_GC(G_period)

                                list_sizes_inf_components_tot.extend(lista_components)
                                dict_period_list_sizes_inf_conn_comp[period].extend(lista_components)



                                if  fract_inf_links != float('NaN'): 
                                    list_evol_fract_inf_links.append(fract_inf_links)
                                if  fract_inf_nodes != float('NaN'): 
                                    list_evol_fract_inf_nodes.append(fract_inf_nodes)
                                if  GC != float('NaN'): 
                                    list_evol_fract_GC_inf.append(GC)

                        ######### end of current period
                        period +=1            


                    ######## end of loop of termporal evolution (all periods)
                    list_lists_fract_inf_links.append(list_evol_fract_inf_links)
                    list_lists_fract_inf_nodes.append(list_evol_fract_inf_nodes)
                    list_lists_GC_inf.append(list_evol_fract_GC_inf)              


                #try:
                   # name_h="../Results/Simulations/histogram_tot_size_infected_connected_components_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                    #histograma_gral.histogram(list_sizes_inf_components_tot, name_h)



                    #### i also dump the raw list of values for KS comparison simu-real data
                   # pickle_filename="../Results/Simulations/List_values_tot_size_infected_connected_components_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"                    
                    #pickle.dump(list_sizes_inf_components_tot, open(pickle_filename, 'wb'))
                    #print "written:",pickle_filename

                #except ValueError: pass  # empty list




                ######## end of loop over iterations    
                #########################
                                   
                for period in sorted(dict_period_list_sizes_inf_conn_comp):

                    pickle_name="../Results/Simulations/List_values_size_inf_con_comp_"+slicing+"_slicing_period"+str(period)+"_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"                    
                    pickle.dump(dict_period_list_sizes_inf_conn_comp[period], open(pickle_name, 'wb'))
                    print "written:",pickle_name
              
      
              
                for tt in range(len(list_evol_fract_inf_links)):

                    list_values_link=[]
                    list_values_node=[]
                    list_values_GC=[]
                    for lista in list_lists_fract_inf_links:
                        list_values_link.append(lista[tt])

                    for lista in list_lists_fract_inf_nodes:
                        list_values_node.append(lista[tt])

                    for lista in list_lists_GC_inf:                        
                        list_values_GC.append(lista[tt])                 

                    print >> file2, tt+1, numpy.mean(list_values_link), numpy.std(list_values_link), numpy.mean(list_values_node), numpy.std(list_values_node), numpy.mean(list_values_GC), numpy.std(list_values_GC), prob_spontaneous, prob_inf, prob_recovery

                file2.close()
                print "written:",name2

                
                
                

            
            ######## end of loop over prob_recovery             
        ######## end of loop over prob_inf          
    ######## end of loop over prob_spontaneous









######################################
######################################

def  infection_dyn(G_period, dict_node_previous_status, prob_inf, prob_recovery):  # i use G for structure and dict for status
     
    for node in G_period.nodes():  # at the begining of the loop, nodes in G have the same status as dict_previous, or, if didnt exist before, S       
        if G_period.node[node]["status"] == "I":
            for neighbor in G_period.neighbors(node):                
                r=random.random()
                if r <= prob_inf:
                    G_period.node[neighbor]["status"] = "I"
                    
        r=random.random()
        if r <= prob_recovery:
            G_period.node[node]["status"] = "S"

    
    ##### undate dict to use as "previous state" for next period
    for node in  G_period.nodes():
        dict_node_previous_status[node] = G_period.node[node]["status"]



######################################
######################################

def count_inf_links_nodes_GC(G_period):



    H_period_aux = G_period.copy()   # make a copy to get only the infected links and nodes (for cluster distribution)

    ##### i count inf. nodes and links
    fract_inf_nodes=0.
    fract_inf_links=0.
    for node in  G_period.nodes():        
        if G_period.node[node]["status"]== "I":
            fract_inf_nodes  +=1.

            for neighbor in G_period.neighbors(node):

                if G_period.node[neighbor]["status"]== "I":

                    if node < neighbor:  # so i dont count each link twice                    
                        fract_inf_links  += 1.

                ###### i remove non-infected links from the aux subgraph
                else:  
                    try:
                        H_period_aux.remove_edge(node,neighbor)
                    except :
                        try:
                            H_period_aux.remove_edge(neighbor,node)
                        except: pass
                            
   
        else:              
            H_period_aux.remove_node(node)   # with this, i remove the node and all its links



    try:
        fract_inf_nodes = fract_inf_nodes / float(len(G_period.nodes()))
    except ZeroDivisionError:
        fract_inf_nodes =float('NaN')

    try:
        fract_inf_links = fract_inf_links/float(len(G_period.edges()))
    except ZeroDivisionError:
        fract_inf_links =float('NaN')





    ##### i remove the isolates from aux graph:
    list_to_remove=[]
    for node in H_period_aux.nodes():
        if H_period_aux.degree(node)==0:
            list_to_remove.append(node)

    H_period_aux.remove_nodes_from(list_to_remove)

   # print " # nodes:  in G:", len(G_period.nodes()), " in H_aux:", len(H_period_aux.nodes())
    #print " # edges:  in G:", len(G_period.edges()), " in H_aux:", len(H_period_aux.edges())


    lista_components=[]
    ##### i calculate components on the infected subgraph
    #print "components of Infected subgraph:"
    for item in nx.connected_component_subgraphs(H_period_aux):
        try:
     #       print "comp. size:",len(item.nodes()),  "  avg.path lenght within component:",nx.average_shortest_path_length(item)            
            lista_components.append(len(item.nodes()))

        except ZeroDivisionError: pass
               #print "comp. size:",len(item.nodes())



    ####### i get the GC of the infected subgraph    
    try:
        Gc = len(max(nx.connected_component_subgraphs(H_period_aux), key=len))/float(len(G_period.edges()))
       # print "GC:", Gc, "\n"
    except ValueError: 
        Gc=float('NaN')







    return fract_inf_links,fract_inf_nodes, Gc, lista_components



######################################
######################################


def  spontaneous_dyn(G_period, dict_node_previous_status, prob_spontaneous):
   
    for node in G_period.nodes():  # at the begining of the loop, nodes in G have the same status as dict_previous, or, if didnt exist before, S 
        r=random.random()
        if r <= prob_spontaneous:
            G_period.node[node]["status"] = "I"
                    
     
    ##### undate dict to use as "previous state" for next period
    for node in  G_period.nodes():
        dict_node_previous_status[node] = G_period.node[node]["status"]  # i save a dict. to have the state for next period
    





######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

