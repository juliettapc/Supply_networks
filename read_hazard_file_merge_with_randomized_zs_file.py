#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept 2016

'''

import datetime as dt
import csv
import pickle
import sys
import datetime as dt


def main():




    list_zscores=[]
    dict_year_dict_micj_zs={}   
    
    list_year_labels=["1985","1986","1987","1988","1989","1990","1991","1992","1993","1994-1995","1996-1997","1998-2000","2001-2005"]
    ########  I read the multiple files for the zscore (controlling for year, and for year + degrees of m and c
    for year_label in list_year_labels:
        name0="../Data/Shuffling_by_year_and_year_degree/"+year_label+"_Null_10000_Shuffles.csv"
        print "reading: ", name0, "......."       

          
        csvfile=open(name0, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   # to skip the header
        #### paidbyfi,paidforf,e_trans,total_trans,e_rate,z-scores,z-scores (deg preserving)


    
        list_current_years=[]
        if "-" not in year_label:
            year=int(year_label)
            list_current_years.append(year)
        else:     # for randomization files that include multiple years
            year_in=int(year_label.split("-")[0])
            year_fin=int(year_label.split("-")[1])

            year_aux=year_in
            while year_aux <= year_fin:
                list_current_years.append(year_aux)
                year_aux +=1

            
       
        for year in list_current_years:
            dict_year_dict_micj_zs[year]={}



     
        cont=1      
        for list_row in reader:                
            cont +=1

           
            
            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm         
            mi_cj=str(manufacturer) + "_"+ str(contractor)
            


            zs_year=float(list_row[5])

            try:
                zs_year_degree=float(list_row[6])
            except ValueError:
               zs_year_degree=0.   # a few (~232) cases have zero failed transactions, but also empty box for shuffling... artificially zs=0.




            list_zscores.append(zs_year_degree)
 
            tupla_zs=(zs_year, zs_year_degree)
                
            for year in list_current_years:
                dict_year_dict_micj_zs[year][mi_cj]=tupla_zs
                  
                
           


    filename_list="../Results/list_zscores_year_degree.pickle"
    pickle.dump(list_zscores, open(filename_list, 'wb'))
    print "written:", filename_list




    ########  I read the P_inf vs variables file
    name0="../Results/Pinf_vs_mulitiple_vars_monthly_netw_dropped_overlaps_randomly_from_list.csv"
    #name0="../Results/Pinf_vs_mulitiple_vars_monthly_netw_dropped_overlaps_randomly_from_list_cohort.csv"
    print "\nreading: ", name0, "......."       



    ###########  output file, adding zc info to the hazard file
    new_output_name="../Results/Pinf_vs_mulitiple_vars_monthly_netw_dropped_overlaps_randomly_from_list_added_zc.csv"

#    new_output_name="../Results/Pinf_vs_mulitiple_vars_monthly_netw_dropped_overlaps_randomly_from_list_cohort_added_zc.csv"
    file2 = open(new_output_name,'wt')


    print >> file2,"P_inf,Mi,Cj,Mi_Cj,MCJ,num_trans,start_date_trans,end_date_trans,first_day_trans,last_day_trans,length_trans,period_end,first_date_mi_cj,first_day_mi_cj,net_adj_gross,tot_pos_gross,tot_neg_gross,frac_neg_pos,acumm_pos_gross,accum_num_trans,k_M_fin,k_C_fin,num_M_i,num_C_i,num_J_i,num_M_j,num_C_j,num_J_j,k_M_fin_accum,k_C_fin_accum,artificial_start_date_trans,artificial_start_time_trans,overlap,year,N,L,CC_m_fin,CC_c_fin,betweenness_m_fin,betweenness_c_fin,max_clique_size_m_fin,max_clique_size_c_fin,kshell_m_fin,kshell_c_fin,p_inf_prev_trans,accum_inf_prev_ij,accum_inf_prev_neighb_i,frac_accum_inf_prev_neighb_i,accum_inf_prev_neighb_j,frac_accum_inf_prev_neighb_j,history_ij,min_dist_i_to_inf,avg_dist_i_to_inf,min_dist_j_to_inf,avg_dist_j_to_inf,degree_asym_ij,business_asym_ij,zs_yearly_error_rate_ij,Dist,zip1,zip2,zs_error_rate_ij_year,zs_error_rate_ij_year_degree"

  

   
    num_missing_entries=0
    cont=1       
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
    #### P_inf	Mi	Cj	Mi_Cj	MCJ	num_trans	start_date_trans	end_date_trans	first_day_trans	last_day_trans	length_trans	period_end	first_date_mi_cj	first_day_mi_cj	net_adj_gross	tot_pos_gross	tot_neg_gross	frac_neg_pos	acumm_pos_gross	accum_num_trans	k_M_fin	k_C_fin	num_M_i	num_C_i	num_J_i	num_M_j	num_C_j	num_J_j	k_M_fin_accum	k_C_fin_accum	artificial_start_date_trans	overlap	year	N	L	CC_m_fin	CC_c_fin	betweenness_m_fin	betweenness_c_fin	max_clique_size_m_fin	max_clique_size_c_fin	kshell_m_fin	kshell_c_fin	p_inf_prev_trans	accum_inf_prev_ij	accum_inf_prev_neighb_i	frac_accum_inf_prev_neighb_i	accum_inf_prev_neighb_j	frac_accum_inf_prev_neighb_j	history_ij	min_dist_i_to_inf	avg_dist_i_to_inf	min_dist_j_to_inf	avg_dist_j_to_inf	degree_asym_ij	business_asym_ij	zs_yearly_error_rate_ij	Dist	zip1	zip2
        

    for list_row in reader:                
        cont +=1

        
        date_end_trans=list_row[7]       # format:   1987-10-31
        trans_year=int(date_end_trans.split("-")[0])


        mi_cj=str(list_row[3])
        try:

            zs_year=dict_year_dict_micj_zs[trans_year][mi_cj][0]
            zs_year_degree=dict_year_dict_micj_zs[trans_year][mi_cj][1]
            
            #print trans_year, mi_cj, dict_year_dict_micj_zs[trans_year][mi_cj],"\n"
        except KeyError:
            zs_year=0.
            zs_year_degree=0.
            num_missing_entries +=1

            
        string_list=str(list_row).replace("[","").replace("]","")

        print >> file2, string_list,",",zs_year ,",",zs_year_degree

    print "# missing entries:",num_missing_entries




    file2.close()
    print "written:",    new_output_name


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

