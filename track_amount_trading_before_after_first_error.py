#!/usr/bin/env python

'''
Created by Julia Poncela, on May. 2016

'''

import datetime as dt
import csv
import pickle
import histogram_bins_increasing
import histograma_gral
import numpy 
import random
import sys
import scipy.stats

def main():

   final_period=240
   time_window=2  # time before and after an error to look at amount of transactions


 

   dict_period_dict_edges_month_first_errors={}
   dict_period_dict_firms_month_first_errors={}
  
   ########### i get the month of the first error for pair and individual firms
   period=0
   while period <= final_period:
      period +=1
 
      dict_period_dict_edges_month_first_errors[period]={}
      dict_period_dict_firms_month_first_errors[period]={}

      ###### i read the actual network structure from the data
      network_filename="../Results/Supply_network_slicing_monthly_period_"+str(period)+"_no_network_metrics.pickle"
      G_period = pickle.load(open(network_filename, 'rb'))    



             # edges:   (9101202, 9101160, {'pos_weight': 64320, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 2.0, 'link_betweeness': 0.0, 'neg_weight': 0.0})

              #nodes:     (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 0, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0})


      for edge in G_period.edges():

         e1=edge[0]     # the ends of the current link                            
         e2=edge[1]                
         
         if int(G_period.edge[e1][e2]["num_neg_trans"]) >0:
            try:
               dict_period_dict_edges_month_first_errors[period][edge] # if it already exists, i do nothing
            except KeyError:
               dict_period_dict_edges_month_first_errors[period][edge]=period

         

            try:
               dict_period_dict_firms_month_first_errors[period][e1]
            except KeyError:
               dict_period_dict_firms_month_first_errors[period][e1]=period

            try:
               dict_period_dict_firms_month_first_errors[period][e2]
            except KeyError:
               dict_period_dict_firms_month_first_errors[period][e2]=period



   list_amounts_firms_before=[]
   list_amounts_firms_after=[]

   list_amounts_edges_before=[]
   list_amounts_edges_after=[]


   ######### i get the amount of business for pairs of firms and individual companies before and after their first error
   period=0
   while period <= final_period:
      period +=1     
    
      list_aux_periods_before=[]
      aux_period=period 
      while aux_period > (period - time_window):
         aux_period -= 1
         if aux_period >0:
            list_aux_periods_before.append(aux_period)


      list_aux_periods_after=[]
      aux_period=period 
      while aux_period < (period + time_window):
         aux_period += 1
         list_aux_periods_after.append(aux_period)

      #print period,  list_aux_periods_before, list_aux_periods_after




      ######## i look at the edges with their first mistake before this period 
      for aux_period in list_aux_periods_before: 

         ###### i read the network for previous/next periods
         network_filename="../Results/Supply_network_slicing_monthly_period_"+str(aux_period)+"_no_network_metrics.pickle"
         G_period = pickle.load(open(network_filename, 'rb'))    



         ##### i look for the currently inf. links in the previous networks  
         for edge in dict_period_dict_edges_month_first_errors[period]:  

            e1=edge[0]     # the ends of the current link                            
            e2=edge[1]                
            
            try:
               weight= G_period.edge[e1][e2]["pos_weight"]
               list_amounts_edges_before.append(weight)

            except KeyError:  # if the link didnt exist in the other period
               pass#weight=0      
           

         for firm in dict_period_dict_firms_month_first_errors[period]:
            try:
               weight= G_period.node[firm]["vol_pos_transct"]
               list_amounts_firms_before.append(weight)
            except KeyError:  # if the node didnt exist in the other period
               pass#weight=0         
           




      ####### i look at the edges with their first mistake after this period 
      for aux_period in list_aux_periods_after:

         ###### i read the network for previous/next periods
         network_filename="../Results/Supply_network_slicing_monthly_period_"+str(aux_period)+"_no_network_metrics.pickle"
         G_period = pickle.load(open(network_filename, 'rb'))    



         ##### i look for the currently inf. nodes in the previous networks  
         for edge in dict_period_dict_edges_month_first_errors[period]:  

            e1=edge[0]     # the ends of the current link                            
            e2=edge[1]                
            
            try:
               weight= G_period.edge[e1][e2]["pos_weight"]
               list_amounts_edges_after.append(weight)
            except KeyError:  # if the link didnt exist in the other period
               pass#weight=0   
           




         for firm in dict_period_dict_firms_month_first_errors[period]:
            try:
               weight= G_period.node[firm]["vol_pos_transct"]
               list_amounts_firms_after.append(weight)
      
            except KeyError:  # if the node didnt exist in the other period
              pass# weight=0         
           

    


   print "KS for list amounts for edges before vs after:", scipy.stats.ks_2samp(list_amounts_edges_before, list_amounts_edges_after)
   print "(D,p), where null hypothesis that 2 independent samples are drawn from the same continuous distribution"
         #KS test Returns:	
              #D : float, KS test statistic
              #p-value : float, One-tailed or two-tailed p-value.
              #This is a two-sided test for the null hypothesis that 2 independent samples are drawn from the same continuous distribution.


   Nbins=100
   path_name_h="../Results/Hist_amount_transactions_edges_before_error_time_window"+str(time_window)+".dat"
   histogram_bins_increasing.histogram(list_amounts_edges_before,Nbins, path_name_h)


   path_name_h="../Results/Hist_amount_transactions_edges_after_error_time_window"+str(time_window)+".dat"
   histogram_bins_increasing.histogram(list_amounts_edges_after,Nbins, path_name_h)





   print "KS for list amounts for firms before vs after:", scipy.stats.ks_2samp(list_amounts_firms_before, list_amounts_firms_after)
   print "(D,p), where null hypothesis that 2 independent samples are drawn from the same continuous distribution"

   path_name_h="../Results/Hist_amount_transactions_firms_before_error_time_window"+str(time_window)+".dat"
   histogram_bins_increasing.histogram(list_amounts_firms_before,Nbins, path_name_h)


   path_name_h="../Results/Hist_amount_transactions_firms_after_error_time_window"+str(time_window)+".dat"
   histogram_bins_increasing.histogram(list_amounts_firms_after,Nbins, path_name_h)




   exit()


   list_previously_inf=[]
   dict_month_list_firms_last_month={}         
   for month_index in range(250):
      month_index +=1

      dict_month_list_firms_last_month[month_index]=[]

      for firm in dict_firm_id_last_month_index:        

         if int(dict_firm_id_last_month_index[firm]) == int(month_index):            
            if firm not in dict_month_list_firms_last_month[month_index]:
               dict_month_list_firms_last_month[month_index].append(firm) 




   cont_cumulat=0
   dict_month_prob_going_ext={}
   dict_month_prob_going_ext_if_inf={}
   dict_month_prob_going_ext_if_NOT_inf={}

   for month in sorted(dict_month_list_firms_last_month):
      cont_cumulat += len(dict_month_list_firms_last_month[month])
      # print month, dict_month_index_num_firms_going_extinct[month], cont_cumulat
         
      list_inf_firms_going_ext=[]
      list_NON_inf_firms_going_ext=[]
      for firm in dict_month_list_firms_last_month[month]:

         flag_firm_presente=0  #  whether the firm is in the list of infected ones for that period  or not
         for link in  dict_periods_list_inf_links[month]:
            e1=link[0]
            e2=link[1]
          #  print e1, e2, firm
            if firm  ==e1  or firm == e2:               
               flag_firm_presente=1
              

         if  flag_firm_presente == 1:           
            if firm not in  list_inf_firms_going_ext:
               list_inf_firms_going_ext.append(firm)
         else:
            if firm not in list_NON_inf_firms_going_ext:
               list_NON_inf_firms_going_ext.append(firm)
               

     # print month,  len(list_inf_firms_going_ext), len(list_NON_inf_firms_going_ext),  len(dict_month_list_firms_last_month[month])













      try:
         dict_month_prob_going_ext[month]=float(len(dict_month_list_firms_last_month[month])) / float(len(dict_month_index_list_active_firms[month]))         
     


         dict_month_prob_going_ext_if_inf[month] = float(len(list_inf_firms_going_ext)) / float(len(dict_month_index_list_active_firms[month]))         
         try:
            prob_going_ext_if_inf_norm_by_tot_last_month =  float(len(list_inf_firms_going_ext)) / len(dict_month_list_firms_last_month[month])
         except: 
            prob_going_ext_if_inf_norm_by_tot_last_month ="NA"


         dict_month_prob_going_ext_if_NOT_inf[month] = float(len(list_NON_inf_firms_going_ext)) / float(len(dict_month_index_list_active_firms[month]))         
         try:         
            prob_going_ext_if_NON_inf_norm_by_tot_last_month =  float(len(list_NON_inf_firms_going_ext)) / len(dict_month_list_firms_last_month[month])
         except:
            prob_going_ext_if_NON_inf_norm_by_tot_last_month = "NA"

       
        # print month, dict_month_prob_going_ext[month], dict_month_prob_going_ext_if_inf[month], 
#                  1            2                                3
#prob_going_ext_if_inf_norm_by_tot_last_month, dict_month_prob_going_ext_if_NOT_inf[month], prob_going_ext_if_NON_inf_norm_by_tot_last_month
#        4                                                     5                                              6
       
         print >> file5, month, dict_month_prob_going_ext[month], dict_month_prob_going_ext_if_inf[month], prob_going_ext_if_inf_norm_by_tot_last_month, dict_month_prob_going_ext_if_NOT_inf[month], prob_going_ext_if_NON_inf_norm_by_tot_last_month

      except KeyError: pass
      


   file5.close()
   print "written:", filename5



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

