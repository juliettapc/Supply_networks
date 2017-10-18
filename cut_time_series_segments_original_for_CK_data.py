
#! /usr/bin/env python

"""
Created by Julia Poncela of October 2011

Given a file for a non-stationary time serie, it calculates the optimum points to cut it, that mark different trends.

More info: It follows the method proposed by Fukuda, Stanley and Amaral PRL 69, 2004.



"""

 
import sys
import os
import math
import numpy
from scipy import stats



def main ():


    significance_threshold=0.95
    min_lenght=30  # to cut the series


    for index_file in range(50):
        index_file+=1

        raw_input()
        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50"
        #file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50_derivative_pwc"
        #file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50_second_derivative_pwc"
    
    
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()



      
        file2=open(file_name+"_t_points_segments"+str(min_lenght)+".dat",'wt')



       
        list_vectors=[]
        list_series=[]

        for line in list_lines_file:
   
            list=line.split(" ")
            
      
            vector=[]
            #values_time_serie.append(float(list[1])) #for the first and second derivative of the original serie

            try:                               
                #list_times.append(float(list[0])) # for the  first and second  derivative of the original serie
                vector.append(float(list[4]))
                vector.append(float(list[2])) 
            except ValueError:                       
                vector.append(float(0.0))
                vector.append(float(list[2]))
        

            vector.append(0.0)  
            list_vectors.append(vector)


        num_lines=len(list_vectors)
       
        list_series.append(list_vectors)


        list_cut_times=[]

        for list_evolution in list_series:  # i analyze the current time serie (or fragment of it)
            

            num_points=len(list_evolution)
            #print "\n\n\nnum_points in the current serie:",num_points
                

            if num_points>=min_lenght:  # if the serie is too short, i wont cut it any further

                t_max=0.0          
       
                for index in range(num_points):
           
                    if index>=1  and index < num_points-1:  # to cut the serie, at least need one point in each list

                        list1=[]  #first segment of the list
                        list2=[]  #second segment of the list
                   
                
                        for x1 in range(num_points):
                                              
                            if x1 <= index:
                                list1.append(list_evolution[x1][1]) #only the list of values (not times!)                           
                            else:
                                list2.append(list_evolution[x1][1])
                            

                   
                        mu1=numpy.mean(list1)
                        mu2=numpy.mean(list2)
                        
                        sd1=numpy.std(list1)
                        sd2=numpy.std(list2)
                        
                        N1=float(len(list1))
                        N2=float(len(list2))
                        
                        S_D=math.sqrt(((N1-1)*sd1*sd1 + (N2-1)*sd2*sd2)/(N1+N2-2))*math.sqrt(1.0/N1 + 1.0/N2)
                        t=math.fabs((mu1-mu2)/S_D)
                        


                                         
                        list_evolution[index][2]=t
                       
                       
                                                                 
                        if t >= t_max:
                            t_max=t
                            index_max_t=index
                            time_max=list_evolution[index][0]
                            
                            
                            segment1=[]
                            segment2=[]    
                            for x2 in range(num_points):   # i save the definitive two segments
                                              
                                if x2 <= index_max_t:                           
                                    segment1.append(list_evolution[x2])   #list of events (time, value,t)
                                else:                           
                                    segment2.append(list_evolution[x2])                                                                 

                   
           
           
            
                eta=4.19*math.log(float(num_points))-11.54
                delta=0.40
                nu=float(num_points)-2.0
                
                a=delta*nu  #for the Incomplete beta function
                b=delta
                x=nu/(nu+t_max*t_max)
                I=stats.mstats.betai(a,b,x)
                
                significance_t_max=math.pow((1.0-I),eta)     #Return x raised to the power y. 
        
        
            
       

                if significance_t_max>significance_threshold :
                    if  len(segment1)>min_lenght  and len(segment2)>min_lenght:
                        
                        print "    file:",index_file,"max_t:", t_max, "at time:",list_evolution[index_max_t][0],"significance:",significance_t_max,"           I:",I,"eta:",eta,"nu:",nu,"x:",x,"a:",a,"N:",num_points
                        
                        list_series.append(segment1)  # next i will analyze the two segments independently
                        list_series.append(segment2)
                        
                        print "   ",len(segment1), len(segment2)


                        list_cut_times.append(time_max)
                    
                else:
                     print "    file:",index_file,"max_t:", t_max, "at time:",list_evolution[index_max_t][0],"NON significant!:",significance_t_max,"           I:",I,"eta:",eta,"nu:",nu,"x:",x,"a:",a,"N:",num_points
                    





        
        list_cut_times=sorted(list_cut_times)
        print len(list_cut_times)
        cut_inferior=0.0

        if len(list_cut_times)!=0:
            for cut in list_cut_times:
        
                for vector in list_vectors:
                               
                    if vector[0]>= cut_inferior and vector[0]<= cut:                       
                        print >> file2, vector[0],vector[1],vector[2]



                print >> file2, "\n"
              

                if cut == list_cut_times[-1]:
                    for vector in list_vectors:
                        if vector[0]> cut:                        
                            print >> file2, vector[0],vector[1],vector[2]
                            

                print >> file2, "\n"
                
                cut_inferior=cut


        else:
            for vector in list_vectors:            
                print >> file2, vector[0],vector[1],vector[2]





        file2.close()




#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
