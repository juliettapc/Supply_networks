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



    flag_hist="NO"
    flag_network_metrics="NO"    # YES or NO



    slicing="monthly"    #"monthly"  # or "yearly"

    threshold_neg_tran=0.35   # fraction of negative dollars out of the total amount of dollars transacted, to consider a link infected between two companies



    flag_remove_selfloops="YES"
    string_filename_loops=""
    if flag_remove_selfloops=="NO":
        string_filename_loops="_with_self_loops"


    string_filename=""
    if flag_network_metrics=="NO":
        string_filename="_no_network_metrics"






    dict_firm_tuple_zip_code_state = pickle.load(open("../Results/dict_firm_id_zip_code.pickle", 'rb')) # example:  05188210: ('94108', 'CA')

    dict_tuple_zips_dist_miles= pickle.load(open("../Results/dict_zip_tuples_dist_miles_from_34Gb.pickle", 'rb'))   ### example:  (zip1,zip2): distance_miles




    name1="../Results/Time_evol_num_transactions_"+slicing+"_slicing.dat"
    file1= open(name1, 'wt')
    file1.close()

    name2="../Results/Time_evol_num_active_firms_"+slicing+"_slicing.dat"
    file2= open(name2, 'wt')
    file2.close()

    name3="../Results/Time_evol_num_neg_transactions_"+slicing+"_slicing.dat"
    file3= open(name3, 'wt')
    file3.close()

    name4="../Results/Time_evol_num_self_transactions_"+slicing+"_slicing.dat"
    file4= open(name4, 'wt')
    file4.close()


    name5="../Results/Time_evol_num_self_neg_transactions_"+slicing+"_slicing.dat"
    file5= open(name5, 'wt')
    file5.close()



    name7="../Results/Time_evol_tot_num_infected_links_nodes_GC_with_neg_transact_larger_than"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"
    file7= open(name7, 'wt')
    file7.close()


    name8="../Results/Time_evol_tot_vol_posit_transactions_"+slicing+"_slicing.dat"
    file8= open(name8, 'wt')





    name6="../Results/Scatter_plot_Pinf_vs_mulitiple_variables_"+slicing+"_slicing"+string_filename+".dat"
    file6= open(name6, 'wt') 

   # header for the file:  
    #   P_inf tot_adj_gross_ij pos_adj_gross_ij neg_adj_gross_ij pos_adj_gross_i neg_adj_gross_i pos_adj_gross_j neg_adj_gross_j P_inf_previous_month Cumulat_num_inf_months frac_previous_inf_months ki kj K_nn_i K_nn_j HHIi_as_manuf HHIi_as_contr HHIj_as_manuf HHIj_as_contr betweenness_i betweenness_j link_betweenness_ij max_clique_i max_clique_j kshell_i kshell_j num_manuf_i num_contr_i num_manuf_j num_contr_j num_transact_ij num_transact_i num_transact_j amount_pos_self_trans_i amount_pos_self_trans_j amount_neg_self_trans_i amount_neg_self_trans_j num_pos_self_trans_i num_pos_self_trans_j num_neg_self_trans_i num_neg_self_trans_j fract_pos_bussiness_of_M_with_C fract_pos_bussiness_of_C_with_M degree_asymmetry_ij business_asymmetry_ij size_tot_errors_ij dist current_data_month current_data_season fract_inf_links_global fract_inf_links_local_manuf fract_inf_links_local_contr history_ij"


   # string_header="P_inf tot_adj_gross_ij pos_adj_gross_ij neg_adj_gross_ij pos_adj_gross_i neg_adj_gross_i pos_adj_gross_j neg_adj_gross_j P_inf_previous_month Cumulat_num_inf_months frac_previous_inf_months ki kj K_nn_i K_nn_j HHIi_as_manuf HHIi_as_contr HHIj_as_manuf HHIj_as_contr betweenness_i betweenness_j link_betweenness_ij max_clique_i max_clique_j kshell_i kshell_j num_manuf_i num_contr_i num_manuf_j num_contr_j num_transact_ij num_transact_i num_transact_j amount_pos_self_trans_i amount_pos_self_trans_j amount_neg_self_trans_i amount_neg_self_trans_j num_pos_self_trans_i num_pos_self_trans_j num_neg_self_trans_i num_neg_self_trans_j fract_pos_bussiness_of_M_with_C fract_pos_bussiness_of_C_with_M degree_asymmetry_ij business_asymmetry_ij size_tot_errors_ij dist  current_data_month current_data_season fract_inf_links_global fract_inf_links_local_manuf fract_inf_links_local_contr history_ij"





   #  print G_period.nodes(data=True)   #example:   (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 2, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0008438954375540839})

    #  print G_period.edges(data=True)  # example: (514603, 2302275, {'pos_weight': 23989, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 1.0, 'link_betweeness': 0.0016097736255839023, 'neg_weight': 0.0})
                               








    G=nx.Graph()

    print
    print
    
    list_periods=[]

    list_firm_ids=[]

    cont_transactions=0.
    cont_neg_transactions=0.

    cont_self_transactions=0.
    cont_self_neg_transactions=0.


    dict_firm_id_active_periods={}
    dict_firm_total_trans_volum={}

   
    dict_firm_num_pos_trans={}
    dict_firm_num_neg_trans={}

    dict_tuple_link_cumulat_previous_Pinf={}
    dict_tuple_link_fract_previous_inf_periods={}
    dict_tuple_link_Pinf_previous_period={}

    dict_tuple_link_previous_periods_together={}   # number of periods the two companies have been working together  (history)


    dict_manuf_dict_contr_amounts={}  # for each manufact., dict of its contractors and total amounts
    dict_contr_dict_manuf_amounts={}   # for each contract., dict of its manuf. and total amounts

    dict_link_num_pos_trans={}
    dict_link_num_neg_trans={}
    dict_link_num_trans={}



    list_neg_adj_gross=[]
    list_pos_adj_gross=[]


    list_tuplas=[]

  

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


    list_sizes_inf_components_tot=[]
    cont_periods=0
    dict_period_tot_vol_posit_transact={}
    ############# loop over periods
    for mark_date_initial in list_starting_date_marks:  
         
        current_year=mark_date_initial.year

        if  slicing=="monthly":
            mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   
        elif slicing=="yearly":
            mark_date_final =  mark_date_initial + dt.timedelta(days = 365)     

        cont_periods +=1    

        print "\n\nperiod:",cont_periods,"with",slicing,  "slicing,  mark_initial_date:", mark_date_initial

        ### period dicts:
        list_neg_adj_gross_period=[]
        list_pos_adj_gross_period=[]

        list_firm_ids_period=[]

        list_tuplas_period=[]

        dict_firm_total_trans_volum_period={}

        dict_firm_tot_pos_trans_period={}
        dict_firm_tot_neg_trans_period={}

        dict_firm_num_pos_trans_period={}
        dict_firm_num_neg_trans_period={}

        dict_link_num_pos_trans_period={}
        dict_link_num_neg_trans_period={}
        dict_link_num_trans_period={}


        dict_firm_amount_pos_self_trans_period={}
        dict_firm_amount_neg_self_trans_period={}

        dict_firm_num_pos_self_trans_period={}
        dict_firm_num_neg_self_trans_period={}


        dict_period_tot_vol_posit_transact[cont_periods]=0.

        dict_manuf_dict_contr_amounts_period={}  # for each manufact., dict of its contractors and total amounts
        dict_contr_dict_manuf_amounts_period={}   # for each contract., dict of its manuf. and total amounts


        cont_transactions_period=0.
        cont_neg_transactions_period=0.
        cont_self_transactions_period=0.
        cont_self_neg_transactions_period=0.


        G_period=nx.Graph()


        list_manuf_period=[]
        list_contr_period=[]
        list_non_self_contractors=[]


        ##################  
        ####### input datafile:    (I NEED TO READ IT EVERY TIME, BECAUSE IT GETS EMPTY EVERY TIME AFTER ITERATING OVER IT)
        name0="fhistory_ALL.csv"
        print "reading: ", path+name0, "......."       


        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
        cont=1       
        csvfile=open(path+name0, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   # to skip the header
             

        for list_row in reader:                
           cont +=1
           flag_ignore_row=0

      #     print "\n",list_row


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
               initial_date=dt.datetime(year, month, day)
           except ValueError: # there are a bunch of incorrect dates!!!  043185   063185     113185   023185
               day =1
               month +=1                
               initial_date=dt.datetime(year, month, day)
          


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
               final_date=dt.datetime(year, month, day)
           except ValueError:   # there are a bunch of incorrect dates!!!  043185   063185     113185   023185  
               day =1
               month +=1
               try:               
                   final_date=dt.datetime(year, month, day)
               except ValueError:
                   flag_ignore_row= 1   # there is at least one month = 21    213101



           ###### i calculate the time inverval for the current transaction
           period=(final_date-initial_date).days                
           if period < 0:
               old_initial=initial_date
               old_final=final_date   #####  some time periods have interved TO and FROM dates!
               initial_date =final_date
               final_date = old_initial
               period=(final_date-initial_date).days          
               list_periods.append(period)

           middle_point=initial_date + dt.timedelta( days=int(float(period)/2.) )
         




           #aux_cont_periods=cont_periods
           #if slicing == "yearly":
            #   aux_cont_periods=cont_periods*12
          # print initial_date, final_date, middle_point, current_data_month



      
           ##### i only look at the rows of the datafile for dates corresponding to the current observation period
           if middle_point >= mark_date_initial  and middle_point <= mark_date_final  :


               current_data_month=   middle_point.month              
             #  print middle_point, current_data_month
               
               if current_data_month <=3:
                   current_data_season=1
               elif current_data_month >3  and current_data_month <=6 :
                   current_data_season=2
               elif current_data_month >6  and current_data_month <=9 :
                   current_data_season=3
               elif current_data_month >9  and current_data_month <=12 :
                   current_data_season=4


               try:   #  some lines are missing the contractor or manufacturer: skip


                    manufacturer=int(list_row[0])     ##paidbyfirm
                    contractor=int(list_row[1])      ## paidforfirm                                
             
                
                    list_manuf_period.append(manufacturer)
                    list_contr_period.append(contractor)
             
             
                    cont_transactions +=1
                    cont_transactions_period +=1


                    ############## for now i deal with integers Dollars !!  (easier for histograms)
                    adj_gross=int(round(float((list_row[4]))))    
              
                                 
                    if manufacturer == contractor:
                          cont_self_transactions  +=1.
                          cont_self_transactions_period  +=1.
                          if flag_remove_selfloops=="YES":
                            flag_ignore_row=1
       
                          ########## if it is a self-transaction, i only record this (no network variables nor HHI etc)
                          if adj_gross <0.:
                              cont_self_neg_transactions  +=1.
                              cont_self_neg_transactions_period  +=1.


                              ###### count number and amount of self neg transactions
                              try:
                                  dict_firm_amount_neg_self_trans_period[manufacturer] +=  adj_gross                   
                              except KeyError:
                                  dict_firm_amount_neg_self_trans_period[manufacturer] = adj_gross                   
                              try:
                                  dict_firm_num_neg_self_trans_period[manufacturer] +=1.
                              except KeyError:
                                  dict_firm_num_neg_self_trans_period[manufacturer] =1.

                          else:
                              ###### count number and amount of self pos transactions
                              try:
                                  dict_firm_amount_pos_self_trans_period[manufacturer] +=  adj_gross                   
                              except KeyError:
                                  dict_firm_amount_pos_self_trans_period[manufacturer] = adj_gross                         
                              try:
                                  dict_firm_num_pos_self_trans_period[manufacturer] +=1.
                              except KeyError:
                                  dict_firm_num_pos_self_trans_period[manufacturer] =1.

                    else:
                          list_non_self_contractors.append(contractor)                 





                    if  flag_ignore_row == 0 :   # in general i do not count the self-transactions (for network metrics nor HHI etc)

                       tupla_link=(manufacturer, contractor)                        

                       list_tuplas_period.append(tupla_link)
                       list_tuplas.append(tupla_link)

                       list_firm_ids.append(manufacturer)
                       list_firm_ids.append(contractor)
        
                       list_firm_ids_period.append(manufacturer)
                       list_firm_ids_period.append(contractor)
                                 


                       ########### list of active periods for firms
                       try:
                           dict_firm_id_active_periods[manufacturer].append(cont_periods)
                       except KeyError:
                           dict_firm_id_active_periods[manufacturer]=[]
                           dict_firm_id_active_periods[manufacturer].append(cont_periods)


                       if manufacturer != contractor:
                           try:
                               dict_firm_id_active_periods[contractor].append(cont_periods)
                           except KeyError:
                               dict_firm_id_active_periods[contractor]=[]
                               dict_firm_id_active_periods[contractor].append(cont_periods)
                        
      
                    
                       ###########  i need to initialize dicts
                       try:
                           dict_firm_num_neg_trans_period[manufacturer]
                       except KeyError:
                           dict_firm_num_neg_trans_period[manufacturer] =0.

                       try:
                           dict_firm_num_neg_trans_period[contractor]
                       except KeyError:
                           dict_firm_num_neg_trans_period[contractor] =0.


                       try:
                           dict_firm_num_neg_trans[manufacturer]
                       except KeyError:
                           dict_firm_num_neg_trans[manufacturer] =0.

                       try:
                           dict_firm_num_neg_trans[contractor]
                       except KeyError:
                           dict_firm_num_neg_trans[contractor] =0.


                       try:
                           dict_firm_num_pos_trans_period[manufacturer]
                       except KeyError:
                           dict_firm_num_pos_trans_period[manufacturer] =0.
       
                       try:
                           dict_firm_num_pos_trans_period[contractor]
                       except KeyError:
                           dict_firm_num_pos_trans_period[contractor] =0.


                       try:
                           dict_firm_num_pos_trans[manufacturer]
                       except KeyError:
                           dict_firm_num_pos_trans[manufacturer] =0.

                       try:
                           dict_firm_num_pos_trans[contractor]
                       except KeyError:
                           dict_firm_num_pos_trans[contractor] =0.

                       #########




                       ########### initialize the same for links
                       try:
                           dict_link_num_pos_trans[tupla_link]
                       except KeyError:
                           dict_link_num_pos_trans[tupla_link] = 0.

                       try:
                           dict_link_num_neg_trans[tupla_link]
                       except KeyError:
                           dict_link_num_neg_trans[tupla_link] = 0.

                       try:
                           dict_link_num_trans[tupla_link]
                       except KeyError:
                           dict_link_num_trans[tupla_link] = 0.






                       try:
                           dict_link_num_pos_trans_period[tupla_link]
                       except KeyError:
                           dict_link_num_pos_trans_period[tupla_link] = 0.

                       try:
                           dict_link_num_neg_trans_period[tupla_link]
                       except KeyError:
                           dict_link_num_neg_trans_period[tupla_link] = 0.

                       try:
                           dict_link_num_trans_period[tupla_link]
                       except KeyError:
                           dict_link_num_trans_period[tupla_link] = 0.
                       ############



                                                 
                       ######## for the HHI index of manuf. and contr.                   
                      #      HHI is a measure of the size of firms in an  industry, and an indicator of the amount of competition among them.  Bounded by: 1/N  (equally distributed industry), 1 (total monopoly).  
                       try:
                           dict_manuf_dict_contr_amounts[manufacturer]
                       except KeyError:
                           dict_manuf_dict_contr_amounts[manufacturer]={}
                       try:
                           dict_manuf_dict_contr_amounts[manufacturer][contractor]
                       except KeyError:
                           dict_manuf_dict_contr_amounts[manufacturer][contractor] = 0.
                       dict_manuf_dict_contr_amounts[manufacturer][contractor] += adj_gross


                       try:
                           dict_manuf_dict_contr_amounts_period[manufacturer]
                       except KeyError:
                           dict_manuf_dict_contr_amounts_period[manufacturer]={}
                       try:
                           dict_manuf_dict_contr_amounts_period[manufacturer][contractor]
                       except KeyError:
                           dict_manuf_dict_contr_amounts_period[manufacturer][contractor] = 0.
                       dict_manuf_dict_contr_amounts_period[manufacturer][contractor] += adj_gross



                       try:
                           dict_contr_dict_manuf_amounts[contractor]
                       except KeyError:
                           dict_contr_dict_manuf_amounts[contractor]={}
                       try:
                           dict_contr_dict_manuf_amounts[contractor][manufacturer]
                       except KeyError:
                           dict_contr_dict_manuf_amounts[contractor][manufacturer]=0.
                       dict_contr_dict_manuf_amounts[contractor][manufacturer] += adj_gross


                       try:
                           dict_contr_dict_manuf_amounts_period[contractor]
                       except KeyError:
                           dict_contr_dict_manuf_amounts_period[contractor]={}
                       try:
                           dict_contr_dict_manuf_amounts_period[contractor][manufacturer]
                       except KeyError:
                           dict_contr_dict_manuf_amounts_period[contractor][manufacturer]=0.
                       dict_contr_dict_manuf_amounts_period[contractor][manufacturer] += adj_gross






                       ########## total volume of (net) transactions
                       try:
                           dict_firm_total_trans_volum[manufacturer] += adj_gross   
                       except KeyError:
                           dict_firm_total_trans_volum[manufacturer] =0.
                           dict_firm_total_trans_volum[manufacturer] += adj_gross   

                       try:
                           dict_firm_total_trans_volum[contractor] += adj_gross   
                       except KeyError:
                           dict_firm_total_trans_volum[contractor] =0.
                           dict_firm_total_trans_volum[contractor] += adj_gross   





                       ##########   volume of (net) transactions PERIOD
                       try:
                           dict_firm_total_trans_volum_period[manufacturer] += adj_gross   
                       except KeyError:
                           dict_firm_total_trans_volum_period[manufacturer] =0.
                           dict_firm_total_trans_volum_period[manufacturer] += adj_gross   

                       try:
                           dict_firm_total_trans_volum_period[contractor] += adj_gross   
                       except KeyError:
                           dict_firm_total_trans_volum_period[contractor] =0.
                           dict_firm_total_trans_volum_period[contractor] += adj_gross   



                       dict_link_num_trans[tupla_link] += 1.
                       dict_link_num_trans_period[tupla_link] += 1.



                     
                       ##########         
                       if adj_gross  <0:                      

                           list_neg_adj_gross.append(-1*adj_gross)
                           list_neg_adj_gross_period.append(-1*adj_gross)

                           cont_neg_transactions   +=1
                           cont_neg_transactions_period   +=1

                       

                           ##### num of neg. transactions PERIOD                   
                           dict_firm_num_neg_trans_period[manufacturer] +=1.                   
                           dict_firm_num_neg_trans_period[contractor] +=1.                    

                           ##### tot num of neg. transactions                  
                           dict_firm_num_neg_trans[manufacturer] +=1.                                        
                           dict_firm_num_neg_trans[contractor] +=1.
                                                         

                           #### same for the link
                           dict_link_num_neg_trans_period[tupla_link] += 1.
                           dict_link_num_neg_trans[tupla_link] += 1.

                                      



                           G_period.add_node(manufacturer)
                           G_period.add_node(contractor)


                           G.add_node(manufacturer)
                           G.add_node(contractor)



                           try:
                               G.edge[manufacturer][contractor]["neg_weight"] += adj_gross               
                           except KeyError:
                               G.add_edge(manufacturer,contractor, neg_weight= adj_gross)

                           try:
                        
                               G_period.edge[manufacturer][contractor]["neg_weight"] += adj_gross
                           except KeyError:                    
                               G_period.add_edge(manufacturer,contractor, neg_weight= adj_gross)



                           #### add up to the total neg. PERIOD amount for each firm
                           try:
                               dict_firm_tot_neg_trans_period[manufacturer] += adj_gross   
                           except KeyError:
                               dict_firm_tot_neg_trans_period[manufacturer] =0.
                               dict_firm_tot_neg_trans_period[manufacturer] += adj_gross   
                           try:
                               dict_firm_tot_neg_trans_period[contractor] += adj_gross   
                           except KeyError:
                               dict_firm_tot_neg_trans_period[contractor] =0.
                               dict_firm_tot_neg_trans_period[contractor] += adj_gross   

   

                       else:

                           list_pos_adj_gross.append(adj_gross)
                           list_pos_adj_gross_period.append(adj_gross)

                           ##### num of posit. transactions PERIOD                   
                           dict_firm_num_pos_trans_period[manufacturer] +=1.                    
                           dict_firm_num_pos_trans_period[contractor] +=1.
                   

                           ##### tot. num of posit. transactions                     
                           dict_firm_num_pos_trans[manufacturer] +=1.                   
                           dict_firm_num_pos_trans[contractor] +=1.                  
                    

                           #### same for the link
                           dict_link_num_pos_trans_period[tupla_link] += 1.
                           dict_link_num_pos_trans[tupla_link] += 1.

                           dict_period_tot_vol_posit_transact[cont_periods] +=adj_gross


                           try:
                               G.edge[manufacturer][contractor]["pos_weight"] += adj_gross               
                           except KeyError:
                               G.add_edge(manufacturer,contractor, pos_weight= adj_gross)

                           try:
                        
                               G_period.edge[manufacturer][contractor]["pos_weight"] += adj_gross
                           except KeyError:                    
                               G_period.add_edge(manufacturer,contractor, pos_weight= adj_gross)


                           #### add up to the total pos. PERIOD amount for each firm
                           try:
                               dict_firm_tot_pos_trans_period[manufacturer] += adj_gross   
                           except KeyError:
                               dict_firm_tot_pos_trans_period[manufacturer] =0.
                               dict_firm_tot_pos_trans_period[manufacturer] += adj_gross   
                           try:
                               dict_firm_tot_pos_trans_period[contractor] += adj_gross   
                           except KeyError:
                               dict_firm_tot_pos_trans_period[contractor] =0.
                               dict_firm_tot_pos_trans_period[contractor] += adj_gross   
       


             

               except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer 
            
          

            
        #############################  end of loop to read ALL-years file
        ###########################

        if  flag_hist == "YES":           
            try:
                name_h="../Results/histogram_pos_adj_gross_values_"+slicing+"_slicing_"+str(cont_periods)+".dat"
                histograma_gral.histogram(list_pos_adj_gross_period, name_h)
            except: pass

            try:
                name_h="../Results/histogram_neg_adj_gross_values_"+slicing+"_slicing_"+str(cont_periods)+".dat"
                histograma_gral.histogram(list_neg_adj_gross_period, name_h)
            except: pass
        


        for  link in dict_link_num_pos_trans_period:
            G_period[link[0]][link[1]]['num_pos_trans']= dict_link_num_pos_trans_period[link]    


        for  link in dict_link_num_neg_trans_period:
            G_period[link[0]][link[1]]['num_neg_trans']= dict_link_num_neg_trans_period[link]    
            G_period[link[0]][link[1]]['fract_neg_trans']= dict_link_num_neg_trans_period[link] / (dict_link_num_neg_trans_period[link] + dict_link_num_pos_trans_period[link] )   

            if  G_period[link[0]][link[1]]['num_neg_trans'] == 0.:
                G_period[link[0]][link[1]]['neg_weight']=0.

            if  G_period[link[0]][link[1]]['num_pos_trans'] == 0.:
                G_period[link[0]][link[1]]['pos_weight']=0.


    


        for firm in G_period.nodes():           

            G_period.node[firm]['vol_transct']=dict_firm_total_trans_volum_period[firm]                                                   
            G_period.node[firm]['fract_neg_transct']=dict_firm_num_neg_trans_period[firm] /(dict_firm_num_neg_trans_period[firm] + dict_firm_num_pos_trans_period[firm])  
                                    
            G_period.node[firm]['num_transact']= dict_firm_num_neg_trans_period[firm] + dict_firm_num_pos_trans_period[firm]
                    
   
     



        for firm in dict_firm_tot_pos_trans_period:
            G_period.node[firm]['vol_pos_transct']=dict_firm_tot_pos_trans_period[firm]

        for firm in dict_firm_tot_neg_trans_period:
            G_period.node[firm]['vol_neg_transct']=dict_firm_tot_neg_trans_period[firm]

        ###### fill in the gaps for those firms without positive or neg. transactions
        for node in G_period.nodes():
            try:
                G_period.node[node]['vol_pos_transct']
            except KeyError:
                G_period.node[node]['vol_pos_transct']=0.

            try:
                G_period.node[node]['vol_neg_transct']
            except KeyError:
                G_period.node[node]['vol_neg_transct']=0.





        print " month",cont_periods
        print "  # firms:", len(set(list_firm_ids_period))
        print "  # manufacturers:", len(set(list_manuf_period))
        print "  # contractors", len(set(list_contr_period)), "(firms can act as both in general)"
        print "  # non-self contractors", len(set(list_non_self_contractors))
    
        print "  # transactions:", int(cont_transactions_period)   
        try:
            print "  # negative transactions:", int(cont_neg_transactions_period), "  ", cont_neg_transactions_period/cont_transactions_period*100., "%"
            print "  # self-transactions:", int(cont_self_transactions_period), "  ", cont_self_transactions_period/cont_transactions_period*100., "%" 
            print "  # self-neg-transactions:", int(cont_self_neg_transactions_period), "  ", cont_self_neg_transactions_period/cont_transactions_period*100., "%" 
        except ZeroDivisionError: pass

        print "  # unique tuples:",len(set(list_tuplas_period))

        print "row count:", cont-1

        file1= open(name1, 'at')       
        print >> file1, cont_periods, int(cont_transactions_period) 
        file1.close()


        file2= open(name2, 'at')       
        print >> file2, cont_periods, len(set(list_firm_ids_period))
        file2.close()

        try:
            file3= open(name3, 'at')       
            print >> file3, cont_periods, int(cont_neg_transactions_period),  cont_neg_transactions_period/cont_transactions_period*100.
            file3.close()


            file4= open(name4, 'at')       
            print >> file4, cont_periods, int(cont_self_transactions_period), cont_self_transactions_period/cont_transactions_period*100.
            file4.close()
            


            file5= open(name5, 'at')       
            print >> file5, cont_periods, int(cont_self_neg_transactions_period), cont_self_neg_transactions_period/cont_transactions_period*100.
            file5.close()

        except ZeroDivisionError: pass

       


        try:
            name_h="../Results/histogram_num_transact_"+slicing+"_slicing_"+str(cont_periods)+".dat"
            histograma_gral.histogram(dict_link_num_trans_period.values() , name_h)
        except ValueError: pass
   


        print "#  manuf. in dict",len(dict_manuf_dict_contr_amounts_period)
        print "#  contr. in dict",len(dict_contr_dict_manuf_amounts_period)
        




        ########  HHI index as manufacturers and contractors

        for node in G_period.nodes():  
            G_period.node[node]['num_manuf']=0
            G_period.node[node]['num_contractors']=0


        for manufacturer in dict_manuf_dict_contr_amounts_period:
            lista=list(dict_manuf_dict_contr_amounts_period[manufacturer].values())
            HHI=Herfindahl_index.calculate_HHI(lista)    ## tuple  (H, H_normalized)   !!!!           
            G_period.node[manufacturer]['HHI_as_manuf']=HHI[0]
            G_period.node[manufacturer]['num_contractors']=len(lista)      

        for contractor in dict_contr_dict_manuf_amounts_period:
            lista=list(dict_contr_dict_manuf_amounts_period[contractor].values())
            HHI=Herfindahl_index.calculate_HHI(lista)    ## tuple  (H, H_normalized)   !!!!      
            G_period.node[contractor]['HHI_as_contr']=HHI[0]
            G_period.node[contractor]['num_manuf']=len(lista)  
            



        ################  i add topological attributes to the nodes
        #############################
        print "calculating network metrics....."
        print "  CC..."

        if   flag_network_metrics== "YES":
            dict_clustering=nx.clustering(G_period)        
        print "  node betweenness..."


        if   flag_network_metrics== "YES":
            dict_betweenness_nodes=nx.betweenness_centrality(G_period)
        list_k=[]
        for node in G_period.nodes():  
            k=G_period.degree(node)           
            G_period.node[node]["degree"]=k
            list_k.append(k)

            if   flag_network_metrics== "YES":
                G_period.node[node]["CC"]=dict_clustering[node]
                G_period.node[node]["betweeness"]= dict_betweenness_nodes[node]
            else:
                G_period.node[node]["CC"]=0.
                G_period.node[node]["betweeness"]= 0.

            
        try:  
            max_k=max(list_k)            
        except ValueError:
            max_k=0


        print "  edge betweenness..."
        if   flag_network_metrics== "YES":
            dict_betweenness_edges=nx.edge_betweenness_centrality(G_period, normalized=True, weight=None)   # it returns  dictionary of edges (tuplas as keys) with betweenness centrality as the value.   ### i can also calculate the edges' betweenness taking into account their weight!!
        for edge in G_period.edges():  
           # print edge
            try:
                if   flag_network_metrics== "YES":
                    G_period.edge[edge[0]][edge[1]]["link_betweeness"]=dict_betweenness_edges[edge]
                else:
                    G_period.edge[edge[0]][edge[1]]["link_betweeness"]=0.
            except KeyError:
                G_period.edge[edge[0]][edge[1]]["link_betweeness"]="NA"
                print "edge",edge, "not found"
          


        for node in G_period.nodes():

            try:
                G_period.node[node]['HHI_as_manuf']
            except KeyError:
                G_period.node[node]['HHI_as_manuf']="NA"


            try:
                G_period.node[node]['HHI_as_contr']
            except KeyError:
                G_period.node[node]['HHI_as_contr']="NA"





        ####### kshell structure
        print "  kshell..."    
        calculate_kshell(G_period, max_k)
 
       

        ####### max clique size        
        print "  max-clique..."
        for i in G_period.nodes():     

            if   flag_network_metrics== "YES":
                maximo=1     
                lista=nx.cliques_containing_node(G_period, i) #list of lists,  ej: [[207925, 203592], [207925, 10500761], [207925, 200554], [207925, 202587]]
            #  print i, lista
            
                for elem in lista:               
                    if len(elem) > maximo:
                        maximo=len(elem)      
                G_period.node[i]['max_clique_size']=maximo
            else:
                G_period.node[i]['max_clique_size']=0
    



        ####### count fraction of infected links (global and local, with  a threshold for size of neg. transact.)
        dict_node_num_inf_local={}
      
        list_inf_nodes=[]
    
        num_inf_links_global =0.  # only consider links with a fraction of negative dollars larger than X

        H_period_aux = G_period.copy()   # copy to get only the infected links and nodes (for cluster distribution)    
        for edge in G_period.edges():
         
            manufacturer=edge[0]
            contractor=edge[1]


            #### for the count of local infection 
            try:
                dict_node_num_inf_local[manufacturer]
            except KeyError:
                dict_node_num_inf_local[manufacturer]  = 0.
                    
            try:
                dict_node_num_inf_local[contractor] 
            except KeyError:
                dict_node_num_inf_local[contractor]  = 0.





            ########## infected nodes 
            if G_period[manufacturer][contractor]['fract_neg_trans'] > threshold_neg_tran:
                num_inf_links_global  +=1.
                dict_node_num_inf_local[manufacturer] += 1.
                dict_node_num_inf_local[contractor]  += 1.       

                if manufacturer not in list_inf_nodes:
                    list_inf_nodes.append(manufacturer)
                if contractor  not in list_inf_nodes:
                    list_inf_nodes.append(contractor)

            else:  # i remove non-infected links from the aux_graph
                H_period_aux.remove_edge(manufacturer,contractor)







        try:
            fract_inf_links_global = num_inf_links_global / len(G_period.edges())
        except ZeroDivisionError:pass  #if empty network
       

     



       
        print "# nodes in G:", len(G_period.nodes()), " in H_aux:", len(H_period_aux.nodes())
        print "# edges in G:", len(G_period.edges()), " in H_aux:", len(H_period_aux.edges())


        ##### i remove the isolates from aux graph:
        list_to_remove=[]
        for node in H_period_aux.nodes():
            if H_period_aux.degree(node)==0:
                list_to_remove.append(node)
        H_period_aux.remove_nodes_from(list_to_remove)
        print " # nodes in G:", len(G_period.nodes()), " in H_aux:", len(H_period_aux.nodes())
        print " # edges in G:", len(G_period.edges()), " in H_aux:", len(H_period_aux.edges())

       

        list_sizes_inf_components=[]
        #print "components of Infected subgraph:"
        for item in nx.connected_component_subgraphs(H_period_aux):
            try:
                #print "comp. size:",len(item.nodes()),  "  avg.path lenght within component:",nx.average_shortest_path_length(item)
                list_sizes_inf_components.append(len(item.nodes()))
                list_sizes_inf_components_tot.append(len(item.nodes()))

            except ZeroDivisionError: pass
               #print "comp. size:",len(item.nodes())

          
        try:
            Gc = len(max(nx.connected_component_subgraphs(H_period_aux), key=len))
            print "GC:", Gc, "\n"
        except ValueError: 
            Gc="NA"




        ##### print out time evol. of number of infected links and nodes (any-size of neg. transaction)
        file7= open(name7, 'at')       
        try:            
            print >> file7, cont_periods, num_inf_links_global, fract_inf_links_global, len(list_inf_nodes), float(len(list_inf_nodes))/len(G_period.nodes()), Gc, len(G_period.nodes()), len(G_period.edges())
        except ZeroDivisionError:
            print >> file7, cont_periods, num_inf_links_global, fract_inf_links_global, len(list_inf_nodes), "NA", Gc, len(G_period.nodes()), len(G_period.edges())
        file7.close()





        try:
            name_h="../Results/histogram_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing_"+str(cont_periods)+".dat"
            histograma_gral.histogram(list_sizes_inf_components, name_h)



            #### i also dump the raw list of values for KS comparison simu-real data
            pickle_filename="../Results/List_values_tot_size_infected_connected_components_"+slicing+"_slicing_"+str(cont_periods)+".pickle"
        
            pickle.dump(list_sizes_inf_components, open(pickle_filename, 'wb'))
            print "written:",pickle_filename


        except ValueError: pass  # empty network
       





        ######### (here i used to write the corresponding line of the MASTER file)
        #####################
        for edge in G_period.edges():

            manufacturer=edge[0]
            contractor=edge[1]
  

            try:
                dict_tuple_link_Pinf_previous_period[edge]
            except KeyError:
                dict_tuple_link_Pinf_previous_period[edge]=0.
            if cont_periods == 1:
                dict_tuple_link_Pinf_previous_period[edge] ="NA"



            #### count tot number of periods manuf.-contr. have been working together
            try:
                dict_tuple_link_previous_periods_together[edge] +=1            
            except KeyError:
                dict_tuple_link_previous_periods_together[edge]=1
            history=dict_tuple_link_previous_periods_together[edge]



            fract_inf_links_local_manuf =  dict_node_num_inf_local[manufacturer] / float(G_period.degree(manufacturer))
            fract_inf_links_local_contr = dict_node_num_inf_local[contractor] / float(G_period.degree(contractor))


          #################  print fract_inf_links_local_manuf, fract_inf_links_local_contr




            ### i retrieve the info on distance between zips
            zip1="NA"
            zip2="NA"
            dist="NA"
            try:
                zip1= dict_firm_tuple_zip_code_state[manufacturer][0]
                zip2= dict_firm_tuple_zip_code_state[contractor][0]
                tupla=(zip1, zip2)

                try:
                    dist=dict_tuple_zips_dist_miles[tupla]  # there should be both (zip1, zip2)  and (zip2, zip1) as keys to the same dist value.
                except KeyError: pass
            except KeyError: pass



            P_inf=0.  #  1: if there has been at least one neg. transaction between manuf. and contr. during the month, 0 otherwise
            if G_period[manufacturer][contractor]['neg_weight'] != 0:
                P_inf =1.


            try:
                dict_tuple_link_cumulat_previous_Pinf[edge] 
            except KeyError:
                dict_tuple_link_cumulat_previous_Pinf[edge] = 0. 
            if cont_periods == 1:
                dict_tuple_link_cumulat_previous_Pinf[edge] = "NA"



            dict_tuple_link_fract_previous_inf_periods[edge]=0.
            if cont_periods > 1:
                dict_tuple_link_fract_previous_inf_periods[edge]=dict_tuple_link_cumulat_previous_Pinf[edge]/float(cont_periods )
            else:
                dict_tuple_link_fract_previous_inf_periods[edge]="NA"



           
            lista=[]     # avg degree of the manufacturer's neighbours
            for n in G_period.neighbors(manufacturer) :
                lista.append(float(G_period.degree(n)))

            K_nn_i=0.
            try:
                K_nn_i=numpy.mean(lista)
            except :pass


            lista=[]     # avg degree of the manufacturer's neighbours
            for n in G_period.neighbors(contractor) :
                lista.append(float(G_period.degree(n)))

            K_nn_j=0.
            try:
                K_nn_j=numpy.mean(lista)
            except: pass





            amount_pos_self_trans_i=0.
            amount_pos_self_trans_j=0.
            try:
                amount_pos_self_trans_i=dict_firm_amount_pos_self_trans_period[manufacturer]
            except KeyError: pass
            try:
                amount_pos_self_trans_j=dict_firm_amount_pos_self_trans_period[contractor]
            except KeyError: pass


            amount_neg_self_trans_i=0.
            amount_neg_self_trans_j=0.
            try:
                amount_neg_self_trans_i=dict_firm_amount_neg_self_trans_period[manufacturer]
            except KeyError: pass
            try:
                amount_neg_self_trans_j=dict_firm_amount_neg_self_trans_period[contractor]
            except KeyError: pass


            num_pos_self_trans_i=0.
            num_pos_self_trans_j=0.
            try:
                num_pos_self_trans_i=dict_firm_num_pos_self_trans_period[manufacturer]
            except KeyError: pass
            try:
                num_pos_self_trans_j=dict_firm_num_pos_self_trans_period[contractor]
            except KeyError: pass


            num_neg_self_trans_i=0.
            num_neg_self_trans_j=0.
            try:
                num_neg_self_trans_i=dict_firm_num_neg_self_trans_period[manufacturer]
            except KeyError: pass
            try:
                num_neg_self_trans_j=dict_firm_num_neg_self_trans_period[contractor]
            except KeyError: pass


            try:
                fract_pos_bussiness_of_M_with_C=  G_period[manufacturer][contractor]['pos_weight'] / G_period.node[manufacturer]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_bussiness_of_M_with_C="NA"  #  (otherwise i cant define business asymmetry)

            try:
                fract_pos_bussiness_of_C_with_M=  G_period[manufacturer][contractor]['pos_weight'] / G_period.node[contractor]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_bussiness_of_C_with_M="NA"  #(otherwise i cant define business asymmetry)


            try:
                error_size_ij= -1.*G_period[manufacturer][contractor]['neg_weight'] / G_period[manufacturer][contractor]['pos_weight']
            except ZeroDivisionError:
                error_size_ij="NA"
                if G_period[manufacturer][contractor]['neg_weight'] != 0.:
                    error_size_ij= -1.

            degree_asymmetry_ij= float(( G_period.degree(manufacturer) - G_period.degree(contractor)) * (G_period.degree(manufacturer)- G_period.degree(contractor))) / float((G_period.degree(manufacturer) + G_period.degree(contractor)) * (G_period.degree(manufacturer)+ G_period.degree(contractor)))



            business_asymmetry_ij="NA"
            try:
                business_asymmetry_ij = ((fract_pos_bussiness_of_M_with_C  - fract_pos_bussiness_of_C_with_M )* (fract_pos_bussiness_of_M_with_C  - fract_pos_bussiness_of_C_with_M)) / ((fract_pos_bussiness_of_M_with_C  + fract_pos_bussiness_of_C_with_M) * (fract_pos_bussiness_of_M_with_C  + fract_pos_bussiness_of_C_with_M))
            except:  pass  # either for a zerodivision error, or because one of the elements is a NA






            print >> file6, P_inf, G_period[manufacturer][contractor]['pos_weight']+G_period[manufacturer][contractor]['neg_weight'],                                            G_period[manufacturer][contractor]['pos_weight'], G_period[manufacturer][contractor]['neg_weight'],                                                                 G_period.node[manufacturer]['vol_pos_transct'] ,   G_period.node[manufacturer]['vol_neg_transct'],                                                                  G_period.node[contractor]['vol_pos_transct'] ,   G_period.node[contractor]['vol_neg_transct'],                                                                      dict_tuple_link_Pinf_previous_period[edge], dict_tuple_link_cumulat_previous_Pinf[edge],                                                                            dict_tuple_link_fract_previous_inf_periods[edge],                                                                                                                   G_period.degree(manufacturer), G_period.degree(contractor),  K_nn_i, K_nn_j, G_period.node[manufacturer]['HHI_as_manuf'],                                           G_period.node[manufacturer]['HHI_as_contr'],  G_period.node[contractor]['HHI_as_manuf'],  G_period.node[contractor]['HHI_as_contr'],                                G_period.node[manufacturer]['betweeness'],  G_period.node[contractor]['betweeness'], G_period[manufacturer][contractor]['link_betweeness'],                         G_period.node[manufacturer]['max_clique_size'], G_period.node[contractor]['max_clique_size'], G_period.node[manufacturer]['kshell'],                                G_period.node[contractor]['kshell'], G_period.node[manufacturer]['num_manuf'], G_period.node[manufacturer]['num_contractors'],                                      G_period.node[contractor]['num_manuf'], G_period.node[contractor]['num_contractors'],                                                                               G_period[manufacturer][contractor]['num_pos_trans']+G_period[manufacturer][contractor]['num_neg_trans'],                                                            G_period.node[manufacturer]['num_transact'], G_period.node[contractor]['num_transact'],                                                                             amount_pos_self_trans_i, amount_pos_self_trans_j, amount_neg_self_trans_i, amount_neg_self_trans_j,                                                                 num_pos_self_trans_i, num_pos_self_trans_j, num_neg_self_trans_i, num_neg_self_trans_j,                                                                             fract_pos_bussiness_of_M_with_C, fract_pos_bussiness_of_C_with_M, degree_asymmetry_ij, business_asymmetry_ij,                                                       error_size_ij, dist , current_data_month,  current_data_season, fract_inf_links_global, fract_inf_links_local_manuf, fract_inf_links_local_contr, history





# print  >> file_master,  manufacturer, contractor,str(manufacturer)+str(contractor), cont_months,                                                                   G_month[manufacturer][contractor]['pos_weight']+G_month[manufacturer][contractor]['neg_weight'],                                                                   G_month[manufacturer][contractor]['pos_weight'], G_month[manufacturer][contractor]['neg_weight'],                                                                  G_month.node[manufacturer]['vol_pos_transct'] ,   G_month.node[manufacturer]['vol_neg_transct'],                                                                   G_month.node[contractor]['vol_pos_transct'] ,   G_month.node[contractor]['vol_neg_transct'],                                                                       P_inf, dict_tuple_link_Pinf_previous_month[edge], dict_tuple_link_cumulat_previous_Pinf[edge],                                                                     dict_tuple_link_fract_previous_inf_months[edge],                                                                                                                   G_month.degree(manufacturer), G_month.degree(contractor),  K_nn_i, K_nn_j, G_month.node[manufacturer]['HHI_as_manuf'],                                             G_month.node[manufacturer]['HHI_as_contr'],  G_month.node[contractor]['HHI_as_manuf'],  G_month.node[contractor]['HHI_as_contr'],                                  G_month.node[manufacturer]['betweeness'],  G_month.node[contractor]['betweeness'], G_month[manufacturer][contractor]['link_betweeness'],                           G_month.node[manufacturer]['max_clique_size'], G_month.node[contractor]['max_clique_size'], G_month.node[manufacturer]['kshell'],                                  G_month.node[contractor]['kshell'], G_month.node[manufacturer]['num_manuf'], G_month.node[manufacturer]['num_contractors'],                                        G_month.node[contractor]['num_manuf'], G_month.node[contractor]['num_contractors'],                                                                                G_month[manufacturer][contractor]['num_pos_trans']+G_month[manufacturer][contractor]['num_neg_trans'],                                                             G_month.node[manufacturer]['num_transact'], G_month.node[contractor]['num_transact'],                                                                              amount_pos_self_trans_i, amount_pos_self_trans_j, amount_neg_self_trans_i, amount_neg_self_trans_j,                                                                num_pos_self_trans_i, num_pos_self_trans_j, num_neg_self_trans_i, num_neg_self_trans_j,                                                                            fract_pos_bussiness_of_M_with_C, fract_pos_bussiness_of_C_with_M, degree_asymmetry_ij, business_asymmetry_ij, error_size_ij            


         
            ### for next month
            try:
                dict_tuple_link_Pinf_previous_period[edge]=P_inf
            except TypeError:
                dict_tuple_link_Pinf_previous_period[edge]= 0.


            try:
                dict_tuple_link_cumulat_previous_Pinf[edge] += P_inf
            except TypeError:
                dict_tuple_link_cumulat_previous_Pinf[edge] = 0.


        
        ########  write the monthly  network
        filename_network="../Results/Supply_network_slicing_"+slicing+"_period_"+str(cont_periods)+string_filename
        pickle.dump(G_period, open(filename_network+".pickle", 'wb'))
        print "  written", filename_network+".pickle"

        nx.write_gml(G_period,filename_network+".gml")
        print "  written", filename_network+".gml"
        print "  N:",len(G_period.nodes()), " L:",len(G_period.edges())


        #### only the infected subgraph
        filename_network="../Results/Supply_network_infected_slicing_"+slicing+"_period_"+str(cont_periods)+string_filename
        nx.write_gml(H_period_aux,filename_network+".gml")
        print "  written", filename_network+".gml"
        print "  N:",len(H_period_aux.nodes()), " L:",len(H_period_aux.edges())



        #nx.write_gexf(G_period,filename_network+".gexf")   # gephi format
        #print "  written", filename_network+".gexf"


        G_no_loops = remove_self_loops(G_period)
        print "   without self-loops:",len(G_no_loops.nodes()), " L:",len(G_no_loops.edges())
        print "# nodes (aggregated so far):",len(G.nodes()), " # links (id):", len(G.edges())


    
    file6.close()
    print "\n\nwritten file:",name6
    
    ########## end of loop over the ALL_years file
    ##################################################
    ##################################################





    try:
        name_h="../Results/histogram_tot_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"
        histograma_gral.histogram(list_sizes_inf_components_tot, name_h)


        #### i also dump the raw list of values for KS comparison simu-real data
        pickle_filename="../Results/List_values_tot_size_infected_connected_components_"+slicing+"_slicing.dat"
        
        pickle.dump(list_sizes_inf_components_tot, open(pickle_filename, 'wb'))
        print "written:",pickle_filename
        

    except ValueError: pass  # empty list
       

       



    try:
        name_h="../Results/histogram_transaction_period_lengths.dat"
        histograma_gral.histogram( list_periods, name_h)



        name_h="../Results/histogram_num_transact_per_period_all.dat"
        histograma_gral.histogram(dict_link_num_trans.values() , name_h)
    except ValueError: pass
   



    print "\n\nAggregated network:"
    print "tot. # firms:", len(set(list_firm_ids))
    print "tot. # transactions:", int(cont_transactions)
    try:
        print "tot. # negative transactions:", int(cont_neg_transactions), "  ", cont_neg_transactions/cont_transactions*100., "%"
        print "tot. # self-transactions:", int(cont_self_transactions), "  ", cont_self_transactions/cont_transactions*100., "%" 
        print "tot. # self-neg-transactions:", int(cont_self_neg_transactions), "  ", cont_self_neg_transactions/cont_transactions*100., "%" 
    except ZeroDivisionError: pass


    print "  # unique tuples:",len(set(list_tuplas))

    for firm in G.nodes():        
        G.node[firm]['vol_transct']=dict_firm_total_trans_volum[firm]                
        G.node[firm]['fract_neg_transct']=dict_firm_num_neg_trans[firm] /(dict_firm_num_neg_trans[firm] + dict_firm_num_pos_trans[firm])      
        G.node[firm]['num_transact']= dict_firm_num_neg_trans[firm] + dict_firm_num_pos_trans[firm]
        
        G.node[firm]['num_manuf']=0
        G.node[firm]['num_contractors']=0

        

    for  link in dict_link_num_pos_trans:
        G[link[0]][link[1]]['num_pos_trans']= dict_link_num_pos_trans[link]    
        G[link[0]][link[1]]['num_neg_trans']= dict_link_num_neg_trans[link]            
        G[link[0]][link[1]]['fract_neg_trans']= dict_link_num_neg_trans[link] / (dict_link_num_neg_trans[link] + dict_link_num_pos_trans[link] )  
        
        if  G[link[0]][link[1]]['num_neg_trans'] == 0.:
            G[link[0]][link[1]]['neg_weight']=0.

        if  G[link[0]][link[1]]['num_pos_trans'] == 0.:
            G[link[0]][link[1]]['pos_weight']=0.





    ################  i add topological attributes to the nodes
    ###########################
    print "calculating network metrics:"
    print "  CC..."
    if   flag_network_metrics== "YES":
        dict_clustering=nx.clustering(G)

     
    print "  node betweenness..."
    if   flag_network_metrics== "YES":
        dict_betweenness_nodes=nx.betweenness_centrality(G)   
    list_k=[]
    for node in G.nodes():  
        k=G.degree(node)           
        G.node[node]["degree"]=k
        list_k.append(k)
        if   flag_network_metrics== "YES":
            G.node[node]["CC"]=dict_clustering[node]
            G.node[node]["betweeness"]=dict_betweenness_nodes[node]
        else:
            G.node[node]["CC"]=0.
            G.node[node]["betweeness"]=0.


    try:  
        max_k=max(list_k)            
    except ValueError:
        max_k=0
   

    print "  edge betweenness..."
    if   flag_network_metrics== "YES":
        dict_betweenness_edges=nx.edge_betweenness_centrality(G, normalized=True, weight=None)   # it returns  dictionary of edges (tuplas as keys) with betweenness centrality as the value.   ### i can also calculate the edges' betweenness taking into account their weight!!
    for edge in G.edges():  
           # print edge
        try:
            if   flag_network_metrics== "YES":
                G.edge[edge[0]][edge[1]]["link_betweeness"]=dict_betweenness_edges[edge]
            else:
                G.edge[edge[0]][edge[1]]["link_betweeness"]=0
        except KeyError:
            G.edge[edge[0]][edge[1]]["link_betweeness"]="NA"
            print "edge",edge, "not found"
          

    #######  k-shell decomposition   (i need to make a copy and remove the self-loops from that before i can proceed)
    print "  kshell..."    
    if   flag_network_metrics== "YES":
        calculate_kshell(G, max_k)
 
       

    ####### max clique size   
    print "  max-clique..."
    for node in G.nodes():    

        if   flag_network_metrics== "YES":   
            maximo=1     
            lista=nx.cliques_containing_node(G, node) #list of lists,  ej: [[207925, 203592], [207925, 10500761], [207925, 200554], [207925, 202587]]
          #  print i, lista
            
            for elem in lista:               
                if len(elem) > maximo:
                    maximo=len(elem)      
            G.node[i]['max_clique_size']=maximo
        else:
            G.node[i]['max_clique_size']=0




    #######  HHI index as manufacturer and as contractor
    for manufact in dict_manuf_dict_contr_amounts:
        lista=list(dict_manuf_dict_contr_amounts[manufact].values())
        HHI=Herfindahl_index.calculate_HHI(lista)         
        G.node[manufact]['HHI_as_manuf']=HHI[0]
        G.node[manufact]['num_contractors']=len(lista)
        
    for contr in dict_contr_dict_manuf_amounts:
        lista=list(dict_contr_dict_manuf_amounts[contr].values())
        HHI=Herfindahl_index.calculate_HHI(lista)       
        G.node[contr]['HHI_as_contr']=HHI[0]
        G.node[contr]['num_manuf']=len(lista)
        





    ########  write the aggregated network
    filename_network="../Results/Supply_network_"+str(initial_year)+"_"+str(final_year)+string_filename
    pickle.dump(G, open(filename_network+".pickle", 'wb'))
    print "written", filename_network+".pickle"

    nx.write_gml(G,filename_network+".gml")
    print "written", filename_network+".gml"

    print "N:",len(G.nodes()), " L:",len(G.edges())

    G_no_loops = remove_self_loops(G)
    print "   without self-loops:",len(G_no_loops.nodes()), " L:",len(G_no_loops.edges())








    print    

    if  flag_hist == "YES":
        name_h="../Results/histogram_pos_adj_gross_values_"+slicing+"_slicing_"+str(initial_year)+"_"+str(final_year)+".dat"
        histograma_gral.histogram(list_pos_adj_gross, name_h)
#    print "# obsrv:",len(list_pos_adj_gross), "  max.", max(list_pos_adj_gross), "  min.", min(list_pos_adj_gross), "  avg:", numpy.mean(list_pos_adj_gross), "  sd:", numpy.std(list_pos_adj_gross)



    print 


    if  flag_hist == "YES":
        name_h="../Results/histogram_neg_adj_gross_values_" +slicing+"_slicing_"+str(initial_year)+"_"+str(final_year)+".dat"
        histograma_gral.histogram(list_neg_adj_gross, name_h)
   # print "# obsrv:",len(list_neg_adj_gross), "  max.", -1.*max(list_neg_adj_gross), "  min.", -1.*min(list_neg_adj_gross), "  avg:", -1.*numpy.mean(list_neg_adj_gross), "  sd:", numpy.std(list_neg_adj_gross)






    print "written:",name1
    print "written:",name2
    print "written:",name3
    print "written:",name4
  




    for period in sorted(dict_period_tot_vol_posit_transact):
        print >> file8, period, dict_period_tot_vol_posit_transact[period]
    file8.close()
    print "written:",name8
  


#############################################
#############################################
#############################################
#############################################
def  remove_self_loops(G):
      
    G_no_self_loops = nx.Graph(G.subgraph(G.nodes()))
    
    list_edges_to_remove=[]
    for edge in G_no_self_loops.edges():
        if edge[0] == edge[1]:
            list_edges_to_remove.append(edge)

    for edge in  list_edges_to_remove:
        G_no_self_loops.remove_edge(edge[0], edge[1])

    return  G_no_self_loops




def  calculate_kshell(G, max_k): ####  k-shell decomposition   (i need to make a copy and remove the self-loops from that before i can proceed)    
        
    G_for_kshell = remove_self_loops(G)
                    

    for node in G_for_kshell.nodes():
        G.node[node]["kshell"]=0


    cont_zeros=0      
    for i in range(max_k):   # k_max is the absolute upper boundary for max kshell index
        kshell= nx.k_shell(G_for_kshell, k=i, core_number=None)  # it returns the k-shell subgraph
        size_shell=len(kshell)
           # print  "    ",i, size_shell, kshell.nodes()
        for node in kshell.nodes():
            G.node[node]["kshell"]=i

        if size_shell==0:
            cont_zeros +=1       
        if cont_zeros >=7:  # to stop calculating shells after a few come back empty ones
            break



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

