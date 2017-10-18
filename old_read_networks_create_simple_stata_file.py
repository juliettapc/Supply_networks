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



    slicing="monthly"    #"monthly"  # or "yearly"

    flag_remove_self_trans="YES"

    list_jobbers_tot = pickle.load(open("../Results/List_jobbers_tot.dat")) 
    
    list_missing_nodes=[]
  



    ######  output file:
    name6="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_"+slicing+"_slicing.dat"
    file6= open(name6, 'wt') 

        # header for the file:                                 
    print >> file6,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans", "start_date", "start_time", "end_date","end_time", "period_start","period_end", "length_period", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "k_M_init", "k_M_fin", "k_C_init", "k_C_fin", "k_M_init_acumm", "k_M_fin_acumm", "k_C_init_acumm", "k_C_fin_acumm" 






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



    dict_period_network_period={}
    dict_period_network_accumulate_year={}

    dict_period_mark_initial_final_date={}

    dict_day_from_85_1_1_period ={}

    cont_periods_aux=1
    for mark_date_initial in list_starting_date_marks:  

        try:
            network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(cont_periods_aux)+".pickle"
            G_period = pickle.load(open(network_period, 'rb'))  
            dict_period_network_period[cont_periods_aux]=G_period

            network_accumulate_year="../Results/Simplified_supply_network_yearly_acummlate_until_period_"+str(cont_periods_aux)+".pickle"
            G = pickle.load(open(network_accumulate_year, 'rb'))  
            dict_period_network_accumulate_year[cont_periods_aux]=G


            if  slicing=="monthly":
                mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   
            elif slicing=="yearly":
                mark_date_final =  mark_date_initial + dt.timedelta(days = 365)     


            dict_period_mark_initial_final_date[cont_periods_aux]=(mark_date_initial, mark_date_final)


        except IOError: pass


        ###### i get a dict to immediately know the period a day belongs to (from the starting date: 1-1-1985)
        aux_date_dict = mark_date_initial
        while aux_date_dict  <= mark_date_final:                        
            day_from_85_1_1 = (aux_date_dict - first_day_history).days
            dict_day_from_85_1_1_period[day_from_85_1_1] = cont_periods_aux
            aux_date_dict += dt.timedelta(days = 1)   
          #  print day_from_85_1_1 , cont_periods_aux0
        cont_periods_aux += 1


   




    dict_micj_dict_dates_aggregate_trans={}
    
    ####### i read the input datafile:    
    ####################
    name0="fhistory_ALL.csv"        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
    cont=0  
    cont_valid=0    
    cont_non_valid=0    
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
           if period < 0:
               old_initial=initial_date_transaction
               old_final=final_date_transaction   #####  some time periods have interved TO and FROM dates!
               initial_date_transaction =final_date_transaction
               final_date_transaction = old_initial
                         

           try:     
            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm                                
                
                 
            if manufacturer == contractor:                  
                if flag_remove_self_trans=="YES":
                    flag_ignore_row=1
                        
                     

            p_inf=0                
            adj_gross=int(round(float((list_row[4]))))     ### i deal with integer Dollars !!  (easier for histograms and comparisons)
            if adj_gross <0:
                p_inf =1
                cont_neg_all +=1
                list_micj_with_neg.append(mi_cj)



            if  flag_ignore_row ==0:

                cont_valid +=1
                if adj_gross <0:
                    cont_neg +=1

                mi_cj=str(manufacturer) + str(contractor)


               
              
                #### i get an index for the presence of jobbers in the transaction
                flag_manuf_jobber=0
                flag_contr_jobber=0
                if manufacturer in list_jobbers_tot:
                    flag_manuf_jobber=1
                if contractor in list_jobbers_tot:
                    flag_contr_jobber=1
           
                MCJ=0         #  1: mc     2: jc     3: mj     4: jj
                if flag_manuf_jobber ==0:
                    if flag_contr_jobber ==0:
                        MCJ=1
                    else:
                        MCJ=3                    
                else:
                    if flag_contr_jobber ==0:
                        MCJ=2
                    else:
                        MCJ=4



                
                try:        
                    ########## i look for the corresponding networks for the beginning and end of the transact.
                    day_from_85_1_1_init_transaction = (initial_date_transaction  - first_day_history).days
                    period_init_transaction = dict_day_from_85_1_1_period[day_from_85_1_1_init_transaction] 
                    G_period_init_transaction=dict_period_network_period[period_init_transaction]
                    
                    
                    day_from_85_1_1_fin_transaction = (final_date_transaction  - first_day_history).days
                    period_fin_transaction = dict_day_from_85_1_1_period[day_from_85_1_1_fin_transaction] 
                    G_period_fin_transaction=dict_period_network_period[period_fin_transaction]
                    


                    G_init_transaction=dict_period_network_accumulate_year[period_init_transaction]
                    G_fin_transaction=dict_period_network_accumulate_year[period_fin_transaction]


                  
                  
                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj]
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj]={}

                 

                    tuple_dates=(initial_date_transaction, final_date_transaction)
                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]={}




                    ####### OJO!!! chequear posible sobreescritura!!!
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["mi"]=manufacturer
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["cj"]=contractor
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["MCJ"]=MCJ
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["init_period"]=period_init_transaction
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["fin_period"]=period_fin_transaction
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["length"]= (period_fin_transaction- period_init_transaction + 1)

                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["num_trans"] += 1
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["num_trans"] =1

                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["net_adj_gross"] +=adj_gross
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["net_adj_gross"] =adj_gross


                   
                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_pos_gross"] 
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_pos_gross"] = 0.


                    try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_neg_gross"] 
                    except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_neg_gross"] = 0.



                    if adj_gross >=0:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_pos_gross"] +=adj_gross
                    else:                       
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_neg_gross"] +=adj_gross
                      
                  
                   
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["p_inf"]= 0
                    if dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["tot_neg_gross"]  <0:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["p_inf"]= 1



                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["degree_m_init"]=G_period_init_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["degree_m_fin"]=G_period_fin_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["degree_c_init"]= G_period_init_transaction.degree(contractor)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["degree_c_fin"]=G_period_fin_transaction.degree(contractor)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["cumm_degree_m_init"]=G_init_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["cumm_degree_m_fin"]= G_fin_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["cumm_degree_c_init"]= G_init_transaction.degree(contractor)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tuple_dates]["cumm_degree_c_fin"]= G_fin_transaction.degree(contractor)
                                        
                   


                except: #nx.exception.NetworkXError:  # some nodes are missing (around 160)
                    list_missing_nodes.append(manufacturer)
                    list_missing_nodes.append(contractor)
                    cont_non_valid +=1

          







           except ValueError:   pass #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
            
          

    cont_entries=0
    cont_faulty_entries=0
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
        dicc=dict_micj_dict_dates_aggregate_trans[mi_cj]
      

       
        for date  in sorted(dicc):                        
           
            try:
                fract=abs(dicc[date]["tot_neg_gross"])/dicc[date]["tot_pos_gross"]
            except ZeroDivisionError:
                fract=0.

            try:
                print >> file6,  dicc[date]["p_inf"], dicc[date]["mi"], dicc[date]["cj"], mi_cj, dicc[date]["MCJ"], dicc[date]["num_trans"],date[0], date[1], dicc[date]["init_period"],dicc[date]["fin_period"], dicc[date]["length"],dicc[date]["net_adj_gross"], dicc[date]["tot_pos_gross"], dicc[date]["tot_neg_gross"] , fract ,  dicc[date]["degree_m_init"], dicc[date]["degree_m_fin"], dicc[date]["degree_c_init"], dicc[date]["degree_c_fin"], dicc[date]["cumm_degree_m_init"], dicc[date]["cumm_degree_m_fin"],  dicc[date]["cumm_degree_c_init"], dicc[date]["cumm_degree_c_fin"]




            except KeyError:               #degree_c_fin
                cont_faulty_entries +=1
               
                                                                      
            cont_entries +=1



 
    file6.close()
    print "\n\nwritten file:",name6

   
    
    #list_micj_with_neg =list(set(list_micj_with_neg))
   



       


    print "num. trans:", cont, "  num valid trans:", cont_valid,  cont_valid/float(cont)
    print "num entries in aggregated dict:", cont_entries
    print "num. unique micj with neg trans:", len(list_micj_with_neg)
    print "num neg. trans:", cont_neg_all, ",  which is",float(cont_neg_all)/cont*100,"% of all transactions"
    print "num neg. trans (excluding self):", cont_neg, ",  which is",float(cont_neg)/cont*100,"% of all transactions"
    print "num. incomplete dict. entries:", cont_faulty_entries , float(cont_faulty_entries )/cont_entries
   
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
