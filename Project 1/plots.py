# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:10:48 2020

@author: fos[i]he
"""
import numpy as np 
import matplotlib.pyplot as plt


#Defining cons[i]tants[i]

alpha = 1/137.036 #Fine-s[i]tructure cons[i]tant

m = 0.10566 #Muon mas[i]s[i] in GeV
M = 4.18   #Bottom quark mas[i]s[i] in GeV
c_vm = -0.04
c_am = -0.5
c_vb = -0.35
c_ab = -0.5

mz = 91.1876
gz = 0.7180
gammaz = 2.4952


e = np.sqrt(4*np.pi*alpha)  #Electron charge
Q =  -1/3*e  #Bottom quark charge

C_conv= 3.8808*10**4    #Conversion factor for areas from NU to barn 


s_sqrt = np.arange(10,125,1) # Centre of mas[i]s[i] energy in GeV
s = s_sqrt**2
sigma_tot = [0]*s.size
#print(sigma_tot.size)
sigma_a = [0]*s.size
sigma_z = [0]*s.size
sigma_az = [0]*s.size


for i in range(0,s.size):
    pi=np.sqrt(s[i]/4 - m**2)
    pf=np.sqrt(s[i]/4 - M**2)
    f_s = (gz**2)/((s[i]-mz**2)**2+mz**2*gammaz**2) 
    K_a = (8*e**4)/(8*s[i]**2)                                                                   #K_gamma
    K_z1 = 8*gz**2*f_s*((c_vm**2+c_am**2)*(c_vb**2+c_ab**2) + 2*c_vm*c_am*c_vb*c_ab)       #K_Z1
    K_z2 = 8*gz**2*f_s*((c_vm**2+c_am**2)*(c_vb**2+c_ab**2) - 2*c_vm*c_am*c_vb*c_ab)        #K_Z2
    K_az1 = (16*e**2*(s[i]-mz**2)/(3*s[i]))*f_s*(c_vm*c_vb+c_am*c_ab)                          #K_gammaz1
    K_az2 = (16*e**2*(s[i]-mz**2)/(3*s[i]))*f_s*(c_vm*c_vb-c_am*c_ab)                          #K_gammaz1
    
    A = (s[i]/4 - m**2)*(s[i]/4 - M**2)*(2*K_a + K_z1 + K_z2 + K_az1 + K_az2)
    B = 0.5*s[i]*np.sqrt((s[i]/4-m**2)*(s[i]/4-M**2))*(-K_z1 + K_z2 -K_az1 + K_az2)
    C = 0.25*s[i]*(m**2+M**2)*(K_az1+K_az2) + 0.25*s[i]*(2*K_a + K_z1 + K_z2 + K_az1 + K_az2)
    
    A_a = 2*K_a*(s[i]/4 - m**2)*(s[i]/4-M**2)
    B_a = K_a*((s[i]**2)/8+(s[i]/2)*(m**2+M**2))
    
    A_z = (pi*pf)**2*(K_z1+K_z2)
    B_z = s[i]/2*pi*pf*(K_z2-K_z1)
    C_z = s[i]/4*(K_z1+K_z2)
    
    #cos[i]_theta = np.arange(0,)

    sigma_tot[i]= C_conv*(3/(16*np.pi*s[i]))*(pf/pi)*((1/3)*A+C)
    sigma_a[i] =  C_conv*(3/(16*np.pi*s[i]))*(pf/pi)*((1/3)*A_a+B_a)
    sigma_z[i] =  C_conv*(3/(16*np.pi*s[i]))*(pf/pi)*((1/3)*A_z+B_z)


plt.figure(0)
#ax1 = plt.s[i]ubplot(311) 
       
plt.xlabel('$\sqrt{s}[GeV]$',size=14)
plt.ylabel('$\sigma[b]$',size=14)
plt.semilogy(s_sqrt, sigma_tot,'b',label = '$\sigma_{tot}$')
plt.semilogy(s_sqrt, sigma_a,'r',label='$\sigma_{\gamma}$')
plt.semilogy(s_sqrt, sigma_z,'g',label='$\sigma_{z}$')
plt.legend()

#print(s[50])
#print(sigma_tot[50])


#X = np.arange(0,10,1)
#Y = X**2
#plt.figure(1)
#plt.plot(X,Y)



        
