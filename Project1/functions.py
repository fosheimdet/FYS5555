
import numpy as np



#Functions to be used in plots

#Defining constants
alpha = 1/137.036 #Fine-s[i]tructure cons[i]tant
e = np.sqrt(4*np.pi*alpha)  #Electron charge

sinWein2 = 0.2397 #sin^2(theta_W) 
mw = 80.379
gw=e/(np.sqrt(sinWein2))
 

mH = 125.18
gammaH=0.013

mz = 91.1876
#gz = 0.7180
gz = e/((np.sqrt(sinWein2))*np.sqrt(1-sinWein2))
gammaz = 2.4952



muonBottom = 1# Set to 1 in case of mM->bB, 0 in case of eE->cC

def particles(muonBottom):
     if(muonBottom == 1):
            m = 0.10566 #Muon mass in GeV
            M = 4.18   #Bottom quark mass in GeV
            c_vm = -0.04
            c_am = -0.5
            c_vb = -0.35
            c_ab = -0.5
            Q =  -1/3*e  #bottom quark charge
            return (m,M,c_vm,c_am,c_vb,c_ab,Q)
     else: 
            m = 0.0005 #electron masss in GeV
            M = 1.3   #charm quark mass in GeV
            c_vm = -0.04
            c_am = -0.5
            c_vb = 0.19
            c_ab = 0.5
            Q =  2/3*e  #charm quark charge
            return (m,M,c_vm,c_am,c_vb,c_ab,Q)

(m,M,c_vm,c_am,c_vb,c_ab,Q) = particles(muonBottom)

def pi(s):
    return np.sqrt(s/4 - m**2)
def pf(s):
    return np.sqrt(s/4 - M**2)

#########
def f_s(s):
        return (gz**2)/((s-mz**2)**2+mz**2*gammaz**2)  

def kappas(s):
 

    K_a = (8*e**2*Q**2)/(s**2)                                                                   #K_gamma
    K_z1 = 8*gz**2*f_s(s)*((c_vm**2+c_am**2)*(c_vb**2+c_ab**2) + 4*c_vm*c_am*c_vb*c_ab)       #K_Z1
    K_z2 = 8*gz**2*f_s(s)*((c_vm**2+c_am**2)*(c_vb**2+c_ab**2) - 4*c_vm*c_am*c_vb*c_ab)        #K_Z2
    K_az1 = -(16*e*Q*(s-mz**2)/(3*s))*f_s(s)*(c_vm*c_vb+c_am*c_ab)                          #K_gammaz1
    K_az2 = -(16*e*Q*(s-mz**2)/(3*s))*f_s(s)*(c_vm*c_vb-c_am*c_ab)                          #K_gammaz1
       
    K_H     = (gw**4*m**2*M**2)/(mw**4*((s-mH**2)**2+mH**2*gammaH**2))
 

    return (K_a,K_z1,K_z2,K_az1,K_az2,K_H)

#To help you with your ABC's
def ABCs(s): 
    
    (K_a,K_z1,K_z2,K_az1,K_az2,K_H) = kappas(s)
    
    
    A = (s/4 - m**2)*(s/4 - M**2)*(2*K_a + K_z1 + K_z2 + K_az1 + K_az2)
    B = 0.5*s*np.sqrt((s/4-m**2)*(s/4-M**2))*(-K_z1 + K_z2 -K_az1 + K_az2)
    C = 0.25*s*(m**2+M**2)*(K_az1+K_az2) + 0.25*s*(2*K_a + K_z1 + K_z2 + K_az1 + K_az2)
    
    A_a = 2*K_a*(s/4 - m**2)*(s/4-M**2)
    B_a = K_a*((s**2)/8+(s/2)*(m**2+M**2))
    
    A_z = (pi(s)*pf(s))**2*(K_z1+K_z2)
    B_z = s/2*pi(s)*pf(s)*(K_z2-K_z1)
    C_z = s/4*(K_z1+K_z2) + 8*gz**2*f_s(s)*(-M**2*(c_vm**2+c_am**2)*c_vb**2+c_ab**2*(s/4+pi(s))-m**2*(c_vb**2+c_ab**2)*c_vm*c_am*(s/4+pf(s))+2*m**2*M**2*c_vm*c_am*c_vb*c_ab)
    
    A_az = (pi(s)*pf(s))**2*(K_az1+K_az2)
    B_az = s/2*pi(s)*pf(s)*(K_az2-K_az1)
    C_az = (s/4+pi(s)**2*pf(s)**2)*(K_az1+K_az2) -3*(16*e*Q*(s-mz**2)/(3*s))*f_s(s)*c_vm*c_vb*s/2*(m**2+M**2)
    
#Spin-averaged matrix element for pure Higgs contribution
    MH = K_H*((s**2)/4 - s*(m**2+M**2)+4*m**2*M**2)



     

    return (A,B,C,A_a,B_a,A_z,B_z,C_z,A_az,B_az,C_az,MH)
  


def readData(f):
    
    lines = f.readlines()[3:]
    
    n = len(lines)
    lines2=[None]*n
    lines3=[None]*2*n
    data1 = [0]*2*n #mantissa
    data2 = [0]*2*n #exponent
 #  data3 = [0]*2*n #Product
    col1 = [0]*n
    col2 = [0]*n
    for i in range(0,n):
        a=lines[i]
        a=a[:-1]
        lines[i]=a
        lines2[i]=lines[i].split()
    
    k = 0
    for j in range(0,n):
        lines3[k]=lines2[j][0].split('E')
        data1[k] = float(lines3[k][0])
        data2[k] = float(lines3[k][1])
        col1[j]=data1[k]*10**data2[k]
        
        lines3[k+1]=lines2[j][1].split('E')
        data1[k+1] = float(lines3[k+1][0])
        data2[k+1] = float(lines3[k+1][1])
        col2[j]=data1[k+1]*10**data2[k+1]
        k=k+2
    
    return (col1,col2)
    print(col1)
    print(n)
    f.close
