#!/usr/bin/env python

'''
Given a pair of curves, calculates the average sum of the distance sqr in each point.
then, given a dict for {file:dist_value},  picks the curve with the minimum value

Created by Julia Poncela, on sep 2012.

'''


import sys
import os
import operator
import numpy

def compare_two_curves(list_actual_evol,list_evol_one_simu):


#in the main code i do:
  #list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,list_single_t_evolution))

 #and then
 
  #list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,string_name,Niter_training,cutting_day)



  
   list_dist=[]
   for i in range(len(list_evol_one_simu)):   # i calculate the sum of distances from one curve to another at each same time step
      list_dist.append((list_evol_one_simu[i]-list_actual_evol[i])*(list_evol_one_simu[i]-list_actual_evol[i]))
              

   
   return sum(list_dist)   
        

def compare_two_curves_testing_segment(list_actual_evol,list_evol_one_simu,cutting_day):
 
  
   list_dist=[]
   for i in range(len(list_evol_one_simu)):   # i calculate the sum of distances from one curve to another at each same time step
      if i >= cutting_day:
         list_dist.append((list_evol_one_simu[i]-list_actual_evol[i])*(list_evol_one_simu[i]-list_actual_evol[i]))
              

   
   return sum(list_dist)   
        


def pick_minimum(dict_filenames_tot_distance,dynamics,all_team,Niter):

   dir_real_data='../Results/'


   if dynamics=="Infection":

      if all_team=="YES":          
         output_file=dir_real_data+"Results_infection_sorted_distance_simulated_to_real_evolutions_all_time_as_adopters"+str(Niter)+"iter_sum.dat"  
      else:
         output_file=dir_real_data+"Results_infection_sorted_distance_simulated_to_real_evolutions"+str(Niter)+"iter_sum.dat"  

   elif dynamics=="Persuasion": 

      if all_team=="YES":             
         output_file=dir_real_data+"Results_persuasion_sorted_distance_simulated_to_real_evolutions_all_time_as_adopters"+str(Niter)+"iter_sum.dat"  
      else:
         output_file=dir_real_data+"Results_persuasion_sorted_distance_simulated_to_real_evolutions"+str(Niter)+"iter_sum.dat"  
     
   else:
      print "wrong name for the type of dynamics"
      exit()



   dir_real_data='../Results/'
   minimum_value=100000.
   for clave in dict_filenames_tot_distance:   
     # print clave,  dict_filenames_tot_distance[clave]     
      if float(dict_filenames_tot_distance[clave][0]) < minimum_value:
           minimum_value= dict_filenames_tot_distance[clave][0]
           minimum_filename=clave


     # el diccionario dict_filenames_tot_distance   es: clave=path/filename  dict_filenames_tot_distance[clave] =[distancia,std_distancia]


   

   

   list_sorted_dict_filenames_tot_distance = sorted(dict_filenames_tot_distance.iteritems(), key=operator.itemgetter(1))


  
   file = open(output_file,'wt')  
   for item in list_sorted_dict_filenames_tot_distance: 
      #print item      
      print >> file,item[0],item[1][0],item[1][1]
      print  item[0],item[1][0],item[1][1]

   file.close()

# ojo!!!! when i sort the dict, what it get is a LIST of TUPLES, and each tuple (item) is ('/path/filename',[distancia, std_distancia])




   print  "the minimun value",minimum_value, " is for:", minimum_filename 

####################################################################



####################################################################




def pick_minimum_same_end(dict_filenames_prod_distances,string_name,Niter_training,cutting_day):#dict_filenames_tot_distance,string_name,all_team,Niter,cutting_day):


# i minimize the product of: sum distances along the traject, dist at the end day, and both SDs
   dir_real_data='../Results/'


   output_file=dir_real_data+"Results_sorted_by_distance_at_end_"+string_name


 
   print "# of sorted solutions:",len(dict_filenames_prod_distances)

  
   list_sorted_dict_filenames_tot_distance = sorted(dict_filenames_prod_distances.iteritems(), key=operator.itemgetter(1))


  
   file = open(output_file,'wt')  
   for item in list_sorted_dict_filenames_tot_distance: 
    #  print item    # (paht/filename, [ sum_dist_tot, st, dist_ending_point]  )
      
      print >> file,item[0],item[1][0],item[1][1],item[1][2]
    #  print  item[0],item[1][0],item[1][1],item[1][2]

   file.close()

# ojo!!!! when i sort the dict, what it get is a LIST of TUPLES, and each tuple (item) is ('/path/filename',[dist_ending_point, sum_dist_tot, st])


   print "written output file",output_file

 
   return list_sorted_dict_filenames_tot_distance






##################################################
######################################



def pick_minimum_prod_distances(dict_filenames_tot_distance,string_name,Niter,cutting_day):


# i minimize the product of: sum distances along the traject, dist at the end day, and both SDs
   dir_real_data='../Results/'


   output_file=dir_real_data+"Results_sorted_by_product_distances_along_and_end_times_final_dist_"+string_name

 
   print "# of sorted solutions:",len(dict_filenames_tot_distance)

  
   list_sorted_dict_filenames_tot_distance = sorted(dict_filenames_tot_distance.iteritems(), key=operator.itemgetter(1))
 

  
   file = open(output_file,'wt')  
   for item in list_sorted_dict_filenames_tot_distance: 
      print >> file,item[0],item[1] 

   file.close()

# ojo!!!! when i sort the dict, what it get is a LIST of TUPLES, and each tuple (item) is ('/path/filename', prod_dist)


   print "written output file",output_file

 
   return list_sorted_dict_filenames_tot_distance

##################################################
######################################
