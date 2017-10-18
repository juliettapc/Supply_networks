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



    path="../Data/95_05NYCgamentdata/"
 

    initial_year=1985
    final_year=2005
 
    first_day_history=dt.datetime(1985,1,1)
    last_day_history= dt.datetime(2005,12,31)

    string_cohort="1996"


    year_for_cohort=int(string_cohort)
    first_join_date_cohort=dt.datetime(year_for_cohort,1,1)  # i am gonna create a set of firms that are active all the time, and follow them
    last_join_date_cohort=dt.datetime(year_for_cohort,12,31)


    list_all_firms=[]
    dict_firm_id_list_trans_dates={}
    dict_year_list_active_firms={}
    dict_micj_list_trans_dates={}
  
    flag_remove_self_trans="YES"


    print "dates for recruiting cohort:", first_join_date_cohort, " - ", last_join_date_cohort


    
    ####### i read the input datafile:    
    ####################
    name0="fhistory_ALL.csv"        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
    cont=0  
    cont_valid=0    
    cont_neg_all=0
    cont_neg=0  # excluding self-trans.
    list_micj_with_neg=[]
    dict_year_num_unique_micj={}


    csvfile=open(path+name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
    

    for list_row in reader:                
           cont +=1
           flag_ignore_row=0  # i will ignore it if missing mi_cj indexes, or if it is a self-transaction
          

           ########### initial date for transaction period
           from_date=list_row[2]       # format examples  040185         #010185                      
           if len(from_date) <6:                   
               from_date="0"+from_date   # when the date is 40185  instead of 040185

           month=int(from_date[:2])
           day=int(from_date[-4:-2])               
           year=int(from_date[-2:])
           
           if year > 80:
               year += 1900
           else:
               year += 2000
       
           try:
               initial_date_transaction=dt.datetime(year, month, day)
           except ValueError: # there are a bunch of incorrect dates!!!  043185   063185     113185   023185
               day =1
               month +=1                
               initial_date_transaction=dt.datetime(year, month, day)
          


           ########### final date for transaction period
           to_date=list_row[3]
           if len(to_date) <6:   # when the date is 40185  instead of 040185
               to_date="0"+to_date

           month=int(to_date[:2])
           day=int(to_date[-4:-2])
           year=int(to_date[-2:])

           if year > 80:
               year += 1900
           else:
               year += 2000

           if year == 2030:
               year = 2003  # there are a bunch of entries with impossible year: 13201742,13200981,40103,63030,-0.18,-18,

           try:
               final_date_transaction=dt.datetime(year, month, day)
           except ValueError:   # there are a bunch of incorrect dates!!!  043185   063185     113185   023185  
               day =1
               month +=1
               try:               
                   final_date_transaction=dt.datetime(year, month, day)
               except ValueError:
                   flag_ignore_row= 1   # there is at least one month = 21    213101



         


           ###### i calculate the time inverval for the current transaction and FLIP it if need be
           period=(final_date_transaction-initial_date_transaction).days                
           if period < 0:   #####  some time periods have interved TO and FROM dates!
               old_initial=initial_date_transaction
               old_final=final_date_transaction   
               initial_date_transaction =final_date_transaction
               final_date_transaction = old_initial
                         

           ### the hazard model doesnt like trans. ending the same day they start    (there are about 260 of them)
           if final_date_transaction == initial_date_transaction:  
               final_date_transaction += dt.timedelta(days = 1)    




           try:     #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
             manufacturer=int(list_row[0])     ##paidbyfirm
             contractor=int(list_row[1])      ## paidforfirm                                
                                 
              


           
             if manufacturer != contractor: # i exclude all self-trans (many companies do not have business with anyone else but themselves!!)
                list_all_firms.append(manufacturer)
                list_all_firms.append(contractor)
                    

 
                mi_cj=str(manufacturer) + "_"+ str(contractor)

                try:
                   dict_firm_id_list_trans_dates[manufacturer].append(initial_date_transaction)
                except KeyError:
                   dict_firm_id_list_trans_dates[manufacturer]=[]
                   dict_firm_id_list_trans_dates[manufacturer].append(initial_date_transaction)

                try:
                   dict_firm_id_list_trans_dates[contractor].append(initial_date_transaction)
                except KeyError:
                   dict_firm_id_list_trans_dates[contractor]=[]
                   dict_firm_id_list_trans_dates[contractor].append(initial_date_transaction)



                try:
                    dict_year_list_active_firms[year].append(manufacturer)
                    dict_year_list_active_firms[year].append(contractor)
                except KeyError:
                    dict_year_list_active_firms[year]=[]
                    dict_year_list_active_firms[year].append(manufacturer)
                    dict_year_list_active_firms[year].append(contractor)




                try:
                    dict_micj_list_trans_dates[mi_cj].append(initial_date_transaction)
                except KeyError:
                    dict_micj_list_trans_dates[mi_cj]=[]
                    dict_micj_list_trans_dates[mi_cj].append(initial_date_transaction)



                aux_year=initial_date_transaction.year
                try: 
                    dict_year_num_unique_micj[aux_year].append(mi_cj)
                except KeyError:
                    dict_year_num_unique_micj[aux_year] =[]
                    dict_year_num_unique_micj[aux_year].append(mi_cj)


           except ValueError:   pass #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
            








    dict_year_num_new_firms={}
    list_firms_cohort=[]
    for firm_id in sorted(dict_firm_id_list_trans_dates):

        date1=sorted(dict_firm_id_list_trans_dates[firm_id])[0]
        #print firm_id, len(dict_firm_id_list_trans_dates[firm_id]),  sorted(dict_firm_id_list_trans_dates[firm_id])       
        #print 
        year=date1.year

        try:
            dict_year_num_new_firms[year] +=1
        except KeyError:
            dict_year_num_new_firms[year] =1


        if date1 >= first_join_date_cohort  and date1 <= last_join_date_cohort:
            list_firms_cohort.append(firm_id)
           
            


    name_cohort_list="../Results/list_cohort_firms_"+string_cohort+".pickle"
    pickle.dump(list_firms_cohort, open(name_cohort_list, 'wb'))
    print "written:", name_cohort_list




    print "\nnum. firms in cohort:",len(list_firms_cohort)

    print " tot num. unique firms:",len(set(list_all_firms))



   
   
    dict_year_list_active_firms_from_cohort={}
    for year in sorted(dict_year_list_active_firms):
        dict_year_list_active_firms_from_cohort[year]=[]
        for firm in dict_year_list_active_firms[year]:
            if firm in list_firms_cohort:
                dict_year_list_active_firms_from_cohort[year].append(firm)


    print "active firms per year within cohort",string_cohort, "and total, and new firms:"
    for year in sorted(dict_year_list_active_firms_from_cohort):
        print year, len(set(dict_year_list_active_firms_from_cohort[year])),len(set(dict_year_list_active_firms[year])), dict_year_num_new_firms[year]



    list_micj_cohort=[]
   
    for micj in dict_micj_list_trans_dates:
        first_date=sorted(dict_micj_list_trans_dates[micj])[0]
        year = first_date.year
       

        if first_date >= first_join_date_cohort  and first_date <= last_join_date_cohort:
            list_micj_cohort.append(micj)
           
        
    






    num_trans_tot=0
    num_trans_tot_cohort=0
    dict_year_num_trans={}
    dict_year_num_trans_cohort={}
    dict_year_num_active_micj_cohort={}



    ####### i read the input datafile again:    
    ####################
    name0="fhistory_ALL.csv"        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
    cont=0  
    cont_valid=0    
    cont_neg_all=0
    cont_neg=0  # excluding self-trans.
    list_micj_with_neg=[]

    csvfile=open(path+name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
    

    for list_row in reader:                
           cont +=1
           flag_ignore_row=0  # i will ignore it if missing mi_cj indexes, or if it is a self-transaction
          

           ########### initial date for transaction period
           from_date=list_row[2]       # format examples  040185         #010185                      
           if len(from_date) <6:                   
               from_date="0"+from_date   # when the date is 40185  instead of 040185

           month=int(from_date[:2])
           day=int(from_date[-4:-2])               
           year=int(from_date[-2:])
           
           if year > 80:
               year += 1900
           else:
               year += 2000
       
           try:
               initial_date_transaction=dt.datetime(year, month, day)
           except ValueError: # there are a bunch of incorrect dates!!!  043185   063185     113185   023185
               day =1
               month +=1                
               initial_date_transaction=dt.datetime(year, month, day)
          


           ########### final date for transaction period
           to_date=list_row[3]
           if len(to_date) <6:   # when the date is 40185  instead of 040185
               to_date="0"+to_date

           month=int(to_date[:2])
           day=int(to_date[-4:-2])
           year=int(to_date[-2:])

           if year > 80:
               year += 1900
           else:
               year += 2000

           if year == 2030:
               year = 2003  # there are a bunch of entries with impossible year: 13201742,13200981,40103,63030,-0.18,-18,

           try:
               final_date_transaction=dt.datetime(year, month, day)
           except ValueError:   # there are a bunch of incorrect dates!!!  043185   063185     113185   023185  
               day =1
               month +=1
               try:               
                   final_date_transaction=dt.datetime(year, month, day)
               except ValueError:
                   flag_ignore_row= 1   # there is at least one month = 21    213101



         


           ###### i calculate the time inverval for the current transaction and FLIP it if need be
           period=(final_date_transaction-initial_date_transaction).days                
           if period < 0:   #####  some time periods have interved TO and FROM dates!
               old_initial=initial_date_transaction
               old_final=final_date_transaction   
               initial_date_transaction =final_date_transaction
               final_date_transaction = old_initial
                         

           ### the hazard model doesnt like trans. ending the same day they start    (there are about 260 of them)
           if final_date_transaction == initial_date_transaction:  
               final_date_transaction += dt.timedelta(days = 1)    




           try:     #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
               manufacturer=int(list_row[0])     ##paidbyfirm
               contractor=int(list_row[1])      ## paidforfirm                                
                                 
               mi_cj=str(manufacturer) + "_"+ str(contractor)


               if manufacturer != contractor:
                   try:
                       dict_year_num_trans[year] +=1
                   except KeyError:
                       dict_year_num_trans[year] =1


                   num_trans_tot +=1
    

                   if (manufacturer in list_firms_cohort     and      contractor in list_firms_cohort):
                       try:
                           dict_year_num_trans_cohort[year] +=1
                       except KeyError:
                           dict_year_num_trans_cohort[year] =1

                       num_trans_tot_cohort +=1

                   if mi_cj  in list_micj_cohort:
                      try:
                          dict_year_num_active_micj_cohort[year].append(mi_cj)
                      except KeyError:
                          dict_year_num_active_micj_cohort[year]=[]
                          dict_year_num_active_micj_cohort[year].append(mi_cj)




           except ValueError:   pass #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer




    print "num. trans. per year within the cohort",string_cohort, "and total:"
    for year in sorted(dict_year_num_trans_cohort):
        print year, dict_year_num_trans_cohort[year], dict_year_num_trans[year]
  

    print "\ntot num. trans in cohort and total:",  num_trans_tot_cohort, num_trans_tot 





    print "\n\n Num. unique active micj from the cohort:", string_cohort, " and total"
    for year in sorted(dict_year_num_active_micj_cohort):
        print year, len(set(dict_year_num_active_micj_cohort[year])), len(set(dict_year_num_unique_micj[year]))





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
