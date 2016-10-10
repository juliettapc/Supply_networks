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


  
    flag_cohort=0  # to only consider firms from the cohort (usually 1985), or every firm

    string_cohort=""
    if flag_cohort==1:
        string_cohort="_cohort"
    print string_cohort




    flag_remove_self_trans="YES"




    flag_hurry=0   # 1:i skip some functions to quickly get to the part where i test others
    




    zs_threshold=2.

    slicing="monthly"    #"monthly"  # or "yearly"

   

    list_firms_cohort = pickle.load(open("../Results/list_cohort_firms_1995.pickle")) 
    


    list_jobbers_tot = pickle.load(open("../Results/List_jobbers_tot.dat")) 
    
    master_dict_year_dict_micj_zscore = pickle.load(open("../Results/dict_year_dict_micj_zscore_error_freq_controlling_year_degree.pickle")) # according to Yifang's randomization of data, preservig year. see Code/read_shuffling_data_add_zscore_to_hazard_file.py  ZSore for how likely it is that a link is infected a given year



    dict_year_dict_firmID_core_score = pickle.load(open("../Results/dict_year_dict_firmID_core_score.pickle")) # score for how stable (closer to 1.0) or unstable (closer to 1/tot_degree) the relationships of a firm are. See code:  core_score.py    # firm id is an int and so is year!!





    if  flag_hurry == 0 :
        print "reading dict. firm zip-code....."
        dict_firm_tuple_zip_code_state = pickle.load(open("../Results/dict_firm_id_zip_code.pickle", 'rb')) # example:  5188210: ('94108', 'CA')
        print "  done"

           #for item in dict_firm_tuple_zip_code_state:
           #   print item, dict_firm_tuple_zip_code_state[item], type(item),type(dict_firm_tuple_zip_code_state[item][0])
           #  raw_input()   #5111808 ('07072', 'NJ') <type 'int'> <type 'str'>
                       #5636243 ('NA', 'NA') <type 'int'> <type 'str'>



  
        print "reading dict. tuple zip-codes dist....."
        dict_tuple_zips_dist_miles= pickle.load(open("../Results/dict_zip_tuples_dist_miles_from_34Gb.pickle", 'rb'))  ### example:  (zip1,zip2): distance_mile
        print "  done"
        
           
             #    print item, dict_tuple_zips_dist_miles[item], type(item[0]), type(dict_tuple_zips_dist_miles[item])  #('20852', '75751') 1150.81406787 <type 'str'> <type 'float'>







    list_missing_nodes_main=[]
  
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


    list_pairs=[]
    list_firms=[]
    dict_period_network_period={}
    dict_period_network_accumulate_year={}

    dict_micj_first_date={}


    # i get all networks and into the dictionary
    dict_day_period ={}
    cont_periods_aux=1
    for mark_date_initial in list_starting_date_marks:  

        try:          
            network_period="../Results/Simplified_supply_network_slicing_"+str(slicing)+"_period_"+str(cont_periods_aux)+string_cohort+"_.pickle"
            G_period = pickle.load(open(network_period, 'rb'))  
            dict_period_network_period[cont_periods_aux]=G_period
          

            
            network_accumulate_year="../Results/Simplified_supply_network_yearly_acummlate_until_period_"+str(cont_periods_aux)+string_cohort+"_.pickle"
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

        except IOError: pass

        cont_periods_aux += 1


   

    print "in main loop to read datafile...."
    list_missing_nodes=[]
    dict_micj_dict_dates_aggregate_trans={}
    
    ####### i read the input datafile:    
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
                                 
            if manufacturer == contractor:                  
                if flag_remove_self_trans=="YES":
                    flag_ignore_row=1
                        
                    
            tupla_dates=(initial_date_transaction, final_date_transaction) 

                          
            adj_gross=int(round(float((list_row[4]))))     ### i deal with integer Dollars !!  (easier for histograms and comparisons)
            if adj_gross <0:           
                cont_neg_all +=1
                list_micj_with_neg.append(mi_cj)




            #####to build networks that include only the firms in the cohort
            if  flag_cohort==1:
                if manufacturer not in list_firms_cohort     or   contractor not in list_firms_cohort: 
                    flag_ignore_row=1








            if  flag_ignore_row ==0:

                cont_valid +=1
                if adj_gross <0:
                    cont_neg +=1

                mi_cj=str(manufacturer) + "_"+ str(contractor)


                list_pairs.append(mi_cj)
                list_firms.append(manufacturer)
                list_firms.append(contractor)

               
              
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
                #day_init_transaction = (initial_date_transaction  - first_day_history).days
                #period_init_transaction = dict_day_period[day_init_transaction] 
                #G_period_init_transaction=dict_period_network_period[period_init_transaction]
                    
               
                day_fin_transaction = (final_date_transaction  - first_day_history).days
                period_fin_transaction = dict_day_period[day_fin_transaction] 
                G_period_fin_transaction=dict_period_network_period[period_fin_transaction]
                                    
                   

                #G_init_transaction=dict_period_network_accumulate_year[period_init_transaction]
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
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["year"]=final_date_transaction.year



                length=(final_date_transaction-initial_date_transaction).days   +1             
                try:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"] 
                except KeyError:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["length"] = length



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



                ####### i add infection label to the nodes themselves                             
                try:
                    G_period_fin_transaction.node[manufacturer]["p_inf"]=0 
                    if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"]  <0:
                        G_period_fin_transaction.node[manufacturer]["p_inf"]=1                       
                except KeyError:  # missing node
                    list_missing_nodes_main.append(manufacturer)
                try:                   
                    G_period_fin_transaction.node[contractor]["p_inf"]=0
                    if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_neg_gross"]  <0:
                        G_period_fin_transaction.node[contractor]["p_inf"]=1
                except KeyError:  # missing node
                    list_missing_nodes_main.append(contractor)



                ###### i add pos and neg gross to the nodes
               
                if adj_gross >=0:
                    if manufacturer in G_period_fin_transaction.nodes():
                        try:                        
                            G_period_fin_transaction.node[manufacturer]['pos_transct'] +=adj_gross
                        except KeyError:
                            G_period_fin_transaction.node[manufacturer]['pos_transct'] =adj_gross

                    if contractor in G_period_fin_transaction.nodes():
                        try:                        
                            G_period_fin_transaction.node[contractor]['pos_transct'] +=adj_gross
                        except KeyError:
                            G_period_fin_transaction.node[contractor]['pos_transct'] =adj_gross


                else:
                    if manufacturer in G_period_fin_transaction.nodes():
                        try:
                            G_period_fin_transaction.node[manufacturer]['neg_transct'] +=adj_gross
                        except KeyError:                        
                            G_period_fin_transaction.node[manufacturer]['neg_transct'] =adj_gross
                    if contractor in G_period_fin_transaction.nodes():
                        try:
                            G_period_fin_transaction.node[contractor]['neg_transct'] +=adj_gross
                        except KeyError:                        
                            G_period_fin_transaction.node[contractor]['neg_transct'] =adj_gross






                if flag_hurry == 0:
                    populate_network_properties(dict_micj_dict_dates_aggregate_trans, G_period_fin_transaction,G_fin_transaction, manufacturer, contractor, mi_cj, tupla_dates)
                    calculate_degree_asym(G_period_fin_transaction, dict_micj_dict_dates_aggregate_trans, mi_cj, tupla_dates, manufacturer, contractor)
     

                 



           except ValueError:   pass #  some lines (very rare, one single instance) are missing the value for contractor or manufacturer 
            

  



    print "calculating business asym....."
    calculate_business_asym(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period)
             
   



    print 
    print
    print "# missing nodes (main)", len(list_missing_nodes_main), " unique:", len(set(list_missing_nodes_main))



    print "num. firms:",len(list_firms), " unique:", len(set(list_firms))
    print "num. pairs:",len(list_pairs), " unique:", len(set(list_pairs))
    


    print "calculating num. of m, c and j for each node, each network...."      
    calculate_num_manuf_contr(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period)





    if flag_hurry == 0:
        print "calculating min. dist. to inf...."
        calculate_min_dist_to_any_other_inf(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period)




    ########### first i need to check for overlapping records and remove one randomly from each pair
    if flag_remove_overlap_randomly ==1:

        try:
            pickle_name="../Results/list_randomly_removed_tuples_micj_dates_from_overlapping_records"+string_cohort+".pickle"
            list_removed_tuplas_micj_dates = pickle.load(open(pickle_name, 'rb'))
            print "loaded pickle with list of removed entries"
        except:
            print "list not found, obtaining list of removed entries....."
            list_removed_tuplas_micj_dates= remove_overlapping_records_randomly(dict_micj_dict_dates_aggregate_trans,first_day_history, dict_micj_first_date, slicing,string_cohort)
    else:
        list_removed_tuplas_micj_dates=[]




    ######### i get the accumulate values of net transactions and number of transactions for each mi_cj
    calculate_accumulate_transactions(dict_micj_dict_dates_aggregate_trans)


    if flag_hurry == 0:
        ######### i calculate prob inf previously and of neighbors etc  and modify the master dict
        print "calculating prob. prev. inf and adding to dict....."
        calculate_prob_inf_prev(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period,list_removed_tuplas_micj_dates)




    pickle_name="../Results/dict_micj_dict_dates_info_transactions"+string_cohort+".pickle"
    pickle.dump(dict_micj_dict_dates_aggregate_trans, open(pickle_name, 'wb'))
    print "written pickle master dict:", pickle_name

 




    print "writing up output datafile....."

    ####### i write up the records
             ##########  output file:
    name6="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_"+slicing+"_slicing_dropped_overlaps_randomly_from_list"+string_cohort+".dat"
    file6= open(name6, 'wt') 


        # header for the file:                                 
    print >> file6,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans",  "start_date_trans","start_time_trans", "end_date_trans","end_time_trans", "first_day_trans","last_day_trans",  "length_trans", "period_end",  "first_date_mi_cj", "first_time_mi_cj", "first_day_mi_cj", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "acumm_pos_gross","accum_num_trans","k_M_fin", "k_C_fin", "num_M_i","num_C_i","num_J_i", "num_M_j","num_C_j","num_J_j" ,  "k_M_fin_accum",  "k_C_fin_accum" , "artificial_start_date_trans","artificial_start_time_trans", "overlap", "year", "N", "L", "CC_m_fin","CC_c_fin","betweenness_m_fin","betweenness_c_fin","max_clique_size_m_fin","max_clique_size_c_fin","kshell_m_fin","kshell_c_fin","p_inf_prev_trans","accum_inf_prev_ij", "accum_inf_prev_neighb_i","frac_accum_inf_prev_neighb_i","accum_inf_prev_neighb_j","frac_accum_inf_prev_neighb_j","history_ij", "min_dist_i_to_inf", "avg_dist_i_to_inf", "min_dist_j_to_inf", "avg_dist_j_to_inf", "degree_asym_ij","business_asym_ij","zs_error_rate_ij_year_degree", "Dist","zip1", "zip2", "core_score_year_i", "core_score_year_j"
                                                                                        

                  


    #### (the file for removed entries is define inside the corresponding function)

    num_signif_trans=0
    not_found_micj=[]
    list_missing_firms_zcode=[]
    print "writing output file...."
    cont_entries=0
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
       dicc=dict_micj_dict_dates_aggregate_trans[mi_cj]            


       for tupla_dates  in sorted(dicc):    

         tupla_remove=(mi_cj, tupla_dates)

         if tupla_remove not in list_removed_tuplas_micj_dates:
                    
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

                 

            ### for the error rate of a given ij pair to be significantly diff. from random that year           
            year=int(dicc[tupla_dates]["year"] )
            try:
                zscore=master_dict_year_dict_micj_zscore[year][mi_cj]
            except KeyError:
                not_found_micj.append(mi_cj)
                zscore=0.0000  

            print mi_cj,tupla_dates, zscore
            if zscore > zs_threshold or zscore  < -1.*zs_threshold:
               # print mi_cj,tupla_dates, zscore
                num_signif_trans +=1



            ######### for the core score (stable vs. fluctuation relationships)

            manufacturer = int(mi_cj.split("_")[0])   
            contractor = int(mi_cj.split("_")[1]) 

            try:        # firm id is an int and so is year!!
                core_score_year_i=dict_year_dict_firmID_core_score[int(year)][manufacturer]   
            except KeyError:
                core_score_year_i="NA"
                

            try:      
                core_score_year_j=dict_year_dict_firmID_core_score[int(year)][contractor]
            except KeyError:
                core_score_year_j="NA"
                

 





            ### i retrieve the info on distance between zips
            zip1="NA"
            zip2="NA"
            dist="NA"
            manufacturer = int(mi_cj.split("_")[0])  
            contractor = int(mi_cj.split("_")[1])   

            try:
                zip1= str(dict_firm_tuple_zip_code_state[manufacturer][0])
                zip2= str(dict_firm_tuple_zip_code_state[contractor][0])
                tupla=(zip1, zip2) #in the dict, both dist(z1, z2) and dist(z2, z1) are supposed to be there with the same value

                if zip1 != zip2:
                    try:
                        dist=dict_tuple_zips_dist_miles[tupla]  # there should be both (zip1, zip2)  and (zip2, zip1) as keys to the same dist value.
                    except KeyError: 
                        list_missing_firms_zcode.append(mi_cj)
                else:
                    dist=0.


               


            except KeyError: 
                list_missing_firms_zcode.append(mi_cj)





            if flag_hurry == 0:
                print >> file6,  dicc[tupla_dates]["p_inf"], dicc[tupla_dates]["mi"], dicc[tupla_dates]["cj"], mi_cj, dicc[tupla_dates]["MCJ"], dicc[tupla_dates]["num_trans"],start_date_trans, end_date_trans, first_day, end_day,  dicc[tupla_dates]["length"], dicc[tupla_dates]["fin_period"], dict_micj_first_date[mi_cj], first_day_mi_cj, dicc[tupla_dates]["net_adj_gross"], dicc[tupla_dates]["tot_pos_gross"], dicc[tupla_dates]["tot_neg_gross"] , fract , dicc[tupla_dates]["accum_pos_gross"], dicc[tupla_dates]["accum_num_trans"],dicc[tupla_dates]["degree_m_fin"], dicc[tupla_dates]["degree_c_fin"], dicc[tupla_dates]["num_m_i"],dicc[tupla_dates]["num_c_i"],dicc[tupla_dates]["num_j_i"],dicc[tupla_dates]["num_m_j"],dicc[tupla_dates]["num_c_j"],dicc[tupla_dates]["num_j_j"],dicc[tupla_dates]["accum_degree_m_fin"], dicc[tupla_dates]["accum_degree_c_fin"], artificial_start_date_trans, dicc[tupla_dates]["overlap"], dicc[tupla_dates]["year"], dicc[tupla_dates]["N"], dicc[tupla_dates]["L"], dicc[tupla_dates]["CC_m_fin"],dicc[tupla_dates]["CC_c_fin"],dicc[tupla_dates]["betweenness_m_fin"],dicc[tupla_dates]["betweenness_c_fin"],dicc[tupla_dates]["max_clique_size_m_fin"],dicc[tupla_dates]["max_clique_size_c_fin"],dicc[tupla_dates]["kshell_m_fin"],dicc[tupla_dates]["kshell_c_fin"], dicc[tupla_dates]["p_inf_prev_trans"], dicc[tupla_dates]["accum_inf_prev_ij"], dicc[tupla_dates]["accum_inf_prev_neighb_i"], dicc[tupla_dates]["frac_accum_inf_prev_neighb_i"], dicc[tupla_dates]["accum_inf_prev_neighb_j"], dicc[tupla_dates]["frac_accum_inf_prev_neighb_j"],dicc[tupla_dates]["history_ij"] , dicc[tupla_dates]["min_dist_i_to_inf"], dicc[tupla_dates]["avg_dist_i_to_inf"], dicc[tupla_dates]["min_dist_j_to_inf"], dicc[tupla_dates]["avg_dist_j_to_inf"], dicc[tupla_dates]["degree_asym_ij"], dicc[tupla_dates]["business_asym_ij"], zscore, dist, zip1, zip2, core_score_year_i, core_score_year_j
                                           

       


            cont_entries +=1      


  
    ###### done writing


    print "num. not found micj in dict shuffing:", len(not_found_micj)," unique:", len(set(not_found_micj))
    print "num. signif. trans:",  num_signif_trans 

    print "num. pairs missing zip code:",len(list_missing_firms_zcode), "unique:",len(set(list_missing_firms_zcode))

    print 
    print "num. trans originally:", cont, "  num valid trans (non-self trans):", cont_valid,  cont_valid/float(cont)
    print "num. unique micj with neg trans:", len(set(list_micj_with_neg))
    print "num neg. trans:", cont_neg_all, ",  which is",float(cont_neg_all)/cont*100,"% of all transactions"
    print "num neg. trans (excluding self):", cont_neg, ",  which is",float(cont_neg)/cont*100,"% of all transactions, and",float(cont_neg)/cont_entries*100, "of all valid entries"
    print "num. entries written:", cont_entries



    file6.close()
    print "\n\nwritten file:",name6







#################################
###################################

def remove_overlapping_records_randomly(dict_micj_dict_dates_aggregate_trans,first_day_history, dict_micj_first_date, slicing,string_cohort):
    

  #  name7="../Results/Removed_overlapping_records_from_simplified_stata_file_Pinf_vs_mulitiple_variables_"+slicing+"_slicing_dropped_overlaps_randomly"+string_cohort+".dat"
   # file7= open(name7, 'wt') 
    
    # header for the file:                                       

    #print >> file7,  "P_inf", "Mi", "Cj", "Mi_Cj", "MCJ", "num_trans",  "start_date_trans","start_time_trans", "end_date_trans","end_time_trans", "first_day_trans","last_day_trans",  "length_trans", "period_end",  "first_date_mi_cj", "first_time_mi_cj", "first_day_mi_cj", "net_adj_gross", "tot_pos_gross", "tot_neg_gross","frac_neg_pos", "acumm_pos_gross","accum_num_trans","k_M_fin", "k_C_fin", "num_M_i","num_C_i","num_J_i", "num_M_j","num_C_j","num_J_j" ,  "k_M_fin_accum",  "k_C_fin_accum" , "artificial_start_date_trans","artificial_start_time_trans", "overlap", "year", "N", "L", "CC_m_fin","CC_c_fin","betweenness_m_fin","betweenness_c_fin","max_clique_size_m_fin","max_clique_size_c_fin","kshell_m_fin","kshell_c_fin","p_inf_prev_trans","accum_inf_prev_ij", "accum_inf_prev_neighb_i","frac_accum_inf_prev_neighb_i","accum_inf_prev_neighb_j","frac_accum_inf_prev_neighb_j","history_ij"#, "min_dist_i_to_inf", "avg_dist_i_to_inf", "min_dist_j_to_inf", "avg_dist_j_to_inf", "degree_asym_ij"
                                      




    list_records_with_overlap=[]
    cont_records= 0
    cont_removed_records =0
   
    list_removed=[]

    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
                    
        dicc=dict_micj_dict_dates_aggregate_trans[mi_cj]            


        for tupla_dates  in dict_micj_dict_dates_aggregate_trans[mi_cj]:    
            cont_records +=1

        if len(dict_micj_dict_dates_aggregate_trans[mi_cj])>1:           
               
            flag_count_overlap =1
            flag_overlap, list_overlapping_pairs_periods = check_for_overlapping_micj (dict_micj_dict_dates_aggregate_trans,mi_cj,first_day_history,flag_count_overlap)
                  
            for item in list_overlapping_pairs_periods:                

 


                r = random.choice([0,1])
                random_choice = item[r]  # i choose one of the periods from the overlapping pair                
                if r ==0:
                    non_choice=item[1]
                else:
                    non_choice=item[0]

           

                for key in dict_micj_dict_dates_aggregate_trans[mi_cj].keys():   # if the value doesnt exist anymore, it doesnt complain
                    if dict_micj_dict_dates_aggregate_trans[mi_cj][key]["list_days"]== random_choice:                            
                            

                            ########  before i remove it, i need to print out the removed records to a different file
                            tupla_dates=key  ##########   OJO!!!
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

                           # if dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"] !=  "NA":  ## a few missing nodes
   



           
                            try:            # to account for overlapping 
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] +=1 
                            except KeyError:
                                dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] =1
                   

                            #print >> file7, dicc[tupla_dates]["p_inf"], dicc[tupla_dates]["mi"], dicc[tupla_dates]["cj"], mi_cj, dicc[tupla_dates]["MCJ"], dicc[tupla_dates]["num_trans"],start_date_trans, end_date_trans, first_day, end_day,  dicc[tupla_dates]["length"], dicc[tupla_dates]["fin_period"], dict_micj_first_date[mi_cj], first_day_mi_cj, dicc[tupla_dates]["net_adj_gross"], dicc[tupla_dates]["tot_pos_gross"], dicc[tupla_dates]["tot_neg_gross"] , fract , dicc[tupla_dates]["accum_pos_gross"], dicc[tupla_dates]["accum_num_trans"],dicc[tupla_dates]["degree_m_fin"], dicc[tupla_dates]["degree_c_fin"], dicc[tupla_dates]["num_m_i"],dicc[tupla_dates]["num_c_i"],dicc[tupla_dates]["num_j_i"],dicc[tupla_dates]["num_m_j"],dicc[tupla_dates]["num_c_j"],dicc[tupla_dates]["num_j_j"],dicc[tupla_dates]["accum_degree_m_fin"], dicc[tupla_dates]["accum_degree_c_fin"], artificial_start_date_trans, dicc[tupla_dates]["overlap"], dicc[tupla_dates]["year"], dicc[tupla_dates]["N"], dicc[tupla_dates]["L"], dicc[tupla_dates]["CC_m_fin"],dicc[tupla_dates]["CC_c_fin"],dicc[tupla_dates]["betweenness_m_fin"],dicc[tupla_dates]["betweenness_c_fin"],dicc[tupla_dates]["max_clique_size_m_fin"],dicc[tupla_dates]["max_clique_size_c_fin"],dicc[tupla_dates]["kshell_m_fin"],dicc[tupla_dates]["kshell_c_fin"], dicc[tupla_dates]["p_inf_prev_trans"], dicc[tupla_dates]["accum_inf_prev_ij"], dicc[tupla_dates]["accum_inf_prev_neighb_i"], dicc[tupla_dates]["frac_accum_inf_prev_neighb_i"], dicc[tupla_dates]["accum_inf_prev_neighb_j"], dicc[tupla_dates]["frac_accum_inf_prev_neighb_j"],dicc[tupla_dates]["history_ij"]# , dicc[tupla_dates]["min_dist_i_to_inf"], dicc[tupla_dates]["avg_dist_i_to_inf"], dicc[tupla_dates]["min_dist_j_to_inf"], dicc[tupla_dates]["avg_dist_j_to_inf"], dicc[tupla_dates]["degree_asym_ij"]
                                      
        




                            ######## i removed the selected record
                            del dict_micj_dict_dates_aggregate_trans[mi_cj][key]
                            tupla=(mi_cj, key)
                            list_removed.append(tupla)
                          

                            cont_removed_records +=1



                    elif dict_micj_dict_dates_aggregate_trans[mi_cj][key]["list_days"]== non_choice:            
                        try:            # to account for overlapping 
                            dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] +=1 
                        except KeyError:
                            dict_micj_dict_dates_aggregate_trans[mi_cj][key]["overlap"] =1

                   


                flag_count_overlap =0  # the secong/third time i check for overlap, i do not count the overlap index again
                flag_overlap, list_overlapping_pairs_periods = check_for_overlapping_micj (dict_micj_dict_dates_aggregate_trans,mi_cj,first_day_history,flag_count_overlap)
                

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




#    file7.close()
 #   print "\n\nwritten file:",name7




    pickle_name="../Results/list_randomly_removed_tuples_micj_dates_from_overlapping_records"+string_cohort+".pickle"
    pickle.dump(list_removed, open(pickle_name, 'wb'))
    print "written pickle list:", pickle_name


    return list_removed
    

################################
################################

def check_for_overlapping_micj (dict_micj_dict_dates_aggregate_trans,mi_cj,first_day_history,flag_count_overlap):

    flag_overlap=0
    list_overlapping_pairs_periods=[]
    dicc= dict_micj_dict_dates_aggregate_trans[mi_cj]   #    all transactions for a given pair    
    if len(dicc)>1:   
               
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
         # print list_overlapping_pairs_periods # example of element of the list: (datetime.datetime(1987, 1, 1, 0, 0), datetime.datetime(1987, 1, 31, 0, 0))
      

    return flag_overlap, list_overlapping_pairs_periods



###########################################
##########################################

def populate_network_properties(dict_micj_dict_dates_aggregate_trans, G_period_fin_transaction,G_fin_transaction, manufacturer, contractor, mi_cj, tupla_dates):
             
          
            ########## for period network (at end date of the transact)
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"]= G_period_fin_transaction.degree(manufacturer)
            except:  # i few missing nodes, around 102
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_m_fin"]= "NA"

         

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"]= G_period_fin_transaction.degree(contractor)
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_c_fin"]= "NA"
        

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["N"]= len(G_period_fin_transaction.nodes())
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["N"]= "NA"

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["L"]= len(G_period_fin_transaction.edges())
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["L"]= "NA"

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["CC_m_fin"]= G_period_fin_transaction.node[manufacturer]["CC"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["CC_m_fin"]= "NA"
                    
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["CC_c_fin"]= G_period_fin_transaction.node[contractor]["CC"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["CC_c_fin"]= "NA"

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["betweenness_m_fin"]= G_period_fin_transaction.node[manufacturer]["betweeness"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["betweenness_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["betweenness_c_fin"]= G_period_fin_transaction.node[contractor]["betweeness"]                    
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["betweenness_c_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["link_betweenness_fin"]= G_period_fin_transaction.edge[manufacturer][contractor]["link_betweeness"]   
            except:
                try:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["link_betweenness_fin"]= G_period_fin_transaction.edge[contractor][manufacturer]["link_betweeness"] 
                except:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["link_betweenness_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_m_fin"]= G_period_fin_transaction.node[manufacturer]["max_clique_size"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_c_fin"]= G_period_fin_transaction.node[contractor]["max_clique_size"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_c_fin"]= "NA"

                   
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["kshell_m_fin"]= G_period_fin_transaction.node[manufacturer]["kshell"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["kshell_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["kshell_c_fin"]= G_period_fin_transaction.node[contractor]["kshell"]      
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["kshell_c_fin"]= "NA"
                   





            ########## for yearly-aggregated  network (at end date)   
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_degree_m_fin"]= G_fin_transaction.degree(manufacturer)
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_degree_m_fin"]="NA"

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_degree_c_fin"]= G_fin_transaction.degree(contractor)
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_degree_c_fin"]= "NA"

   
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_CC_m_fin"]= G_fin_transaction.node[manufacturer]["CC"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_CC_m_fin"]= "NA"
                    
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_CC_c_fin"]= G_fin_transaction.node[contractor]["CC"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_CC_c_fin"]= "NA"

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_betweenness_m_fin"]= G_fin_transaction.node[manufacturer]["betweeness"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_betweenness_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_betweenness_c_fin"]= G_fin_transaction.node[contractor]["betweeness"]                            
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_betweenness_c_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_link_betweenness_fin"]= G_fin_transaction.edge[manufacturer][contractor]["link_betweeness"]   
            except:
                try:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_link_betweenness_fin"]= G_fin_transaction.edge[contractor][manufacturer]["link_betweeness"]   
                except:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_link_betweenness_fin"]= "NA"




            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_m_fin"]= G_fin_transaction.node[manufacturer]["max_clique_size"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["max_clique_size_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_max_clique_size_c_fin"]= G_fin_transaction.node[contractor]["max_clique_size"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_max_clique_size_c_fin"]= "NA"

                   
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_kshell_m_fin"]= G_fin_transaction.node[manufacturer]["kshell"]
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_kshell_m_fin"]= "NA"


            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_kshell_c_fin"]= G_fin_transaction.node[contractor]["kshell"]      
            except:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_kshell_c_fin"]= "NA"
        


            
 



##########################
###########################

def calculate_min_dist_to_any_other_inf(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period):

                  
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):

        manufacturer = int(mi_cj.split("_")[0])   #### OJO!!! ESTO ES IMPORTANTISIMO!! SI NO INT(), ENTONCES NO ENCUENTRA LOS NODOS!!!!!
        contractor = int(mi_cj.split("_")[1])             
        
            
        for tupla_dates  in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):    
            
            ### i search for the corresponding network for the end date of the current transaction
            final_date_transaction=tupla_dates[1]
            day_fin_transaction = (final_date_transaction  - first_day_history).days
            period_fin_transaction = dict_day_period[day_fin_transaction] 
            G=dict_period_network_period[period_fin_transaction]



            list_inf_nodes=[]
            num_nodes_not_found=0
            for node in G.nodes():
                try:
                    if G.node[node]["p_inf"] ==1 :
                        if node != manufacturer  and   node != contractor: # i dont want the distance contractor-manufacturer to be the min. dist. 
                            list_inf_nodes.append(node)
                except KeyError: 
                    num_nodes_not_found +=1 



            pair_nodes=[manufacturer, contractor]
            for focus_node in pair_nodes:                          

                 min_dist=10000000
                 list_dist=[]
                 for node in list_inf_nodes:
                   try:
                     try:
                        dist=len(nx.shortest_path(G,source=focus_node,target=node))  ## ojo!! it returns a list with the explicit path!!
                    
                        if dist >0:
                            dist = dist -1  ## because if two nodes are directly connected, path length=2, not 1..

                        list_dist.append(dist)
                        if dist < min_dist:
                            min_dist = dist 
                     except nx.exception.NetworkXError: #pass  # if the node is not in the network
                        pass#print "node not in network"
                   except nx.exception.NetworkXNoPath: 
                       dist=10000000    #pass#print "no path"#pass  # if the two nodes are not connected by any path


                
                 if len(list_dist)>0:
                     avg_dist=numpy.mean(list_dist)
                 else:
                    avg_dist=10000000


                 if focus_node == manufacturer:
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["min_dist_i_to_inf"] = min_dist
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["avg_dist_i_to_inf"] = avg_dist
                 elif focus_node == contractor:        
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["min_dist_j_to_inf"] = min_dist
                    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["avg_dist_j_to_inf"] = avg_dist

           






##################################
##################################

def calculate_degree_asym(G, dict_micj_dict_dates_aggregate_trans, mi_cj, tupla_dates, manufacturer, contractor):

    ######## degree asym.
    degree_asymmetry_ij="NA"
    try:
        degree_asymmetry_ij= float(( G.degree(manufacturer) - G.degree(contractor)) * (G.degree(manufacturer)- G.degree(contractor))) / float((G.degree(manufacturer) + G.degree(contractor)) * (G.degree(manufacturer)+ G.degree(contractor)))
    except:
        pass

    dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["degree_asym_ij"]=degree_asymmetry_ij


#####################################
###########################################

def calculate_business_asym(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period):
  

    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):     
        
              
        manufacturer = int(mi_cj.split("_")[0])   #### OJO!!! ESTO ES IMPORTANTISIMO!! SI NO INT(), ENTONCES NO ENCUENTRA LOS NODOS!!!!!
        contractor = int(mi_cj.split("_")[1])                       
        
        for tupla_dates in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):            
              
            
            #### i get the current network for this tupla_dates (for the ending) 
            final_date_transaction=tupla_dates[1]
            day_fin_transaction = (final_date_transaction  - first_day_history).days
            period_fin_transaction = dict_day_period[day_fin_transaction] 
            G_period=dict_period_network_period[period_fin_transaction]
            
            
            
            ####### business asym.
            try:        
                frac_pos_business_of_M_with_C=  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] / G_period.node[manufacturer]['pos_transct']
            except: #ZeroDivisionError: or KeyError
                frac_pos_business_of_M_with_C="NA"  
                
            try:
                frac_pos_business_of_C_with_M=  dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] / G_period.node[contractor]['pos_transct']
            except:# ZeroDivisionError:  or KeyError
                frac_pos_business_of_C_with_M="NA"  
                  

        

            business_asymmetry_ij="NA"
            try:
                business_asymmetry_ij = ((frac_pos_business_of_M_with_C  - frac_pos_business_of_C_with_M )* (frac_pos_business_of_M_with_C  - frac_pos_business_of_C_with_M)) / ((frac_pos_business_of_M_with_C  + frac_pos_business_of_C_with_M) * (frac_pos_business_of_M_with_C  + frac_pos_business_of_C_with_M))
            except:  pass  # either for a zerodivision error, or because one of the elements is NA
            



            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["business_asym_ij"] = business_asymmetry_ij
           

# except nx.exception.NetworkXError: pass






#########################################
##########################################


def  calculate_prob_inf_prev(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period,list_removed_tuplas_micj_dates):

 
    for mi_cj in dict_micj_dict_dates_aggregate_trans:        
        for tupla_dates in dict_micj_dict_dates_aggregate_trans[mi_cj]:

            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf_prev_trans"]=0.
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_ij"]=0.

            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_i"]=0.
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_i"]=0.
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_j"]=0.
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_j"]=0.           

            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["history_ij"]=0.   # number of times working together
           


   
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):    
       
        prev_value=0.
        accum=0.
        history=1
        for tupla_dates in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):            
            tupla_remove=(mi_cj, tupla_dates)
            if tupla_remove not in list_removed_tuplas_micj_dates:   # i need to ignore the tuplas removed due to overlapping

              
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf_prev_trans"] = prev_value
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_ij"] = accum
                
                prev_value= dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf"]  
                accum +=dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["p_inf"]                               

                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["history_ij"] = history
                history +=1

      
          

    tot=len(dict_micj_dict_dates_aggregate_trans)
    cont=0
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):     

      cont +=1
      #print cont, tot, mi_cj   


      manufacturer = int(mi_cj.split("_")[0])   #### OJO!!! ESTO ES IMPORTANTISIMO!! SI NO INT(), ENTONCES NO ENCUENTRA LOS NODOS!!!!!
      contractor = int(mi_cj.split("_")[1])             
      
      
      for tupla_dates in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):
        
    
         norm_i=0.
         norm_j=0. 
         
         
         accum_inf_prev_neighb_i=0.
         accum_inf_prev_neighb_j=0.
         frac_accum_inf_prev_neighb_i=0.
         frac_accum_inf_prev_neighb_j=0.     
         
         tupla_remove=(mi_cj, tupla_dates)
         if tupla_remove not in list_removed_tuplas_micj_dates:   # i need to ignore the tuplas removed due to overlapping
         
       

            #### i get the current network for this tupla_dates (for the ending) 
            final_date_transaction=tupla_dates[1]
            day_fin_transaction = (final_date_transaction  - first_day_history).days
            period_fin_transaction = dict_day_period[day_fin_transaction] 
            G_period=dict_period_network_period[period_fin_transaction]



            try:
             


              ##### i check the infected among the manuf.'s neighbors
              for neigh in  G_period.neighbors(manufacturer):
                new_micj =  str(manufacturer) + "_"+ str(neigh)
                new_micj_bis =  str(neigh) + "_"+ str(manufacturer)

                if neigh != contractor:
                    
                    if new_micj in dict_micj_dict_dates_aggregate_trans.keys(): 
                        if tupla_dates in dict_micj_dict_dates_aggregate_trans[new_micj].keys():
                            accum_inf_prev_neighb_i += dict_micj_dict_dates_aggregate_trans[new_micj][tupla_dates]["p_inf"]
                            norm_i +=1.
                           

                    elif  new_micj_bis in dict_micj_dict_dates_aggregate_trans.keys():
                        if tupla_dates in dict_micj_dict_dates_aggregate_trans[new_micj_bis].keys():
                             accum_inf_prev_neighb_i += dict_micj_dict_dates_aggregate_trans[new_micj_bis][tupla_dates]["p_inf"]
                             norm_i +=1.                               
            except nx.exception.NetworkXError: pass


            try:
              ##### i check the infected among the contr.'s neighbors
              for neigh in  G_period.neighbors(contractor):
                new_micj =  str(contractor) + "_"+ str(neigh)
                new_micj_bis =  str(neigh) + "_"+ str(contractor)

                if neigh != manufacturer:
                    
                    if new_micj in dict_micj_dict_dates_aggregate_trans.keys(): 
                        if tupla_dates in dict_micj_dict_dates_aggregate_trans[new_micj].keys():
                            accum_inf_prev_neighb_j += dict_micj_dict_dates_aggregate_trans[new_micj][tupla_dates]["p_inf"]
                            norm_j +=1.

                    elif  new_micj_bis in dict_micj_dict_dates_aggregate_trans.keys():
                        if tupla_dates in dict_micj_dict_dates_aggregate_trans[new_micj_bis].keys():
                             accum_inf_prev_neighb_j += dict_micj_dict_dates_aggregate_trans[new_micj_bis][tupla_dates]["p_inf"]
                             norm_j +=1.

            except nx.exception.NetworkXError: pass



            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_i"] = accum_inf_prev_neighb_i
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_j"] = accum_inf_prev_neighb_j
         
          
            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_i"] = accum_inf_prev_neighb_i/ norm_i        
            except ZeroDivisionError:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_i"] = 0.
                

            try:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_j"] = accum_inf_prev_neighb_j/ norm_j
            except ZeroDivisionError:
                dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_j"] = 0.
               


           # print " ", tupla_dates,  "acc_i:",dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_i"],  " frac_i",dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_i"], "norm_i:", norm_i, "    acc_j",dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_inf_prev_neighb_j"],"frac_j",dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["frac_accum_inf_prev_neighb_j"], "norm_j:", norm_j, "degrees:", len(G_period.neighbors(manufacturer)), len(G_period.neighbors(contractor)) 




##################################
######################################


def  calculate_accumulate_transactions(dict_micj_dict_dates_aggregate_trans):
     


    for mi_cj in dict_micj_dict_dates_aggregate_trans:                    
        for tupla_dates  in dict_micj_dict_dates_aggregate_trans[mi_cj]:    

            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_pos_gross"] =0.
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_num_trans"] =0.



  
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):  
        accum_num_trans=0.                  
        accum_net_gross=0. 
                 
        for tupla_dates  in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):    # i sort the dict chronologically

            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_pos_gross"] = accum_net_gross
            dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["accum_num_trans"] = accum_num_trans


            accum_net_gross += dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["tot_pos_gross"] 
            accum_num_trans += dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_trans"] 

          

##################################
######################################

def calculate_num_manuf_contr(dict_micj_dict_dates_aggregate_trans,first_day_history,dict_day_period,dict_period_network_period):   
  
    #missing_nodes=0
  
   
    ######  i assign the values for prob inf prev trans for the node's neighboring links
    for mi_cj in sorted(dict_micj_dict_dates_aggregate_trans):
      
        manufacturer = int(mi_cj.split("_")[0])   #### OJO!!! ESTO ES IMPORTANTISIMO!! SI NO INT(), ENTONCES NO ENCUENTRA LOS NODOS!!!!!
        contractor = int(mi_cj.split("_")[1])             
            

        for tupla_dates  in sorted(dict_micj_dict_dates_aggregate_trans[mi_cj]):    # i sort the dict chronologically
            
            ### i search for the corresponding network (for the next time)
            final_date_transaction=tupla_dates[1]
            day_fin_transaction = (final_date_transaction  - first_day_history).days
            period_fin_transaction = dict_day_period[day_fin_transaction] 
            G_period_fin_transaction=dict_period_network_period[period_fin_transaction]
            

            if manufacturer not in G_period_fin_transaction.nodes():
                print "manuf", manufacturer, "not in network"
            if contractor not in G_period_fin_transaction.nodes():
                print "contr", contractor, "not in network"


            pair_nodes=[manufacturer, contractor]
         
            for node in pair_nodes:
                num_m=0
                num_c=0
                num_j=0
                try:
                    for neigh in G_period_fin_transaction.neighbors(node):                                              
                        if G_period_fin_transaction.node[neigh]["type"]  =="manuf":
                            num_m +=1
                        elif G_period_fin_transaction.node[neigh]["type"]  =="contr":
                            num_c +=1
                        elif G_period_fin_transaction.node[neigh]["type"]  =="jobber":
                            num_j +=1

                except nx.exception.NetworkXError: pass  # for a few missing nodes
              
                if node == manufacturer:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_m_i"]=num_m
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_c_i"]=num_c
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_j_i"]=num_j
                elif node == contractor:
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_m_j"]=num_m
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_c_j"]=num_c
                        dict_micj_dict_dates_aggregate_trans[mi_cj][tupla_dates]["num_j_j"]=num_j
                        
                
               
  

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
