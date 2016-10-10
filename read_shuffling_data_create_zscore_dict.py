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


    master_dict_year_dict_micj_zscore={}
    


    zs_threshold=2.

    list_pairs=[]
    list_firms=[]
    list_small_zscores=[]
    list_large_zscores=[]



    list_years=["1985","1986","1987","1988","1989","1990","1991","1992","1993","1994-1995","1996-1997","1998-2000","2001-2005"]



    cont=0
    for year_string in list_years:
       
 

        list_real_years=[]
        if "-" not in year_string:
            list_real_years.append(int(year_string))

        else:

            aux_year_ini=int(year_string.split("-")[0])
            aux_year_fin=int(year_string.split("-")[1])

            aux_year = aux_year_ini
            while aux_year <= aux_year_fin:
                list_real_years.append(aux_year)
                aux_year +=1



        for year in list_real_years:
            master_dict_year_dict_micj_zscore[year]={}



        name0="../Data/Shuffling_by_year/"+str(year_string)+"_Null_10000_Shuffles.csv" ####  paidbyfi,paidforf,e_trans,total_trans,e_rate,z-scores
        print name0
        csvfile=open(name0, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   # to skip the header
        
        
        for list_row in reader:                
            cont +=1
            
            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm                    

            mi_cj=str(manufacturer) + "_"+ str(contractor)
            zscore=float(list_row[5])



            for year in list_real_years:
                master_dict_year_dict_micj_zscore[year][mi_cj]=zscore
                
            list_pairs.append(mi_cj)
            list_firms.append(manufacturer)
            list_firms.append(contractor)
            
            print cont, mi_cj, list_real_years,zscore
            if zscore > zs_threshold :
                list_large_zscores.append(mi_cj)
            elif zscore < -1.*zs_threshold: 
                list_small_zscores.append(mi_cj)
   





    pickle_name="../Results/dict_year_dict_micj_zscore_error_freq_controlling_year_degree.pickle"
    pickle.dump(master_dict_year_dict_micj_zscore, open(pickle_name, 'wb'))
    print "written picke list:", pickle_name

    print "final count:", cont
    print "num. firms:",len(list_firms), " unique:", len(set(list_firms))
    print "num. pairs:",len(list_pairs), " unique:", len(set(list_pairs))
    print "   num. pairs with larger zs's:", len(list_large_zscores), " unique:", len(set(list_large_zscores))
    print "   num. pairs with smaller zs's:", len(list_small_zscores), " unique:", len(set(list_small_zscores))

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
