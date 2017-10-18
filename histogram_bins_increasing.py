#! /usr/bin/env python


import numpy as np

def histogram(lista,Nbins, name_h):

    file = open(name_h,'wt')
   
    list_values = [x for x in lista if str(x) != 'nan']
    hist, bin_edges = np.histogram(list_values,bins=Nbins, normed=True)
    #print "edges:",bin_edges, len(bin_edges)
    #print "hist:",hist, len(hist)
    
    #print "diff. bin_edges:", np.diff(bin_edges)
    bin_width=np.diff(bin_edges)[0]
    
    #print "diff. bin_edges* hist:", np.diff(bin_edges)*hist
    
    cdf =list(np.cumsum(hist*np.diff(bin_edges)))
   # print "cumulat values:", cdf, len(cdf)
    
    
   # print bin_edges[0]-bin_width/2., 0.,0.
    print >> file,bin_edges[0]-bin_width/2., 0.,0.
    for i in range(len(cdf)):
        try:
    #        print bin_edges[i]+bin_width/2., cdf[i], hist[i]
            print >> file, bin_edges[i]+bin_width/2., cdf[i], hist[i]
        except IndexError: pass
      

    print "written histogram:",name_h
    file.close()
   
