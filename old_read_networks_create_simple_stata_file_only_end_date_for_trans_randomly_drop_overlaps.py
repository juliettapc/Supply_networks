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



    flag_remove_overlap_randomly =1  # to deal with overlapping records


    slicing="monthly"    #"monthly"  # or "yearly"

    flag_remove_self_trans="YES"

    list_jobbers_tot = pickle.load(open("../Results/List_jobbers_tot.dat")) 
    
    list_missing_nodes=[]
  



    ######  output file:
    name6="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_"+slicing+"_slicing_only_end_date_dropped_overlaps_randomly_from_list.dat"
    file6= open(name6, 'wt') 

        # header for the file:                                 
    print >> file6,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans",  "start_date_trans","start_time_trans", "end_date_trans","end_time_trans", "first_day_trans","last_day_trans",  "length_trans", "period_end",  "first_date_mi_cj", "first_time_mi_cj", "first_day_mi_cj", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "k_M_fin", "k_C_fin",  "k_M_fin_acumm",  "k_C_fin_acumm" , "artificial_start_date_trans","artificial_start_time_trans", "overlap"



    name7="../Results/Removed_overlapping_records_from_simplified_stata_file_Pinf_vs_mulitiple_variables_"+slicing+"_slicing_only_end_date_dropped_overlaps_randomly.dat"
    file7= open(name7, 'wt') 

        # header for the file:                                 
    print >> file7,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans",  "start_date_trans","start_time_trans", "end_date_trans","end_time_trans", "first_day_trans","last_day_trans",  "length_trans", "period_end",  "first_date_mi_cj", "first_time_mi_cj", "first_day_mi_cj", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "k_M_fin", "k_C_fin",  "k_M_fin_acumm",  "k_C_fin_acumm" , "artificial_start_date_trans","artificial_start_time_trans", "overlap"




    
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

    dict_micj_first_date={}

    dict_day_period ={}

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



        

            ###### i get a dict to immediately know the period a day belongs to (from the starting date: 1-1-1985)
            aux_date_dict = mark_date_initial
            while aux_date_dict  <= mark_date_final:                        
                day = (aux_date_dict - first_day_history).days
                dict_day_period[day] = cont_periods_aux     # days:  1-7669  
                aux_date_dict += dt.timedelta(days = 1)   
                #  print day_from_85_1_1 , cont_periods_aux


        except IOError: pass

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
                         

           try:     #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm                                
                                 
            if manufacturer == contractor:                  
                if flag_remove_self_trans=="YES":
                    flag_ignore_row=1
                        
                    
            tupla_dates=(initial_date_transaction, final_date_transaction) 

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

                mi_cj=str(manufacturer) + "_"+ str(contractor)


               
              
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



                
                     
                ########## i look for the corresponding networks for the beginning and end of the transact.
                day_init_transaction = (initial_date_transaction  - first_day_history).days
                period_init_transaction = dict_day_period[day_init_transaction] 
                G_period_init_transaction=dict_period_network_period[period_init_transaction]
                    
               
                day_fin_transaction = (final_date_transaction  - first_day_history).days
                period_fin_transaction = dict_day_period[day_fin_transaction] 
                G_period_fin_transaction=dict_period_network_period[period_fin_transaction]
                                    
                   

                G_init_transaction=dict_period_network_accumulate_year[period_init_transaction]
                G_fin_transaction=dict_period_network_accumulate_year[period_fin_transaction]


                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj]
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj]={}

                 

                       #                    tuple_dates=(initial_date_transaction, final_date_transaction)
                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]  # i only consider the end_date for aggregating trans.
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]={}




                 ####### OJO!!! chequear posible sobreescritura!!!
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["mi"]=manufacturer
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cj"]=contractor
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["MCJ"]=MCJ
                   #dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["init_period"]=period_init_transaction
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["fin_period"]=period_fin_transaction

                aux_length=(final_date_transaction-initial_date_transaction).days   +1             
                try:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"] 
                except KeyError:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"] = aux_length

                if aux_length > dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"] :  # i keep only the length of the longest trans.
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"]  = aux_length



                try:  # i need to save the first time mi_cj work together, to use as enter() date in stata
                    dict_micj_first_date[mi_cj]
                except KeyError:
                    dict_micj_first_date[mi_cj]=initial_date_transaction
                if initial_date_transaction <  dict_micj_first_date[mi_cj]:
                    dict_micj_first_date[mi_cj]=initial_date_transaction


               
                try:   # i automatically aggregate all transactions with exactly the same micj, and start and end dates
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_trans"] += 1
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_trans"] =1

                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["net_adj_gross"] +=adj_gross
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["net_adj_gross"] =adj_gross


                   
                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] 
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] = 0.


                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"] 
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"] = 0.


                try:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["overlap"] +=1  # this accounts for exact overlap, not partial (see below for that)
                except KeyError:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["overlap"] = 0




                if adj_gross >=0:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] +=adj_gross
                else:                       
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"] +=adj_gross
                      
                  
                   
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf"]= 0
                if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"]  <0:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf"]= 1


 
                try:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"]= G_period_fin_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"]= G_period_fin_transaction.degree(contractor)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_m_fin"]= G_fin_transaction.degree(manufacturer)
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_c_fin"]= G_fin_transaction.degree(contractor)

                except:  # i few missing nodes, around 102
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"]= "NA"
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"]= "NA"
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_m_fin"]="NA"
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_c_fin"]= "NA"

                    cont_non_valid += 1
#                    print final_date_transaction, list_row, period, initial_date_transaction,final_date_transaction
                   
               





           except ValueError:   pass #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
            
          
   

    ########### first i need to check for overlapping records and remove one randomly from each pair
    if flag_remove_overlap_randomly ==1:                
        remove_overlapping_records_randomly(dict_micj_dict_dates_aggregate_trans,first_day_history, dict_micj_first_date,file7)
    




    ####### i write up the records
    cont_entries=0
    cont_faulty_entries=0
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
        dicc=dict_micj_dict_dates_aggregate_trans[mi_cj]      
       # print dicc
        #raw_input()


        for tupla_dates  in sorted(dicc):                        
            start_date_trans=tupla_dates[0]
            end_date_trans=tupla_dates[1]

            first_day=(start_date_trans-first_day_history).days
            end_day=(end_date_trans-first_day_history).days

            first_day_mi_cj=(dict_micj_first_date[mi_cj] - first_day_history).days
            artificial_start_date_trans= end_date_trans - dt.timedelta(days = 1)  

       
            try:
                fract=abs(dicc[tupla_dates]["tot_neg_gross"])/dicc[tupla_dates]["tot_pos_gross"]
            except ZeroDivisionError:               
                fract=0.

            if dicc[tupla_dates]["degree_m_fin"] !=  "NA":  ## a few missing nodes
   
                print >> file6,  dicc[tupla_dates]["p_inf"], dicc[tupla_dates]["mi"], dicc[tupla_dates]["cj"], mi_cj, dicc[tupla_dates]["MCJ"], dicc[tupla_dates]["num_trans"],start_date_trans, end_date_trans, first_day, end_day,  dicc[tupla_dates]["length"], dicc[tupla_dates]["fin_period"], dict_micj_first_date[mi_cj], first_day_mi_cj, dicc[tupla_dates]["net_adj_gross"], dicc[tupla_dates]["tot_pos_gross"], dicc[tupla_dates]["tot_neg_gross"] , fract , dicc[tupla_dates]["degree_m_fin"], dicc[tupla_dates]["degree_c_fin"], dicc[tupla_dates]["cumm_degree_m_fin"], dicc[tupla_dates]["cumm_degree_c_fin"], artificial_start_date_trans, dicc[tupla_dates]["overlap"]
                                                        
            cont_entries +=1

  
           


    print "num. trans originally:", cont, "  num valid trans (non-self trans):", cont_valid,  cont_valid/float(cont)
    print "num. unique micj with neg trans:", len(set(list_micj_with_neg))
    print "num neg. trans:", cont_neg_all, ",  which is",float(cont_neg_all)/cont*100,"% of all transactions"
    print "num neg. trans (excluding self):", cont_neg, ",  which is",float(cont_neg)/cont*100,"% of all transactions, and",float(cont_neg)/cont_entries*100, "of all valid entries"
    print "num. non-valid entries:",   cont_non_valid
    print "num. entries written:", cont_entries



    file6.close()
    print "\n\nwritten file:",name6



    file7.close()
    print "\n\nwritten file:",name7











#################################
###################################

def remove_overlapping_records_randomly(dict_micj_dict_dates_aggregate_trans,first_day_history, dict_micj_first_date,file7):
    
    list_records_with_overlap=[]
    cont_records= 0
    cont_removed_records =0
   
      for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
                    
        for tupla_dates  in dict_micj_dict_dates_aggregate_trans[mi_cj]:    
            cont_records +=1

        if len(dict_micj_dict_dates_aggregate_trans[mi_cj])>1:           
               
            flag_overlap, list_overlapping_pairs_periods = check_for_overlapping_micj(dict_micj_dict_dates_aggregate_trans[mi_cj],first_day_history)
                  
            for item in list_overlapping_pairs_periods:                

                r = random.choice([0,1])
                random_choice = item[r]  # i choose one of the periods from the overlapping pair                
                if r ==0:
                    non_choice=item[1]
                else:
                    non_choice=item[0]

                   
                for key in dict_micj_dict_dates_aggregate_trans[mi_cj].keys():   # if the value doesnt exist anymore, it doesnt complain
                    if dict_micj_dict_dates_aggregate_trans[mi_cj][key]["list_days"]== random_choice:                            
                            
                            try:  # i account for partial overlapping
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] +=1 
                            except KeyError:
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] =1

                            ########  before i remove it, i need to print out the removed records to a different file
                            tupla_dates=key
                            start_date_trans=tupla_dates[0]
                            end_date_trans=tupla_dates[1]
                            
                            first_day=(start_date_trans-first_day_history).days
                            end_day=(end_date_trans-first_day_history).days
                            
                            first_day_mi_cj=(dict_micj_first_date[mi_cj] - first_day_history).days
                            artificial_start_date_trans= end_date_trans - dt.timedelta(days = 1)  
                            
                            
                            try:
                                fract=abs(dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"])/dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"]
                            except ZeroDivisionError:               
                                fract=0.

                            if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"] !=  "NA":  ## a few missing nodes
   
                                print >> file7,  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["mi"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cj"], mi_cj, dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["MCJ"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_trans"],start_date_trans, end_date_trans, first_day, end_day,  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["fin_period"], dict_micj_first_date[mi_cj], first_day_mi_cj, dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["net_adj_gross"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"] , fract , dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_m_fin"], dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["cumm_degree_c_fin"], artificial_start_date_trans, dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["overlap"]


                            ######## i removed the selected record
                            del dict_micj_dict_dates_aggregate_trans[mi_cj][key]
                           

                            cont_removed_records +=1



                    elif dict_micj_dict_dates_aggregate_trans[mi_cj][key]["list_days"]== non_choice:  # i account for partial overlapping
                            try:
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] +=1 
                            except KeyError:
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] =1



                flag_overlap, list_overlapping_pairs_periods = check_for_overlapping_micj(dict_micj_dict_dates_aggregate_trans[mi_cj],first_day_history)

                if flag_overlap ==0:
                   # print "break"
                    break  # i stop removing transactions for that mi_cj if the overlap is gone
          



    print "cont records before",cont_records, "num removed records:", cont_removed_records, 
    cont_records= 0
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
        dicc=dict_micj_dict_dates_aggregate_trans[mi_cj]                 
        for tupla_dates  in dicc:    
            cont_records +=1
    print " cont records after:", cont_records



    

################################
################################

def check_for_overlapping_micj (dicc,first_day_history):

    flag_overlap=0
    list_overlapping_pairs_periods=[]
    if len(dicc)>1:   #  dicc= dict_micj_dict_dates_aggregate_trans[mi_cj]        
               
        list_periods=[]   
        list_keys =  list( dicc.keys())      # i cant shuffle a dict, but i can shuffle a list of its keys       
        random.shuffle(list_keys)
        
        for tupla_dates  in list_keys:
                    
                start_date_trans=tupla_dates[0]
                end_date_trans=tupla_dates[1]
                
                first_day=(start_date_trans-first_day_history).days
                end_day=(end_date_trans-first_day_history).days
                
                lista=[]
                aux_init=first_day
                while aux_init <= end_day:  # i create list of days to make the comparison of transaction periods easier
                    lista.append(aux_init)
                    aux_init +=1
                dicc[tupla_dates]["list_days"]= lista
                list_periods.append(lista)
                  
        for pair_periods in itertools.combinations(list_periods,2):
                lista1=pair_periods[0]
                lista2=pair_periods[1]

                if len(set(lista1) & set(lista2)) >0:  # if the two periods overlap at all
                    list_overlapping_pairs_periods.append(pair_periods)




    if len(list_overlapping_pairs_periods)>0:
        flag_overlap= 1

    return flag_overlap, list_overlapping_pairs_periods





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
