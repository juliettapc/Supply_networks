#!/usr/bin/env python

'''
Created by Julia Poncela, on Feb. 2016

'''

import datetime as dt
import csv
import pickle
import random
import sys
import datetime as dt
import Herfindahl_index


def main():





    path="../Data/95_05NYCgamentdata/"
 


    ##################  
    ####### input datafile:    (I NEED TO READ IT EVERY TIME, BECAUSE IT GETS EMPTY EVERY TIME AFTER ITERATING OVER IT)
    name0="fhistory_ALL.csv"
    print "reading: ", path+name0, "......."       
    

    ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode    
    csvfile=open(path+name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header


              ### tot # rows:  779798
             
    cont=0
    list_unique_manuf=[]
    list_unique_contr=[]
    list_manuf=[]
    list_contr=[]
    for list_row in reader:
        cont +=1
        print cont
        try:   #  some lines are missing the contractor or manufacturer: skip

            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm                                            


            list_manuf.append(manufacturer)
            list_contr.append(contractor)                    
            if manufacturer != contractor:
                list_unique_manuf.append(manufacturer)
                list_unique_contr.append(contractor)                    

        except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer   
            


   
    print "size of list unique manuf.:", len(set(list_unique_manuf)), "  id. contr:", len(set(list_unique_contr))  # 1417 ,  7768
    print "   overlap between unique_manuf and unique_contr:", len(list(set(list_unique_manuf) & set(list_unique_contr)))   ### 496
    print "size of list all manuf.:", len(set(list_manuf)), "  id. contr:", len(set(list_contr))   ## 5747 , 10535
    print "   overlap between all manuf and all contr:", len(list(set(list_manuf) & set(list_contr))) #  5695

    raw_input()
   
    print "reading: ", path+name0, "......."           

    ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode    
    csvfile=open(path+name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
             

    num_self_trans_manuf_from_contr_list=0
    num_self_trans_contr_from_manuf_list=0
    cont_self_transactions =0
    cont_transactions =0
    cont=0
    for list_row in reader:                
        cont +=1      

        print cont
        try:   #  some lines are missing the contractor or manufacturer: skip

            manufacturer=int(list_row[0])     ##paidbyfirm
            contractor=int(list_row[1])      ## paidforfirm                                
                        
            cont_transactions +=1                  

            ############## for now i deal with integers Dollars !!  (easier for histograms)
            #adj_gross=int(round(float((list_row[4]))))                               
                    
            if manufacturer == contractor:
                cont_self_transactions  +=1.
                if manufacturer in list_unique_contr:
                    num_self_trans_manuf_from_contr_list +=1
                    
                if contractor in list_unique_manuf:
                    num_self_trans_contr_from_manuf_list +=1


        except ValueError:   pass #  some lines (very rare, one single instance) are missing the contractor or manufacturer



    print "cont:",cont," cont trans:", cont_transactions, " # self tr.:", cont_self_transactions, " # self tr. contr from manuf. list:",num_self_trans_contr_from_manuf_list, " # self tr. manuf from contr list:", num_self_trans_manuf_from_contr_list
        

#######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

