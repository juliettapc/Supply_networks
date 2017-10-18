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
import scipy.stats

def main():


  
    list_prob_spontaneous=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]
  
    list_prob_inf=[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]

    list_prob_recovery=[0.,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]




    threshold_neg_trans=0.0

    Niter=20    # iterations for a given set of parameters


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


    ########### output file with best parameters per each period, when minimizing inf links, nodes or inf. GC
    filename_optimum1="../Results/Time_evol_optimum_param_by_min_dist_inf_links.dat"
    file_optimum1=open(filename_optimum1,'wt')

    filename_optimum2="../Results/Time_evol_optimum_param_by_min_dist_inf_nodes.dat"
    file_optimum2=open(filename_optimum2,'wt')

    filename_optimum3="../Results/Time_evol_optimum_param_by_min_dist_inf_GC.dat"
    file_optimum3=open(filename_optimum3,'wt')

    filename_optimum4="../Results/Time_evol_optimum_param_by_min_sum_dist_inf_links_nodes_GC.dat"
    file_optimum4=open(filename_optimum4,'wt')






    ####### i read the datafile with the real data for the infection:  
    #########################                     
    filename_real="../Results/Time_evol_tot_num_infected_links_nodes_GC_with_neg_transact_larger_than"+str(threshold_neg_trans)+"_"+slicing+"_slicing.dat"
    # time num_inf_links frac_inf_links num_inf_nodes fract_inf_nodes  GC_inf  N_inf  L_inf
    #  0         1            2               3             4           5      6  7

  
    file_real=open(filename_real,'r')
    list_lines_file_real=file_real.readlines()
    
    dict_t_fract_inf_links_real={}
    dict_t_fract_inf_nodes_real={}
    dict_t_inf_GC_real={}
    dict_t_fract_inf_GC_real={}

  
    for line in list_lines_file_real:     
        list_row= line.split(" ")
        try:                             
            t=int(list_row[0])

            fract_inf_links_real=float(list_row[2])
            dict_t_fract_inf_links_real[t]=fract_inf_links_real

            num_inf_nodes_real=float(list_row[3])   
          
            fract_inf_nodes_real=float(list_row[4])   
            dict_t_fract_inf_nodes_real[t]=fract_inf_nodes_real

            GC_real_inf=float(list_row[5])  
            dict_t_inf_GC_real[t]=GC_real_inf       

            dict_t_N_inf=float(list_row[6])  



            try:
                dict_t_fract_inf_GC_real[t]= GC_real_inf / num_inf_nodes_real
            except ZeroDivisionError:
                dict_t_fract_inf_GC_real[t]= "NA"
   
           

        except ValueError:  pass   # for when there is an NA
          



    ########## i also need to read the size of the entire network
    filename3="../Results/Time_evol_network_metrics_monthly.dat"
    file3 = open(filename3,'r')
 
    list_lines_file_real=file3.readlines()


    dict_t_N={}
    for line in list_lines_file_real:     
        list_row= line.split(" ")
        
        t=int(list_row[0])        
        N=float(list_row[1])
        dict_t_N[t]=N

      

    
    dict_parameters_dict_time_evols={}   
    for  prob_spontaneous in list_prob_spontaneous:
        for  prob_inf in list_prob_inf:                        
            for  prob_recovery in list_prob_recovery:                
            
                try:
                    ####### i read the datafiles with the simulations 
                    ###################                                                                 

                    filename_simu="../Results/Simulations/Avg_time_evol_num_infected_links_and_nodes_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                   
                      # time  fract_inf_links   SD    frac_inf_nodes    SD     GC_inf     SD   P_spont  P_inf  P_recov
                      #  0         1            2          3             4      5          6      7       8       9

                      # print filename_simu
                    
                    parameters=str(prob_spontaneous)+"_"+str(prob_inf)+"_"+str(prob_recovery)                  

                    dict_parameters_dict_time_evols[parameters]={}


                    dict_t_fract_inf_links_simu={}
                    dict_t_fract_inf_nodes_simu={}
                    dict_t_inf_GC_simu={}
                    dict_t_fract_inf_GC_simu={}
                  
                    
                    file_simu=open(filename_simu,'r')
                    list_lines_file_simu=file_simu.readlines()
                                        
                    for line in list_lines_file_simu:     
                        list_row= line.split(" ")
                        try:                             
                            t=int(list_row[0])
                            
                            fract_inf_links_simu=float(list_row[1])
                            dict_t_fract_inf_links_simu[t]=fract_inf_links_simu
                            
                            fract_inf_nodes_simu=float(list_row[3])   
                            dict_t_fract_inf_nodes_simu[t]=fract_inf_nodes_simu
                            
                            GC_simu_inf=float(list_row[5])  
                            dict_t_inf_GC_simu[t]=GC_simu_inf          
                             
                           
                           # try:
                                try:
                                    dict_t_fract_inf_GC_simu[t]=GC_simu_inf/(fract_inf_nodes_simu * dict_t_N[t])
                                except KeyError:
                                    dict_t_fract_inf_GC_simu[t]="NA"
                                    #print t, GC_simu_inf, fract_inf_nodes_simu, dict_t_N[t]


                          #  except ZeroDivisionError:
                           #     dict_t_fract_inf_GC_simu[t]="NA"

                        except ValueError:  pass   # for when there is an NA
      
                 
                    dict_parameters_dict_time_evols[parameters]["evol_fract_inf_links"]=dict_t_fract_inf_links_simu
                    dict_parameters_dict_time_evols[parameters]["evol_fract_inf_nodes"]=dict_t_fract_inf_nodes_simu
                    dict_parameters_dict_time_evols[parameters]["evol_fract_inf_GC"]=dict_t_fract_inf_GC_simu

       
                except IOError:  pass # missing file
                    #print "file not found"


    dict_period_dict_param_dist={}
    for period in range(final_period):
       period +=1
       print period
       dict_period_dict_param_dist[period]={}


       dict_period_dict_param_dist[period]["dist_fract_inf_links"]={}
       dict_period_dict_param_dist[period]["dist_fract_inf_nodes"]={}
       dict_period_dict_param_dist[period]["dist_fract_inf_GC"]={}
       dict_period_dict_param_dist[period]["sum_dist_fract_inf_links_nods_GC"]={}
    

       ############### i calculate the metrics for correlation or distance...
       #####################
       
       for  prob_spontaneous in list_prob_spontaneous:
           for  prob_inf in list_prob_inf:                        
               for  prob_recovery in list_prob_recovery:                
                   #  print "prob_spontaneous:", prob_spontaneous,  " prob_inf:", prob_inf, "  prob_recovery:", prob_recovery

                   parameters=str(prob_spontaneous)+"_"+str(prob_inf)+"_"+str(prob_recovery)
                  
                 
                   try:
                       dict_period_dict_param_dist[period]["dist_fract_inf_links"][parameters]= abs(dict_t_fract_inf_links_real[period] - dict_parameters_dict_time_evols[parameters]["evol_fract_inf_links"][period])

                       dict_period_dict_param_dist[period]["dist_fract_inf_nodes"][parameters]= abs(dict_t_fract_inf_links_real[period] - dict_parameters_dict_time_evols[parameters]["evol_fract_inf_nodes"][period])

                       try:
                           dict_period_dict_param_dist[period]["dist_fract_inf_GC"][parameters]= abs(dict_t_fract_inf_links_real[period] - dict_parameters_dict_time_evols[parameters]["evol_fract_inf_GC"][period])
                       except TypeError:
                           print dict_t_fract_inf_links_real[period],  dict_parameters_dict_time_evols[parameters]["evol_fract_inf_GC"][period]
                           raw_input()


                       dict_period_dict_param_dist[period]["sum_dist_fract_inf_links_nods_GC"][parameters] = dict_period_dict_param_dist[period]["dist_fract_inf_links"][parameters] + dict_period_dict_param_dist[period]["dist_fract_inf_nodes"][parameters] + dict_period_dict_param_dist[period]["dist_fract_inf_GC"][parameters]
                      
                    
                   except KeyError: 
                      
                       dict_period_dict_param_dist[period]["dist_fract_inf_links"][parameters]= "NA"
                       
                       dict_period_dict_param_dist[period]["dist_fract_inf_nodes"][parameters]= "NA"
                       
                       dict_period_dict_param_dist[period]["dist_fract_inf_GC"][parameters]= "NA"


                       dict_period_dict_param_dist[period]["sum_dist_fract_inf_links_nods_GC"][parameters]="NA"



    print "top sets of parameters, optimizing by min. dist in fract. inf links:\n"
    for period in range(final_period):
        period +=1
       
        list_sorted_dict= sorted(dict_period_dict_param_dist[period]["dist_fract_inf_links"].items(), key=operator.itemgetter(1))    
        list_optimum_param=list_sorted_dict[0][0].split("_")
        optimum_dist=list_sorted_dict[0][1]
        print >> file_optimum1, period, list_optimum_param[0],list_optimum_param[1],list_optimum_param[2],optimum_dist
         

        list_sorted_dict= sorted(dict_period_dict_param_dist[period]["dist_fract_inf_nodes"].items(), key=operator.itemgetter(1))    
        list_optimum_param=list_sorted_dict[0][0].split("_")
        optimum_dist=list_sorted_dict[0][1]
        print >> file_optimum2, period, list_optimum_param[0],list_optimum_param[1],list_optimum_param[2],optimum_dist
         

        list_sorted_dict= sorted(dict_period_dict_param_dist[period]["dist_fract_inf_GC"].items(), key=operator.itemgetter(1))    
        list_optimum_param=list_sorted_dict[0][0].split("_")
        optimum_dist=list_sorted_dict[0][1]
        print >> file_optimum3, period, list_optimum_param[0],list_optimum_param[1],list_optimum_param[2],optimum_dist
         

        list_sorted_dict= sorted(dict_period_dict_param_dist[period]["sum_dist_fract_inf_links_nods_GC"].items(), key=operator.itemgetter(1))    
        list_optimum_param=list_sorted_dict[0][0].split("_")
        optimum_dist=list_sorted_dict[0][1]
        print >> file_optimum4, period, list_optimum_param[0],list_optimum_param[1],list_optimum_param[2],optimum_dist
         






    file_optimum1.close()    
    print "written:",filename_optimum1
    file_optimum2.close()    
    print "written:",filename_optimum2
    file_optimum3.close()
    print "written:",filename_optimum3
    file_optimum4.close()
    print "written:",filename_optimum4


####################################
####################################


def calculate_avg_dist_two_curves(dict_evol_real, dict_evol_simu):
  
    list_dist=[]
    for t in sorted(dict_evol_real):   # i calculate the avg distances from one curve to another at each same time step
        try:
            dist=abs(dict_evol_real[t]-dict_evol_simu[t])
            list_dist.append(dist)
          #  print t,dict_evol_real[t],dict_evol_simu[t], "  ", dist
        except KeyError: pass  # some simus and real data are missing a time period
        
    avg=numpy.mean(list_dist)    # to account for some time series being longer than others, i need the avg
   # print "   ",avg
    return avg, "blah"  ## because the other metrics are a tuple




####################################
###################################

def calculate_pearson_correlation_two_curves(dict_evol_real,dict_evol_simu):


#Returns  TUPLE!!!:	 (Pearson's correlation coefficient,2-tailed p-value)

#The Pearson correlation coefficient measures the linear relationship between two datasets. Strictly speaking, Pearson's correlation requires that each dataset be normally distributed. Like other correlation coefficients, this one  varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact linear relationship. Positive correlations imply that as x increases, so does y. Negative correlations imply that as x increases, y decreases.
#The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson correlation at least as extreme as the one computed from these datasets. The p-values are not entirely reliable but are probably reasonable for datasets larger than 500 or so.



    list1=[]
    list2=[]
    for t in sorted(dict_evol_real):

        if t in dict_evol_simu:    # some simus and real data are missing a time period
            list1.append(dict_evol_real[t])     
            list2.append(dict_evol_simu[t])

    pearson_corr_coeff= scipy.stats.pearsonr(list1,list2)
    

    return  pearson_corr_coeff


####################################
###################################

def calculate_spearman_correlation_two_curves(dict_evol_real,dict_evol_simu):

#The Spearman correlation is a nonparametric measure of the monotonicity of the relationship between two datasets. Unlike the Pearson correlation, the Spearman correlation does not assume that both datasets are normally distributed. Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact monotonic relationship. Positive correlations imply that as x increases, so does y. Negative correlations imply that as x increases, y decreases.

#The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Spearman correlation at least as extreme as the one computed from these datasets. The p-values are not entirely reliable but are probably reasonable for datasets larger than 500 or so.



#Returns  TUPLE!!!:   rho: float or ndarray (2-D square) Spearman correlation matrix or correlation coefficient (if only 2 variables are given as parameters. Correlation matrix is square with length equal to total number of variables (columns or rows) in a and b combined.
    #       p-value: float, The two-sided p-value for a hypothesis test whose null hypothesis is that two sets of data are uncorrelated, has same dimension as rho.


    list1=[]
    list2=[]
    for t in sorted(dict_evol_real):

        if t in dict_evol_simu:    # some simus and real data are missing a time period
            list1.append(dict_evol_real[t])     
            list2.append(dict_evol_simu[t])
        
    spearman_corr_coeff= scipy.stats.spearmanr(list1,list2)   

  
    return  spearman_corr_coeff



####################################
###################################


def  get_dict_diffenreces_with_previous(dictionary_time_evol):

    dict_diff_with_previous={}
    cont=0
    try:
        previous_value=dictionary_time_evol[1]
    except KeyError:
        for t in  sorted(dictionary_time_evol):
            print t
        raw_input()

    for t in sorted(dictionary_time_evol):
        if cont >1:
            try:
                dict_diff_with_previous[t]= dictionary_time_evol[t] - previous_value
                previous_value= dictionary_time_evol[t]
            except KeyError: pass
        
        cont +=1
 
    return dict_diff_with_previous
            

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

