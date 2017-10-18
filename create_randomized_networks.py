#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept 2016

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
import itertools
import random

def main():


    slicing="monthly"    #"monthly"  # or "yearly"
    string_cohort=""

    cont_periods =0
    max_periods = 252
    while cont_periods <= max_periods:

        cont_periods  +=1


        try:
            network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(cont_periods)+string_cohort+"_.pickle"
            G = pickle.load(open(network_period, 'rb'))  
          

            print network_period

            new_H = G.copy()  # copy to manipulate
           # print "N:",len(H.nodes()),"L:",len(H.edges())

            #new_H=randomize(H, cont_periods)
            #print "   done!"
            #print "   N:",len(new_H.nodes()),"L:",len(new_H.edges())

           
          
           

            pickle_name=network_period.strip(".pickle")+"randomized.pickle"


            print network_period
            print pickle_name

            pickle.dump(new_H, open(pickle_name, 'wb'))
            print "  written", pickle_name
            raw_input()


        except IOError:pass
        


 
######################################
######################################



def randomize(H, cont_periods):


    Niter=2*len(H.edges())

    print " randomizing network......"
   
    for i in range(Niter):


        list_edges=H.edges()

        link1=random.choice(list_edges)
        link2=random.choice(list_edges)

        if link1 != link2:
            n1=link1[0]
            n2=link1[1]
            
            n3=link2[0]
            n4=link2[1]


            if n1 != n2  and n1 != n3  and n1 != n4:      
                if n2 != n3  and n2 != n4  and n2 != n1:      
                

                       # if i add existing links, i am effectively losing links!!!
                   

                    if (n1, n4)  not in H.edges()  and (n4, n1)  not in H.edges():
                        if (n2, n3)  not in H.edges()  and (n3, n2)  not in H.edges():
                            
                            
                            H.add_edge(n1, n4)
                            H.add_edge(n2, n3)
                            
                            H.remove_edge(n1, n2)
                            H.remove_edge(n3, n4)
                            




                           # print cont_periods, "  ",i, "/",Niter, "   N:",len(H.nodes()),"L:",len(H.edges())
  

    return H

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
