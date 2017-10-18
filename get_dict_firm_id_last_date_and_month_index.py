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
import random
import sys


def main():



    path="../Data/95_05NYCgamentdata/"

    slicing="monthly"

    initial_year=1985
    final_year=2005
 
    first_day_history=dt.datetime(1985,1,1)
    last_day_history= dt.datetime(2005,12,31)






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



    dict_firm_id_list_active_dates={}
   
    name0="fhistory_ALL.csv"
    print "reading: ", path+name0, "......."       

    ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
    cont=1       
    csvfile=open(path+name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
             

    for list_row in reader:                
        cont +=1

      
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


        try:   #  some lines are missing the contractor or manufacturer: skip

            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm         




            try: 
                dict_firm_id_list_active_dates[manufacturer]
            except KeyError:
                dict_firm_id_list_active_dates[manufacturer]=[]

            dict_firm_id_list_active_dates[manufacturer].append(initial_date)
            dict_firm_id_list_active_dates[manufacturer].append(final_date)




            try: 
                dict_firm_id_list_active_dates[contractor]
            except KeyError:
                dict_firm_id_list_active_dates[contractor]=[]

            dict_firm_id_list_active_dates[contractor].append(initial_date)
            dict_firm_id_list_active_dates[contractor].append(final_date)


        except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer 


    dict_month_index_active_firms={}

    dict_firm_id_last_month_index={}
    dict_firm_id_first_last_dates={}
    tot_num_firms= len(dict_firm_id_list_active_dates)
    cont_firms =0
    for firm_id in sorted(dict_firm_id_list_active_dates):
        cont_firms +=1
        sorted_list_dates=sorted(dict_firm_id_list_active_dates[firm_id])

        print cont_firms, tot_num_firms

        first=sorted_list_dates[0]
        last=sorted_list_dates[-1]

        dict_firm_id_first_last_dates[firm_id]=[]
        dict_firm_id_first_last_dates[firm_id].append(first)
        dict_firm_id_first_last_dates[firm_id].append(last)
     


        index=0
        for mark_date_initial in list_starting_date_marks:  
            index +=1
            if  slicing=="monthly":
                mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   

            if last > mark_date_initial  and last <= mark_date_final :
                dict_firm_id_last_month_index[firm_id]=index
              


        for current_date in sorted_list_dates:
            index=0
            for mark_date_initial in list_starting_date_marks:  
                index +=1
                if  slicing=="monthly":
                    mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   

                if current_date > mark_date_initial  and current_date <= mark_date_final :
                    try:
                        dict_month_index_active_firms[index]
                    except KeyError:
                        dict_month_index_active_firms[index]=[]

                    if firm_id not in dict_month_index_active_firms[index]:
                        dict_month_index_active_firms[index].append(firm_id)



    filename_pickle="../Results/dict_firm_id_first_last_date.pickle"
    pickle.dump(dict_firm_id_first_last_dates, open(filename_pickle, 'wb'))
    print "  written", filename_pickle



    filename_pickle2="../Results/dict_firm_id_last_date_month_index.pickle"
    pickle.dump(dict_firm_id_last_month_index, open(filename_pickle2, 'wb'))
    print "  written", filename_pickle2



    filename_pickle3="../Results/dict_month_index_list_active_firms.pickle"
    pickle.dump(dict_month_index_active_firms, open(filename_pickle3, 'wb'))
    print "  written", filename_pickle3


    for month in dict_month_index_active_firms:
        print month, len(dict_month_index_active_firms[month])


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

