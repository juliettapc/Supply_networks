#! /usr/bin/env python

"""
Created by Julia Poncela of Feb 2016

HHI is a measure of the size of firms in an  industry, and an indicator of the amount of competition among them.  Bounded by: 1/N  (equally distributed industry), 1 (total monopoly).  
For a given industry, it is defined just as the sum of the squares of the market shares of each company in the sector.

The normalised one is:  (H- 1/N)  /  (1-1/N)   between 0 and 1

"""


def calculate_HHI (list_data) :


    #list_data = [1,1,1,1,1,1,1,50,1,1,10,1,1,1,1,1,1,1,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.8]
  #  list_data=[100,43,50,1]  HHI=0.38
   
    N=float(len(list_data))
  #  print list_data, type(list_data)

    HHI=0.
    if N>1:
        norm= sum(list_data)
        if norm >0.:
            for element in list_data:               
                HHI  += float(element)*float(element)/(norm*norm)               
            HHI_norm= (HHI - 1./N) / (1.-1./N)

        else:
            HHI="NA"    # for example, if data= [0.0, 0.0, 0.0]
            HHI_norm="NA"    



    else:
        HHI=1.
        HHI_norm= 1.

    
  #  print "HHI:", HHI, " HHI_norm:", HHI_norm
    return HHI, HHI_norm
