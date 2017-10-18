#! /usr/bin/env python

"""
Created by Julia Poncela of July 2012

Calculate the GINI coef of a dataset  0:perfectly equally distributed, 1: totally unequally distributed (all for one person)

"""
import numpy



def calculate_GINI (list_data) :

#people = [1,6,1,1,1,1,1,1,1,1,1,1,1,1,1,11,0,0,1]
#list_data = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.8]
    N = len(list_data) 
  #  print list_data, type(list_data)

    if N>1:

        list_data.sort()    # i order the list, from larger 
        list_data.reverse()  # to smaller



# given a list, enumerate(list) is a list of tuples, where for each tuple, the first element is the index, the second is the actual element in the original list#for item in  enumerate(list_data):


        product = 0
        for i, value in enumerate(list_data):   # enumerate adds a counter to an iterable

            value=float(value)  # weird things happen with integers... (product of integer*float)
            i=float(i)
            
            product = product + ((i+1.)*value)   #(i+1) es el ranking en la lista ordenada, del valor "value"
    
 
        u = numpy.mean(list_data)
        G = (N+1.0)/(N-1.0) - (product/(N*(N-1.0)*u))*2.0

    else:
        G=1.
 
    #print "GINI: ", G
    return G
