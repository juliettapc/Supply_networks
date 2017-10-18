#!/usr/bin/env python

'''
Code to read the file original, partial datafiles and compile an file with
useful info with paper_id, year, subject_category, issue_id

Created by Julia Poncela, on Dec. 2015

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


def main():





    path="../Data/95_05NYCgamentdata/"
    flag_hist = "YES"

    initial_year=85
    final_year=105

    y_aux=initial_year


    print
    print

    
    list_neg_adj_gross=[]
    list_pos_adj_gross=[]
   
    while y_aux <= final_year:

      list_neg_adj_gross_year=[]
      list_pos_adj_gross_year=[]


      if y_aux < 95:
          y= y_aux          
           ##################  
           ####### input datafile:   
          name0="fhist"+str(y)+".csv"       
           ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode      

      if y_aux >= 95:   # this way i get a duplicate histogram for 95  and 1995
            y=y_aux + 1900
            name0="Fhistory"+str(y)+".csv"

      print "\nreading: ", path+name0, "......."        
    
      with open(path+name0, 'rb') as csvfile:
          reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
          next(reader, None)   # to skip the header
          
          for list_row in reader:                   

                        
              if y_aux < 95:
                  adj_gross=int(round(float((list_row[4]))))    ## for now i deal with integers Dollars !!  (easier for histograms)
              else:
                 # adj_gross=int(round(float((list_row[23])) / 100.))    ### DISCREPANCY BETWEEN DATA 85-95  AND 1995-2005 BY 2 ORDERS OF MAGNITUDE
                  adj_gross=int(round(float((list_row[23])) ))    
                  


  
              if adj_gross  <0:    ######### negative transaction  (ERROR)
                  list_neg_adj_gross.append(-1*adj_gross)
                  list_neg_adj_gross_year.append(-1*adj_gross)
              else:      ######### positive or zero  transaction
                  list_pos_adj_gross.append(adj_gross)
                  list_pos_adj_gross_year.append(adj_gross)
            
          
       


            
          
      print " # observations  (+,-):", len(list_pos_adj_gross_year), len(list_neg_adj_gross_year) 
      print "avg  (+,-)", numpy.mean(list_pos_adj_gross_year), numpy.mean(list_neg_adj_gross_year)
      print "sdt  (+,-)", numpy.std(list_pos_adj_gross_year), numpy.std(list_neg_adj_gross_year)

      if  flag_hist == "YES":
          print "creating histogram + ...."
          name_h="../Results/histogram_pos_adj_gross_values_year_"+str(y)+".dat"
          histograma_gral.histogram(list_pos_adj_gross_year, name_h)
          

          print "creating histogram - ...."
          name_h="../Results/histogram_neg_adj_gross_values_year_"+str(y)+".dat"
          histograma_gral.histogram(list_neg_adj_gross_year, name_h)





    
      y_aux +=1
      ################  new year file
      ##################################################
      ##################################################



    print "\n tot # observations  (+,-):", len(list_pos_adj_gross), len(list_neg_adj_gross)
    print "avg  (+,-)", numpy.mean(list_pos_adj_gross), numpy.mean(list_neg_adj_gross)
    print "sdt  (+,-)", numpy.std(list_pos_adj_gross), numpy.std(list_neg_adj_gross)
    if  flag_hist == "YES":
        print "creating histogram + ...."
        name_h="../Results/histogram_pos_adj_gross_values_years_"+str(initial_year)+"_"+str(final_year-100)+".dat"
        histograma_gral.histogram(list_pos_adj_gross, name_h)


        print "creating histogram - ...."
        name_h="../Results/histogram_neg_adj_gross_values_years_"+str(initial_year)+"_"+str(final_year-100)+".dat"
        histograma_gral.histogram(list_neg_adj_gross, name_h)




############################################
###############################################
################################################


def  calculate_kshell(G, max_k): ####  k-shell decomposition   (i need to make a copy and remove the self-loops from that before i can proceed)
    
        
    G_for_kshell = nx.Graph(G.subgraph(G.nodes()))
    
    list_edges_to_remove=[]
    for edge in G_for_kshell.edges():
        if edge[0] == edge[1]:
            list_edges_to_remove.append(edge)

    for edge in  list_edges_to_remove:
        G_for_kshell.remove_edge(edge[0], edge[1])
            
    cont_zeros=0      
    for i in range(max_k):   # k_max is the absolute upper boundary for max kshell index
        kshell= nx.k_shell(G_for_kshell, k=i, core_number=None)  # it returns the k-shell subgraph
        size_shell=len(kshell)
           # print  "    ",i, size_shell, kshell.nodes()
        for node in kshell.nodes():
            G.node[node]["kshell"]=i

        if size_shell==0:
            cont_zeros +=1       
        if cont_zeros >=7:  # to stop calculating shells after a few come back empty ones
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

