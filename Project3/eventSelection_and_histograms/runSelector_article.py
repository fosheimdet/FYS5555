#from ROOT import *
import ROOT
import sys, os, time

t0 = time.time() 

arg1 = sys.argv[1]  

if arg1 == 'Data': 
        input_dir = '2lep/Data/'
elif arg1 == 'MC': 
        input_dir = '2lep/MC/'


myChain = ROOT.TChain('mini') 


for filename in os.listdir(input_dir):
        if not '.root' in filename: continue 
        print(filename)  
        myChain.Add(input_dir+filename) 
if arg1 == 'MC': 
        for filename in os.listdir(input_dir):
                if not '.root' in filename: continue 
                print(filename)  
                myChain.Add(input_dir+filename)

if not os.path.exists('./Histograms_article'): #Needs to change directory according to mass range
    os.makedirs('./Histograms_article')
if not os.path.exists('./Histograms_article/MC/'):
    os.makedirs('./Histograms_article/MC')
if not os.path.exists('./Histograms_article/Data/'):
    os.makedirs('./Histograms_article/Data')

entries = myChain.GetEntries() 

print("-------------------------------------------")
if arg1 == 'Data': 
        print("Running on real data!")
else: 
        print("Running on Monte Carlo!") 
print("Number of events to process: ", entries) 
print("-------------------------------------------")

if arg1 == 'Data': 
        myChain.Process("MySelector.C+", "Data") #Need to change which MySelector according to mass range
else: 
        myChain.Process("MySelector.C+", "MC") #Need to change which MySelector according to mass range

t = int( time.time()-t0 )/60  

print("Time spent: %d min" %t) 
