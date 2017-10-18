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
import numpy as np
import networkx as nx
import random
import sys

def main():





    path="../Data/95_05NYCgamentdata/"
 


 
    ##################  
    ####### input datafile:   
    name0="Fhistory1996.xls"
    print "reading: ", path+name0, "......."       
   

    ####  paidbyfi,paidforf,periodfr,periodto,adjgr,gross,net,caf,liqdmg,cafper,rateper,ratecode


    
    cont=0 
    with open(path+name0, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for list_row in spamreader:
            
            manufacturer=list_row[0]     ##paidbyfirm
            contractor=list_row[1]      ## paidforfirm
            from_date=list_row[2]
            to_date=list_row[3]
            adj_gross=list_row[4]




            print manufacturer, contractor, from_date, to_date,  adj_gross
            

   


















######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

