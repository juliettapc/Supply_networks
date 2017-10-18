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


def main():

  
   filename_pickle="../Results/dict_firm_id_last_date_month_index.pickle"
   print "reading:", filename_pickle
   dict_firm_id_last_month_index = pickle.load(open(filename_pickle, 'rb'))
   print "  done."


   filename_pickle2="../Results/dict_periods_list_inf_links.pickle"
   print "reading:", filename_pickle2
   dict_periods_list_inf_links = pickle.load(open(filename_pickle2, 'rb'))
   print "  done."


   #filename_pickle3="../Results/dict_periods_dict_links_list_neighboring_links.pickle"
   #print "reading:", filename_pickle3
   #dict_periods_dict_links_list_neighboring_links = pickle.load(open(filename_pickle3, 'rb'))
   #print "  done."


   filename_pickle4="../Results/dict_month_index_list_active_firms.pickle"
   print "reading:", filename_pickle4
   dict_month_index_list_active_firms = pickle.load(open(filename_pickle4, 'rb'))
   print "  done."






   ########  output file
   filename5="../Results/Time_evol_prob_going_extinct.dat"
   file5 = open(filename5,'wt')



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

