#!/usr/bin/env python

'''
Created by Julia Poncela, on Feb. 2016

'''

import csv
import pickle



def main():


    dict_firm_tuple_zip_code_state = pickle.load(open("../Results/dict_firm_id_zip_code.pickle", 'rb'))  # example:  05188210 ('94108', 'CA')



    list_zips=[]
    for item in  dict_firm_tuple_zip_code_state:
        zip_c = dict_firm_tuple_zip_code_state[item][0]
        if zip_c not in list_zips:
            list_zips.append(zip_c)
 

    N=len(list_zips)
    print "# number of distinct zips:", N, " # number of posible pairs:", N*(N-1.)/2.

 

    name0="../Data/Distances_zip_codes/sf12000zcta5distancemiles.csv"       ### "zip1","zip2",distance_miles
    print "reading: ", name0, "......."       
       
   
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
    

    cont=1       
    dict_firm_tuple_zip_dist_miles={}  
    for list_row in reader:                
        cont +=1        

        zip1 = str(list_row[0] )
        zip2 = str(list_row[1] )

        dist=float(list_row[2])

        if zip1 in list_zips and zip2 in list_zips:

            tuplaAB=(zip1, zip2)
            tuplaBA=(zip2, zip1)

            dict_firm_tuple_zip_dist_miles[tuplaAB]=dist
            dict_firm_tuple_zip_dist_miles[tuplaBA]=dist


            print cont

     



    filename="../Results/dict_zip_tuples_dist_miles.pickle"
    pickle.dump(dict_firm_tuple_zip_dist_miles, open(filename, 'wb'))
    print "written:", filename,   "  # entries in dict.:", len(dict_firm_tuple_zip_dist_miles)



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

