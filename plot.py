import numpy as np
import matplotlib.pyplot as plt
import pylab
from datetime import datetime
import matplotlib.gridspec as gridspec
import glob
import os, sys

os.chdir(r'/home/pi/enviro/data')
dataFiles = glob.glob('*.txt')
numberDataFiles = len(dataFiles)
print("\nWhat data would you like to look at? \n")
for (i, item) in enumerate(dataFiles, start=1):
    print i, item
while True:
    try:
        dataChoice = int(raw_input(": "))
        if dataChoice > numberDataFiles or dataChoice < 1:
            print("\nWoops! Enter one of the numbers given: ")
        else:
            print("\nCreating axis...")
            break
    except ValueError:
        print("\nWoops! Enter one of the numbers given: ")

myfile = open(dataFiles[dataChoice-1],"rt")
contents = myfile.readlines()

# The last line of the data is removed to account for abrupt shutdown
# of the device
contents = contents[:-1]

#print(contents)

time = []
light = []
temp = []
pressure = []
humid = []
carbmon = []
nitrox = []
ammonia = []
smallpm = []
mediumpm = []
largepm = []

for line in contents:
    timedummy = line.split('\t')[0]
    timedummy = timedummy[:-7]
    x = datetime.strptime(timedummy, '%Y-%m-%d %H:%M:%S')
    time.append(x)

    light.append(float(line.split('\t')[1]))
#    print(light)
    temp.append(float(line.split('\t')[2]))
    pressure.append(float(line.split('\t')[3]))
    humid.append(float(line.split('\t')[4]))

#Due to CO and NH3 being inverted, the reciprocal is plotted
    carbmon.append(1000000/float(line.split('\t')[5]))
    nitrox.append(float(line.split('\t')[6])/1000)
    ammonia.append(1000000/float(line.split('\t')[7]))

    smallpm.append(float(line.split('\t')[8]))
    mediumpm.append(float(line.split('\t')[9]))
    largepm.append(float(line.split('\t')[10]))

del time[0]
del light[0]
del temp[0]
del pressure[0]
del humid[0]
del carbmon[0]
del nitrox[0]
del ammonia[0]
del smallpm[0]
del mediumpm[0]
del largepm[0]

myfile.close()

allData = [time,light,temp,pressure,humid,carbmon,nitrox,ammonia,smallpm,mediumpm,largepm]
allYLabels = ["s","Lumens","deg. C","Pressure","Humidity","CO","NO2","NH3","pm1.0","pm2.5","pm10.0"]
# create a system where the user chooses what to see, and plots appear live

fig = plt.figure()
plt.xlabel("Time (day, hour:min)")
# To avoid the axes error...
#warnings.warn(message, mplDeprecation, stacklevel=1)

plt.ion()
plt.show()

plotNumber = []

while True:
#    ask the user to give a number linking to a paricular type of data
    data1 = raw_input("\nWhat would you like to look at?\n1: Light levels\n2: Temperature\n3: Pressure \
    \n4: Humidity\n5: Carbon Monoxide\n6: Nitrous Oxide\n7: Ammonia\n8: PM 1.0\n9: PM 2.5\n10: PM 10.0 \
    \n________\n11: I'm done\n\nEnter number here: ")
    try:
        plotNumber.append(int(data1))
        
        if int(data1) == 11:
            break
        elif int(data1) > 11 or int(data1)<1:
            print("\nWoops! Enter a number between 1 and 11")
            plotNumber.pop(-1) 
        else:    
    #        plt.plot(time,allData[int(data1)])
            print("Plotting data...")
            for i in range(len(plotNumber)):            
                plt.subplot(len(plotNumber),1,i+1)
                plt.ylabel(allYLabels[plotNumber[i]])
                plt.plot(time,allData[plotNumber[i]])
        plt.pause(1)
    except ValueError:
        print("\nWoops! Enter a number between 1 and 11")
        plt.pause(1)
