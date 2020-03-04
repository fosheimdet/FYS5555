
import numpy as np 
import matplotlib.pyplot as plt

from functions2 import pi
from functions2 import pf
from functions2 import readData
from functions2 import particles
from functions2 import muonBottom
#from functions import kappas
from functions2 import ABCs




#muonBottom = 1 # Set to 1 in case of mM->bB, 0 in case of eE->cC

    
        
(m,M,c_vm,c_am,c_vb,c_ab,Q) = particles(muonBottom)       
         
#delta = (c_vm**2+c_am**2)*(c_vb*c_ab)
#delta2= c_vm*c_am*c_vb*c_ab


C_conv= (0.197)**2*10**(-2)*10**12   #Conversion factor for areas from NU to barn 

###########################################################################################   
#Total Cross Section and asymmetry
###########################################################################################

s_sqrt = np.arange(20,200,0.5) # Centre of mass energy in GeV
s = s_sqrt**2
sigma_tot = [0]*s.size
#print(sigma_tot.size)
sigma_a = [0]*s.size
sigma_z = [0]*s.size
sigma_az = [0]*s.size
sigma_H = [0]*s.size
A_fb = [0]*s.size


for i in range(0,s.size):
#    pi = np.sqrt(s[i]/4 - m**2)
#    pf = np.sqrt(s[i]/4-M**2)
    (A,B,C,A_a,B_a,A_z,B_z,C_z,A_az,B_az,C_az,MH) = ABCs(s[i])
    


    sigma_tot[i]= C_conv*(3/(16*np.pi*s[i]))*(pf(s[i])/pi(s[i]))*((1/3)*A+C)
    sigma_a[i] =  C_conv*(3/(16*np.pi*s[i]))*(pf(s[i])/pi(s[i]))*((1/3)*A_a+B_a)
    sigma_z[i] =  C_conv*(3/(16*np.pi*s[i]))*(pf(s[i])/pi(s[i]))*((1/3)*A_z+B_z)
    sigma_H[i] =  C_conv*(3/(16*np.pi*s[i]))*(pf(s[i])/pi(s[i]))*(MH)
#    

    A_fb[i] = 0.5*(B)/(1/3*A+C)

    
###########################################################################################   
#Differential Cross Section
###########################################################################################
S_sqrt=130
S=S_sqrt**2


x = np.linspace(-1,1,100) #Cos(theta)
dsigma_tot = [0]*x.size
dsigma_a = [0]*x.size
dsigma_z = [0]*x.size
dsigma_az = [0]*x.size

(A,B,C,A_a,B_a,A_z,B_z,C_z,A_az,B_az,C_az,MH) = ABCs(S)


for i in range(0,x.size):
    
     dsigma_tot[i] = C_conv*(3/(32*np.pi*S))*(pf(S)/pi(S))*(A*x[i]**2+B*x[i]+C)
     dsigma_a[i]   = C_conv*(3/(32*np.pi*S))*(pf(S)/pi(S))*(A_a*x[i]**2+B_a)
     dsigma_z[i]   = C_conv*(3/(32*np.pi*S))*(pf(S)/pi(S))*(A_z*x[i]**2+B_z*x[i]+C_z)
     dsigma_az[i]  = C_conv*(3/(32*np.pi*S))*(pf(S)/pi(S))*(A_az*x[i]**2+B_az*x[i]+C_az)
 
print(gz)
######################################################################
#Reading in compHEP data
######################################################################

#Data for el.mag., electroweak and higgs diagrams
filename1 = "sigma_tot_nh_100.txt"
filename2 = "dsigma_a_100.txt"
filename3 = "gammaplusz.txt"

#No higgs
filename4 = "dsigma_tot_nh.txt"


#Z-prime included
filename5 = "Afb_Zp_n100.txt"
filename6 = "sigma_Zp_n100.txt"
filename7 = "dsigma_Zp_s5000.txt"
filename8 = "dsigma_Zp_s6000.txt"

filename9 = "dsigma_tot_s130.txt"
filename10= "dsigma_a_s130.txt"
filename11= "dsigma_z_s130.txt"
filename12="dsigma_H_s130.txt"

f= open(filename10,"r")
col1,col2 = readData(f)

#########################################################################
#Plots
#########################################################################


fig0=plt.figure(0)

       
plt.xlabel('$\sqrt{s}[GeV]$',size=12)
plt.ylabel('$\sigma[pb]$',size=12)
plt.semilogy(s_sqrt, sigma_tot,'b',label = '$\sigma_{\gamma + Z +\gamma Z}$')
plt.semilogy(s_sqrt, sigma_a,'r',label='$\sigma_{\gamma}$')
plt.semilogy(s_sqrt, sigma_z,'g',label='$\sigma_{z}$')
#plt.semilogy(s_sqrt, sigma_H,'m',label='$\sigma_{H}$')
#plt.semilogy(col1,col2,'k',label='$\sigma_{CompHEP}$')
#plt.semilogy(col1, col2,'m',label = '$\sigma_{\gamma + Z + H +Z\'}$')

ax = fig0.gca()
ax.set_xticks(np.arange(20, 210, 10))
#ax.set_yticks(np.arange(0, 1., 30))
#plt.scatter(x, y)
plt.grid()
plt.show()
plt.legend()


fig1=plt.figure(1)
plt.title("$\sqrt{s} = 130$ GeV", size = 12 )
#plt.title("Total differential cross section") 
#plt.title("Differential cross section for $|M_{\gamma}|^2$ contribution")    
#plt.title("Differential cross section for $|M_{Z}|^2$ contribution")  
#plt.title("Diff. cross section for $M_\gamma*M_Z$ contr.")   
plt.xlabel('$\\cos{\\theta}[1]$',size=12)
plt.ylabel('$d\sigma/d\\cos{\\theta}[pb/rad]$',size=12)
#plt.ylabel('$\sigma[pb]$',size=14)

plt.plot(x, dsigma_tot,'b',label = '$d\sigma_{\gamma + Z +\gamma*Z +H }$')
plt.plot(x, dsigma_a,'r',label='$d\sigma_{\gamma}$')
plt.plot(x, dsigma_z,'g',label='$d\sigma_{z}$')
#plt.plot(x, dsigma_az,'m',label='$d\sigma_{\gamma}z}$')
ax1 = fig1.gca()
ax1.set_xticks(np.arange(-1, 1.1, 0.2))
#ax.set_yticks(np.arange(0, 1., 30))
#plt.scatter(x, y)
plt.grid()
plt.show()
plt.legend()



fig2=plt.figure(2)
if (muonBottom == 1):
    plt.title("Forward-backward asymmetry for $\mu^{-},\mu^{+}\\rightarrow b,\\bar{b}$")
    plt.title("Forward-backward asymmetry")
    plt.xlabel('$\sqrt{s}[GeV]$',size=12)
    plt.ylabel('$A_{FB}[pb]$',size=12)
    plt.plot(s_sqrt, A_fb,'r',label = '$\mu^{-},\mu^{+}\\rightarrow b,\\bar{b}$')

#    ax.set_yticks(np.arange(0, 1., 30))
    #plt.scatter(x, y)
    plt.grid()
    plt.show()
    plt.legend()
else:
    plt.title("Forward-backward asymmetry for $e^{-},e^{+}\\rightarrow c,\\bar{c}$")
    plt.title("Forward-backward asymmetry")
    plt.xlabel('$\sqrt{s}[GeV]$',size=12)
    plt.ylabel('$A_{FB}[pb]$',size=12)
    plt.plot(s_sqrt, A_fb,'b',label = '$e^{-},e^{+}\\rightarrow c,\\bar{c}$')
#    ax = fig2.gca()
#    ax.set_xticks(np.arange(20, 210, 10))
#    ax.set_yticks(np.arange(0, 1., 30))
    #plt.scatter(x, y)
    plt.grid()

    plt.legend()
    plt.show()





##############################################################################
#No Z prime
##############################################################################

#fig3=plt.figure(3)
#plt.title("Differential cross section, no Higgs, CompHEP")
#plt.xlabel('$\sqrt{s}[GeV]$',size=12)
#plt.ylabel('$dd\\cos{\\theta}[pb/rad]$',size=12)
#plt.plot(col1, col2,'b',label = '$d\sigma_{\gamma + Z }$')
#ax = fig3.gca()
#ax.set_xticks(np.arange(-1,1,0.2))
##ax.set_yticks(np.arange(0, 1., 30))
##plt.scatter(x, y)
#plt.grid()
#plt.show()
#plt.legend()

#fig3=plt.figure(3)
#plt.title("Total cross section, no Higgs, CompHEP")
#plt.xlabel('$\sqrt{s}[GeV]$',size=12)
#plt.ylabel('$\sigma[pb]$',size=12)
#plt.semilogy(col1, col2,'b',label = '$\sigma_{\gamma + Z }$')
#ax = fig3.gca()
#ax.set_xticks(np.arange(20, 210, 10))
##ax.set_yticks(np.arange(0, 1., 30))
##plt.scatter(x, y)
#plt.grid()
#plt.show()
#plt.legend()
#############################
#Z prime
##############################

#fig3=plt.figure(3)
#plt.title("Total cross section, including Z'")
#plt.xlabel('$\sqrt{s}[GeV]$',size=12)
#plt.ylabel('$\sigma[pb]$',size=12)
#plt.semilogy(col1, col2,'b',label = '$\sigma_{\gamma + Z + H +Z\'}$')
#ax = fig3.gca()
#ax.set_xticks(np.arange(50, 11000, 1000))
##ax.set_yticks(np.arange(0, 1., 30))
##plt.scatter(x, y)
#plt.grid()
#plt.show()
#plt.legend()

#fig4=plt.figure(4)
#plt.title("Differential cross section with Z' included")
#plt.xlabel('$\\cos{\\theta}[1]$',size=12)
#plt.ylabel('$d\sigma_{\gamma + Z + H +Z\'}/d\\cos{\\theta}[pb/rad]$',size=12)
#plt.plot(col1, col2,'r',label="$\sqrt{s} = 6TeV$")
#
#ax = fig4.gca()
#ax.set_xticks(np.arange(-1, 1.2, 0.2))
##ax.set_yticks(np.arange(0, 1., 30))
##plt.scatter(x, y)
#plt.grid()
#plt.show()
#plt.legend()

#fig5=plt.figure(5)
#plt.title("Forward-backward asymmetry with Z' included")
#plt.xlabel('$\sqrt{s}[GeV]$',size=12)
#plt.ylabel('$A_{FB}[pb]$',size=12)
#plt.plot(col1, col2,'b')
#
#ax = fig5.gca()
#ax.set_xticks(np.arange(50, 11000, 1000))
##ax.set_yticks(np.arange(0, 1., 30))
##plt.scatter(x, y)
#plt.grid()
#plt.show()
    
fig6=plt.figure(6)
plt.title("Differential cross sections from CompHEP, $\sqrt{s} = 130GeV$")
plt.xlabel('$\\cos{\\theta}[1]$',size=12)
plt.ylabel('$d\sigma/d\\cos{\\theta}[pb/rad]$',size=12)
#plt.plot(col1, col2,'b',label="$d\sigma_{\gamma + Z + H}$")
plt.plot(col1, col2,'r',label="$d\sigma_{\gamma}$")
#plt.plot(col1, col2,'g',label="$d\sigma_{Z}$")
#plt.plot(col1, col2,'m',label="$d\sigma_{ H}$")

ax = fig6.gca()
ax.set_xticks(np.arange(-1, 1.2, 0.2))
#ax.set_yticks(np.arange(0, 1., 30))
#plt.scatter(x, y)
plt.grid()
plt.show()
plt.legend()


#plt.figure(3)
#plt.semilogy(s_sqrt, sigma_H,'m',label='$\sigma_{H}$')



