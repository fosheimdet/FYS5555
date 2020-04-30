import glob
import pandas as pd
import numpy as np
from scipy.optimize import least_squares
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


#Sorts filenames in dates (ascending) and extracts the files containing measurements during the expedition

def extractExpedition(filenames):
    f1= [None]*len(filenames)
#split filenames in order to sort by dates
    def splitter(filenames):
        for i in range(0,len(filenames)):
            f1[i] = filenames[i].split('_')
            # f1[i][1].split('-')
            # print(f1[i][1])
        return f1

    splitNames= splitter(filenames)


    def dateSorter(splitnames):
        return splitnames[2]
    # def daySorter(splitnames):
    #     return splitnames[2]


    #Sort filenames in dates (ascending)
    filenamesList = sorted(splitNames,key=dateSorter)


    for i in range(0,len(filenamesList)):
        filenames[i] = '{}_{}_{}_{}_{}'.format(filenamesList[i][0],filenamesList[i][1],filenamesList[i][2],filenamesList[i][3],filenamesList[i][4])
        # print(filenames[i])



    indices = []
    # words = ['2018-07-22','2018-09-04']
#find indices of files corresponding to start and end date of the expedition

    # matches = []
    # for c in filenamesList:
    #   if c in words:
    #     indices.append(c)

    # for i, elem in enumerate(filenamesList):
    #     if '2018-07-22' in elem:
    #         indices.append(i)
    #     if '2018-09-04' in elem:
    #         indices.append(i)

    for i, elem in enumerate(filenamesList):
        if '2018-07-22' in elem:
            indices.append(i)
        if '2018-09-04' in elem:
            indices.append(i)
    # print(indices)



    # for i in range(indices[0],indices[-1]):
    #     print(filenames[i])

    # print(indices[-1])
#construct pandas frames from every file in from the expedition
    frames=[None]*(indices[-1]-indices[0])
    for i in range(0,indices[-1]-indices[0]):
        frames[i] = pd.read_csv(filenames[i+indices[0]])
#Concatenate the frames
    expeditionFrame = pd.concat(frames, ignore_index=True)
#To array for further manipulation and plotting of data
    expeditionArr = expeditionFrame.to_numpy()
    return expeditionArr


#######################################################################
#Construct array corresponding to the date of the measurements
#######################################################################


def secondsToDates(weatherArr):
    dateArray = np.zeros((len(weatherArr), 2), int)
    contractedDateArray = list()
    monthStartDays = [22, 1, 1]
    dayCounter = 0  # Is to be subtracted from the amount of days since start of measurements to produce day in month
    monthCounter = 0

    timeArray = []


    for i in range(0,len(weatherArr)):
        if(i==0):
            time = 0
            timeArray.append(time)
            dateArray[i][0]=22
            dateArray[i][1]=7

        else:

            time += weatherArr[i][0] - weatherArr[i - 1][0]
            timeArray.append(time)
            dateArray[i][0] = monthStartDays[monthCounter] + int((timeArray[i] - timeArray[0]) / (60 * 60 * 24)) - dayCounter
            # print(int((timeArray[i] - timeArray[0]) / (60 * 60 * 24)))

            if((i!=0) & (dateArray[i][0]%32==0)):
                dateArray[i][1] = dateArray[i-1][1] +1
                dateArray[i][0] = 1
                monthCounter += 1
                if(monthCounter == 1):
                    dayCounter = 31-22+1 #Number of measurement days in July
                elif(monthCounter ==2 ):
                    dayCounter = 31+10 #Number of measurement days in August

            else:
                dateArray[i][1] = dateArray[i-1][1]

        contractedDateArray.append(str(dateArray[i][0]) + '/' + str(dateArray[i][1]))


        # print(str(dateArray[i][0]) + '/' + str(dateArray[i][1]))

        # indoorTemp.append(weatherArr[i][1])
        # outdoorTemp.append(weatherArr[i][2])
        # pressure.append(weatherArr[i][3])

    return (timeArray, dateArray, contractedDateArray)

def getWeatherData(weatherArr):
    indoorTemp = []
    outdoorTemp = []
    pressure = []
    for i in range(0,len(weatherArr)):
        indoorTemp.append(weatherArr[i][1])
        outdoorTemp.append(weatherArr[i][2])
        pressure.append(weatherArr[i][3])
    return indoorTemp,outdoorTemp,pressure



def getHeaderData(headerArr, headerArrString):
    rawRateArr = []
    longitudeArr = []
    latitudeArr = []
    runtimes = []
    numEvents = []
    # print(type(headerArr))
    meanTime = np.mean(headerArr[:,3])
    sigma = np.std(headerArr[:,4]/headerArr[:,3])
    for i in range(0,len(headerArr)):
        rawRate = (headerArr[i][4])/(headerArr[i][3])
        # print(type(headerArr[i][4]), '  ', type(headerArr[i][3]))
        runtimes.append(float(headerArr[i][3]))
        numEvents.append(float(headerArr[i][4]))
        # print(rawRate)
        # rawRateArr.append(rawRate)
        #Adjust for "wrong" data in POLA1
        if(headerArrString == 'POLA1'):
            if(i<len(headerArr[:,3])-5):
                if(rawRate>100):
                    rawRateArr.append(headerArr[i][4]/2050)
                else:
                    rawRateArr.append(headerArr[i][4]/headerArr[i][3])
            else:
                rawRateArr.append(rawRate)
        else:
            rawRateArr.append(rawRate)



        latitudeArr.append(headerArr[i][19])
        longitudeArr.append(headerArr[i][20])
    print('minimum runtime: ', min(runtimes))
    print('sorted: ', np.sort(rawRateArr)[0:20])

    print('maximum numEvents: ', max(numEvents))
    print('sorted events: ', np.sort(numEvents)[-20:])
    print('Ratio: ', len(rawRateArr)/len(longitudeArr))


    return rawRateArr, longitudeArr, latitudeArr

def linearRegression(x,y):
    regr = linear_model.LinearRegression()

    # x_train,x_test,y_train,y_test = train_test_split(pressure3,rawRate3,test_size=0.2,random_state=4)
    #
    # x = np.arange(0, 20, 1)
    # y = np.arange(0, 40, 2)

    # Train the model using the training sets
    sigma = np.std(y)
    deleteIndices = []
    #delete values that deviate too much
    for i in range(0,len(y)):
        if (abs(y[i])>200):
            deleteIndices.append(i)
    x = np.delete(x, deleteIndices)
    y = np.delete(y, deleteIndices)


    regr.fit(np.array(x).reshape(-1, 1), y)

    # Make predictions using the testing set
    # diabetes_y_pred = regr.predict(diabetes_X_test)

    slope = regr.coef_
    y_intercept = regr.intercept_

    # print('Coefficients: \n', regr.coef_)
    # #
    # print(regr.intercept_)

    x_arr = np.array(x)
    y_fitted = y_intercept + slope * x
    return x_arr,y_fitted,slope,y_intercept
