
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from functions import extractExpedition
from functions import secondsToDates
from functions import getWeatherData
from functions import getHeaderData
from functions import linearRegression
import re

import os

test_header = pd.read_csv('/home/haakon/FYS5555/Project2/data/POLA01/POLA-01_2020-01-06_2020-01-07_summary_Header.csv')
test_trending = pd.read_csv('/home/haakon/FYS5555/Project2/data/POLA01/POLA-01_2020-01-06_2020-01-07_summary_Trending.csv')
test_weather = pd.read_csv('/home/haakon/FYS5555/Project2/data/POLA01/POLA-01_2020-01-06_2020-01-07_summary_Weather.csv')

print(test_trending)
#######################################################################
#Load weather files for 2018
#######################################################################
filenamesPOLA1 = glob.glob('/home/haakon/FYS5555/Project2/data/POLA01/POLA-01_2018*_summary_Weather.csv')
filenamesPOLA2 = glob.glob('/home/haakon/FYS5555/Project2/data/POLA02/POLA-02_2018*_summary_Weather.csv')
filenamesPOLA3 = glob.glob('/home/haakon/FYS5555/Project2/data/POLA03/POLA-03_2018*_summary_Weather.csv')
#######################################################################
#Load header files
#######################################################################
filenamesPOLA1_H = glob.glob('/home/haakon/FYS5555/Project2/data/POLA01/POLA-01_2018*_summary_Header.csv')
filenamesPOLA2_H = glob.glob('/home/haakon/FYS5555/Project2/data/POLA02/POLA-02_2018*_summary_Header.csv')
filenamesPOLA3_H = glob.glob('/home/haakon/FYS5555/Project2/data/POLA03/POLA-03_2018*_summary_Header.csv')




#######################################################################
#Extract data taken during expedition and concatenate to a single array
#######################################################################
weatherArr1 = extractExpedition(filenamesPOLA1)
weatherArr2 = extractExpedition(filenamesPOLA2)
weatherArr3 = extractExpedition(filenamesPOLA3)

headerArr1 = extractExpedition(filenamesPOLA1_H)
headerArr2 = extractExpedition(filenamesPOLA2_H)
headerArr3 = extractExpedition(filenamesPOLA3_H)


#######################################################################
#Date of each measurement
#######################################################################
# timeArray1,  dateArray1, contractedDateArray1 = secondsToDates(weatherArr1)
# timeArray2, dateArray2, contractedDateArray2 = secondsToDates(weatherArr2)
# timeArray3, dateArray3, contractedDateArray3 = secondsToDates(weatherArr3)
#######################################################################
#Weather data
#######################################################################
indoorTemp1, outdoorTemp1, pressure1 = getWeatherData(weatherArr1)
indoorTemp2, outdoorTemp2, pressure2 = getWeatherData(weatherArr2)
indoorTemp3, outdoorTemp3, pressure3 = getWeatherData(weatherArr3)
#######################################################################
#Header data
#######################################################################
print('timearray1 length: ', len(headerArr1[:,1]))
print('timearray2 length: ', len(headerArr2[:,1]))
timeArray1, dateArray1, contractedDateArray1 = secondsToDates(headerArr1)
timeArray2, dateArray2, contractedDateArray2 = secondsToDates(headerArr2)
timeArray3, dateArray3, contractedDateArray3= secondsToDates(headerArr3)

rawRate1, longitude1, latitude1 = getHeaderData(headerArr1, 'POLA1')
rawRate2, longitude2, latitude2 = getHeaderData(headerArr2, 'POLA2')
rawRate3, longitude3, latitude3 = getHeaderData(headerArr3, 'POLA3')









#######################################################################
#Plots
#######################################################################

# fig0 = plt.figure(0)
# ax = fig0.gca()
# # legends.append(r'$\sigma_b$ numeric')
# # legends.append(r'$\sigma_b$ analytic')
# #plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
# plt.plot(timeArray, indoorTemp,'r',linestyle = '-',label='$indoor$')
# plt.plot(timeArray, outdoorTemp,'b',linestyle = '-',label='$outdoor$')
#
# plt.xlabel('Date [d/m/2018]', size=14)
# plt.ylabel('Indoor Temperature [$^\circ$C]', size=14)
#
# plt.legend(fontsize = 12)
# ax.set_xticks(timeArray[0:-1:150])
# ax.set_xticklabels(contractedDateArray[0:-1:150], rotation='horizontal')
# plt.grid('on')
# ax.tick_params(axis='both', which='major', labelsize=14)
# # Show the minor grid lines with very faint and almost transparent grey lines
# plt.minorticks_on()
# ax.tick_params(axis='x', which='minor', bottom=False)
# plt.tight_layout()
#
# plt.show()
#
# fig1 = plt.figure(1)
# ax = fig1.gca()
# # legends.append(r'$\sigma_b$ numeric')
# # legends.append(r'$\sigma_b$ analytic')
# #plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
# plt.plot(timeArray, pressure,'k',linestyle = '-',label='$pressure$')
#
#
# plt.xlabel('Date [d/m/2018]', size=14)
# plt.ylabel('Pressure [hPa]', size=14)
#
# # plt.legend(fontsize = 12)
# ax.set_xticks(timeArray[0:-1:150])
# ax.set_xticklabels(contractedDateArray[0:-1:150], rotation='horizontal')
# plt.grid('on')
# ax.tick_params(axis='both', which='major', labelsize=14)
# # Show the minor grid lines with very faint and almost transparent grey lines
# plt.minorticks_on()
# ax.tick_params(axis='x', which='minor', bottom=False)
#
#
# plt.show()

#######################################################################
#POLA2
#######################################################################





#######################################################################
#Weather plots
#######################################################################
fig0 = plt.figure(0)
ax = fig0.gca()
plt.title('POLA1', size = 14)

plt.plot(timeArray1,indoorTemp1,c='r', label = 'Indoor temperature')
plt.plot(timeArray1,[np.mean(indoorTemp1)]*len(indoorTemp1), 'r',linestyle = '--',label = 'Average indoor temperature')
plt.plot(timeArray1,outdoorTemp1,c='b', label = 'Outdoor temperature')
plt.plot(timeArray1,[np.mean(outdoorTemp1)]*len(outdoorTemp1), 'b',linestyle = '--',label = 'Average outdoor temperature')

# plt.scatter(timeArray2,indoorTemp2,s=0.9,c='r', label = 'Indoor temperature')
# plt.plot(timeArray2,[np.mean(indoorTemp2)]*len(indoorTemp2), 'r',label = 'Average indoor temperature')
# plt.scatter(timeArray2,outdoorTemp2,s=0.9,c='b', label = 'Outdoor temperature')
# plt.plot(timeArray2,[np.mean(outdoorTemp2)]*len(outdoorTemp2), 'b',label = 'Average outdoor temperature')
#
# plt.scatter(timeArray3,indoorTemp3,s=0.9,c='r', label = 'Indoor temperature')
# plt.plot(timeArray3,[np.mean(indoorTemp3)]*len(indoorTemp3), 'r',label = 'Average indoor temperature')
# plt.scatter(timeArray3,outdoorTemp3,s=0.9,c='b', label = 'Outdoor temperature')
# plt.plot(timeArray3,[np.mean(outdoorTemp3)]*len(outdoorTemp3), 'b',label = 'Average outdoor temperature')

plt.xlabel('Date [d/m/2018]', size=16)
plt.ylabel('Indoor Temperature [$^\circ$C]', size=16)

plt.legend(fontsize = 14)
ax.set_xticks(timeArray1[0:-1:200])
ax.set_xticklabels(contractedDateArray1[0:-1:200], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
plt.tight_layout()

plt.show()
#######################################################################
#pressure
#######################################################################
fig1 = plt.figure(1)
ax = fig1.gca()
# legends.append(r'$\sigma_b$ numeric')
# legends.append(r'$\sigma_b$ analytic')
#plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
# plt.plot(timeArray, pressure,linestyle='dotted',label='$pressure$')
plt.scatter(timeArray1,pressure1,s=0.9,c='g', label = 'POLA1')
plt.plot(timeArray1, [np.mean(pressure1)]*len(pressure1), 'g', label = 'POLA1 average')
plt.scatter(timeArray2,pressure2,s=0.9,c='b', label = 'POLA2')
plt.plot(timeArray2, [np.mean(pressure2)]*len(pressure2), 'b', label = 'POLA2 average')
plt.scatter(timeArray3,pressure3,s=0.9,c='r', label = 'POLA3')
plt.plot(timeArray3, [np.mean(pressure3)]*len(pressure3), 'r', label = 'POLA3 average')



plt.xlabel('Date [d/m/2018]', size=16)
plt.ylabel('Pressure [hPa]', size=16)

plt.legend(fontsize = 14)
ax.set_xticks(timeArray2[0:-1:400])
ax.set_xticklabels(contractedDateArray2[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=14)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)


plt.show()

#######################################################################
#Header plots
#######################################################################
fig2 = plt.figure(2)
ax = fig2.gca()
# legends.append(r'$\sigma_b$ numeric')
# legends.append(r'$\sigma_b$ analytic')
#plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
# plt.plot(timeArray1_H,rawRate1,linestyle='dotted',label='POLA1')
# plt.plot(timeArray2_H,rawRate2,linestyle='dotted',label='POLA2')
# plt.plot(timeArray3_H,rawRate3,linestyle='dotted',label='POLA3')

#plot every 22th measurement (corresponding to approximately 12h since each measurement duration is about 2000s)


plt.scatter(timeArray1[0:-1:8],rawRate1[0:-1:8],s=10,c='g', label = 'POLA1')
plt.scatter(timeArray2[0:-1:22],rawRate2[0:-1:22],s=10, label = 'POLA2')
plt.scatter(timeArray3[0:-1:22],rawRate3[0:-1:22],s=10,c='r', label = 'POLA3')

# plt.plot(dateArray12h1,adjustedRawRate12h1,'g', label = 'POLA1')
# plt.plot(dateArray12h2,adjustedRawRate12h2, label = 'POLA2')
# plt.plot(dateArray12h3,adjustedRawRate12h3,'r', label = 'POLA3')


plt.xlabel('Date [d/m/2018]', size=16)
plt.ylabel('Raw rate [#events/s]', size=16)

plt.legend(fontsize = 14)
ax.set_ylim([0,50])
ax.set_xticks(timeArray2[0:-1:400])
ax.set_xticklabels(contractedDateArray2[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
plt.show()
#######################################################################
#Latitude
#######################################################################
fig3 = plt.figure(3)
ax = fig3.gca()
# legends.append(r'$\sigma_b$ numeric')
# legends.append(r'$\sigma_b$ analytic')
#plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
plt.plot(timeArray1,latitude1,'g',linestyle='-',label='POLA1')
# plt.plot(timeArray2_H,rawRate2,linestyle='dotted',label='POLA2')
# plt.plot(timeArray3_H,rawRate3,linestyle='dotted',label='POLA3')

#plot every 22th measurement (corresponding to approximately 12h since each measurement duration is about 2000s)
# plt.scatter(timeArray1_H,latitude1,s=10,c='g', label = 'POLA1')

# plt.scatter(timeArray2_H[0:-1:22],rawRate2[0:-1:22],s=10, label = 'POLA2')
# plt.scatter(timeArray3_H[0:-1:22],rawRate3[0:-1:22],s=10,c='r', label = 'POLA3')


plt.xlabel('Date [d/m/2018]', size=16)
plt.ylabel('Latitude [$^\circ$]', size=16)

plt.legend(fontsize = 14)
ax.set_ylim([60,90])
ax.set_xticks(timeArray2[0:-1:400])
ax.set_xticklabels(contractedDateArray2[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)


plt.show()
#######################################################################
#Longitude
#######################################################################
fig4 = plt.figure(4)
ax = fig4.gca()
# legends.append(r'$\sigma_b$ numeric')
# legends.append(r'$\sigma_b$ analytic')
#plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
plt.plot(timeArray1,longitude1,'g',linestyle='-',label='POLA1')
# plt.plot(timeArray2_H,rawRate2,linestyle='dotted',label='POLA2')
# plt.plot(timeArray3_H,rawRate3,linestyle='dotted',label='POLA3')

#plot every 22th measurement (corresponding to approximately 12h since each measurement duration is about 2000s)
# plt.scatter(timeArray1_H[0:-1:5],latitude1[0:-1:5],s=10,c='g', label = 'POLA1')

# plt.scatter(timeArray2_H[0:-1:22],rawRate2[0:-1:22],s=10, label = 'POLA2')
# plt.scatter(timeArray3_H[0:-1:22],rawRate3[0:-1:22],s=10,c='r', label = 'POLA3')


plt.xlabel('Date [d/m/2018]', size=14)
plt.ylabel('Longitude [$^\circ$]', size=14)

plt.legend(fontsize = 12)
ax.set_ylim([-40,40])
ax.set_xticks(timeArray2[0:-1:400])
ax.set_xticklabels(contractedDateArray2[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=14)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
plt.show()

#######################################################################
#Raw rate vs pressure
#######################################################################
fig5 = plt.figure(5)
ax = fig5.gca()
# legends.append(r'$\sigma_b$ numeric')
# legends.append(r'$\sigma_b$ analytic')
#plt.plot(exponent, sigma_k, linestyle = '-',label='$\sigma_k^2/n_k$')
# plt.plot(pressure1[0:-1:22],rawRate1[0:-1:22],'g',linestyle='-',label='POLA1')
# plt.plot(timeArray2_H,rawRate2,linestyle='dotted',label='POLA2')
# plt.plot(timeArray3_H,rawRate3,linestyle='dotted',label='POLA3')

#plot every 22th measurement (corresponding to approximately 12h since each measurement duration is about 2000s)

# plt.scatter(pressure1,rawRate1,s=10,c='g', label = 'POLA1')
# plt.scatter(pressure2,rawRate2,s=10,c='b', label = 'POLA2')
# plt.scatter(pressure3,rawRate3,s=10,c='r', label = 'POLA3')

#Do a simple linear regression using least squares


# Create linear regression object




# fig9 = plt.figure(9)
x1,y1,slope1,intercept1 = linearRegression(pressure1, rawRate1)
x2,y2,slope2,intercept2 = linearRegression(pressure2, rawRate2)
x3,y3,slope3,intercept3 = linearRegression(pressure3, rawRate3)

# print(Y)
print('slope1: ', slope1, 'y_intercept1: ', intercept1)
print('slope2: ', slope2, 'y_intercept2: ', intercept2)
print('slope3: ', slope3, 'y_intercept3: ', intercept3)



plt.scatter(pressure1,rawRate1,s=10,c='g', label = 'POLA1')
plt.scatter(pressure2,rawRate2,s=10,c='b', label = 'POLA2')
plt.scatter(pressure3,rawRate3,s=10,c='r', label = 'POLA3')



plt.plot(x1, y1,'k', label = 'POLA1 fitted')
plt.plot(x2, y2, 'magenta', label = 'POLA2 fitted')
plt.plot(x3, y3, 'cyan', label = 'POLA3 fitted')




plt.xlabel('Pressure [hPa]', size=16)
plt.ylabel('Raw rate [#events/s]', size=16)

plt.legend(fontsize = 14)
# ax.set_ylim([20,50])
ax.set_ylim([-1,50])

# ax.set_xticks(timeArray2_H[0:-1:400])
# ax.set_xticklabels(contractedDateArray2_H[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
plt.show()

#######################################################################
#Corrected raw rate
#######################################################################
fig6 = plt.figure(6)
ax = fig6.gca()



x1,y1,slope1,intercept1 = linearRegression(pressure1, rawRate1)
x2,y2,slope2,intercept2 = linearRegression(pressure2, rawRate2)
x3,y3,slope3,intercept3 = linearRegression(pressure3, rawRate3)

# print(Y)
print('slope1: ', slope1, 'y_intercept1: ', intercept1)
print('slope2: ', slope2, 'y_intercept2: ', intercept2)
print('slope3: ', slope3, 'y_intercept3: ', intercept3)

p1_ref = 1011.86
p2_ref = 1008.53
p3_ref = 985.87

N1_ref = 32.8296
N2_ref = 32.886
N3_ref = 27.5751

beta1 = slope1/N1_ref
print('beta1: ', beta1)
beta2 = slope2/N2_ref
print('beta2: ', beta2)
beta3 = slope3/N3_ref
print('beta3: ', beta3)

rawRateCorrected1 = [0]*len(rawRate1)
rawRateCorrected2 = [0]*len(rawRate2)
rawRateCorrected3 = [0]*len(rawRate3)

for i in range(0,len(pressure1)):
    rawRateCorrected1[i] = rawRate1[i] / (1 + beta1 * (pressure1[i] - p1_ref))
for i in range(0,len(pressure2)):
    rawRateCorrected2[i] = rawRate2[i] / (1 + beta2 * (pressure2[i] - p2_ref))
    # print(1 + beta2 * (pressure2[i] - p2_ref))
for i in range(0,len(pressure3)):
    rawRateCorrected3[i] = rawRate3[i] / (1 + beta3 * (pressure3[i] - p3_ref))

print(len(dateArray3))
print(len(rawRateCorrected3))


plt.scatter(timeArray1[0:-1:8],rawRateCorrected1[0:-1:8],s=10,c='g', label = 'POLA1_corrected')
plt.scatter(timeArray2[0:-1:22],rawRateCorrected2[0:-1:22],s=10,c='b', label = 'POLA2_corrected')
plt.scatter(timeArray3[0:-1:22],rawRateCorrected3[0:-1:22],s=10,c='r', label = 'POLA3_corrected')




plt.xlabel('Date [d/m/2018]', size=16)
plt.ylabel('Corrected Raw rate [#events/s]', size=16)

plt.legend(fontsize = 14)
ax.set_ylim([0,50])


ax.set_xticks(timeArray2[0:-1:400])
ax.set_xticklabels(contractedDateArray2[0:-1:400], rotation='horizontal')
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
plt.show()
#######################################################################
#Raw rate vs temperature
#######################################################################
fig7 = plt.figure(7)
ax = fig7.gca()
plt.scatter(outdoorTemp1,rawRate1,s=10,c='g', label = 'POLA1')
plt.scatter(outdoorTemp2,rawRate2,s=10,c='b', label = 'POLA2')
plt.scatter(outdoorTemp3,rawRate3,s=10,c='r', label = 'POLA3')
plt.xlabel('Outdoor temperature [$^\circ$C]', size=16)
plt.ylabel('Raw rate [#events/s]', size=16)

plt.legend(fontsize = 14)
ax.set_ylim([10,50])
plt.grid('on')
ax.tick_params(axis='both', which='major', labelsize=16)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.show()
