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
import scipy.stats


def main():





    name0="../Results/Simplified_stata_file_Pinf_vs_mulitiple_variables_monthly_slicing_dropped_overlaps_randomly_from_list.dat"
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
    next(reader, None)   # to skip the header
    

    dict_year_dict_firm_id_fract_errors={}
    dict_year_dict_micj_fract_errors={}
    dict_year_dict_micj_tupla_core_score_i_j={}
    dict_year_dict_micj_core_score_firm={}

    year=1985
    while year <=2005:
        dict_year_dict_firm_id_fract_errors[year]={}
        dict_year_dict_micj_fract_errors[year]={}
     
        dict_year_dict_micj_core_score_firm[year]={}
        dict_year_dict_micj_tupla_core_score_i_j[year]={}

        dict_year_dict_micj_history[year]={}


        year +=1


    list_pinf_high_score_manuf=[]
    list_pinf_low_score_manuf=[]
    list_all_records=[]
    for list_row in reader:                
        
        p_inf=float(list_row[0])

        mi=int(list_row[1])
        cj=int(list_row[2])
        mi_cj=list_row[3]
        
        history_ij=int(list_row[53])
        year=int(list_row[36])
        core_score_year_i=float(list_row[64])
        core_score_year_j=float(list_row[65])


        if core_score_year_i > .65:
            list_pinf_high_score_manuf.append(p_inf)
        elif core_score_year_i < 0.3:
            list_pinf_low_score_manuf.append(p_inf)
        list_all_records.append(p_inf)


        dict_year_dict_micj_tupla_core_score_i_j[year][mi_cj]=(core_score_year_i,core_score_year_j)
        dict_year_dict_micj_core_score_firm[year][mi]=core_score_year_i
        dict_year_dict_micj_core_score_firm[year][cj]=core_score_year_j


        try:
            dict_year_dict_firm_id_fract_errors[year][mi].append(p_inf)
        except KeyError:
            dict_year_dict_firm_id_fract_errors[year][mi]=[]
            dict_year_dict_firm_id_fract_errors[year][mi].append(p_inf)


      #  try:
       #     dict_year_dict_firm_id_fract_errors[year][cj].append(p_inf)
        #except KeyError:
         #   dict_year_dict_firm_id_fract_errors[year][cj]=[]
          #  dict_year_dict_firm_id_fract_errors[year][cj].append(p_inf)


        try:
            dict_year_dict_micj_fract_errors[year][mi_cj].append(p_inf)
        except KeyError:
            dict_year_dict_micj_fract_errors[year][mi_cj]=[]
            dict_year_dict_micj_fract_errors[year][mi_cj].append(p_inf)





    

    print "for company ids:"
    for year in sorted(dict_year_dict_firm_id_fract_errors):

        name6="../Results/Scatter_plot_yearly_avg_fract_errors_core_score_only_manuf"+str(year)+".dat"
        file6= open(name6, 'wt') 

        list_avg_p_inf_high_core_score=[]
        list_avg_p_inf_low_core_score=[]
        list_all=[]
        for firm_id in sorted(dict_year_dict_firm_id_fract_errors[year]):
            print >> file6,  dict_year_dict_micj_core_score_firm[year][firm_id], numpy.mean(dict_year_dict_firm_id_fract_errors[year][firm_id]), year, firm_id


            list_all.append(numpy.mean(dict_year_dict_firm_id_fract_errors[year][firm_id]))
            if dict_year_dict_micj_core_score_firm[year][firm_id] >.65:
                list_avg_p_inf_high_core_score.append(numpy.mean(dict_year_dict_firm_id_fract_errors[year][firm_id]))

            if dict_year_dict_micj_core_score_firm[year][firm_id] < .35:
                list_avg_p_inf_low_core_score.append(numpy.mean(dict_year_dict_firm_id_fract_errors[year][firm_id]))



        #print  "written:",name6

        print year, numpy.mean(list_avg_p_inf_high_core_score),1.96*scipy.stats.sem(list_avg_p_inf_high_core_score),      numpy.mean(list_avg_p_inf_low_core_score),  1.96*scipy.stats.sem(list_avg_p_inf_low_core_score),     numpy.mean(list_all), 1.96*scipy.stats.sem(list_all)
        file6.close()


    print "fraction of errors among subpopulations, over all years:"     
    print  "high core score:",numpy.mean(list_pinf_high_score_manuf),"   low core score:",  numpy.mean(list_pinf_low_score_manuf), "   all:",numpy.mean(list_all_records)

  #  print "for mi_cj:"
   # for year in sorted(dict_year_dict_micj_fract_errors):
    #    for mi_cj in sorted(dict_year_dict_micj_fract_errors[year]):
     #       print year, mi_cj, numpy.mean(dict_year_dict_micj_fract_errors[year][mi_cj]) ,dict_year_dict_micj_tupla_core_score_i_j[year][mi_cj][0], dict_year_dict_micj_tupla_core_score_i_j[year][mi_cj][1]
      


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
