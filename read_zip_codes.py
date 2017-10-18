#!/usr/bin/env python

'''
Created by Julia Poncela, on Feb. 2016

'''


import csv
import pickle



def main():

    name0="../Data/95_05NYCgamentdata/Firm_attributes_Master.csv"

    print "reading: ", name0, "......."       
    
    
        ####  Firm_Number	Firm_Addr1	Firm_Addr2	Firm_City	Firm_State	Firm_Zip	Firm_Phone	Date_Out_of_Business	Product_Code1	Product_Code1_Description	Product_code2	Product_Code2_Description	Product_Code3	Product_Code3_Description	Business_Type_Code	Business_Type_Code_Description	Federal_EIN	Local	Vacation_%_1	Vacation_%_2	Vacation_%_3	Date_First_HW_Contribution	Date_First_RET_Contribution	Date_First_HSP_Contribution	Date_Last_Wages_Posted	Shop_Status_Code	Association_Code	Association_Code_Description	Association_Period_From_Date	Association_Period_To_Date	Number_of_Employees	Prior_Firm_Number	Prior_Firm_Number_Name	Parent_Firm_Number	Parent_Firm_Number_Name	Grand_Parent_Firm_Number	Grand_Parent_Firm_Number_Name	Next_Firm_Number	Next_Firm_Number_Name	Date_First_In_Business	Date_Organized	Date_Last_Chargeable_Payroll	CEO1_LName	CEO1_FName	CEO2_LName	CEO2_FName	CEO3_LName	CEO3_FName	Last_Audit_From_Date	Last_Audit_To_Date	Showroom_Address_1	Showroom_Address_2	Showroom_City	Showroom_State	Showroom_Zip	Showroom_Phone	Shipping_Address1	Shipping_Address2	Shipping_City	Shipping_State	Shipping_Zip	Shipping_Phone	Mailing_Address1	Mailing_Address2	Mailing_City	Mailing_State	Mailing_Zip	Mailing_Phone

    cont=1       
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   # to skip the header
    

    dict_firm_tuple_zip_code_state={}
   
    for list_row in reader:                
      cont +=1    
      try:
        firm=int(list_row[0])
      

        zip_code="NA"
        if len(str(list_row[5])) > 3:
            zip_code=str(list_row[5])
        if len(str(list_row[5]))>5:
            zip_code=list_row[0:5]


       
        mailing_zip_code="NA"
        if len(str(list_row[66])) > 3: 
            mailing_zip_code=str(list_row[66])  
     

        state="NA"
        if len(str(list_row[4])) > 0:
            state=str(list_row[4])    



        if  len(str(list_row[5])) < 5:
            if len(str(list_row[66])) <=3 :               
               pass# missing_zips +=1  
            else:
                zip_code = mailing_zip_code      
      
  
        
        if type(zip_code) == list:
            if len(mailing_zip_code) >3:
                zip_code= mailing_zip_code
            

      #  print cont, firm, "zip:", zip_code, len(zip_code), type(zip_code),"   zip mail:",mailing_zip_code, state
        dict_firm_tuple_zip_code_state[firm]=(zip_code, state)


      except ValueError:
           print list_row


           
    missing_zips=0.
    for item in dict_firm_tuple_zip_code_state:
#        print item, dict_firm_tuple_zip_code_state[item]
        if dict_firm_tuple_zip_code_state[item][0] == "NA":
            missing_zips +=1.  



    filename="../Results/dict_firm_id_zip_code.pickle"
    pickle.dump(dict_firm_tuple_zip_code_state, open(filename, 'wb'))
    print "written:", filename

    print "# entries in dict.:", len(dict_firm_tuple_zip_code_state)
    print " tot # missing zips:", missing_zips, missing_zips/len(dict_firm_tuple_zip_code_state)

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

