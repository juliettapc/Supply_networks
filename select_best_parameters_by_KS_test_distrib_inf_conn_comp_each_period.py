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
import operator
import  scipy.stats

def main():


  
    list_prob_spontaneous=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]
    list_prob_inf=[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]
    list_prob_recovery=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]




    Niter=20    # iterations for a given set of parameters


   #num. files read: 120786  with restriction


    Num_periods=250

    min_num_datapoints=20 # min. number observations to even run the KS test  


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


    num_files_read=0
    dict_period_dict_filename_magnitude_to_optimize={}
    for period in range(Num_periods):
        #print "t:",period
        period +=1
        dict_period_dict_filename_magnitude_to_optimize[period]={}

        try:
            ####### i read the datafile with the list of sized of infected connected components         
            ###################                                                            
               
            pickle_filename_real_data="../Results/List_values_tot_size_infected_connected_components_monthly_slicing_"+str(period)+".pickle"
            list_values_size_inf_clusters_real = pickle.load(open(pickle_filename_real_data, 'rb'))                  
                 # print "loaded pickle with real data"                            
        
            print period, "num obs. actual data:", len(list_values_size_inf_clusters_real)

            for  prob_spontaneous in list_prob_spontaneous:
                for  prob_inf in list_prob_inf:                        
                    for  prob_recovery in list_prob_recovery:                
                        
                        list_values_size_inf_clusters_simu=[]
                        
                        try:
                            ###### i read the datafiles with the simulations 
                            ###################       
                          
                            
                                                                                                      
                            pickle_filename_simu= "../Results/Simulations/List_values_size_inf_con_comp_monthly_slicing_period"+str(period)+"_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                            list_values_size_inf_clusters_simu = pickle.load(open( pickle_filename_simu, 'rb')) 
       

                            num_files_read +=1

                            ############### i calculate the KS test for the two list of values...
                            #####################
                            
                            measure_correlation= scipy.stats.ks_2samp(list_values_size_inf_clusters_real, list_values_size_inf_clusters_simu)
                            


                           # print "num obs. actual data:", len(list_values_size_inf_clusters_real),"  num obs. simu:",  len(list_values_size_inf_clusters_simu)
                            if len(list_values_size_inf_clusters_real) < min_num_datapoints  or len(list_values_size_inf_clusters_simu) < min_num_datapoints:
                                measure_correlation="NA"   # too short a list to be able to use the KS test

                            
                            #Returns:	
                            #D : float, KS test statistic
                            #p-value : float, One-tailed or two-tailed p-value.
                            #This is a two-sided test for the null hypothesis that 2 independent samples are drawn from the same continuous distribution. If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions of the two samples are the same.
                            
                           # print " KS test real-simu:",measure_correlation
                         
                                              


                  
                            try:
                                int(measure_correlation[1])  # to get rid of the nan values
                                dict_period_dict_filename_magnitude_to_optimize[period][pickle_filename_simu]=measure_correlation
                            except ValueError:  pass




                        except IOError:  pass # missing simu file

    
        except IOError:  #pass # missing actual data file
            pass






    print "\n\n best set of parameters for each period, optimizing by KS"
    print "       (D, p-value), null hyp.: samples from same distrib.\n"
    print "If the K-S statistic is small or the p-value is high, then we cannot reject the (null) hypothesis that the distributions of the two samples are the same."




    filename3="../Results/Time_evol_optimum_parameters_"+str(Niter)+"iter.dat"
    file3 = open(filename3,'wt')


    filename4="../Results/List_optimum_distrib_size_inf_clusters_for_each_period_"+str(Niter)+"iter.dat"
    file4 = open(filename4,'wt')

    #### i sort the dict by value  (avg dist or pearson corr.)                    

    for period in range(Num_periods):
        period +=1
       
        try:
        
            #   list_sorted_dict = reversed(sorted(dict_period_dict_filename_magnitude_to_optimize[period].iteritems(), key=operator.itemgetter(1)))
           
            list_optimum = sorted(dict_period_dict_filename_magnitude_to_optimize[period].iteritems(), key=operator.itemgetter(1))
 
           # example: list_optimum[0] :   ('../Results/Simulations/List_values_tot_size_inf_con_comp_monthly_slicing_period1_P_spontan0.0_P_inf0.2_P_recovery0.7_2iter.dat', (0.21111111111111114, 0.51654420549292857)) THE OPTIMUM IS [0], SORTED FROM BETTER TO WORSE
   

            filename_chosen_simu_list=list_optimum[0][0]
            list_values_size_inf_clusters_simu = pickle.load(open( filename_chosen_simu_list, 'rb')) 


            prob_spontaneous=filename_chosen_simu_list.split("P_spontan")[1].split("_P_inf")[0]
            prob_inf=filename_chosen_simu_list.split("_P_inf")[1].split("_P_recovery")[0]
            prob_recovery=filename_chosen_simu_list.split("_P_recovery")[1].split("_"+str(Niter))[0]

           # print period, prob_spontaneous, prob_inf, prob_recovery, list_optimum[0][1]
            print >> file3, period, prob_spontaneous, prob_inf, prob_recovery, list_optimum[0][1][0], list_optimum[0][1][1]

            name_h="../Results/Simulations/histogram_tot_size_infected_con_comp_"+slicing+"_slicing_period"+str(period)+"_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
            histograma_gral.histogram(list_values_size_inf_clusters_simu, name_h)


            actual_data_hist="../Results/histogram_size_infected_connected_components_threshold_neg_tran0.0_monthly_slicing_"+str(period)+".dat"
            print "print against actual data one:\n", actual_data_hist




            print >> file4, "period:",period, "\n", name_h, "\n", actual_data_hist
            print >> file4

        except IndexError:  pass  ## to account for the couple missing networks
       
    file3.close()
    print "\n\nwritten: ", filename3


    file4.close()
    print "\n\nwritten: ", filename4

    print "num. files read:", num_files_read

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

