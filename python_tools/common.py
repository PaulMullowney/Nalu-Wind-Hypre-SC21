import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import os
import sys
import warnings
import string
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')

SMALL_SIZE = 16
MEDIUM_SIZE = 19
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


######################################################################
# Get Data from files
#
def getEquationData(path_to,Date,nodes,nDevs,name,sim_name,filenames,strong,equation_name):
    y1 = np.array([])
    y2 = np.array([])
    y3 = np.array([])
    y4 = np.array([])
    y5 = np.array([])
    y6 = np.array([])
    y7 = np.array([])
    if (strong):
        if (not filenames):
            for node,nDev in zip(nodes,nDevs):
                f = path_to + "timings_"+Date+"/"+sim_name+"_" + str(nDev) + name + ".log"
                filenames.append(f)
    else:
        if (not filenames):
            for node,nDev in zip(nodes,nDevs):
                if (node==1):
                    f = path_to + 'timings_'+Date+'/abl40m_'+str(node)+'_'+str(nDev)+name+'-HypreReuse.log'
                elif (node==4):
                    f = path_to + 'timings_'+Date+'/abl20m_'+str(node)+'_'+str(nDev)+name+'-HypreReuse.log'
                elif (node==32):
                    f = path_to + 'timings_'+Date+'/abl10m_'+str(node)+'_'+str(nDev)+name+'-HypreReuse.log'
                elif (node==256):
                    f = path_to + 'timings_'+Date+'/abl05m_'+str(node)+'_'+str(nDev)+name+'-HypreReuse.log'
                filenames.append(f)

    for (nDev, f) in zip(nDevs,filenames):
        if (os.path.isfile(f)):
            init, assem, load_complete, solve, precon, misc, norm, linIters, pre, nli, post, tot, timesteps = readLogFile(f,equation_name)
            y1 = np.append(y1,precon)
            y2 = np.append(y2,solve)
            y3 = np.append(y3,assem)
            y4 = np.append(y4,load_complete)
            y5 = np.append(y5,init)
            y6 = np.append(y6,misc)
            y7 = np.append(y7,init+assem+load_complete+solve+precon+misc)
            print(equation_name, " ",nDev," "+name+" : solve dt=",solve, " assemble dt=(", init, assem, load_complete, ") precon setup dt=",precon," total dt=",y7[-1]," linear iterations=",linIters)

    y1 = y1/float(timesteps)
    y2 = y2/float(timesteps)
    y3 = y3/float(timesteps)
    y4 = y4/float(timesteps)
    y5 = y5/float(timesteps)
    y6 = y6/float(timesteps)
    y7 = y7/float(timesteps)
    return y1, y2, y3, y4, y5, y6, y7


######################################################################
# Get Data from files
#
def getTimeStepData(path_to,Date,nodes,nDevs,name,sim_name,filenames,strong=True):
    y1 = np.array([])
    y2 = np.array([])
    y3 = np.array([])
    y4 = np.array([])
    if (not filenames):
        for node,nDev in zip(nodes,nDevs):
            if (path_to.find("fy20q4baseline")>=0 or path_to.find("eagle")>=0):
                f = path_to + "/" + sim_name + "_" + str(nDev) + name + ".log"
            else:
                f = path_to + "timings_"+Date+"/" + sim_name + "_" + str(nDev) + name + ".log"
            filenames.append(f)

    for (nDev, f) in zip(nDevs,filenames):
        if (os.path.isfile(f)):
            init, assem, load_complete, solve, precon, misc, norm, linIters, pre, nli, post, tot, timesteps = readLogFile(f,'')
            tot = np.expand_dims(tot,axis=0)
            nli = np.expand_dims(nli,axis=0)
            pre = np.expand_dims(pre,axis=0)
            if (y1.size==0):
                y1 = tot
                y2 = nli
                y3 = pre
            else:
                y1 = np.vstack((y1,tot))
                y2 = np.vstack((y2,nli))
                y3 = np.vstack((y3,pre))
            y4 = np.append(y4,nDev)
            print(nDev," "+name+" Average Pre=",np.mean(pre)," NLI=",np.mean(nli), " Post=",np.mean(post), " Total=",np.mean(tot))
        else:
            print(f)

    return y1, y2, y3, y4


def readLogFile(f,equation_name):
    count = 0
    found = False
    init = np.NaN
    assem = np.NaN
    lc = np.NaN
    solve = np.NaN
    precon = np.NaN
    misc = np.NaN
    norm = np.NaN
    linIters = np.NaN
    pre=[]
    nli=[]
    post=[]
    total=[]
    timesteps = 0
    with open(f) as fp: 
        for line in fp: 
            count += 1
            line = line.strip()

            if (line.find("WallClockTime")>=0):
                timesteps = timesteps + 1
                index1 = line.find(": ")
                line = line[index1+2:]
                crap = line.split(" ")
                pre.append(float(crap[2]))
                nli.append(float(crap[4]))
                post.append(float(crap[6]))
                total.append(float(crap[8]))
                #index1 = line.find(" ")
                #norm = float(line[:index1])
                #print("Line{}: Mean System Norm={}".format(count,norm))
                continue

            if (line.find("Mean System Norm")>=0):
                index1 = line.find(": ")
                line = line[index1+2:]
                index1 = line.find(" ")
                norm = float(line[:index1])
                #print("Line{}: Mean System Norm={}".format(count,norm))
                continue

            if (line.find("Timing for IO")>=0):
                found = False
                continue
            if (line.find("Timing for Eq: %s"%equation_name)>=0 and found==False):
                found = True
            elif (line.find("Timing for Eq:")<0 and found==True):
                if (line.find("init")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    init = float(line[index1+4:index2])
                elif (line.find("assemble")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    assem = float(line[index1+4:index2])
                elif (line.find("load_complete")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    lc = float(line[index1+4:index2])
                elif (line.find("solve")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    solve = float(line[index1+4:index2])
                elif (line.find("precond setup")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    precon = float(line[index1+4:index2])
                elif (line.find("misc")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    misc = float(line[index1+4:index2])
                elif (line.find("linear iterations")>=0):
                    index1 = line.find("avg:")
                    index2 = line.find("min:")
                    linIters = float(line[index1+4:index2])
            else:
                found=False
    return init, assem, lc, solve, precon, misc, norm, linIters, np.array(pre), np.array(nli), np.array(post), np.array(total), timesteps
