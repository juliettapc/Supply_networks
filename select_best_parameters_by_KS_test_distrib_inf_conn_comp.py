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
import operator
import  scipy.stats

def main():


  
    list_prob_spontaneous=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]
  
    list_prob_inf=[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]

    list_prob_recovery=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]






    Niter=20    # iterations for a given set of parameters


    optimize_by = "KS"


    threshold_neg_tran=0.0

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


   


    ####### i read the datafile with the list of sized of infected connected components
#    pickle_filename_real_data= "../Results/List_values_tot_size_infected_connected_components_"+slicing+"_slicing.dat"


    pickle_filename_real_data="../Results/List_values_tot_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"   # when applying threshold on the min. size of transactions to be included in the calculations



    list_values_size_inf_clusters_real = pickle.load(open(pickle_filename_real_data, 'rb')) 

  
    print "loaded pickle with real data"
    
    dict_filename_magnitude_to_optimize={}
    for  prob_spontaneous in list_prob_spontaneous:
        for  prob_inf in list_prob_inf:                        
            for  prob_recovery in list_prob_recovery:                
                print "prob_spontaneous:", prob_spontaneous,  " prob_inf:", prob_inf, "  prob_recovery:", prob_recovery


                try:
                    ####### i read the datafiles with the simulations 
                    ###################
                    pickle_filename_simu="../Results/Simulations/List_values_tot_size_infected_connected_components_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                    
                    # list values sizes of infected connected components, by month but aggregated over all of them
                    
                    
                    print  pickle_filename_simu
                    
                    
                    list_values_size_inf_clusters_simu = pickle.load(open( pickle_filename_simu, 'rb')) 


                



                    ############### i calculate the KS test for the two list of values...
                    #####################
                    if  optimize_by == "KS":
                        measure_correlation= scipy.stats.ks_2samp(list_values_size_inf_clusters_real, list_values_size_inf_clusters_simu)[1]

                        #Returns:	
                        #D : float, KS test statistic
                        #p-value : float, One-tailed or two-tailed p-value.
                        #This is a two-sided test for the null hypothesis that 2 independent samples are drawn from the same continuous distribution.

                        print " KS test real-simu:",measure_correlation
                       



                    else:
                        print "wrong optimization criterium"
                        print optimize_by
                        exit()
                    


                  
                    try:
                        int(measure_correlation)  # to get rid of the nan values
                        dict_filename_magnitude_to_optimize[pickle_filename_simu]=measure_correlation                   
                    except ValueError:
                        pass




                except IOError:  #pass # missing file
                    print "file not found"

    

    print "\n\ntop sets of parameters, optimizing by:", optimize_by ,"  (D, p-value), null hyp.: samples from same distrib.\n"
    #### i sort the dict by value  (avg dist or pearson corr.)
    if  optimize_by == "KS":
             # reversed, because i want to pick the case with the largest p-value (most likely couple of list to come from same distribution)
       
        list_sorted_dict = reversed(sorted(dict_filename_magnitude_to_optimize.iteritems(), key=operator.itemgetter(1)))
        for item in list_sorted_dict:
            print item
#REAL: ../Results/histogram_tot_size_infected_connected_components_monthly_slicing.dat
#SIMU: ../Results/Simulations/histogram_tot_size_infected_connected_components_monthly_slicing_P_spontan0.0_P_inf0.0_P_recovery0.3_20iter.dat


            raw_input()

    else: pass


        







####################################
####################################



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

