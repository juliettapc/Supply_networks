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
   time_window_before=1  # time a node needs to have been healthy before an infection
   time_window_after=10
  

 #  filename_pickle="../Results/dict_firm_id_last_date_month_index.pickle"
  # print "reading:", filename_pickle
   #dict_firm_id_last_month_index = pickle.load(open(filename_pickle, 'rb'))
   #print "  done."


   #filename_pickle2="../Results/dict_periods_list_inf_links.pickle"
   #print "reading:", filename_pickle2
   #dict_periods_list_inf_links = pickle.load(open(filename_pickle2, 'rb'))
   #print "  done."


   #filename_pickle3="../Results/dict_periods_dict_links_list_neighboring_links.pickle"
   #print "reading:", filename_pickle3
   #dict_periods_dict_links_list_neighboring_links = pickle.load(open(filename_pickle3, 'rb'))
   #print "  done."


   #filename_pickle4="../Results/dict_month_index_list_active_firms.pickle"
   #print "reading:", filename_pickle4
   #dict_month_index_list_active_firms = pickle.load(open(filename_pickle4, 'rb'))
   #print "  done."




   dict_edges_list_month_errors={}
   dict_firms_list_month_errors={}


  
   dict_period_edges={}
   dict_period_firms={}
  


   dict_period_dict_firm_equiv_non_inf_firm={}

   ########### i get the list of error-months for pairs and individual firms
   period=0
   while period <= final_period:
      period +=1
 
   
      ###### i read the actual network structure from the data
      network_filename="../Results/Supply_network_slicing_monthly_period_"+str(period)+"_no_network_metrics.pickle"
      G_period = pickle.load(open(network_filename, 'rb'))    



      dict_period_edges[period]=G_period.edges()
      dict_period_firms[period]=G_period.nodes()
  

      dict_period_dict_firm_equiv_non_inf_firm[period]={}

             # edges:   (9101202, 9101160, {'pos_weight': 64320, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 2.0, 'link_betweeness': 0.0, 'neg_weight': 0.0})

              #nodes:     (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 0, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0})


      for edge in G_period.edges():

         e1=edge[0]     # the ends of the current link                            
         e2=edge[1]                
         
         if int(G_period.edge[e1][e2]["num_neg_trans"]) >0:
            try:
               if period not in dict_edges_list_month_errors[edge]:
                  dict_edges_list_month_errors[edge].append(period) # if it already exists, i do nothing
            except KeyError:
               dict_edges_list_month_errors[edge]=[]
               dict_edges_list_month_errors[edge].append(period)
         

            try:
               if period not in dict_firms_list_month_errors[e1]:
                  dict_firms_list_month_errors[e1].append(period)
            except KeyError:
               dict_firms_list_month_errors[e1]=[]
               dict_firms_list_month_errors[e1].append(period)


            try:
               if period not in dict_firms_list_month_errors[e2]:
                  dict_firms_list_month_errors[e2].append(period)
            except KeyError:
               dict_firms_list_month_errors[e2]=[]
               dict_firms_list_month_errors[e2].append(period)





   ############## 

   dict_t_plusX_count_inf_firms={}
   dict_t_plusX_count_NON_inf_firms={}
   for i in range(time_window_after+1):
      dict_t_plusX_count_inf_firms[i]=0
      dict_t_plusX_count_NON_inf_firms[i]=0


   for firm in dict_firms_list_month_errors:
      print firm,   dict_firms_list_month_errors[firm]         



      for current_period in dict_firms_list_month_errors[firm]:
         print current_period

         #### i pick a random, equivalent firm, active on that period but not inf.
         flag_found=0
         while flag_found ==0:
            chosen_firm=random.choice(dict_period_firms[current_period])
            try:
               if current_period not in dict_firms_list_month_errors[chosen_firm]:
                  
                  if (current_period-1)  not in dict_firms_list_month_errors[chosen_firm]: # if not inf. in previous period either
                     dict_period_dict_firm_equiv_non_inf_firm[current_period][firm]=chosen_firm
                     flag_found=1

            except KeyError:  # if the chosen firm has no error record, i can use it as comparison too
               dict_period_dict_firm_equiv_non_inf_firm[current_period][firm]=chosen_firm
               flag_found=1




         ###### i create the list of previous-periods to check
         list_periods_previous=[]
         for i in range(time_window_before):
            list_periods_previous.append((current_period-i-1))

         ###### i create the list of after-periods to check 
         list_periods_after=[]
         for i in range(time_window_after):
            list_periods_after.append((current_period+i+1))

         print "periods after",  list_periods_after
        
         ##### i only consider current inf. IF NO previous inf.
         flag_inf=0
         for previous_period in list_periods_previous:
            if previous_period in dict_firms_list_month_errors[firm]:
               flag_inf=1
               break

         if flag_inf==0:
            dict_t_plusX_count_inf_firms[0] +=1  # i use this [0] as the norm

            flag_continue=1           
            for period_plusX in list_periods_after: 

               if period_plusX in dict_firms_list_month_errors[firm]:

                  if flag_continue==1 :  # to avoid cases like:  28 30   (missing 29, so it doesnt count as t+2)

                     dict_t_plusX_count_inf_firms[period_plusX-current_period] +=1
                     #print "  update"
               else:
                  flag_continue=0
                  #print "discontinuity"



            #### i compute the equivalent, non-inf case
            dict_t_plusX_count_NON_inf_firms[0] +=1
           
            equiv_firm= dict_period_dict_firm_equiv_non_inf_firm[current_period][firm]

            flag_continue=1    
            for period_plusX in list_periods_after: 

               try:

                  if period_plusX in dict_firms_list_month_errors[equiv_firm]:
                     
                     if flag_continue==1 :  # to avoid cases like:  28 30   (missing 29, so it doesnt count as t+2)
                        
                        dict_t_plusX_count_NON_inf_firms[period_plusX-current_period] +=1
                     #print "  update"
                  else:
                     flag_continue=0
                     #print "discontinuity"

               except KeyError: pass  # if the equivalent firm has no error record, it is ok




          

 
          
         print "dict_plusX:", dict_t_plusX_count_inf_firms
         print "dict_plusX non-inf:", dict_t_plusX_count_NON_inf_firms
         print 
      print 
      print 
      #raw_input()



   for period in dict_t_plusX_count_inf_firms:      
      print period, dict_t_plusX_count_inf_firms[period], dict_t_plusX_count_inf_firms[period]/float(dict_t_plusX_count_inf_firms[0]) , dict_t_plusX_count_NON_inf_firms[period], dict_t_plusX_count_NON_inf_firms[period]/float(dict_t_plusX_count_NON_inf_firms[0])













































   exit()

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
         for edge in dict_edges_list_month_errors:           
            if aux_period in dict_edges_list_month_errors[edge]:
               e1=edge[0]     # the ends of the current link                            
               e2=edge[1]                
               
               try:
                  weight= G_period.edge[e1][e2]["pos_weight"]
                  list_amounts_edges_before.append(weight)
                  
               except KeyError:  # if the link didnt exist in the other period
                  pass#weight=0      
           

         for firm in dict_firms_list_month_errors:
            if aux_period in dict_firms_list_month_errors[firm]:
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


         ##### i look for the currently inf. links in the previous networks  
         for edge in dict_edges_list_month_errors:           
            if aux_period in dict_edges_list_month_errors[edge]:
               e1=edge[0]     # the ends of the current link                            
               e2=edge[1]                
               
               try:
                  weight= G_period.edge[e1][e2]["pos_weight"]
                  list_amounts_edges_after.append(weight)
                  
               except KeyError:  # if the link didnt exist in the other period
                  pass#weight=0      
           

         for firm in dict_firms_list_month_errors:
            if aux_period in dict_firms_list_month_errors[firm]:
               try:
                  weight= G_period.node[firm]["vol_pos_transct"]
                  list_amounts_firms_after.append(weight)
               except KeyError:  # if the node didnt exist in the other period
                  pass#weight=0         
        
           

    


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

