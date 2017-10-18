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



    slicing="yearly"    #"monthly"  # or "yearly"

    threshold_neg_tran=0.   # fraction of negative dollars out of the total amount of dollars transacted, to consider a link infected between two companies



    flag_remove_selfloops="YES"
    string_filename_loops=""
    if flag_remove_selfloops=="NO":
        string_filename_loops="_with_self_loops"


    string_filename=""
    if flag_network_metrics=="NO":
        string_filename="_no_network_metrics"






    dict_firm_tuple_zip_code_state = pickle.load(open("../Results/dict_firm_id_zip_code.pickle", 'rb')) # example:  05188210: ('94108', 'CA')

    dict_tuple_zips_dist_miles= pickle.load(open("../Results/dict_zip_tuples_dist_miles_from_34Gb.pickle", 'rb'))   ### example:  (zip1,zip2): distance_miles



    list_jobbers_tot = pickle.load(open("../Results/List_jobbers_tot.dat"))



   

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



    name7="../Results/Time_evol_tot_num_infected_links_nodes_GC_"+slicing+"_slicing.dat"
    file7= open(name7, 'wt')
    file7.close()


    name8="../Results/Time_evol_tot_num_infected_links_nodes_GC_with_neg_transact_larger_than"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"
    file8= open(name8, 'wt')
    file8.close()




    name6="../Results/Scatter_plot_Pinf_vs_mulitiple_variables_"+slicing+"_slicing"+string_filename+"_for_doublechecking.dat"
    file6= open(name6, 'wt') 
   # header for the file:  
  

    print >> file6,  "P_inf", "Mi", "Cj", "Mi_Cj", "adj_gross_ij", "cumulat_adj_gross_ij", "pos_adj_gross_ij", "neg_adj_gross_ij", "cumulat_pos_adj_gross_ij", "cumulat_neg_adj_gross_ij", "pos_adj_gross_i", "neg_adj_gross_i", "pos_adj_gross_j", "neg_adj_gross_j", "cumulat_pos_adj_gross_i", "cumulat_neg_adj_gross_i", "cumulat_pos_adj_gross_j", "cumulat_neg_adj_gross_j", "P_inf_previous_month_link", "Cumulat_num_inf_months_link", "frac_previous_inf_months_link", "P_inf_previous_month_i", "Cumulat_num_inf_months_i", "frac_previous_inf_months_i", "P_inf_previous_month_j", "Cumulat_num_inf_months_j", "frac_previous_inf_months_j", "ki", "kj", "K_nn_i", "K_nn_j", "HHIi_as_manuf", "HHIi_as_contr", "HHIj_as_manuf", "HHIj_as_contr", "betweenness_i", "betweenness_j", "link_betweenness_ij", "max_clique_i", "max_clique_j",  "cumulat_max_clique_i", "cumulat_max_clique_j","kshell_i", "kshell_j","cumulat_kshell_i", "cumulat_kshell_j", "num_manuf_i", "num_contr_i", "num_manuf_j", "num_contr_j", "num_transact_ij", "num_transact_i", "num_transact_j", "amount_pos_self_trans_i", "amount_pos_self_trans_j", "amount_neg_self_trans_i", "amount_neg_self_trans_j", "num_pos_self_trans_i", "num_pos_self_trans_j", "num_neg_self_trans_i", "num_neg_self_trans_j", "fract_pos_bussiness_of_M_with_C", "fract_pos_bussiness_of_C_with_M", "degree_asymmetry_ij", "business_asymmetry_ij", "error_size_ij", "dist", "month", "season", "fract_inf_links_global", "fract_inf_links_local_i", "fract_inf_links_local_j", "fract_inf_links_local_i_previous", "fract_inf_links_local_j_previous", "history_ij", "month_count","year","N", "L"




   #  print G_period.nodes(data=True)   #example:   (2318295, {'degree': 3, 'num_contractors': 0, 'HHI_as_contr': 0.3724172065553589, 'CC': 0.0, 'num_transact': 4.0, 'vol_transct': 13121.0, 'fract_neg_transct': 0.25, 'HHI_as_manuf': 'NA', 'max_clique_size': 2, 'num_manuf': 3, 'vol_pos_transct': 13122.0, 'vol_neg_transct': -1.0, 'kshell': 2, 'betweeness': 0.0008438954375540839})

    #  print G_period.edges(data=True)  # example: (514603, 2302275, {'pos_weight': 23989, 'num_neg_trans': 0.0, 'fract_neg_trans': 0.0, 'num_pos_trans': 1.0, 'link_betweeness': 0.0016097736255839023, 'neg_weight': 0.0})
                               


    G=nx.Graph()   ##  this is the cumulative network including all transactions up to time period t


    print
    print
    
    list_periods=[]

    list_firm_ids=[]

    cont_transactions=0.
    cont_neg_transactions=0.
    cont_neg_transactions_threshold=0.
    cont_self_transactions=0.
    cont_self_neg_transactions=0.


    dict_firm_id_active_periods={}
    dict_tuple_ids_active_periods={}
    dict_firm_total_trans_volum={}

   
    dict_firm_num_pos_trans={}
    dict_firm_num_neg_trans={}

    dict_tuple_link_cumulat_previous_Pinf={}
    dict_tuple_link_fract_previous_inf_periods={}
    dict_tuple_link_Pinf_previous_period={}


    dict_firm_cumulat_previous_Pinf={}
    dict_firm_fract_previous_inf_periods={}
    dict_firm_Pinf_previous_period={}





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



    list_manuf_tot=[]  # list all manuf, and contr (excluding any selftransaction)
    list_contr_tot=[]

    list_sizes_inf_components_tot=[]
    list_sizes_inf_components_tot_threshold=[]
    cont_periods=0
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




        dict_manuf_dict_contr_amounts_period={}  # for each manufact., dict of its contractors and total amounts
        dict_contr_dict_manuf_amounts_period={}   # for each contract., dict of its manuf. and total amounts


        cont_transactions_period=0.
        cont_neg_transactions_period=0.
        cont_neg_transactions_period_threshold=0.
        cont_self_transactions_period=0.
        cont_self_neg_transactions_period=0.

## examples of firms that act boths as manuf. and contractor (AFTER EXCLUDING ALREADY SELF-TRANSACTIONS!!)  "JOBBERS"
#overlap between manuf. and contr: set([409601, 518153, 506199, 512023, 2324507, 901155, 9900068, 2310181, 518207, 600131, 116804, 9900101, 9900111, 200785, 3201107, 2324571, 2300011, 2392173, 9900147, 522363, 106321, 202885, 2001032, 2306190, 260241, 510099, 66404501, 2300055, 510105, 700575, 2304181, 700599, 1300672, 106689, 403659, 2324684, 2390221, 2304211, 405723, 1300702, 2366873, 510181, 401638, 501992, 2320617, 102635, 800466, 6203632, 401651, 116981, 2320630, 508287, 6203644, 600325, 700681, 9900299, 2324866, 205072, 106771, 411929, 102684, 151841, 9101603, 411942, 9900329, 9900330, 203051, 2314541, 411954, 114996, 9900342, 2314552, 2304314, 2324799, 522562, 2318659, 2320708, 1300805, 9101640, 522569, 514381, 9101652, 500055, 512345, 2302299, 2322781, 2324830, 203105, 2003314, 801173, 6601081, 2306426, 2322811, 12200316, 901866, 412031, 403842, 2308484, 520585, 9101706, 2392461, 2304399, 504208, 520597, 2396567, 700824, 20591002, 2316699, 500124, 2320794, 412065, 9101731, 500136, 405929, 9101743, 700851, 2324921, 2366197, 2322882, 408311, 2003405, 115150, 2300369, 2365908, 6203863, 512473, 2320861, 12200419, 2001381, 6203887, 408049, 510452, 109046, 512503, 107001, 6203899, 2365952, 403970, 800171, 102921, 2320927, 2316833, 10500187, 100900, 2365990, 400804, 2325044, 401985, 2306827, 1301060, 102982, 2319457, 2003533, 506448, 600660, 6203991, 150125, 205424, 510580, 2366073, 205436, 600702, 109186, 203397, 9106054, 2394765, 111247, 522909, 402084, 412326, 901799, 504488, 2319020, 109231, 2306736, 2366134, 400055, 10500795, 2314940, 2364098, 2323141, 901830, 408268, 2366157, 2366159, 512722, 506591, 2300643, 703205, 2321130, 207597, 105201, 113396, 412405, 516855, 203521, 15502083, 2319111, 6204171, 2366223, 2312980, 2366233, 2321181, 402217, 406314, 6204211, 3200139, 2323281, 2304855, 404317, 901982, 504671, 516961, 2319202, 207721, 500586, 2311021, 207731, 2319226, 207743, 516995, 902020, 101254, 521097, 2321294, 2325391, 402321, 101278, 20595620, 2366373, 2323370, 904107, 6204338, 2393013, 406454, 406466, 510749, 500677, 2366413, 2001871, 408530, 402394, 2700256, 900783, 2319330, 703461, 2325329, 2323436, 204626, 601071, 703473, 2366452, 517291, 408581, 15502344, 10501131, 2324994, 2366478, 902159, 402448, 2319378, 113694, 404512, 2323503, 2366516, 410691, 2366535, 502856, 2302135, 2321488, 410706, 2318179, 2323540, 201820, 513118, 513121, 513131, 2366572, 101485, 2002036, 402281, 2325627, 2324672, 900229, 12203147, 801151, 2323606, 410780, 2321579, 402291, 20591798, 506059, 2301131, 408785, 410834, 509139, 2323679, 408803, 9905388, 6601972, 2366709, 2321658, 15502587, 105727, 521474, 410883, 509191, 2319627, 10503437, 109848, 1500442, 2324015, 150812, 517409, 111909, 2002218, 408876, 402734, 504713, 513337, 2366779, 2307388, 3200322, 2319688, 402761, 404810, 101710, 2323795, 408918, 2301271, 1502554, 406879, 2325861, 505201, 3200371, 603508, 411000, 515450, 402813, 501128, 517513, 2366858, 521620, 505237, 2307480, 521796, 9100702, 900515, 2321828, 2301350, 522563, 9900615, 2323886, 2366573, 13200816, 2323898, 2309567, 6604225, 66405826, 6600131, 800201, 19000783, 406995, 153047, 2366714, 800223, 20590055, 2309609, 501232, 2323953, 20596211, 2301428, 260010, 20500055, 511501, 509462, 2303577, 9100829, 2323998, 509474, 800296, 1500715, 513581, 511535, 6602290, 9910537, 108091, 507453, 6207042, 105739, 1500740, 1201741, 1201744, 2324052, 517719, 151129, 151130, 2700891, 6602332, 106082, 2303590, 2313832, 106094, 104048, 2319986, 2700918, 2324091, 104061, 405127, 2324106, 411280, 405140, 800405, 6207126, 2305689, 6203036, 1900079, 2324131, 411310, 2324143, 507568, 116403, 2305720, 521929, 153291, 513741, 6207182, 1500880, 411346, 100055, 6207194, 2305756, 1300192, 507623, 2301672, 412284, 2322158, 2324222, 2307595, 411401, 151312, 503769, 407321, 501530, 2324261, 501542, 2307881, 2322055, 509747, 151348, 517941, 114492, 505675, 6604625, 6604626, 6604630, 501591, 110425, 113979, 2324325, 1503078, 409455, 411504, 104309, 505493, 15507329, 20596612, 2314125, 2000787, 2324374, 2318121, 2700271, 522565, 1300386, 501669, 202666, 522568, 202678, 2305975, 202681, 20593994, 200645, 6203334, 401353, 2324428, 405462, 12202660, 501724, 411619, 401389, 2701297, 102386, 9900020, 600055, 516090, 260095]) (excluding first all self transactions)





        G_period=nx.Graph()   ##  this is the cumulative network including all transactions during time period t


        list_manuf_period=[]
        list_contr_period=[]
        list_non_self_contractors=[]

        cont_jobber_involved=0



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

           if year == 2030:
               year = 2003  # there are a bunch of entries with impossible year: 13201742,13200981,40103,63030,-0.18,-18,


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

                    flag_manuf_jobber=0
                    flag_contr_jobber=0

                    manufacturer=int(list_row[0])     ##paidbyfirm
                    contractor=int(list_row[1])      ## paidforfirm                                
             

                    if manufacturer in list_jobbers_tot:
                        flag_manuf_jobber=1
                    if contractor in list_jobbers_tot:
                        flag_contr_jobber=1




                    if manufacturer != contractor :
                        list_manuf_tot.append(manufacturer)
                        list_contr_tot.append(contractor)

                        list_manuf_period.append(manufacturer)
                        list_contr_period.append(contractor)
             


             
                    cont_transactions +=1
                    cont_transactions_period +=1



                    ########### list of active periods for pairs
                    tupla_link=(manufacturer, contractor)       
                    try:
                        dict_tuple_ids_active_periods[tupla_link].append(cont_periods)
                    except KeyError:
                        dict_tuple_ids_active_periods[tupla_link]=[]
                        dict_tuple_ids_active_periods[tupla_link].append(cont_periods)





                    ############## for now i deal with integers Dollars !!  (easier for histograms)
                    adj_gross=int(round(float((list_row[4]))))    
              
                                 
                    if manufacturer == contractor:
                          cont_self_transactions  +=1.
                          cont_self_transactions_period  +=1.
                          if flag_remove_selfloops=="YES":
                            flag_ignore_row=1
       
                          ########## if it is a self-transaction, i only record these variables (no network variables nor HHI etc)
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


                       G_period.add_node(manufacturer)
                       G_period.add_node(contractor)


                       G.add_node(manufacturer)
                       G.add_node(contractor)


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





            try:
                G[link[0]][link[1]]['num_neg_trans'] #+= G_period[link[0]][link[1]]['num_neg_trans']
                G[link[0]][link[1]]['neg_weight'] #+= G_period[link[0]][link[1]]['neg_weight']
            except KeyError:
                G[link[0]][link[1]]['num_neg_trans'] = 0.
                G[link[0]][link[1]]['neg_weight'] = 0.


            try:               
                G[link[0]][link[1]]['pos_weight'] #+= G_period[link[0]][link[1]]['pos_weight']
            except KeyError:
                G[link[0]][link[1]]['pos_weight'] = 0.


    



        for firm in G_period.nodes():           

            G_period.node[firm]['vol_transct']=dict_firm_total_trans_volum_period[firm]                                                   
            G_period.node[firm]['fract_neg_transct']=dict_firm_num_neg_trans_period[firm] /(dict_firm_num_neg_trans_period[firm] + dict_firm_num_pos_trans_period[firm])  
                                    
            G_period.node[firm]['num_transact']= dict_firm_num_neg_trans_period[firm] + dict_firm_num_pos_trans_period[firm]
                    
   
     



        for firm in dict_firm_tot_pos_trans_period:
            G_period.node[firm]['vol_pos_transct']=dict_firm_tot_pos_trans_period[firm]
            try:
                G.node[firm]['vol_pos_transct']  +=G_period.node[firm]['vol_pos_transct']
            except KeyError:
                G.node[firm]['vol_pos_transct']=0.


        for firm in dict_firm_tot_neg_trans_period:
            G_period.node[firm]['vol_neg_transct']=dict_firm_tot_neg_trans_period[firm]

            try:
                G.node[firm]['vol_neg_transct'] +=G_period.node[firm]['vol_neg_transct']
            except KeyError:
                G.node[firm]['vol_neg_transct']=0.




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




            try:
                G.node[node]['vol_pos_transct']
            except KeyError:
                G.node[node]['vol_pos_transct']=0.

            try:
                G.node[node]['vol_neg_transct']
            except KeyError:
                G.node[node]['vol_neg_transct']=0.





        list_jobbers_period= list(set(list_manuf_period) & set(list_contr_period))
        jobbers_period=len(list_jobbers_period)
        jobbers_total=len(set(list_manuf_tot) & set(list_contr_tot))

        list_manuf_period_no_jobbers= list(set(list_manuf_period) - set(list_jobbers_period))
        num_manuf_period_no_jobbers=len(set(list_manuf_period_no_jobbers))

        list_contr_period_no_jobbers= list(set(list_contr_period) - set(list_jobbers_period))
        num_contr_period_no_jobbers=len(set(list_contr_period_no_jobbers))


        try:
            print " period",cont_periods
            print "  # firms:", len(set(list_firm_ids_period))
            print "  # manufacturers:", len(set(list_manuf_period)), " excluding jobbers:", num_manuf_period_no_jobbers,  float(jobbers_period) / num_manuf_period_no_jobbers
            print "  # contractors", len(set(list_contr_period)),  " excluding jobbers:", num_contr_period_no_jobbers,  float(jobbers_period) / num_contr_period_no_jobbers
            #  print "  # non-self contractors", len(set(list_non_self_contractors))
            
            print "  # jobbers (overlap between manuf. & contr period):", jobbers_period , "(excluding self-trans)     and total:", jobbers_total
            
            print "  manuf + contr+ jobbers:",  num_manuf_period_no_jobbers + num_contr_period_no_jobbers + jobbers_period
            print "  # transactions:", int(cont_transactions_period)   
            
            print "  # negative transactions:", int(cont_neg_transactions_period), "  ", cont_neg_transactions_period/cont_transactions_period*100., "%"
            print "  # self-transactions:", int(cont_self_transactions_period), "  ", cont_self_transactions_period/cont_transactions_period*100., "%" 
            print "  # self-neg-transactions:", int(cont_self_neg_transactions_period), "  ", cont_self_neg_transactions_period/cont_transactions_period*100., "%" 

           # print "num instances with jobber involved:", cont_jobber_involved, float(cont_jobber_involved)/(2.*cont_transactions_period)
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

       


       # try:
        #    name_h="../Results/histogram_num_transact_"+slicing+"_slicing_"+str(cont_periods)+".dat"
         #   histograma_gral.histogram(dict_link_num_trans_period.values() , name_h)
        #except ValueError: pass
   



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
 #       print "calculating network metrics....."
#        print "  CC..."

        if   flag_network_metrics== "YES":
            dict_clustering=nx.clustering(G_period)        
#        print "  node betweenness..."


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


#        print "  edge betweenness..."
        if   flag_network_metrics== "YES":
            dict_betweenness_edges=nx.edge_betweenness_centrality(G_period, normalized=True, weight=None)   # it returns  dictionary of edges (tuplas as keys) with betweenness centrality as the value.   ### i can also calculate the edges' betweenness taking into account their weight!!
        for edge in G_period.edges():  

            try:
                if   flag_network_metrics== "YES":
                    G_period.edge[edge[0]][edge[1]]["link_betweeness"]=dict_betweenness_edges[edge]
                else:
                    G_period.edge[edge[0]][edge[1]]["link_betweeness"]=0.
            except TypeError:                             
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





        ####### kshell structure  (i need to make a copy and remove the self-loops from that before i can proceed)
#        print "  kshell..."    
        calculate_kshell(G_period, max_k)
        calculate_kshell(G, max_k)
 
       

        ####### max clique size        
#        print "  max-clique (period)...."
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
                G_period.node[i]['max_clique_size']=1
    

 
       

        ####### max clique size   
#        print "  max-clique (cumulative network)...."
        for i in G.nodes():    

            if   flag_network_metrics== "YES":   
                maximo=1     
                lista=nx.cliques_containing_node(G, node) #list of lists,  ej: [[207925, 203592], [207925, 10500761], [207925, 200554], [207925, 202587]]
          #  print i, lista
            
                for elem in lista:               
                    if len(elem) > maximo:
                        maximo=len(elem)      
                G.node[i]['max_clique_size']=maximo
            else:
                G.node[i]['max_clique_size']=1






        ####### count fraction of infected links (global and local, with and without a threshold for size of neg. transact.)
        dict_node_num_inf_local={}
        dict_node_fract_inf_local_previous_time={}

        dict_node_num_inf_local_threshold={}

        list_inf_nodes=[]
        list_inf_nodes_threshold=[]

        num_inf_links_global =0.
        num_inf_links_global_threshold =0.  # only consider links with a fraction of negative dollars larger than X

      #  H_period_aux = G_period.copy()   # copy to get only the infected links and nodes (for cluster distribution)
       # H_period_aux_threshold = G_period.copy()
        for edge in G_period.edges():
         
            manufacturer=edge[0]
            contractor=edge[1]



            #### for the count of local infection  (no threshold)
            try:
                dict_node_num_inf_local[manufacturer]
            except KeyError:
                dict_node_num_inf_local[manufacturer]  = 0.
                    
            try:
                dict_node_num_inf_local[contractor] 
            except KeyError:
                dict_node_num_inf_local[contractor]  = 0.


             #### for the count of local infection  (threshold for size of neg transactions)
            try:
                dict_node_num_inf_local_threshold[manufacturer]
            except KeyError:
                dict_node_num_inf_local_threshold[manufacturer]  = 0.
                    
            try:
                dict_node_num_inf_local_threshold[contractor] 
            except KeyError:
                dict_node_num_inf_local_threshold[contractor]  = 0.





            ########## infected nodes no threshold
            if G_period[manufacturer][contractor]['neg_weight'] != 0: 
                num_inf_links_global  +=1.
                dict_node_num_inf_local[manufacturer] += 1.
                dict_node_num_inf_local[contractor]  += 1.       

                if manufacturer not in list_inf_nodes:
                    list_inf_nodes.append(manufacturer)
                if contractor  not in list_inf_nodes:
                    list_inf_nodes.append(contractor)

          #  else:  # i remove non-infected links from the aux_graph
           #     H_period_aux.remove_edge(manufacturer,contractor)



            ########## infected nodes with threshold
            if G_period[manufacturer][contractor]['fract_neg_trans'] >= threshold_neg_tran:
                num_inf_links_global_threshold  += 1. 
                dict_node_num_inf_local_threshold[manufacturer] += 1.
                dict_node_num_inf_local_threshold[contractor]  += 1.     

                if manufacturer not in list_inf_nodes_threshold:
                    list_inf_nodes_threshold.append(manufacturer)
                if contractor  not in list_inf_nodes_threshold:
                    list_inf_nodes_threshold.append(contractor)

          #  else:  # i remove non-infected links from the aux_graph (with threshold)
           #     H_period_aux_threshold.remove_edge(manufacturer,contractor)




        try:
            fract_inf_links_global = num_inf_links_global / len(G_period.edges())
        except ZeroDivisionError:pass  #if empty network
       

        try:
            fract_inf_links_global_threshold = num_inf_links_global_threshold / len(G_period.edges())
        except ZeroDivisionError:pass  #if empty network
       



       
#        print "# nodes in G:", len(G_period.nodes()), " in H_aux:", len(H_period_aux.nodes())
 #       print "# edges in G:", len(G_period.edges()), " in H_aux:", len(H_period_aux.edges())


        ##### i remove the isolates from aux graph:
       # list_to_remove=[]
        #for node in H_period_aux.nodes():
         #   if H_period_aux.degree(node)==0:
          #      list_to_remove.append(node)
        #H_period_aux.remove_nodes_from(list_to_remove)
        print " # nodes in G:", len(G_period.nodes())#, " in H_aux:", len(H_period_aux.nodes())
        print " # edges in G:", len(G_period.edges())#, " in H_aux:", len(H_period_aux.edges())

       

        list_sizes_inf_components=[]
        #print "components of Infected subgraph:"
       # for item in nx.connected_component_subgraphs(H_period_aux):
        #    try:
                #print "comp. size:",len(item.nodes()),  "  avg.path lenght within component:",nx.average_shortest_path_length(item)
         #       list_sizes_inf_components.append(len(item.nodes()))
          #      list_sizes_inf_components_tot.append(len(item.nodes()))

           # except ZeroDivisionError: pass
               #print "comp. size:",len(item.nodes())

          
        #try:
         #   Gc = len(max(nx.connected_component_subgraphs(H_period_aux), key=len))
           # print "GC:", Gc, "\n"
        #except ValueError: 
         #   Gc="NA"



        #try:
         #   name_h="../Results/histogram_size_infected_connected_components_"+slicing+"_slicing_"+str(cont_periods)+".dat"
          #  histograma_gral.histogram(list_sizes_inf_components, name_h)
        #except ValueError: pass  # empty network
       



        ##### print out time evol. of number of infected links and nodes (any-size of neg. transaction)
      #  file7= open(name7, 'at')       
       # try:            
        #    print >> file7, cont_periods, num_inf_links_global, fract_inf_links_global, len(list_inf_nodes), float(len(list_inf_nodes))/len(G_period.nodes()), Gc, len(G_period.nodes()), len(G_period.edges())
        #except ZeroDivisionError:
         #   print >> file7, cont_periods, num_inf_links_global, fract_inf_links_global, len(list_inf_nodes), "NA", Gc, len(G_period.nodes()), len(G_period.edges())
        #file7.close()











        ##### i remove the isolates from aux graph:  (threshold for neg. transactions)
       # list_to_remove=[]
        #for node in H_period_aux_threshold.nodes():
         #   if H_period_aux_threshold.degree(node)==0:
          #      list_to_remove.append(node)
        #H_period_aux_threshold.remove_nodes_from(list_to_remove)
      #  print " # nodes in G:", len(G_period.nodes()), " in H_aux:", len(H_period_aux_threshold.nodes())
       # print " # edges in G:", len(G_period.edges()), " in H_aux:", len(H_period_aux_threshold.edges())

       

        #list_sizes_inf_components=[]
#        print "components of Infected subgraph:"
      #  for item in nx.connected_component_subgraphs(H_period_aux_threshold):
       #     try:
              #  print "comp. size:",len(item.nodes()),  "  avg.path lenght within component:",nx.average_shortest_path_length(item)
        #        list_sizes_inf_components.append(len(item.nodes()))
         #       list_sizes_inf_components_tot_threshold.append(len(item.nodes()))

          #  except ZeroDivisionError: pass
               #print "comp. size:",len(item.nodes())

          
      #  try:
       #     Gc_threshold = len(max(nx.connected_component_subgraphs(H_period_aux_threshold), key=len))
            #print "GC:", Gc_threshold, "\n"
        #except ValueError: 
           # Gc_threshold="NA"



       # try:
        #    name_h="../Results/histogram_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing_"+str(cont_periods)+".dat"
         #   histograma_gral.histogram(list_sizes_inf_components, name_h)
        #except ValueError: pass  # empty network
       




        ##### print out time evol. of number of infected links and nodes (applying a threshold for size of neg. transaction)
       # file8= open(name8, 'at')       
        #try:            
         #   print >> file8, cont_periods, num_inf_links_global_threshold, fract_inf_links_global_threshold, len(list_inf_nodes_threshold), float(len(list_inf_nodes_threshold))/len(G_period.nodes()), Gc_threshold, len(G_period.nodes()), len(G_period.edges())
        #except ZeroDivisionError:
         #   print >> file8, cont_periods, num_inf_links_global_threshold, fract_inf_links_global_threshold, len(list_inf_nodes_threshold), "NA", Gc_threshold, len(G_period.nodes()), len(G_period.edges())
        #file8.close()





        
        for firm in G_period.nodes():   # i need a separate loop over firms (because i write one line in the output file per LINK, not per node)

            try:
                dict_firm_Pinf_previous_period[firm]
            except KeyError:
                dict_firm_Pinf_previous_period[firm]=0.
            if cont_periods == 1:
                dict_firm_Pinf_previous_period[firm] ="NA"



            try:
                dict_firm_cumulat_previous_Pinf[firm] 
            except KeyError:
                dict_firm_cumulat_previous_Pinf[firm] = 0. 
            if cont_periods == 1:
                dict_firm_cumulat_previous_Pinf[firm] = "NA"



            dict_firm_fract_previous_inf_periods[firm]=0.
            if cont_periods > 1:
                norm=len(set(dict_firm_id_active_periods[firm]))
                dict_firm_fract_previous_inf_periods[firm]=dict_firm_cumulat_previous_Pinf[firm]/float(norm)
            else:
                dict_firm_fract_previous_inf_periods[firm]="NA"







        ################ i will write one entry per link in the network (and per month) for the Scatter plot file:
        ######### (here i used to write the corresponding line of the MASTER file)
        #####################
        #########################
#        print "writing all edges for scatter..."
        for edge in G_period.edges():

            manufacturer_aux=edge[0]
            contractor_aux=edge[1]

            manufacturer=edge[0]
            contractor=edge[1]

           
            ##### i  need to deal with the instances regarding jobbers and with the order manuf.-contr being reversed by python!!!!
            if G_period.node[manufacturer_aux]["type"] == "manuf":  
                if G_period.node[contractor_aux]["type"] == "contr":
                    pass
                elif G_period.node[contractor_aux]["type"] == "manuf":
                    pass
                elif G_period.node[contractor_aux]["type"] == "jobber":
                    pass
            if G_period.node[manufacturer_aux]["type"] == "contr":  
                if G_period.node[contractor_aux]["type"] == "contr":
                    pass
                elif G_period.node[contractor_aux]["type"] == "manuf":
                    manufacturer=contractor_aux
                    contractor=manufacturer_aux
                elif G_period.node[contractor_aux]["type"] == "jobber":
                    manufacturer=contractor_aux
                    contractor=manufacturer_aux

            if G_period.node[manufacturer_aux]["type"] == "jobber":                              
                if G_period.node[contractor_aux]["type"] == "contr":
                   pass
                elif G_period.node[contractor_aux]["type"] == "manuf":                
                    manufacturer=contractor_aux
                    contractor=manufacturer_aux           
                elif G_period.node[contractor_aux]["type"] == "jobber":
                    pass

                   

            tupla_link=(manufacturer, contractor)                        

       


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

            


            try:
                dict_node_fract_inf_local_previous_time[manufacturer]
            except KeyError:
                dict_node_fract_inf_local_previous_time[manufacturer]="NA"
            try:
                dict_node_fract_inf_local_previous_time[contractor]
            except KeyError:
                dict_node_fract_inf_local_previous_time[contractor]="NA"




            ####### i exclude the edge in focus from the count of inf. links around a node

           
            if dict_node_num_inf_local[manufacturer] >0:
                fract_inf_links_local_manuf =  dict_node_num_inf_local[manufacturer] / float(G_period.degree(manufacturer))
            else:
                fract_inf_links_local_manuf =0.
            
            if dict_node_num_inf_local[contractor] >0:
                fract_inf_links_local_contr = dict_node_num_inf_local[contractor] / float(G_period.degree(contractor))
            else:
                fract_inf_links_local_contr =0.

            


            fract_inf_links_local_manuf_threshold =  (dict_node_num_inf_local_threshold[manufacturer] - 1.)/ float(G_period.degree(manufacturer))
            fract_inf_links_local_contr_threshold = (dict_node_num_inf_local_threshold[contractor] - 1.)/ float(G_period.degree(contractor))  



          



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
                try:
                    norm=len(set(dict_tuple_ids_active_periods[tupla_link]))                
                    dict_tuple_link_fract_previous_inf_periods[edge]=dict_tuple_link_cumulat_previous_Pinf[edge]/float(norm)
                except KeyError:
                     dict_tuple_link_fract_previous_inf_periods[edge]="NA"
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
                fract_pos_business_of_M_with_C=  G_period[manufacturer][contractor]['pos_weight'] / G_period.node[manufacturer]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_business_of_M_with_C="NA"  #  (otherwise i cant define business asymmetry)

            try:
                fract_pos_business_of_C_with_M=  G_period[manufacturer][contractor]['pos_weight'] / G_period.node[contractor]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_business_of_C_with_M="NA"  #(otherwise i cant define business asymmetry)


            try:
                error_size_ij= -1.*G_period[manufacturer][contractor]['neg_weight'] / G_period[manufacturer][contractor]['pos_weight']
            except ZeroDivisionError:
                error_size_ij="NA"
                if G_period[manufacturer][contractor]['neg_weight'] != 0.:
                    error_size_ij= -1.

            degree_asymmetry_ij= float(( G_period.degree(manufacturer) - G_period.degree(contractor)) * (G_period.degree(manufacturer)- G_period.degree(contractor))) / float((G_period.degree(manufacturer) + G_period.degree(contractor)) * (G_period.degree(manufacturer)+ G_period.degree(contractor)))



            business_asymmetry_ij="NA"
            try:
                business_asymmetry_ij = ((fract_pos_business_of_M_with_C  - fract_pos_business_of_C_with_M )* (fract_pos_business_of_M_with_C  - fract_pos_business_of_C_with_M)) / ((fract_pos_business_of_M_with_C  + fract_pos_business_of_C_with_M) * (fract_pos_business_of_M_with_C  + fract_pos_business_of_C_with_M))
            except:  pass  # either for a zerodivision error, or because one of the elements is a NA






            print >> file6, P_inf,  manufacturer, contractor,str(manufacturer)+str(contractor),                                                                                 G_period[manufacturer][contractor]['pos_weight']+G_period[manufacturer][contractor]['neg_weight'],                                                                  G[manufacturer][contractor]['pos_weight']+G[manufacturer][contractor]['neg_weight'],                                                                               G_period[manufacturer][contractor]['pos_weight'], G_period[manufacturer][contractor]['neg_weight'],                                                                 G[manufacturer][contractor]['pos_weight'], G[manufacturer][contractor]['neg_weight'],                                                                               G_period.node[manufacturer]['vol_pos_transct'] ,   G_period.node[manufacturer]['vol_neg_transct'],                                                                  G_period.node[contractor]['vol_pos_transct'] ,   G_period.node[contractor]['vol_neg_transct'],                                                                     G.node[manufacturer]['vol_pos_transct'] ,   G.node[manufacturer]['vol_neg_transct'],                                                                                 G.node[contractor]['vol_pos_transct'] ,   G.node[contractor]['vol_neg_transct'],                                                                                   dict_tuple_link_Pinf_previous_period[edge], dict_tuple_link_cumulat_previous_Pinf[edge], dict_tuple_link_fract_previous_inf_periods[edge],                          dict_firm_Pinf_previous_period[manufacturer],   dict_firm_cumulat_previous_Pinf[manufacturer], dict_firm_fract_previous_inf_periods[manufacturer],                  dict_firm_Pinf_previous_period[contractor],   dict_firm_cumulat_previous_Pinf[contractor], dict_firm_fract_previous_inf_periods[contractor],                         G_period.degree(manufacturer), G_period.degree(contractor),  K_nn_i, K_nn_j, G_period.node[manufacturer]['HHI_as_manuf'],                                           G_period.node[manufacturer]['HHI_as_contr'],  G_period.node[contractor]['HHI_as_manuf'],  G_period.node[contractor]['HHI_as_contr'],                                G_period.node[manufacturer]['betweeness'],  G_period.node[contractor]['betweeness'], G_period[manufacturer][contractor]['link_betweeness'],                        G_period.node[manufacturer]['max_clique_size'], G_period.node[contractor]['max_clique_size'],                                                                       G.node[manufacturer]['max_clique_size'], G.node[contractor]['max_clique_size'],                                                                                    G_period.node[manufacturer]['kshell'],  G_period.node[contractor]['kshell'],                                                                                        G.node[manufacturer]['kshell'],  G.node[contractor]['kshell'],                                                                                                       G_period.node[manufacturer]['num_manuf'], G_period.node[manufacturer]['num_contractors'],                                                                           G_period.node[contractor]['num_manuf'], G_period.node[contractor]['num_contractors'],                                                                               G_period[manufacturer][contractor]['num_pos_trans']+G_period[manufacturer][contractor]['num_neg_trans'],                                                            G_period.node[manufacturer]['num_transact'], G_period.node[contractor]['num_transact'],                                                                             amount_pos_self_trans_i, amount_pos_self_trans_j, amount_neg_self_trans_i, amount_neg_self_trans_j,                                                                 num_pos_self_trans_i, num_pos_self_trans_j, num_neg_self_trans_i, num_neg_self_trans_j,                                                                             fract_pos_business_of_M_with_C, fract_pos_business_of_C_with_M, degree_asymmetry_ij, business_asymmetry_ij,                                                       error_size_ij, dist , current_data_month,  current_data_season, fract_inf_links_global, fract_inf_links_local_manuf,                                                fract_inf_links_local_contr, dict_node_fract_inf_local_previous_time[manufacturer], dict_node_fract_inf_local_previous_time[contractor],                            history, cont_periods , current_year, len(G_period.nodes()),  len(G_period.edges())






         
            ############## for next month       
            try:
                dict_tuple_link_Pinf_previous_period[edge]=P_inf
            except KeyError:
                dict_tuple_link_Pinf_previous_period[edge]= 0.

            try:
                dict_tuple_link_cumulat_previous_Pinf[edge] += P_inf
            except TypeError:   # for the case when i would force to do:  "NA" + 1, which is not allowed
                dict_tuple_link_cumulat_previous_Pinf[edge] = 0.

 
            dict_node_fract_inf_local_previous_time[manufacturer]= fract_inf_links_local_manuf
            dict_node_fract_inf_local_previous_time[contractor]= fract_inf_links_local_contr






        ### for next month
        for firm in G_period.nodes():
           
            P_inf_firm=0.  #  1: if there has been at least one neg. transaction involving the firm     
        
                     
            if  G_period.node[firm]['vol_neg_transct'] != 0:
                P_inf_firm =1.
            dict_firm_Pinf_previous_period[firm]=P_inf_firm
          

            try:
                dict_firm_cumulat_previous_Pinf[firm] += P_inf_firm
            except TypeError:
                dict_firm_cumulat_previous_Pinf[firm] = 0.





        
        ########  write the monthly  network
        filename_network="../Results/Supply_network_slicing_"+slicing+"_period_"+str(cont_periods)+string_filename
        pickle.dump(G_period, open(filename_network+".pickle", 'wb'))
        print "  written", filename_network+".pickle"

        #nx.write_gml(G_period,filename_network+".gml")
        #print "  written", filename_network+".gml"
       # print "  N:",len(G_period.nodes()), " L:",len(G_period.edges())


        #### only the infected subgraph
       # filename_network="../Results/Supply_network_infected_slicing_"+slicing+"_period_"+str(cont_periods)+string_filename
      #  nx.write_gml(H_period_aux,filename_network+".gml")
        #print "  written", filename_network+".gml"
        #print "  N:",len(H_period_aux.nodes()), " L:",len(H_period_aux.edges())



        #nx.write_gexf(G_period,filename_network+".gexf")   # gephi format
        #print "  written", filename_network+".gexf"


        G_no_loops = remove_self_loops(G_period)
     #   print "   without self-loops:",len(G_no_loops.nodes()), " L:",len(G_no_loops.edges())
        print "# nodes (aggregated so far):",len(G.nodes()), " # links (id):", len(G.edges())


    
    file6.close()
    print "\n\nwritten file:",name6
    
    ########## end of loop over the ALL_years file
    ##################################################
    ##################################################





  #  try:
   #     name_h="../Results/histogram_tot_size_infected_connected_components_"+slicing+"_slicing.dat"
    #    histograma_gral.histogram(list_sizes_inf_components_tot, name_h)


        #### i also dump the raw list of values for KS comparison simu-real data
     #   pickle_filename="../Results/List_values_tot_size_infected_connected_components_"+slicing+"_slicing.dat"
        
      #  pickle.dump(list_sizes_inf_components_tot, open(pickle_filename, 'wb'))
       # print "written:",pickle_filename
        

    #except ValueError: pass  # empty list
       

    #try:
     #   name_h="../Results/histogram_tot_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"
      #  histograma_gral.histogram(list_sizes_inf_components_tot_threshold, name_h)




         #### i also dump the raw list of values for KS comparison simu-real data
      #  pickle_filename="../Results/List_values_tot_size_infected_connected_components_threshold_neg_tran"+str(threshold_neg_tran)+"_"+slicing+"_slicing.dat"
        
       # pickle.dump(list_sizes_inf_components_tot_threshold, open(pickle_filename, 'wb'))
        #print "written:",pickle_filename
        

    #except ValueError: pass  # empty list
       



    try:
        name_h="../Results/histogram_transaction_period_lengths.dat"
        histograma_gral.histogram( list_periods, name_h)



        name_h="../Results/histogram_num_transact_per_period_all.dat"
        histograma_gral.histogram(dict_link_num_trans.values() , name_h)
    except ValueError: pass
   


    num_manuf_tot=len(set(list_manuf_tot))
    num_contr_tot= len(set(list_contr_tot))
    list_jobbers_tot= list(set(list_manuf_tot) & set(list_contr_tot))
    jobbers_tot=len(list_jobbers_tot)


    filename_jobbers="../Results/List_jobbers_tot_from_slicing_"+slicing+".dat"
    pickle.dump(list_jobbers_tot, open(filename_jobbers, 'wb'))
    print "written list jobbers:", filename_jobbers

  
    
    list_manuf_tot_no_jobbers= list(set(list_manuf_tot) - set(list_jobbers_tot))
    num_manuf_tot_no_jobbers=len(set(list_manuf_tot_no_jobbers))
    
    list_contr_tot_no_jobbers= list(set(list_contr_tot) - set(list_jobbers_tot))
    num_contr_tot_no_jobbers=len(set(list_contr_tot_no_jobbers))
    



    print "\n\nAggregated network:"
    print "tot. # firms:", len(set(list_firm_ids))

    print "tot. # manuf:",num_manuf_tot, " excluding jobbers:", num_manuf_tot_no_jobbers, float(jobbers_tot)/num_manuf_tot
    print "tot. # contr:", num_contr_tot, " excluding jobbers:", num_contr_tot_no_jobbers , float(jobbers_tot)/num_contr_tot
    print "Jobbers (overlap between manuf. & contr total list):", jobbers_tot,  "(excluding first all self-transactions)"
  

    print "tot. # transactions:", int(cont_transactions)
    try:
        print "tot. # negative transactions:", int(cont_neg_transactions), "  ", cont_neg_transactions/cont_transactions*100., "%"
        print "tot. # self-transactions:", int(cont_self_transactions), "  ", cont_self_transactions/cont_transactions*100., "%" 
        print "tot. # self-neg-transactions:", int(cont_self_neg_transactions), "  ", cont_self_neg_transactions/cont_transactions*100., "%" 
    except ZeroDivisionError: pass

      
    print "manuf + contr+ jobbers:",  num_manuf_tot + num_contr_tot + jobbers_tot



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

