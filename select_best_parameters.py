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


    optimize_by = "spearman"     #"combo_dist"     #"testing"     #"avg_dist"  # "avg_dist"  or "pearson"  or "spearman"  or  "pearson_diff_with_previous" "spearman_combined"  # Spearman doesnt assume normality




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


   


    ####### i read the datafile with the real data for the infection:  
    #filename_real="../Results/Time_evol_tot_num_infected_links_nodes_GC_"+slicing+"_slicing.dat"
    # time num_inf_links frac_inf_links num_inf_nodes fract_inf_nodes  GC
    #  0         1            2               3             4           5

    filename_real="../Results/Time_evol_tot_num_infected_links_nodes_GC_with_neg_transact_larger_than"+str(threshold_neg_trans)+"_monthly_slicing.dat"
    # time num_inf_links frac_inf_links num_inf_nodes fract_inf_nodes  GC  N  L
    #  0         1            2               3             4           5  6  7

    dict_t_fract_inf_links_real={}
    dict_t_fract_inf_nodes_real={}
    dict_t_inf_GC_real={}


    file_real=open(filename_real,'r')
    list_lines_file_real=file_real.readlines()
    

    for line in list_lines_file_real:     
        list_row= line.split(" ")
        try:                             
            t=int(list_row[0])

            fract_inf_links_real=float(list_row[2])
            dict_t_fract_inf_links_real[t]=fract_inf_links_real

            fract_inf_nodes_real=float(list_row[4])   
            dict_t_fract_inf_nodes_real[t]=fract_inf_nodes_real

            GC_real=float(list_row[5])  
            dict_t_inf_GC_real[t]=GC_real          

        except ValueError:  pass   # for when there is an NA
          

    
    dict_filename_magnitude_to_optimize={}
    for  prob_spontaneous in list_prob_spontaneous:
        for  prob_inf in list_prob_inf:                        
            for  prob_recovery in list_prob_recovery:                
                print "prob_spontaneous:", prob_spontaneous,  " prob_inf:", prob_inf, "  prob_recovery:", prob_recovery


                try:
                    ####### i read the datafiles with the simulations 
                    ###################
                    filename_simu="../Results/Simulations/Avg_time_evol_num_infected_links_and_nodes_"+slicing+"_slicing_P_spontan"+str(prob_spontaneous)+"_P_inf"+str(prob_inf)+"_P_recovery"+str(prob_recovery)+"_"+str(Niter)+"iter.dat"
                   
                      # time  fract_inf_links   SD    frac_inf_nodes    SD     GC     SD   P_spont  P_inf  P_recov
                      #  0         1            2          3             4      5     6      7       8       9

                    print filename_simu
                    
                    dict_t_fract_inf_links_simu={}
                    dict_t_fract_inf_nodes_simu={}
                    dict_t_inf_GC_simu={}
                    
                    
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
                            
                            GC_simu=float(list_row[5])  
                            dict_t_inf_GC_simu[t]=GC_simu          
                            
                        except ValueError:  pass   # for when there is an NA
      
                 




                    ############### i calculate the metrics for correlation or distance...
                    #####################
                    if  optimize_by == "pearson":
                        measure_correlation=calculate_pearson_correlation_two_curves(dict_t_fract_inf_links_real, dict_t_fract_inf_links_simu)   
                       
                        
                    elif  optimize_by == "spearman":
                        measure_correlation=calculate_spearman_correlation_two_curves(dict_t_fract_inf_links_real, dict_t_fract_inf_links_simu)


                    elif  optimize_by =="spearman_combined":  # i create a combined score with the optimum of fract_links, nodes and GC over time

                        #### this function returs a tuple: corr_coeff, p-value
                        correlation_link=calculate_spearman_correlation_two_curves(dict_t_fract_inf_links_real, dict_t_fract_inf_links_simu)   
                        correlation_node=calculate_spearman_correlation_two_curves(dict_t_fract_inf_nodes_real, dict_t_fract_inf_nodes_simu)
                        correlation_GC=calculate_spearman_correlation_two_curves(dict_t_inf_GC_real, dict_t_inf_GC_simu)

                         

                        dict_diff_previous_real=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_real)
                        dict_diff_previous_simu=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_simu)
                    
                        correlation_diff_previous=calculate_pearson_correlation_two_curves(dict_diff_previous_real,dict_diff_previous_simu)
                                                                

                        measure_correlation=(correlation_link[0] + correlation_diff_previous[0])/2.
                       


                    elif  optimize_by =="combo_dist":  # i create a combined score with the optimum of fract_links, nodes and GC over time

                       
                        correlation_link=calculate_avg_dist_two_curves(dict_t_fract_inf_links_real, dict_t_fract_inf_links_simu)   
                        correlation_node=calculate_avg_dist_two_curves(dict_t_fract_inf_nodes_real, dict_t_fract_inf_nodes_simu)
                        correlation_GC=calculate_avg_dist_two_curves(dict_t_inf_GC_real, dict_t_inf_GC_simu)
                     

                     #   dict_diff_previous_real=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_real)
                      #  dict_diff_previous_simu=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_simu)
                    
                      #  correlation_diff_previous=calculate_pearson_correlation_two_curves(dict_diff_previous_real,dict_diff_previous_simu)
                        #measure_correlation=(correlation_link[0] + correlation_diff_previous[0])/2.


                        try:
                            
                            int(correlation_GC[0])
                            measure_correlation= ((correlation_link[0] + correlation_node[0] + correlation_GC[0])/3.,"blah")
                        except ValueError:
                            measure_correlation= ((correlation_link[0] + correlation_node[0])/2., "blah")



                       
                        measure_correlation= correlation_GC



                    elif optimize_by == "avg_dist":
                        measure_correlation=calculate_avg_dist_two_curves(dict_t_fract_inf_links_real, dict_t_fract_inf_links_simu)
                      

                    elif optimize_by =="pearson_diff_with_previous":
                       
                        dict_diff_previous_real=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_real)
                        dict_diff_previous_simu=get_dict_diffenreces_with_previous(dict_t_fract_inf_links_simu)                   

                        measure_correlation=calculate_pearson_correlation_two_curves(dict_diff_previous_real,dict_diff_previous_simu)
                      



                    elif optimize_by == "testing":

                        # i generate testing "real" curve and simulated, to try

                        dict_t_real={}
                        dict_t_simu={}


                        list_real=[0.1,   0.12, 0.09, 0.099, 0.15, 0.7,  0.2,   0.15,  0.1, 0.12]
                        list_simu1=[0.25, 0.26, 0.25, 0.251, 0.24, 0.23, 0.245, 0.261, 0.2, 0.241]  # avg_diff = 0.1539
                        list_simu2=[0.75, 0.77, 0.74, 0.751, 0.741,0.723,0.745, 0.7661, 0.71, 0.741]  #avg_diff =0.627

                        for t in range(10):
                            dict_t_real[t+1]=list_real[t]
                            dict_t_simu[t+1]=list_simu2[t]

                      
                       # avg_dist_evol_links=calculate_avg_dist_two_curves(dict_t_real, dict_t_simu)
                       #print avg_dist_evol_links
                        spearman=calculate_spearman_correlation_two_curves(dict_t_real, dict_t_simu)
                        print spearman


                      
                        raw_input()
                      

                    else:
                        print "wrong optimization criterium"
                        print optimize_by
                        exit()
                    


                  
                    try:
                        int(measure_correlation[0])  # to get rid of the nan values
                        dict_filename_magnitude_to_optimize[filename_simu]=measure_correlation                   
                    except ValueError:
                        pass




                except IOError:  #pass # missing file
                    print "file not found"

    

    print "top sets of parameters, optimizing by:", optimize_by ,"\n"
    #### i sort the dict by value  (avg dist or pearson corr.)
    if  optimize_by == "pearson"  or   optimize_by == "spearman"  or   optimize_by == "spearman_combined"  or optimize_by == "pearson_diff_with_previous":
        list_sorted_dict = reversed(sorted(dict_filename_magnitude_to_optimize.iteritems(), key=operator.itemgetter(1)))
        for item in list_sorted_dict:
            print item
            raw_input()

    elif optimize_by == "avg_dist"  or  optimize_by == "testing"   or optimize_by == "combo_dist":

        list_sorted_dict = sorted(dict_filename_magnitude_to_optimize.iteritems(), key=operator.itemgetter(1))
        for item in list_sorted_dict:
            print item
            raw_input()

    else: pass


        







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

