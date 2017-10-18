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


def main():



    path="../Data/95_05NYCgamentdata/"
 

    initial_year=1985
    final_year=2005
 
    first_day_history=dt.datetime(1985,1,1)
    last_day_history= dt.datetime(2005,12,31)


    flag_cohort=1  # to only consider firms from the cohort, or every firm


    string_cohort=""
    if flag_cohort==1:
        string_cohort="_cohort_"




    slicing="monthly"    #"monthly"  # or "yearly"

    flag_remove_selfloops="YES"


    list_firms_cohort = pickle.load(open("../Results/list_1985_cohort_firms.pickle")) 
    


    list_jobbers_tot = pickle.load(open("../Results/List_jobbers_tot.dat")) 
    
    list_periods=[]
    list_firm_ids=[]

  
  

    #### to do further slicing of the data into months (instead or years)
    list_starting_date_marks=[]
    y= initial_year
    if  slicing=="monthly":
        while y <= final_year:
            aux_day=1
            aux_month=1
            aux_year=y                    
            while aux_month <= 12:           
                aux_date=dt.datetime(aux_year, aux_month, aux_day)
                list_starting_date_marks.append(aux_date)            
                aux_month += 1    
            y +=1

    elif slicing=="yearly":
         aux_day=1
         aux_month=1
         aux_year=y               
         while aux_year <= final_year:                                
             aux_date=dt.datetime(aux_year, aux_month, aux_day)
             list_starting_date_marks.append(aux_date)                    
             aux_year +=1
            
    else:
        print "wrong slicing"
        exit()



    list_manuf_tot=[]  # list all manuf, and contr (excluding any selftransaction)
    list_contr_tot=[]

    list_sizes_inf_components_tot=[]
    list_sizes_inf_components_tot_threshold=[]
    cont_periods=0
    ############# loop over periods
    for mark_date_initial in list_starting_date_marks:  

        cont_periods +=1    


        current_year=mark_date_initial.year
        current_month=mark_date_initial.month

     

        if current_month == 1:
            G=nx.Graph()   ##  this is the cumulative network including all transactions within that year, until the current period




        if  slicing=="monthly":
            mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   
        elif slicing=="yearly":
            mark_date_final =  mark_date_initial + dt.timedelta(days = 365)     

      
     

        print "\n\n",cont_periods, "period dates:  ",mark_date_initial, "  to  ", mark_date_final 


        G_period=nx.Graph()   ##  this is the cumulative network including all transactions during time period t


        ##################  
        ####### input datafile:    (I NEED TO READ IT EVERY TIME, BECAUSE IT GETS EMPTY EVERY TIME AFTER ITERATING OVER IT)
        name0="fhistory_ALL.csv"
     
        
        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
        cont=1       
        csvfile=open(path+name0, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   # to skip the header
             
        for list_row in reader:   
           #print cont             
           cont +=1
           flag_ignore_row=0
          
           try:
               adj_gross=int(round(float((list_row[4]))))    
           except ValueError:  # there a few rows missing the value for $$
               flag_ignore_row=1
              
              

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
          
           ###### i skip the rest of the file if the date is later than the window i am looking at (the datafile is shorted chronologically)
           if year > current_year:              
               break 


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



           ###### i calculate the time inverval for the current transaction
           period=(final_date_transaction-initial_date_transaction).days                
           if period < 0:
               old_initial=initial_date_transaction
               old_final=final_date_transaction   #####  some time periods have interved TO and FROM dates!
               initial_date_transaction =final_date_transaction
               final_date_transaction = old_initial
            
             



           ###### i creat a list with all dates included in the transaction period, for comparison purposes
           list_dates_transaction=[]
           aux_date_trans= initial_date_transaction #+ dt.timedelta(days = 1) 
           while aux_date_trans <= final_date_transaction:                              
               list_dates_transaction.append(aux_date_trans)
               aux_date_trans += dt.timedelta(days = 1)   

    
           try:
             #########  i establish whether the transaction belongs to the sliced network
             flag_include_transaction=0
             if  (mark_date_initial in list_dates_transaction)  or (mark_date_final in list_dates_transaction):
               flag_include_transaction= 1  # transaction to be included
          

             if  (mark_date_initial >= list_dates_transaction[0])  and (mark_date_final <= list_dates_transaction[-1]): 
               flag_include_transaction= 1   # transaction longer than the slicing period (to be included)
           

             if  (mark_date_initial <= list_dates_transaction[0])  and (mark_date_final >= list_dates_transaction[-1]): 
               flag_include_transaction= 1     # transaction shorter and all-inside the the slicing period (to be included)
      

           except IndexError:  # for one-day transactions:
            

              new_list_dates_transaction=[]
              aux_date_trans= initial_date_transaction 
              new_list_dates_transaction.append(aux_date_trans)
              
              while aux_date_trans <= final_date_transaction:                              
                  aux_date_trans += dt.timedelta(days = 1)   
                  new_list_dates_transaction.append(aux_date_trans)
                  
             

              if  (mark_date_initial in new_list_dates_transaction)  or (mark_date_final in new_list_dates_transaction):
                  flag_include_transaction= 1  # transaction to be included
                
              if  (mark_date_initial <= new_list_dates_transaction[0])  and (mark_date_final >= new_list_dates_transaction[-1]): 
                  flag_include_transaction= 1     # transaction shorter and all-inside the the slicing period (to be included)
                 

                

           if flag_include_transaction ==0:
               flag_ignore_row= 1 





           try:   #  some lines are missing the contractor or manufacturer: skip                
              flag_manuf_jobber=0
              flag_contr_jobber=0
                
              manufacturer=int(list_row[0])     ##paidbyfirm
              contractor=int(list_row[1])      ## paidforfirm                                
                
                
              if manufacturer in list_jobbers_tot:
                    flag_manuf_jobber=1
              if contractor in list_jobbers_tot:
                    flag_contr_jobber=1

                 
              if manufacturer == contractor:                  
                  if flag_remove_selfloops=="YES":
                      flag_ignore_row=1
                        

              #####to build networks that include only the firms in the cohort
              if  flag_cohort==1:
                   if manufacturer not in list_firms_cohort     or   contractor not in list_firms_cohort: 
                       flag_ignore_row=1




              ##### i only look at the rows of the datafile for dates corresponding to the current observation period
              if  flag_ignore_row ==0:


                       G_period.add_node(manufacturer)
                       G_period.add_node(contractor)
                       G_period.add_edge(manufacturer,contractor)

                       G.add_node(manufacturer)
                       G.add_node(contractor)
                       G.add_edge(manufacturer,contractor)


                       if adj_gross < 0.:            
                           try:          
                               G_period.node[manufacturer]["neg_weight"] += adj_gross               
                           except :
                               G_period.node[manufacturer]["neg_weight"] = adj_gross      
                           try:
                               G_period.node[contractor]["neg_weight"] += adj_gross      
                           except :
                               G_period.node[contractor]["neg_weight"] = adj_gross      

                           try:
                               G.node[manufacturer]["neg_weight"] += adj_gross               
                           except :
                               G.node[manufacturer]["neg_weight"]= adj_gross      
                           try:                               
                               G.node[contractor]["neg_weight"] += adj_gross      
                           except :
                               G.node[contractor]["neg_weight"] = adj_gross      
         

                       else:
                           try:   
                               G_period.node[manufacturer]["pos_weight"] += adj_gross               
                           except :
                               G_period.node[manufacturer]["pos_weight"] = adj_gross
                           try:   
                               G_period.node[contractor]["pos_weight"] += adj_gross      
                           except :
                               G_period.node[contractor]["pos_weight"] = adj_gross      

                           try:   
                               G.node[manufacturer]["pos_weight"] += adj_gross               
                           except :
                                G.node[manufacturer]["pos_weight"] = adj_gross      
                           try:   
                               G.node[contractor]["pos_weight"] += adj_gross      
                           except :
                               G.node[contractor]["pos_weight"] = adj_gross      
                       

                       if flag_manuf_jobber ==0:
                               G.node[manufacturer]["type"] = "manuf"
                               G_period.node[manufacturer]["type"] = "manuf"
                       else:
                               G.node[manufacturer]["type"] = "jobber"
                               G_period.node[manufacturer]["type"] = "jobber"

                       if flag_contr_jobber ==0:
                               G.node[contractor]["type"] = "contr"
                               G_period.node[contractor]["type"] = "contr"
                       else:
                               G.node[contractor]["type"] = "jobber"
                               G_period.node[contractor]["type"] = "jobber"
                                                                                      








           except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer 
            
          



        
        print " # nodes in G_period:", len(G_period.nodes()), " # edges in G_period:", len(G_period.edges())

             
        ########  write the monthly  network
        filename_network="../Results/Simplified_supply_network_slicing_"+slicing+"_period_"+str(cont_periods)+string_cohort
        pickle.dump(G_period, open(filename_network+".pickle", 'wb'))
        print "  written", filename_network+".pickle"

     


        print " Aggregated network:  # nodes in G:", len(G.nodes()), " # edges in G:", len(G.edges())




        ########  write the aggregated network   
        filename_network="../Results/Simplified_supply_network_yearly_acummlate_until_period_"+str(cont_periods)+string_cohort
        pickle.dump(G, open(filename_network+".pickle", 'wb'))
        print "written", filename_network+".pickle"

    



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

