#! /usr/bin/env python


import numpy


def histograma_bins_norm(lista,Nbins, name_h):
                      
     #if i want to compare several distrib. i MUST give same Nbins and (max,min) range too!!!
    file = open(name_h,'wt')
   

    minimum=float(min(lista))
    maximum=float(max(lista))   # fixed range so i can compare histograms from diff. models
    print "min:",minimum, " max:",maximum, " N:", len(lista), " Nbins:", Nbins



    counts, bin_edges= numpy.histogram(lista,bins=Nbins, range=(minimum,maximum), normed= False)
  
    counts_n= counts/ sum(counts* numpy.diff(bin_edges))

    list_diff_bins=numpy.diff(bin_edges)
    
    bin_size=float(bin_edges[1]-bin_edges[0])



    Cumul_prob=[0]*500000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




    for i in range(len(counts_n)):   
        print >> file, bin_edges[i]-list_diff_bins[i]/2., counts_n[i], counts[i],float(Cumul_prob[i])/(float(len(lista))*bin_size), Cumul_prob[i]


    print "written histogram:",name_h






################################
################################


def histograma_bins(lista,Nbins, name_h):
                      

    minimum=float(min(lista))
    maximum=float(max(lista))   # fixed range so i can compare histograms from diff. models
    print "min:",minimum, " max:",maximum, " N:", len(lista)
    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(minimum,maximum))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*500000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas=[]
    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        #if  hist[b] !=0:
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b]),  float(hist[b])/float(len(lista))       
        tupla=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(hist[b])/(float(len(lista))*bin_size))
        lista_tuplas.append(tupla)
        
       

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   

    print  "written histogram:",name_h

    print "    Data Columns:  x, norm_count, count, norm_cumulat, cumulat, float(hist[b])/float(len(lista))"   

 #   print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size), cumul_prob (normalization by N events only)"
   
    return lista_tuplas




################################
################################




def histograma_bins_zero(lista,Nbins, name_h):# bins centered on the left corner of the bin  (not the center)
                      
    print min(lista),max(lista)
    minimum=0#float(min(lista))
    maximum=20000#float(max(lista))   # fixed range so i can compare histograms from diff. models
 
    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(minimum,maximum))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
   
   

    Cumul_prob=[0]*500000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas=[]
    origin=float(bin_edges[0]) 
   
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        #if  hist[b] !=0:
        print >> file,bin_edges[b],  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b]),  float(hist[b])/float(len(lista))       
        tupla=(bin_edges[b],  float(hist[b])/(float(len(lista))*bin_size))
        lista_tuplas.append(tupla)
        
       

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   

    print  "written histogram:",name_h
 #   print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size), cumul_prob (normalization by N events only)"
   
    return lista_tuplas



########################
########################

def histograma_bins_zero_small_bins_at_start(lista,Nbins, name_h):# bins centered on the left corner of the bin  (not the center)
                      

    minimum=0#float(min(lista))
    maximum=60000#float(max(lista))   # fixed range so i can compare histograms from diff. models
 
    num_small_bins=10   # the rest of the bins, will be collapsed to a big one


    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(minimum,maximum))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
   
   

    Cumul_prob=[0]*500000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas=[]
    origin=float(bin_edges[0]) 
    
    file = open(name_h,'wt')
    for b in range (num_small_bins -1):    
        #if  hist[b] !=0:
        print >> file,bin_edges[b],  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b]),  float(hist[b])/float(len(lista))       
        tupla=(bin_edges[b],  float(hist[b])/(float(len(lista))*bin_size))
        lista_tuplas.append(tupla)
               
        origin=origin+(bin_edges[b+1]-bin_edges[b])

    rest_prob=0.
    for element in hist[num_small_bins:]:
        rest_prob+=element


    bin_size=float(bin_edges[-1]-bin_edges[num_small_bins])
    print >> file,bin_edges[num_small_bins],rest_prob/(float(len(lista))*bin_size)



    file.close()
   

    print  "written histogram:",name_h
 #   print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size), cumul_prob (normalization by N events only)"
   
    return lista_tuplas


def histograma_bins_return_only_freq(lista,Nbins, name_h):
                      

    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(float(min(lista)),float(max(lista))))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
  #  print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*50000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
   
    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        if  hist[b] !=0:
            print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b])/float(len(lista)),float(Cumul_prob[b])     
      

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   
    print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size)"
   
    return hist


def histograma_bins_return_prob_and_cumul(lista,Nbins, name_h):
                      

    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(float(min(lista)),float(max(lista))))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
  #  print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*50000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas_prob=[]
    lista_tuplas_cumulat_prob=[]

    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        if  hist[b] !=0:
            print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b])/float(len(lista)),float(Cumul_prob[b])

        
        tupla_prob=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(hist[b])/(float(len(lista))*bin_size))
        tupla_cumulat=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(Cumul_prob[b])/(float(len(lista))*bin_size))

        lista_tuplas_prob.append(tupla_prob)
        lista_tuplas_cumulat_prob.append(tupla_cumulat)
      
       

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   
    print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size)"
   
    return lista_tuplas_prob,lista_tuplas_cumulat_prob

