#!/usr/bin/env python

'''
Code to read the file original, partial datafiles and compile an file with
useful info with paper_id, year, subject_category, issue_id

Created by Julia Poncela, on Dec. 2015

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
 
    first_day=dt.datetime(1985,1,1)

    y=initial_year


    flag_hist="NO"
    flag_network_metrics="NO"
    flag_remove_selfloops="YES"



    string_filename_loops=""
    if flag_remove_selfloops=="YES":
        string_filename_loops="_no_self_loops"


    string_filename=""
    if flag_network_metrics=="NO":
        string_filename="_no_network_metrics"




    name1="../Results/Time_evol_num_transactions.dat"
    file1= open(name1, 'wt')
    file1.close()

    name2="../Results/Time_evol_num_firms.dat"
    file2= open(name2, 'wt')
    file2.close()

    name3="../Results/Time_evol_num_neg_transactions.dat"
    file3= open(name3, 'wt')
    file3.close()

    name4="../Results/Time_evol_num_self_transactions.dat"
    file4= open(name4, 'wt')
    file4.close()


    name5="../Results/Time_evol_num_self_neg_transactions.dat"
    file5= open(name5, 'wt')
    file5.close()


    master_name="../Results/Master_file_transactions"+string_filename+string_filename_loops+".csv"
    file_master= open(master_name, 'wt')
    print >> file_master, "Mi Cj Mi_Cj tot_adj_gross_ij pos_adj_gross_ij neg_adj_gross_ij pos_adj_gross_i neg_adj_gross_i pos_adj_gross_j neg_adj_gross_j P_inf P_inf_previous_year Cumulat_num_inf_years frac_previous_inf_years year ki kj K_nn_i K_nn_j HHIi_as_manuf HHIi_as_contr HHIj_as_manuf HHIj_as_contr betweenness_i betweenness_j link_betweenness_ij max_clique_i max_clique_j kshell_i kshell_j num_manuf_i num_contr_i num_manuf_j num_contr_j num_transact_ij num_transact_i num_transact_j amount_pos_self_trans_i amount_pos_self_trans_j amount_neg_self_trans_i amount_neg_self_trans_j num_pos_self_trans_i num_pos_self_trans_j num_neg_self_trans_i num_neg_self_trans_j fract_pos_bussiness_of_M_with_C fract_pos_bussiness_of_C_with_M degree_asymmetry_ij business_asymmetry_ij size_tot_errors_ij"


    file_master.close()



    G=nx.Graph()

    print
    print
    
    list_periods=[]

    list_firm_ids=[]

    cont_transactions=0.
    cont_neg_transactions=0.
    cont_self_transactions=0.
    cont_self_neg_transactions=0.


    dict_firm_id_active_years={}
    dict_firm_total_trans_volum={}

   
    dict_firm_num_pos_trans={}
    dict_firm_num_neg_trans={}

    dict_tuple_link_cumulat_previous_Pinf={}
    dict_tuple_link_fract_previous_inf_years={}
    dict_tuple_link_Pinf_previous_year={}

    dict_manuf_dict_contr_amounts={}  # for each manufact., dict of its contractors and total amounts
    dict_contr_dict_manuf_amounts={}   # for each contract., dict of its manuf. and total amounts

    dict_link_num_pos_trans={}
    dict_link_num_neg_trans={}



    list_neg_adj_gross=[]
    list_pos_adj_gross=[]


    list_tuplas=[]

    while y <= final_year:

        list_neg_adj_gross_year=[]
        list_pos_adj_gross_year=[]

        list_firm_ids_year=[]


        list_tuplas_year=[]

        dict_firm_total_trans_volum_year={}

        dict_firm_tot_pos_trans_year={}
        dict_firm_tot_neg_trans_year={}

        dict_firm_num_pos_trans_year={}
        dict_firm_num_neg_trans_year={}

        dict_link_num_pos_trans_year={}
        dict_link_num_neg_trans_year={}


        dict_firm_amount_pos_self_trans_year={}
        dict_firm_amount_neg_self_trans_year={}

        dict_firm_num_pos_self_trans_year={}
        dict_firm_num_neg_self_trans_year={}




        dict_manuf_dict_contr_amounts_year={}  # for each manufact., dict of its contractors and total amounts
        dict_contr_dict_manuf_amounts_year={}   # for each contract., dict of its manuf. and total amounts


        cont_transactions_year=0.
        cont_neg_transactions_year=0.
        cont_self_transactions_year=0.
        cont_self_neg_transactions_year=0.


        G_year=nx.Graph()


        list_manuf_year=[]
        list_contr_year=[]
        list_non_self_contractors=[]


        ##################  
        ####### input datafile:   
        name0="fhistory"+str(y)+".csv"
        print "\nreading: ", path+name0, "......."       

        ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode
   
        cont=1       
        csvfile=open(path+name0, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   # to skip the header

        for list_row in reader:                
           cont +=1

           try:   #  some lines are missing the contractor or manufacturer: skip

             manufacturer=int(list_row[0])     ##paidbyfirm
             contractor=int(list_row[1])      ## paidforfirm                                
             
             
             list_manuf_year.append(manufacturer)
             list_contr_year.append(contractor)
             
             
             cont_transactions +=1
             cont_transactions_year +=1


              ############## for now i deal with integers Dollars !!  (easier for histograms)
             adj_gross=int(round(float((list_row[4]))))    
              
             
             flag_ignore_row=0
             if manufacturer == contractor:
                 cont_self_transactions  +=1.
                 cont_self_transactions_year  +=1.
                 if flag_remove_selfloops=="YES":
                     flag_ignore_row=1


                 ####### if it is a self-transaction, i only record this (no network variables nor HHI etc)
                 if adj_gross <0.:
                     cont_self_neg_transactions  +=1.
                     cont_self_neg_transactions_year  +=1.

                     try:
                         dict_firm_amount_neg_self_trans_year[manufacturer] +=  adj_gross                   
                     except KeyError:
                         dict_firm_amount_neg_self_trans_year[manufacturer] = adj_gross                   

                     try:
                         dict_firm_num_neg_self_trans_year[manufacturer] +=1.
                     except KeyError:
                         dict_firm_num_neg_self_trans_year[manufacturer] =1.

                 else:
                     try:
                         dict_firm_amount_pos_self_trans_year[manufacturer] +=  adj_gross                   
                     except KeyError:
                         dict_firm_amount_pos_self_trans_year[manufacturer] = adj_gross                   

                     try:
                         dict_firm_num_pos_self_trans_year[manufacturer] +=1.
                     except KeyError:
                         dict_firm_num_pos_self_trans_year[manufacturer] =1.

             else:
                 list_non_self_contractors.append(contractor)                 





             if  flag_ignore_row == 0 :   # in general i do not count the self-transactions (for network metrics nor HHI etc)


                tupla_link=(manufacturer, contractor)                        


                list_tuplas_year.append(tupla_link)
                list_tuplas.append(tupla_link)

                list_firm_ids.append(manufacturer)
                list_firm_ids.append(contractor)
        

                list_firm_ids_year.append(manufacturer)
                list_firm_ids_year.append(contractor)


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
                    final_date=dt.datetime(year, month, day)


                period=(final_date-initial_date).days                
                if period < 0:
                    old_initial=initial_date
                    old_final=final_date   #  some time periods have interved TO and FROM dates!
                    initial_date =final_date
                    final_date = old_initial
                    period=(final_date-initial_date).days          
                list_periods.append(period)
               
                
                


                ########### list of active years for firms
                try:
                    dict_firm_id_active_years[manufacturer].append(year)
                except KeyError:
                    dict_firm_id_active_years[manufacturer]=[]
                    dict_firm_id_active_years[manufacturer].append(year)


                if manufacturer != contractor:
                    try:
                        dict_firm_id_active_years[contractor].append(year)
                    except KeyError:
                        dict_firm_id_active_years[contractor]=[]
                        dict_firm_id_active_years[contractor].append(year)
                        
      
                    
                ###########  i need to initialize dicts
                try:
                    dict_firm_num_neg_trans_year[manufacturer]
                except KeyError:
                    dict_firm_num_neg_trans_year[manufacturer] =0.

                try:
                    dict_firm_num_neg_trans_year[contractor]
                except KeyError:
                    dict_firm_num_neg_trans_year[contractor] =0.


                try:
                    dict_firm_num_neg_trans[manufacturer]
                except KeyError:
                    dict_firm_num_neg_trans[manufacturer] =0.

                try:
                    dict_firm_num_neg_trans[contractor]
                except KeyError:
                    dict_firm_num_neg_trans[contractor] =0.


                try:
                    dict_firm_num_pos_trans_year[manufacturer]
                except KeyError:
                    dict_firm_num_pos_trans_year[manufacturer] =0.

                try:
                    dict_firm_num_pos_trans_year[contractor]
                except KeyError:
                    dict_firm_num_pos_trans_year[contractor] =0.


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
                    dict_link_num_pos_trans_year[tupla_link]
                except KeyError:
                    dict_link_num_pos_trans_year[tupla_link] = 0.

                try:
                    dict_link_num_neg_trans_year[tupla_link]
                except KeyError:
                    dict_link_num_neg_trans_year[tupla_link] = 0.
                ############





               
           

                ########OJO! NOT SURE ABOUT THIS!!  do i want total, or only positive?
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
                    dict_manuf_dict_contr_amounts_year[manufacturer]
                except KeyError:
                    dict_manuf_dict_contr_amounts_year[manufacturer]={}
                try:
                    dict_manuf_dict_contr_amounts_year[manufacturer][contractor]
                except KeyError:
                    dict_manuf_dict_contr_amounts_year[manufacturer][contractor] = 0.
                dict_manuf_dict_contr_amounts_year[manufacturer][contractor] += adj_gross



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
                    dict_contr_dict_manuf_amounts_year[contractor]
                except KeyError:
                    dict_contr_dict_manuf_amounts_year[contractor]={}
                try:
                    dict_contr_dict_manuf_amounts_year[contractor][manufacturer]
                except KeyError:
                    dict_contr_dict_manuf_amounts_year[contractor][manufacturer]=0.
                dict_contr_dict_manuf_amounts_year[contractor][manufacturer] += adj_gross






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





                ##########   volume of (net) transactions YEARLY
                try:
                    dict_firm_total_trans_volum_year[manufacturer] += adj_gross   
                except KeyError:
                    dict_firm_total_trans_volum_year[manufacturer] =0.
                    dict_firm_total_trans_volum_year[manufacturer] += adj_gross   

                try:
                    dict_firm_total_trans_volum_year[contractor] += adj_gross   
                except KeyError:
                    dict_firm_total_trans_volum_year[contractor] =0.
                    dict_firm_total_trans_volum_year[contractor] += adj_gross   





              
                ##########         
                if adj_gross  <0:                      

                    list_neg_adj_gross.append(-1*adj_gross)
                    list_neg_adj_gross_year.append(-1*adj_gross)

                    cont_neg_transactions   +=1
                    cont_neg_transactions_year   +=1


                    ##### num of neg. transactions YEARLY                   
                    dict_firm_num_neg_trans_year[manufacturer] +=1.                   
                    dict_firm_num_neg_trans_year[contractor] +=1.                    

                    ##### tot num of neg. transactions                  
                    dict_firm_num_neg_trans[manufacturer] +=1.                                        
                    dict_firm_num_neg_trans[contractor] +=1.
                                                         

                    #### same for the link
                    dict_link_num_neg_trans_year[tupla_link] += 1.
                    dict_link_num_neg_trans[tupla_link] += 1.



                   



                    G_year.add_node(manufacturer)
                    G_year.add_node(contractor)


                    G.add_node(manufacturer)
                    G.add_node(contractor)



                    try:
                        G.edge[manufacturer][contractor]["neg_weight"] += adj_gross               
                    except KeyError:
                        G.add_edge(manufacturer,contractor, neg_weight= adj_gross)

                    try:
                        
                        G_year.edge[manufacturer][contractor]["neg_weight"] += adj_gross
                    except KeyError:                    
                        G_year.add_edge(manufacturer,contractor, neg_weight= adj_gross)



                    #### add up to the total neg. yearly amount for each firm
                    try:
                        dict_firm_tot_neg_trans_year[manufacturer] += adj_gross   
                    except KeyError:
                        dict_firm_tot_neg_trans_year[manufacturer] =0.
                        dict_firm_tot_neg_trans_year[manufacturer] += adj_gross   
                    try:
                        dict_firm_tot_neg_trans_year[contractor] += adj_gross   
                    except KeyError:
                        dict_firm_tot_neg_trans_year[contractor] =0.
                        dict_firm_tot_neg_trans_year[contractor] += adj_gross   

   

                else:

                    list_pos_adj_gross.append(adj_gross)
                    list_pos_adj_gross_year.append(adj_gross)

                    ##### num of posit. transactions YEARLY                   
                    dict_firm_num_pos_trans_year[manufacturer] +=1.                    
                    dict_firm_num_pos_trans_year[contractor] +=1.
                   

                    ##### tot. num of posit. transactions                     
                    dict_firm_num_pos_trans[manufacturer] +=1.                   
                    dict_firm_num_pos_trans[contractor] +=1.                  
                    

                    #### same for the link
                    dict_link_num_pos_trans_year[tupla_link] += 1.
                    dict_link_num_pos_trans[tupla_link] += 1.


                    try:
                        G.edge[manufacturer][contractor]["pos_weight"] += adj_gross               
                    except KeyError:
                        G.add_edge(manufacturer,contractor, pos_weight= adj_gross)

                    try:
                        
                        G_year.edge[manufacturer][contractor]["pos_weight"] += adj_gross
                    except KeyError:                    
                        G_year.add_edge(manufacturer,contractor, pos_weight= adj_gross)


                    #### add up to the total neg. yearly amount for each firm
                    try:
                        dict_firm_tot_pos_trans_year[manufacturer] += adj_gross   
                    except KeyError:
                        dict_firm_tot_pos_trans_year[manufacturer] =0.
                        dict_firm_tot_pos_trans_year[manufacturer] += adj_gross   
                    try:
                        dict_firm_tot_pos_trans_year[contractor] += adj_gross   
                    except KeyError:
                        dict_firm_tot_pos_trans_year[contractor] =0.
                        dict_firm_tot_pos_trans_year[contractor] += adj_gross   



             

           except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer                  
            
          

            
        #############################  end of loop to read year file
        ###########################

        if  flag_hist == "YES":
            try:
                name_h="../Results/histogram_pos_adj_gross_values_years_"+str(y)+".dat"
                histograma_gral.histogram(list_pos_adj_gross_year, name_h)
            except: pass

            try:
                name_h="../Results/histogram_neg_adj_gross_values_years_"+str(y)+".dat"
                histograma_gral.histogram(list_neg_adj_gross_year, name_h)
            except: pass


         


        for  link in dict_link_num_pos_trans_year:
            G_year[link[0]][link[1]]['num_pos_trans']= dict_link_num_pos_trans_year[link]    
        for  link in dict_link_num_neg_trans_year:
            G_year[link[0]][link[1]]['num_neg_trans']= dict_link_num_neg_trans_year[link]    
            G_year[link[0]][link[1]]['fract_neg_trans']= dict_link_num_neg_trans_year[link] / (dict_link_num_neg_trans_year[link] + dict_link_num_pos_trans_year[link] )   

            if  G_year[link[0]][link[1]]['num_neg_trans'] == 0.:
                G_year[link[0]][link[1]]['neg_weight']=0.

            if  G_year[link[0]][link[1]]['num_pos_trans'] == 0.:
                G_year[link[0]][link[1]]['pos_weight']=0.






        for firm in G_year.nodes():           

            G_year.node[firm]['vol_transct']=dict_firm_total_trans_volum_year[firm]                                                   
            G_year.node[firm]['fract_neg_transct']=dict_firm_num_neg_trans_year[firm] /(dict_firm_num_neg_trans_year[firm] + dict_firm_num_pos_trans_year[firm])  
                                    
            G_year.node[firm]['num_transact']= dict_firm_num_neg_trans_year[firm] + dict_firm_num_pos_trans_year[firm]
                    

     



        for firm in dict_firm_tot_pos_trans_year:
            G_year.node[firm]['vol_pos_transct']=dict_firm_tot_pos_trans_year[firm]

        for firm in dict_firm_tot_neg_trans_year:
            G_year.node[firm]['vol_neg_transct']=dict_firm_tot_neg_trans_year[firm]

        ###### fill in the gaps for those firms without positive or neg. transactions
        for node in G_year.nodes():
            try:
                G_year.node[node]['vol_pos_transct']
            except KeyError:
                G_year.node[node]['vol_pos_transct']=0.

            try:
                G_year.node[node]['vol_neg_transct']
            except KeyError:
                G_year.node[node]['vol_neg_transct']=0.





        print " year",y
        print "  # firms:", len(set(list_firm_ids_year))
        print "  # manufacturers:", len(set(list_manuf_year))
        print "  # contractors", len(set(list_contr_year)), "(firms can act as both in general)"
        print "  # non-self contractors", len(set(list_non_self_contractors))
    
        print "  # transactions:", int(cont_transactions_year)   
        print "  # negative transactions:", int(cont_neg_transactions_year), "  ", cont_neg_transactions_year/cont_transactions_year*100., "%"
        print "  # self-transactions:", int(cont_self_transactions_year), "  ", cont_self_transactions_year/cont_transactions_year*100., "%" 
        print "  # self-neg-transactions:", int(cont_self_neg_transactions_year), "  ", cont_self_neg_transactions_year/cont_transactions_year*100., "%" 

        print "  # unique tuples:",len(set(list_tuplas_year))

        print "row count:", cont-1

        file1= open(name1, 'at')       
        print >> file1, y,int(cont_transactions_year) 
        file1.close()


        file2= open(name2, 'at')       
        print >> file2, y, len(set(list_firm_ids_year))
        file2.close()


        file3= open(name3, 'at')       
        print >> file3, y, int(cont_neg_transactions_year),  cont_neg_transactions_year/cont_transactions_year*100.
        file3.close()


        file4= open(name4, 'at')       
        print >> file4, y, int(cont_self_transactions_year), cont_self_transactions_year/cont_transactions_year*100.
        file4.close()




        print "#  manuf. in dict",len(dict_manuf_dict_contr_amounts_year)
        print "#  contr. in dict",len(dict_contr_dict_manuf_amounts_year)
        




        ########  HHI index as manufacturers and contractors

        for node in G_year.nodes():  
            G_year.node[node]['num_manuf']=0
            G_year.node[node]['num_contractors']=0


        for manufacturer in dict_manuf_dict_contr_amounts_year:
            lista=list(dict_manuf_dict_contr_amounts_year[manufacturer].values())
            HHI=Herfindahl_index.calculate_HHI(lista)    ## tuple  (H, H_normalized)   !!!!           
            G_year.node[manufacturer]['HHI_as_manuf']=HHI[0]
            G_year.node[manufacturer]['num_contractors']=len(lista)      

        for contractor in dict_contr_dict_manuf_amounts_year:
            lista=list(dict_contr_dict_manuf_amounts_year[contractor].values())
            HHI=Herfindahl_index.calculate_HHI(lista)    ## tuple  (H, H_normalized)   !!!!      
            G_year.node[contractor]['HHI_as_contr']=HHI[0]
            G_year.node[contractor]['num_manuf']=len(lista)  
            



        ################  i add topological attributes to the nodes
        #############################
        print "calculating network metrics....."
        print "  CC..."

        if   flag_network_metrics== "YES":
            dict_clustering=nx.clustering(G_year)        
        print "  node betweenness..."


        if   flag_network_metrics== "YES":
            dict_betweenness_nodes=nx.betweenness_centrality(G_year)
        list_k=[]
        for node in G_year.nodes():  
            k=G_year.degree(node)           
            G_year.node[node]["degree"]=k
            list_k.append(k)

            if   flag_network_metrics== "YES":
                G_year.node[node]["CC"]=dict_clustering[node]
                G_year.node[node]["betweeness"]= dict_betweenness_nodes[node]
            else:
                G_year.node[node]["CC"]=0.
                G_year.node[node]["betweeness"]= 0.

            
               
        max_k=max(list_k)            


        print "  edge betweenness..."
        if   flag_network_metrics== "YES":
            dict_betweenness_edges=nx.edge_betweenness_centrality(G_year, normalized=True, weight=None)   # it returns  dictionary of edges (tuplas as keys) with betweenness centrality as the value.   ### i can also calculate the edges' betweenness taking into account their weight!!
        for edge in G_year.edges():  
           # print edge
            try:
                if   flag_network_metrics== "YES":
                    G_year.edge[edge[0]][edge[1]]["link_betweeness"]=dict_betweenness_edges[edge]
                else:
                    G_year.edge[edge[0]][edge[1]]["link_betweeness"]=0.
            except KeyError:
                G_year.edge[edge[0]][edge[1]]["link_betweeness"]="NA"
                print "edge",edge, "not found"
          


        for node in G_year.nodes():

            try:
                G_year.node[node]['HHI_as_manuf']
            except KeyError:
                G_year.node[node]['HHI_as_manuf']="NA"


            try:
                G_year.node[node]['HHI_as_contr']
            except KeyError:
                G_year.node[node]['HHI_as_contr']="NA"





        ####### kshell structure
        print "  kshell..."    
        calculate_kshell(G_year, max_k)
 
       

        ####### max clique size        
        print "  max-clique..."
        for i in G_year.nodes():     

            if   flag_network_metrics== "YES":
                maximo=1     
                lista=nx.cliques_containing_node(G_year, i) #list of lists,  ej: [[207925, 203592], [207925, 10500761], [207925, 200554], [207925, 202587]]
            #  print i, lista
            
                for elem in lista:               
                    if len(elem) > maximo:
                        maximo=len(elem)      
                G_year.node[i]['max_clique_size']=maximo
            else:
                G_year.node[i]['max_clique_size']=0
    


        ############## i write the corresponding rows in the master file (one line per link and per year)
        #########################
        file_master= open(master_name, 'at')
        for edge in G_year.edges():

            try:
                dict_tuple_link_Pinf_previous_year[edge]
            except KeyError:
                dict_tuple_link_Pinf_previous_year[edge]=0.
            if year == initial_year:
                dict_tuple_link_Pinf_previous_year[edge] ="NA"


            manufacturer=edge[0]
            contractor=edge[1]

            
            P_inf=0.  #  1: if there has been at least one neg. transaction between manuf. and contr. during the year, 0 otherwise
            if G_year[manufacturer][contractor]['neg_weight'] != 0:
                P_inf =1.

            try:
                dict_tuple_link_cumulat_previous_Pinf[edge] 
            except KeyError:
                dict_tuple_link_cumulat_previous_Pinf[edge] = 0. 
            if year == initial_year:
                dict_tuple_link_cumulat_previous_Pinf[edge] = "NA"



            dict_tuple_link_fract_previous_inf_years[edge]=0.
            if y > initial_year:
                dict_tuple_link_fract_previous_inf_years[edge]=dict_tuple_link_cumulat_previous_Pinf[edge]/(y-1985.)
            else:
                dict_tuple_link_fract_previous_inf_years[edge]="NA"



           
            lista=[]     # avg degree of the manufacturer's neighbours
            for n in G.neighbors(manufacturer) :
                lista.append(float(G.degree(n)))

            K_nn_i=0.
            try:
                K_nn_i=numpy.mean(lista)
            except :pass


            lista=[]     # avg degree of the manufacturer's neighbours
            for n in G.neighbors(contractor) :
                lista.append(float(G.degree(n)))

            K_nn_j=0.
            try:
                K_nn_j=numpy.mean(lista)
            except: pass





            amount_pos_self_trans_i=0.
            amount_pos_self_trans_j=0.
            try:
                amount_pos_self_trans_i=dict_firm_amount_pos_self_trans_year[manufacturer]
            except KeyError: pass
            try:
                amount_pos_self_trans_j=dict_firm_amount_pos_self_trans_year[contractor]
            except KeyError: pass


            amount_neg_self_trans_i=0.
            amount_neg_self_trans_j=0.
            try:
                amount_neg_self_trans_i=dict_firm_amount_neg_self_trans_year[manufacturer]
            except KeyError: pass
            try:
                amount_neg_self_trans_j=dict_firm_amount_neg_self_trans_year[contractor]
            except KeyError: pass


            num_pos_self_trans_i=0.
            num_pos_self_trans_j=0.
            try:
                num_pos_self_trans_i=dict_firm_num_pos_self_trans_year[manufacturer]
            except KeyError: pass
            try:
                num_pos_self_trans_j=dict_firm_num_pos_self_trans_year[contractor]
            except KeyError: pass


            num_neg_self_trans_i=0.
            num_neg_self_trans_j=0.
            try:
                num_neg_self_trans_i=dict_firm_num_neg_self_trans_year[manufacturer]
            except KeyError: pass
            try:
                num_neg_self_trans_j=dict_firm_num_neg_self_trans_year[contractor]
            except KeyError: pass


            try:
                fract_pos_bussiness_of_M_with_C=  G_year[manufacturer][contractor]['pos_weight'] / G_year.node[manufacturer]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_bussiness_of_M_with_C="NA"  #  (otherwise i cant define business asymmetry)

            try:
                fract_pos_bussiness_of_C_with_M=  G_year[manufacturer][contractor]['pos_weight'] / G_year.node[contractor]['vol_pos_transct']
            except ZeroDivisionError: 
                fract_pos_bussiness_of_C_with_M="NA"  #(otherwise i cant define business asymmetry)


            try:
                error_size_ij= -1.*G_year[manufacturer][contractor]['neg_weight'] / G_year[manufacturer][contractor]['pos_weight']
            except ZeroDivisionError:
                error_size_ij="NA"
                if G_year[manufacturer][contractor]['neg_weight'] != 0.:
                    error_size_ij= -1.

            degree_asymmetry_ij= float(( G_year.degree(manufacturer) - G_year.degree(contractor)) * (G_year.degree(manufacturer)- G_year.degree(contractor))) / float((G_year.degree(manufacturer) + G_year.degree(contractor)) * (G_year.degree(manufacturer)+ G_year.degree(contractor)))



            business_asymmetry_ij="NA"
            try:
                business_asymmetry_ij = ((fract_pos_bussiness_of_M_with_C  - fract_pos_bussiness_of_C_with_M )* (fract_pos_bussiness_of_M_with_C  - fract_pos_bussiness_of_C_with_M)) / ((fract_pos_bussiness_of_M_with_C  + fract_pos_bussiness_of_C_with_M) * (fract_pos_bussiness_of_M_with_C  + fract_pos_bussiness_of_C_with_M))
            except:  pass  # either for a zerodivision error, or because one of the elements is a NA

#     print >> file_master, "Mi Cj Mi_Cj tot_adj_gross_ij pos_adj_gross_ij neg_adj_gross_ij pos_adj_gross_i neg_adj_gross_i pos_adj_gross_j neg_adj_gross_j P_inf P_inf_previous_year Cumulat_num_inf_years frac_previous_inf_years year ki kj K_nn_i K_nn_j HHIi_as_manuf HHIi_as_contr HHIj_as_manuf HHIj_as_contr betweenness_i betweenness_j link_betweenness_ij max_clique_i max_clique_j kshell_i kshell_j num_manuf_i num_contr_i num_manuf_j num_contr_j num_transact_ij num_transact_i num_transact_j amount_pos_self_trans_i amount_pos_self_trans_j amount_neg_self_trans_i amount_neg_self_trans_j num_pos_self_trans_i num_pos_self_trans_j num_neg_self_trans_i num_neg_self_trans_j fract_pos_bussiness_of_M_with_C fract_pos_bussiness_of_C_with_M degree_asymmetry_ij business_asymmetry_ij size_tot_errors_ij"
            
            print  >> file_master,  manufacturer, contractor,str(manufacturer)+str(contractor),                                                                                  G_year[manufacturer][contractor]['pos_weight']+G_year[manufacturer][contractor]['neg_weight'],                                                                       G_year[manufacturer][contractor]['pos_weight'], G_year[manufacturer][contractor]['neg_weight'],                                                                      G_year.node[manufacturer]['vol_pos_transct'] ,   G_year.node[manufacturer]['vol_neg_transct'],                                                                       G_year.node[contractor]['vol_pos_transct'] ,   G_year.node[contractor]['vol_neg_transct'],                                                                           P_inf, dict_tuple_link_Pinf_previous_year[edge], dict_tuple_link_cumulat_previous_Pinf[edge], dict_tuple_link_fract_previous_inf_years[edge], y,                     G_year.degree(manufacturer), G_year.degree(contractor),  K_nn_i, K_nn_j, G_year.node[manufacturer]['HHI_as_manuf'],                                                  G_year.node[manufacturer]['HHI_as_contr'],  G_year.node[contractor]['HHI_as_manuf'],  G_year.node[contractor]['HHI_as_contr'],                                       G_year.node[manufacturer]['betweeness'],  G_year.node[contractor]['betweeness'], G_year[manufacturer][contractor]['link_betweeness'],                                G_year.node[manufacturer]['max_clique_size'], G_year.node[contractor]['max_clique_size'], G_year.node[manufacturer]['kshell'],                                       G_year.node[contractor]['kshell'], G_year.node[manufacturer]['num_manuf'], G_year.node[manufacturer]['num_contractors'],                                             G_year.node[contractor]['num_manuf'], G_year.node[contractor]['num_contractors'],                                                                                    G_year[manufacturer][contractor]['num_pos_trans']+G_year[manufacturer][contractor]['num_neg_trans'],                                                                 G_year.node[manufacturer]['num_transact'], G_year.node[contractor]['num_transact'],                                                                                  amount_pos_self_trans_i, amount_pos_self_trans_j, amount_neg_self_trans_i, amount_neg_self_trans_j,                                                                  num_pos_self_trans_i, num_pos_self_trans_j, num_neg_self_trans_i, num_neg_self_trans_j,                                                                              fract_pos_bussiness_of_M_with_C, fract_pos_bussiness_of_C_with_M, degree_asymmetry_ij, business_asymmetry_ij, error_size_ij            


            ### for next year
            try:
                dict_tuple_link_Pinf_previous_year[edge]=P_inf
            except TypeError:
                dict_tuple_link_Pinf_previous_year[edge]= 0.


            try:
                dict_tuple_link_cumulat_previous_Pinf[edge] += P_inf
            except TypeError:
                dict_tuple_link_cumulat_previous_Pinf[edge] = 0.


        file_master.close()





        
        ########  write the yearly  network
        filename_network="../Results/Supply_network_year_"+str(y)
        pickle.dump(G_year, open(filename_network+".pickle", 'wb'))
        print "  written", filename_network+".pickle"

        nx.write_gml(G_year,filename_network+".gml")
        print "  written", filename_network+".gml"
        print "  N:",len(G_year.nodes()), " L:",len(G_year.edges())


        G_no_loops = remove_self_loops(G_year)
        print "   without self-loops:",len(G_no_loops.nodes()), " L:",len(G_no_loops.edges())



        print "# nodes (aggregated so far):",len(G.nodes()), " # links (id):", len(G.edges())



    
        y +=1
        ################  new year file
        ##################################################
        ##################################################
        ##################################################


    print "written:", master_name



    print "\n\nAggregated network:"
    print "tot. # firms:", len(set(list_firm_ids))
    print "tot. # transactions:", int(cont_transactions)
    print "tot. # negative transactions:", int(cont_neg_transactions), "  ", cont_neg_transactions/cont_transactions*100., "%"
    print "tot. # self-transactions:", int(cont_self_transactions), "  ", cont_self_transactions/cont_transactions*100., "%" 
    print "tot. # self-neg-transactions:", int(cont_self_neg_transactions), "  ", cont_self_neg_transactions/cont_transactions*100., "%" 

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


#    print sorted(list_periods)
    name_h="../Results/histogram_period_lengths.dat"
    histograma_gral.histogram( list_periods, name_h)
   



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
    max_k=max(list_k)        


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
    filename_network="../Results/Supply_network_"+str(initial_year)+"_"+str(final_year)
    pickle.dump(G, open(filename_network+".pickle", 'wb'))
    print "written", filename_network+".pickle"

    nx.write_gml(G,filename_network+".gml")
    print "written", filename_network+".gml"

    print "N:",len(G.nodes()), " L:",len(G.edges())

    G_no_loops = remove_self_loops(G)
    print "   without self-loops:",len(G_no_loops.nodes()), " L:",len(G_no_loops.edges())








    print 

    if  flag_hist == "YES":
        name_h="../Results/histogram_pos_adj_gross_values_years_"+str(initial_year)+"_"+str(final_year)+".dat"
        histograma_gral.histogram(list_pos_adj_gross, name_h)
#    print "# obsrv:",len(list_pos_adj_gross), "  max.", max(list_pos_adj_gross), "  min.", min(list_pos_adj_gross), "  avg:", numpy.mean(list_pos_adj_gross), "  sd:", numpy.std(list_pos_adj_gross)



    print 


    if  flag_hist == "YES":
        name_h="../Results/histogram_neg_adj_gross_values_years_"+str(initial_year)+"_"+str(final_year)+".dat"
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

