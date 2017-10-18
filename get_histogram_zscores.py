#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept. 2016

'''


import pickle
import histogram_bins_increasing
import histograma_bines_gral
import numpy 

def main():

  
    list_zscores = pickle.load(open("../Results/list_zscores_year_degree.pickle")) 

    Nbins=50
    name_h="../Results/histogram_zscore_year_degree"+str(Nbins)+"bins.dat"


#    histogram_bins_increasing.histogram(list_zscores,Nbins, name_h)
    histograma_bines_gral.histograma_bins_norm(list_zscores,Nbins, name_h)


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
