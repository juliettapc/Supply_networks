#!/usr/bin/env python

'''
Created by Julia Poncela, on Sept. 2016

'''

import numpy

def main():



    Niter=100
    existing=0   # as to not overwrite existing random files

  

    dict_variables_real_coeff={}

    dict_variables_real_coeff["1.prev_p_inf_rand"]=6.296048 
    dict_variables_real_coeff["betweenness_c_fin"]=2.951969
    dict_variables_real_coeff["overlap"]=1.159515 

    dict_variables_real_coeff["2.mcj"]=1.127337
    dict_variables_real_coeff["3.mcj"]=1.364266 
    dict_variables_real_coeff["4.mcj"]=1.399656

    dict_variables_real_coeff["num_prev_errors_ij_rand"]=1.073006

    dict_variables_real_coeff["2.kshell_c_fin"]=.7590157 
    dict_variables_real_coeff["3.kshell_c_fin"]=.6942834 
    dict_variables_real_coeff["4.kshell_c_fin"]=.654963 
    dict_variables_real_coeff["5.kshell_c_fin"]=1.605525

    dict_variables_real_coeff["2.kshell_m_fin"]=.7492776 
    dict_variables_real_coeff["3.kshell_m_fin"]=.5897558
    dict_variables_real_coeff["4.kshell_m_fin"]=.4932979
    dict_variables_real_coeff["5.kshell_m_fin"]= .2641236

    dict_variables_real_coeff["2.history"]=.5720651
    dict_variables_real_coeff["3.history"]=.5299784 
    dict_variables_real_coeff["4.history"]=.4086193

    dict_variables_real_coeff["2.min_dist"]=.4574937 
    dict_variables_real_coeff["3.min_dist"]=.3784308
    dict_variables_real_coeff["4.min_dist"]=.2293746
    dict_variables_real_coeff["5.min_dist"]= .3068703
    dict_variables_real_coeff["6.min_dist"]=.3067221
    dict_variables_real_coeff["7.min_dist"]=.7817264
    dict_variables_real_coeff["8.min_dist"]=8.19e-13
    dict_variables_real_coeff["no_path_to_inf"]= .1796795

    dict_variables_real_coeff["degree_asym_ij"]= .2989893


    
    
    
    ####### original file :
    #name0="../Results/log_hazard_model_random.log"
    #csvfile=open(name0, 'rb')
    #reader = csv.reader(csvfile, delimiter=' ', quotechar='"')            
    #next(reader, None)   # to skip the header
    




#  _t | Haz. Ratio   Std. Err.      z    P>|z|     [95% Conf.  
# > Interval]


    ####### original file :
    name0="../log_hazard_model_random1000partial.log"#../Results/log_hazard_model_random.log"
    file_real=open(name0,'r')
    list_lines=file_real.readlines()
    

    flag_mcj = 0
    flag_kshell_c = 0
    flag_kshell_m = 0
    flag_history = 0
    flag_dist = 0

    dict_var_list_values={}
    cont=0
    for line in list_lines:


        cont +=1

        line=line.strip()  # i remove all initial spaces in the line


        if "1.prev_p_inf_rand" in line:        
            list_row= line.split("   ")
            value=float(list_row[1])
            
            try:
                dict_var_list_values["1.prev_p_inf_rand"].append(value)
            except KeyError:
                dict_var_list_values["1.prev_p_inf_rand"]=[]
                dict_var_list_values["1.prev_p_inf_rand"].append(value)


            # print line
            #print value, list_row
            #print


        if "betweenness_c_fin |" in line:           
            list_row= line.split("   ")
            value=float(list_row[1])
           
            try:
                dict_var_list_values["betweenness_c_fin"].append(value)
            except KeyError:
                dict_var_list_values["betweenness_c_fin"]=[]
                dict_var_list_values["betweenness_c_fin"].append(value)

            #print line
            #print value, list_row
            #print



        if "overlap |" in line:         
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["overlap"].append(value)
            except KeyError:
                dict_var_list_values["overlap"]=[]
                dict_var_list_values["overlap"].append(value)

            #print line
            #print value, list_row
            #print



        if "mcj |" in line:   
            flag_mcj =1


        if   flag_mcj ==1    and   "2  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["2.mcj"].append(value)
            except KeyError:
                dict_var_list_values["2.mcj"]=[]
                dict_var_list_values["2.mcj"].append(value)

            #print line
            #print value, list_row
            #print
           
        
        if   flag_mcj ==1    and   "3  |" in line:            
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["3.mcj"].append(value)
            except KeyError:
                dict_var_list_values["3.mcj"]=[]
                dict_var_list_values["3.mcj"].append(value)

            #print line
            #print value, list_row
            #print
           


        if   flag_mcj ==1    and   "4  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["4.mcj"].append(value)
            except KeyError:
                dict_var_list_values["4.mcj"]=[]
                dict_var_list_values["4.mcj"].append(value)


            flag_mcj =0

            #print line
            #print value, list_row
            #print         
            #raw_input()



        if "num_prev_errors_ij_r~d |" in line:           
            list_row= line.split("   ")
            value=float(list_row[1])
           
            try:
                dict_var_list_values["num_prev_errors_ij_rand"].append(value)
            except KeyError:
                dict_var_list_values["num_prev_errors_ij_rand"]=[]
                dict_var_list_values["num_prev_errors_ij_rand"].append(value)

            #print line
            #print value, list_row
            #print






        if "kshell_c_fin |" in line:   
            flag_kshell_c =1


        if   flag_kshell_c ==1    and   "2  |" in line:              
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["2.kshell_c_fin"].append(value)
            except KeyError:
                dict_var_list_values["2.kshell_c_fin"]=[]
                dict_var_list_values["2.kshell_c_fin"].append(value)

            #print line
            #print value, list_row
            #print
           
        
        if    flag_kshell_c ==1     and   "3  |" in line:              
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["3.kshell_c_fin"].append(value)
            except KeyError:
                dict_var_list_values["3.kshell_c_fin"]=[]
                dict_var_list_values["3.kshell_c_fin"].append(value)

           # print line
            #print value, list_row
            #print
           


        if    flag_kshell_c ==1     and   "4  |" in line:              
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["4.kshell_c_fin"].append(value)
            except KeyError:
                dict_var_list_values["4.kshell_c_fin"]=[]
                dict_var_list_values["4.kshell_c_fin"].append(value)


            #print line
            #print value, list_row
            #print



        if    flag_kshell_c ==1     and   "5  |" in line:              
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["5.kshell_c_fin"].append(value)
            except KeyError:
                dict_var_list_values["5.kshell_c_fin"]=[]
                dict_var_list_values["5.kshell_c_fin"].append(value)


            flag_kshell_c=0

            #print line
            #print value, list_row
            #print         
            #raw_input()





        if "kshell_m_fin |" in line:   
            flag_kshell_m =1


        if   flag_kshell_m ==1    and   "2  |" in line:               
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["2.kshell_m_fin"].append(value)
            except KeyError:
                dict_var_list_values["2.kshell_m_fin"]=[]
                dict_var_list_values["2.kshell_m_fin"].append(value)

            #print line
            #print value, list_row
            #print
           
        
        if    flag_kshell_m ==1     and   "3  |" in line:               
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["3.kshell_m_fin"].append(value)
            except KeyError:
                dict_var_list_values["3.kshell_m_fin"]=[]
                dict_var_list_values["3.kshell_m_fin"].append(value)

            #print line
            #print value, list_row
            #print
           


        if    flag_kshell_m ==1     and   "4  |" in line:              
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["4.kshell_m_fin"].append(value)
            except KeyError:
                dict_var_list_values["4.kshell_m_fin"]=[]
                dict_var_list_values["4.kshell_m_fin"].append(value)


            #print line
            #print value, list_row
            #print



        if    flag_kshell_m ==1     and   "5  |" in line:   
            list_row= line.split("   ")



            value=float(list_row[1])

            try:
                dict_var_list_values["5.kshell_m_fin"].append(value)
            except KeyError:
                dict_var_list_values["5.kshell_m_fin"]=[]
                dict_var_list_values["5.kshell_m_fin"].append(value)


            flag_kshell_m=0

            #print line
            #print value, list_row
            #print         
            #raw_input()




        if "history_ij_cat |" in line:   
            flag_history =1


        if    flag_history ==1    and   "2  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["2.history"].append(value)
            except KeyError:
                dict_var_list_values["2.history"]=[]
                dict_var_list_values["2.history"].append(value)

            #print line
            #print value, list_row
            #print
           
        
        if    flag_history ==1      and   "3  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["3.history"].append(value)
            except KeyError:
                dict_var_list_values["3.history"]=[]
                dict_var_list_values["3.history"].append(value)

            #print line
            #print value, list_row
            #print
           


        if    flag_history ==1      and   "4  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["4.history"].append(value)
            except KeyError:
                dict_var_list_values["4.history"]=[]
                dict_var_list_values["4.history"].append(value)



            flag_history = 0

            #print line
            #print value, list_row
            #print         
            #raw_input()

           






        if "min_dist_i_to_inf |" in line:   
            flag_dist =1


        if    flag_dist ==1    and   "2  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["2.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["2.min_dist"]=[]
                dict_var_list_values["2.min_dist"].append(value)

            #print line
            #print value, list_row
            #print
           
        
        if    flag_dist ==1     and   "3  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["3.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["3.min_dist"]=[]
                dict_var_list_values["3.min_dist"].append(value)

            #print line
            #print value, list_row
            #print
           


        if    flag_dist ==1       and   "4  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["4.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["4.min_dist"]=[]
                dict_var_list_values["4.min_dist"].append(value)

            #print line
            #print value, list_row
            #print


        if    flag_dist ==1    and   "5  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["5.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["5.min_dist"]=[]
                dict_var_list_values["5.min_dist"].append(value)

           # print line
            #print value, list_row
            #print
           
        
        if    flag_dist ==1     and   "6  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["6.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["6.min_dist"]=[]
                dict_var_list_values["6.min_dist"].append(value)

            #print line
            #print value, list_row
            #print
           


        if    flag_dist ==1       and   "7  |" in line:   
            list_row= line.split("   ")            
            value=float(list_row[1])

            try:
                dict_var_list_values["7.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["7.min_dist"]=[]
                dict_var_list_values["7.min_dist"].append(value)

            #print line
            #print value, list_row
            #print



        if    flag_dist ==1       and   "8  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["8.min_dist"].append(value)
            except KeyError:
                dict_var_list_values["8.min_dist"]=[]
                dict_var_list_values["8.min_dist"].append(value)

            #print line
            #print value, list_row
            #print


        if    flag_dist ==1       and   "10000000  |" in line:   
            list_row= line.split("   ")
            value=float(list_row[1])

            try:
                dict_var_list_values["no_path_to_inf"].append(value)
            except KeyError:
                dict_var_list_values["no_path_to_inf"]=[]
                dict_var_list_values["no_path_to_inf"].append(value)

            #print line
            #print value, list_row
            #print



            flag_dist = 0

           

           

        if "degree_asym_ij |" in line:           
            list_row= line.split("   ")
            value=float(list_row[1])
           
            try:
                dict_var_list_values["degree_asym_ij"].append(value)
            except KeyError:
                dict_var_list_values["degree_asym_ij"]=[]
                dict_var_list_values["degree_asym_ij"].append(value)

           











        #file_new.close()
        #print "written:", new_name


    print
    print
    print  "avg  1.prev_p_inf_rand:",numpy.mean(dict_var_list_values["1.prev_p_inf_rand"]), " real:", dict_variables_real_coeff["1.prev_p_inf_rand"]," zscore:", (dict_variables_real_coeff["1.prev_p_inf_rand"]- numpy.mean(dict_var_list_values["1.prev_p_inf_rand"]))/numpy.std(dict_var_list_values["1.prev_p_inf_rand"])
    print 
    print  "avg betweenness_c_fin:",numpy.mean(dict_var_list_values["betweenness_c_fin"]),  " real:",dict_variables_real_coeff["betweenness_c_fin"]," zscore:", (dict_variables_real_coeff["betweenness_c_fin"]- numpy.mean(dict_var_list_values["betweenness_c_fin"]))/numpy.std(dict_var_list_values["betweenness_c_fin"])
    print 
    print  "avg overlap:",numpy.mean(dict_var_list_values["overlap"]), " real:",dict_variables_real_coeff["overlap"], " zscore:", (dict_variables_real_coeff["overlap"]- numpy.mean(dict_var_list_values["overlap"]))/numpy.std(dict_var_list_values["overlap"])
    print 
    print  "avg 2.mcj:",numpy.mean(dict_var_list_values["2.mcj"]),  " real:",dict_variables_real_coeff["2.mcj"]," zscore:", (dict_variables_real_coeff["2.mcj"]- numpy.mean(dict_var_list_values["2.mcj"]))/numpy.std(dict_var_list_values["2.mcj"])
    print  "avg 3.mcj:",numpy.mean(dict_var_list_values["3.mcj"]),  " real:",dict_variables_real_coeff["3.mcj"]," zscore:", (dict_variables_real_coeff["3.mcj"]- numpy.mean(dict_var_list_values["3.mcj"]))/numpy.std(dict_var_list_values["3.mcj"])
    print  "avg 4.mcj:",numpy.mean(dict_var_list_values["4.mcj"]),  " real:",dict_variables_real_coeff["4.mcj"]," zscore:", (dict_variables_real_coeff["4.mcj"]- numpy.mean(dict_var_list_values["4.mcj"]))/numpy.std(dict_var_list_values["4.mcj"])

    print 
    print  "avg num_prev_errors_ij_rand:",numpy.mean(dict_var_list_values["num_prev_errors_ij_rand"]),  " real:",dict_variables_real_coeff["num_prev_errors_ij_rand"],"zscore:", (dict_variables_real_coeff["num_prev_errors_ij_rand"]- numpy.mean(dict_var_list_values["num_prev_errors_ij_rand"]))/numpy.std(dict_var_list_values["num_prev_errors_ij_rand"])

    print 
    print  "avg 2.kshell_c_fin:",numpy.mean(dict_var_list_values["2.kshell_c_fin"]), " real:",dict_variables_real_coeff["2.kshell_c_fin"], " zscore:", (dict_variables_real_coeff["2.kshell_c_fin"]- numpy.mean(dict_var_list_values["2.kshell_c_fin"]))/numpy.std(dict_var_list_values["2.kshell_c_fin"])
    print  "avg 3.kshell_c_fin:",numpy.mean(dict_var_list_values["3.kshell_c_fin"]),  " real:",dict_variables_real_coeff["3.kshell_c_fin"]," zscore:", (dict_variables_real_coeff["3.kshell_c_fin"]- numpy.mean(dict_var_list_values["3.kshell_c_fin"]))/numpy.std(dict_var_list_values["3.kshell_c_fin"])
    print  "avg 4.kshell_c_fin:",numpy.mean(dict_var_list_values["4.kshell_c_fin"]),  " real:",dict_variables_real_coeff["4.kshell_c_fin"]," zscore:", (dict_variables_real_coeff["4.kshell_c_fin"]- numpy.mean(dict_var_list_values["4.kshell_c_fin"]))/numpy.std(dict_var_list_values["4.kshell_c_fin"])
    print  "avg 5.kshell_c_fin:",numpy.mean(dict_var_list_values["5.kshell_c_fin"]),  " real:",dict_variables_real_coeff["5.kshell_c_fin"]," zscore:", (dict_variables_real_coeff["5.kshell_c_fin"]- numpy.mean(dict_var_list_values["5.kshell_c_fin"]))/numpy.std(dict_var_list_values["5.kshell_c_fin"])
    print 


    print  "avg 2.kshell_m_fin:",numpy.mean(dict_var_list_values["2.kshell_m_fin"]),  " real:",dict_variables_real_coeff["2.kshell_m_fin"]," zscore:", (dict_variables_real_coeff["2.kshell_m_fin"]- numpy.mean(dict_var_list_values["2.kshell_m_fin"]))/numpy.std(dict_var_list_values["2.kshell_m_fin"])
    print  "avg 3.kshell_m_fin:",numpy.mean(dict_var_list_values["3.kshell_m_fin"]),  " real:",dict_variables_real_coeff["3.kshell_m_fin"]," zscore:", (dict_variables_real_coeff["3.kshell_m_fin"]- numpy.mean(dict_var_list_values["3.kshell_m_fin"]))/numpy.std(dict_var_list_values["3.kshell_m_fin"])
    print  "avg 4.kshell_m_fin:",numpy.mean(dict_var_list_values["4.kshell_m_fin"]),  " real:",dict_variables_real_coeff["4.kshell_m_fin"]," zscore:", (dict_variables_real_coeff["4.kshell_m_fin"]- numpy.mean(dict_var_list_values["4.kshell_m_fin"]))/numpy.std(dict_var_list_values["4.kshell_m_fin"])
    print  "avg 5.kshell_m_fin:",numpy.mean(dict_var_list_values["5.kshell_m_fin"]),  " real:",dict_variables_real_coeff["5.kshell_m_fin"]," zscore:", (dict_variables_real_coeff["5.kshell_m_fin"]- numpy.mean(dict_var_list_values["5.kshell_m_fin"]))/numpy.std(dict_var_list_values["5.kshell_m_fin"])
    

    print 
    print  "avg 2.history_ij_cat:",numpy.mean(dict_var_list_values["2.history"]),  " real:",dict_variables_real_coeff["2.history"]," zscore:", (dict_variables_real_coeff["2.history"]- numpy.mean(dict_var_list_values["2.history"]))/numpy.std(dict_var_list_values["2.history"])
    print  "avg 3.history_ij_cat:",numpy.mean(dict_var_list_values["3.history"]),  " real:",dict_variables_real_coeff["3.history"]," zscore:", (dict_variables_real_coeff["3.history"]- numpy.mean(dict_var_list_values["3.history"]))/numpy.std(dict_var_list_values["3.history"])
    print  "avg 4.history_ij_cat:",numpy.mean(dict_var_list_values["4.history"]),  " real:",dict_variables_real_coeff["4.history"]," zscore:", (dict_variables_real_coeff["4.history"]- numpy.mean(dict_var_list_values["4.history"]))/numpy.std(dict_var_list_values["4.history"])

    print 

    print  "avg 2.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["2.min_dist"]),  " real:",dict_variables_real_coeff["2.min_dist"]," zscore:", (dict_variables_real_coeff["2.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 3.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["3.min_dist"]),  " real:",dict_variables_real_coeff["3.min_dist"]," zscore:", (dict_variables_real_coeff["3.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 4.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["4.min_dist"]), " real:",dict_variables_real_coeff["4.min_dist"], " zscore:", (dict_variables_real_coeff["4.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 5.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["5.min_dist"]),  " real:",dict_variables_real_coeff["5.min_dist"]," zscore:", (dict_variables_real_coeff["5.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 6.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["6.min_dist"]),  " real:",dict_variables_real_coeff["6.min_dist"]," zscore:", (dict_variables_real_coeff["6.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 7.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["7.min_dist"]),  " real:",dict_variables_real_coeff["7.min_dist"]," zscore:", (dict_variables_real_coeff["7.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg 8.min_dist_i_to_inf:",numpy.mean(dict_var_list_values["8.min_dist"]),  " real:",dict_variables_real_coeff["8.min_dist"]," zscore:", (dict_variables_real_coeff["8.min_dist"]- numpy.mean(dict_var_list_values["2.min_dist"]))/numpy.std(dict_var_list_values["2.min_dist"])
    print  "avg no_path_to_inf:",numpy.mean(dict_var_list_values["no_path_to_inf"]),  " real:",dict_variables_real_coeff["no_path_to_inf"]," zscore:", (dict_variables_real_coeff["no_path_to_inf"]- numpy.mean(dict_var_list_values["no_path_to_inf"]))/numpy.std(dict_var_list_values["no_path_to_inf"])
    

    print 
    print  "avg degree_asym_ij:",numpy.mean(dict_var_list_values["degree_asym_ij"]),  " real:",dict_variables_real_coeff["degree_asym_ij"]," zscore:", (dict_variables_real_coeff["degree_asym_ij"]- numpy.mean(dict_var_list_values["degree_asym_ij"]))/numpy.std(dict_var_list_values["degree_asym_ij"])




    
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
