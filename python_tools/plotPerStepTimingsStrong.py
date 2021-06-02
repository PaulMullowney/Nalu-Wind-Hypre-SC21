#
# This script makes strong scaling plots.
# 
# To run the script, do the following:
#   python plotPerStepTimingsStrong.py PATH_TO DATE PLOTCPU PLOTFY20Q4BASELINE PLOTEAGLE
#
#  Figure 3 : python plotPerStepTimingsStrong.py ../nrel5mw/ 5-28-2021 1 1 0
#  Figure 11 : python plotPerStepTimingsStrong.py ../nrel5mw/ 5-28-2021 0 0 1
#  Figure 8 : python plotPerStepTimingsStrong.py ../nrel5mw2t/ 3-9-2021 1 0 0
#  Figure 9 : python plotPerStepTimingsStrong.py ../nrel5mw_refined/ 3-26-2021 1 0 0

from common import *

path_to =  sys.argv[1]
date = sys.argv[2]
plotCPU = int(sys.argv[3])
plotFY20Q4Baseline = int(sys.argv[4])
plotEagle = int(sys.argv[5])

if (path_to[-1]=='/'):
    sim_name = path_to.split('/')[-2]
else:
    sim_name = path_to.split('/')[-1]

if (sim_name=="nrel5mw"):
    nodes = np.array([2,3,4,5,6,7,8,9,10,11,12,16,20,24])
elif (sim_name=="nrel5mw2t"):
    nodes = np.array([4,6,8,10,16,22,28,34,40,48])
elif (sim_name=="nrel5mw_refined"):
    nodes = np.array([60,90,120,150,180,210,240,300,360,480,600,720])

x = np.array([nodes[0],nodes[-1]])
nlabels=[]
ngpuLabels=[]
for node in nodes:
    nlabels.append(str(node))
    ngpuLabels.append(str(6*node))

dates = ['%s'%date]
gpu_descriptions = ['GPU']
cpu_descriptions = ['CPU']

gpu_strs = ['r*-','r*--','r*:','r*-.']

fig1 = plt.figure(figsize=(10,10))
fig2 = plt.figure(figsize=(10,10))
fig3 = plt.figure(figsize=(10,10))

min1 = 1.e10
min2 = 1.e10
min3 = 1.e10

nGPUs = nodes*6
nCPUs = nodes*6*7

def myround(x, base=5):
    return int(base * np.ceil(float(x)/base))

def getNextPowerUp(x,xerr,base):
    xmax = []
    xmin = []
    for i, (xx, xxerr) in enumerate(zip(x,xerr)):
        xmax.append(np.max(xx+xxerr))
        xmin.append(np.min(xx-xxerr))

    mmin = np.min(xmin)
    mmax = np.max(xmax)
    pmax = myround(mmax,base)
    pmin = myround(mmin,base)
    yticks = np.arange(pmin,pmax,base).astype(np.int32)
    yticklabels = []
    for y in yticks:
        yticklabels.append(str(y))
    return yticks, yticklabels, mmin, mmax

min_total = []
min_nli = []
min_pre = []

total_all = []
total_err_all = []
nli_all = []
nli_err_all = []
pre_all = []
pre_err_all = []


######################################################################
# Hypre GPU
#
mformat=['o','x','d']
lformat=['--','.-']

tot_handles = []
tot_handles = []
for i, Date in enumerate(dates):
    total_gpu, nli_gpu, pre_gpu, nodes_gpu = getTimeStepData(path_to,Date,nodes,nGPUs,'GPUs',sim_name,[])

    total_err_gpu = np.std(total_gpu,axis=1)
    total_gpu = np.mean(total_gpu,axis=1)

    nli_err_gpu = np.std(nli_gpu,axis=1)
    nli_gpu = np.mean(nli_gpu,axis=1)

    pre_err_gpu = np.std(pre_gpu,axis=1)
    pre_gpu = np.mean(pre_gpu,axis=1)

    plt.figure(fig1.number)
    poly_total_gpu = np.polyfit(np.log(nodes), np.log(total_gpu), 1)
    best_gpu = np.exp(poly_total_gpu[1]+poly_total_gpu[0]*np.log(x))
    plt.gca().errorbar(nodes, total_gpu, yerr=total_err_gpu, fmt='r%s'%mformat[i], mfc='r', ms=8, capsize=4, label='%s System 1 (slope=%0.2f)'%(gpu_descriptions[i],poly_total_gpu[0]))
    plt.gca().plot(x,best_gpu,'r%s'%lformat[i])

    plt.figure(fig2.number)
    poly_nli_gpu = np.polyfit(np.log(nodes), np.log(nli_gpu), 1)
    best_gpu = np.exp(poly_nli_gpu[1]+poly_nli_gpu[0]*np.log(x))
    plt.gca().errorbar(nodes, nli_gpu, yerr=nli_err_gpu, fmt='r%s'%mformat[i], mfc='r', ms=8, capsize=4, label='%s System 1 (slope=%0.2f)'%(gpu_descriptions[i],poly_nli_gpu[0]))
    plt.gca().plot(x,best_gpu,'r%s'%lformat[i])

    plt.figure(fig3.number)
    poly_pre_gpu = np.polyfit(np.log(nodes), np.log(pre_gpu), 1)
    best_gpu = np.exp(poly_pre_gpu[1]+poly_pre_gpu[0]*np.log(x))
    plt.gca().errorbar(nodes, pre_gpu, yerr=pre_err_gpu, fmt='r%s'%mformat[i], mfc='r', ms=8, capsize=4, label='%s System 1 (slope=%0.2f)'%(gpu_descriptions[i],poly_pre_gpu[0]))
    plt.gca().plot(x,best_gpu,'r%s'%lformat[i])

    min_total.append(total_gpu[0])
    min_nli.append(nli_gpu[0])
    min_pre.append(pre_gpu[0])

    total_all.append(total_gpu)
    total_err_all.append(total_err_gpu)
    nli_all.append(nli_gpu)
    nli_err_all.append(nli_err_gpu)
    pre_all.append(pre_gpu)
    pre_err_all.append(pre_err_gpu)


######################################################################
# Hypre CPU
#
if (plotCPU):
    for i, Date in enumerate(dates):
        total_cpu, nli_cpu, pre_cpu, nodes_cpu = getTimeStepData(path_to,Date,nodes,nCPUs,'CPUs',sim_name,[])
        
        total_err_cpu = np.std(total_cpu,axis=1)
        total_cpu = np.mean(total_cpu,axis=1)

        nli_err_cpu = np.std(nli_cpu,axis=1)
        nli_cpu = np.mean(nli_cpu,axis=1)
        
        pre_err_cpu = np.std(pre_cpu,axis=1)
        pre_cpu = np.mean(pre_cpu,axis=1)
        
        plt.figure(fig1.number)
        poly_cpu_tot = np.polyfit(np.log(nodes), np.log(total_cpu), 1)
        best_cpu = np.exp(poly_cpu_tot[1]+poly_cpu_tot[0]*np.log(x))
        plt.gca().errorbar(nodes, total_cpu, yerr=total_err_cpu, fmt='b%s'%mformat[i+1], mfc='b', ms=8, capsize=4, label='%s (slope=%0.2f)'%(cpu_descriptions[i],poly_cpu_tot[0]))
        plt.gca().plot(x,best_cpu,'b%s'%lformat[i])
        
        plt.figure(fig2.number)
        poly_cpu_nli = np.polyfit(np.log(nodes), np.log(nli_cpu), 1)
        best_cpu = np.exp(poly_cpu_nli[1]+poly_cpu_nli[0]*np.log(x))
        plt.gca().errorbar(nodes, nli_cpu, yerr=nli_err_cpu, fmt='b%s'%mformat[i+1], mfc='b', ms=8, capsize=4, label='%s (slope=%0.2f)'%(cpu_descriptions[i],poly_cpu_nli[0]))
        plt.gca().plot(x,best_cpu,'b%s'%lformat[i])
        
        plt.figure(fig3.number)
        poly_cpu_pre = np.polyfit(np.log(nodes), np.log(pre_cpu), 1)
        best_cpu = np.exp(poly_cpu_pre[1]+poly_cpu_pre[0]*np.log(x))
        plt.gca().errorbar(nodes, pre_cpu, yerr=pre_err_cpu, fmt='b%s'%mformat[i+1], mfc='b', ms=8, capsize=4, label='%s (slope=%0.2f)'%(cpu_descriptions[i],poly_cpu_pre[0]))
        plt.gca().plot(x,best_cpu,'b%s'%lformat[i])

        min_total.append(total_cpu[0])
        min_nli.append(nli_cpu[0])
        min_pre.append(pre_cpu[0])

        total_all.append(total_cpu)
        total_err_all.append(total_err_cpu)
        nli_all.append(nli_cpu)
        nli_err_all.append(nli_err_cpu)
        pre_all.append(pre_cpu)
        pre_err_all.append(pre_err_cpu)


if (plotFY20Q4Baseline):
    for i, Date in enumerate(dates):
        PATH_TO = path_to + "/fy20q4baseline/"
        total_gpu, nli_gpu, pre_gpu, nodes_baseline = getTimeStepData(PATH_TO,Date,nodes,nGPUs,'GPUs',sim_name,[])
        nodes_baseline = nodes_baseline/6.

        total_err_gpu = np.std(total_gpu,axis=1)
        total_gpu = np.mean(total_gpu,axis=1)
        
        nli_err_gpu = np.std(nli_gpu,axis=1)
        nli_gpu = np.mean(nli_gpu,axis=1)
        
        pre_err_gpu = np.std(pre_gpu,axis=1)
        pre_gpu = np.mean(pre_gpu,axis=1)

        plt.figure(fig1.number)
        #poly_total_gpu = np.polyfit(np.log(nodes_baseline[2:]), np.log(total_gpu[2:]), 1)
        plt.gca().errorbar(nodes_baseline, total_gpu, yerr=total_err_gpu, fmt='r%s'%mformat[i], mfc='none', ms=8, capsize=4, label='GPU baseline')
        #best_gpu = np.exp(poly_total_gpu[1]+poly_total_gpu[0]*np.log(x))
        #plt.gca().plot(x,best_gpu,'g%s'%lformat[i], label='FY20 %s (slope=%0.2f)'%(gpu_descriptions[i],poly_total_gpu[0]))
        
        plt.figure(fig2.number)
        #poly_nli_gpu = np.polyfit(np.log(nodes_baseline[2:]), np.log(nli_gpu[2:]), 1)
        plt.gca().errorbar(nodes_baseline, nli_gpu, yerr=nli_err_gpu, fmt='r%s'%mformat[i], mfc='none', ms=8, capsize=4, label='GPU baseline')
        #best_gpu = np.exp(poly_nli_gpu[1]+poly_nli_gpu[0]*np.log(x))
        #plt.gca().plot(x,best_gpu,'g%s'%lformat[i], label='FY20 Q4 %s (slope=%0.2f)'%(gpu_descriptions[i],poly_nli_gpu[0]))
        
        plt.figure(fig3.number)
        #poly_pre_gpu = np.polyfit(np.log(nodes_baseline[2:]), np.log(pre_gpu[2:]), 1)
        plt.gca().errorbar(nodes_baseline, pre_gpu, yerr=pre_err_gpu, fmt='r%s'%mformat[i], mfc='none', ms=8, capsize=4, label='GPU baseline')
        #best_gpu = np.exp(poly_pre_gpu[1]+poly_pre_gpu[0]*np.log(x))
        #plt.gca().plot(x,best_gpu,'g%s'%lformat[i], label='FY20 %s (slope=%0.2f)'%(gpu_descriptions[i],poly_pre_gpu[0]))
        
        total_all.append(total_gpu)
        total_err_all.append(total_err_gpu)
        nli_all.append(nli_gpu)
        nli_err_all.append(nli_err_gpu)
        pre_all.append(pre_gpu)
        pre_err_all.append(pre_err_gpu)

if (plotEagle):
    for i, Date in enumerate(dates):
        PATH_TO = path_to + "/timings_eagle/"
        nodes_eagle = np.array([2,3,4,5,6,7,8,10,12])
        nGPUs_eagle = nodes_eagle*6

        total_gpu, nli_gpu, pre_gpu, nodes_eagle = getTimeStepData(PATH_TO,Date,nodes_eagle,nGPUs_eagle,'GPUs',sim_name,[])
        nodes_eagle = nodes_eagle/6.

        total_err_gpu = np.std(total_gpu,axis=1)
        total_gpu = np.mean(total_gpu,axis=1)
        
        nli_err_gpu = np.std(nli_gpu,axis=1)
        nli_gpu = np.mean(nli_gpu,axis=1)
        
        pre_err_gpu = np.std(pre_gpu,axis=1)
        pre_gpu = np.mean(pre_gpu,axis=1)

        plt.figure(fig1.number)
        poly_total_gpu = np.polyfit(np.log(nodes_eagle), np.log(total_gpu), 1)
        best_gpu = np.exp(poly_total_gpu[1]+poly_total_gpu[0]*np.log(x))
        plt.gca().errorbar(nodes_eagle, total_gpu, yerr=total_err_gpu, fmt='gs', mfc='none', ms=8, capsize=4, label='GPU System 2 (slope=%0.2f)'%(poly_total_gpu[0]))
        plt.gca().plot(x,best_gpu,'g%s'%lformat[i])
        
        plt.figure(fig2.number)
        poly_nli_gpu = np.polyfit(np.log(nodes_eagle), np.log(nli_gpu), 1)
        plt.gca().errorbar(nodes_eagle, nli_gpu, yerr=nli_err_gpu, fmt='gs', mfc='none', ms=8, capsize=4, label='GPU System 2 (slope=%0.2f)'%(poly_nli_gpu[0]))
        best_gpu = np.exp(poly_nli_gpu[1]+poly_nli_gpu[0]*np.log(x))
        plt.gca().plot(x,best_gpu,'g%s'%lformat[i])
        
        plt.figure(fig3.number)
        poly_pre_gpu = np.polyfit(np.log(nodes_eagle), np.log(pre_gpu), 1)
        plt.gca().errorbar(nodes_eagle, pre_gpu, yerr=pre_err_gpu, fmt='gs', mfc='none', ms=8, capsize=4, label='GPU Eagle (slope=%0.2f)'%(poly_pre_gpu[0]))
        best_gpu = np.exp(poly_pre_gpu[1]+poly_pre_gpu[0]*np.log(x))
        plt.gca().plot(x,best_gpu,'g%s'%lformat[i])

######################################################################
# Save files
#
min1 = np.mean(min_total)
min2 = np.mean(min_nli)
min3 = np.mean(min_pre)

# Total
yticks, yticklabels, yaxismin, yaxismax = getNextPowerUp(total_all,total_err_all,5)
plt.figure(fig1.number)
plt.gca().plot(x,np.array([min1,min1/(nodes[-1]/nodes[0])]),'k--', label="Perfect Scaling")
plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.ylabel("Average time per time step (seconds)")
handles, labels = plt.gca().get_legend_handles_labels()
if (plotEagle):
    plt.xlabel("Number of V100 GPUs")
    plt.xticks(nodes,labels=ngpuLabels)
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
elif (plotCPU and plotFY20Q4Baseline):
    handles = [handles[1], handles[3], handles[2], handles[0]]
    labels = [labels[1], labels[3], labels[2], labels[0]]
elif (plotCPU):
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
plt.legend(handles,labels)
plt.xlim((nodes[0]-.1,nodes[-1]+1))
plt.ylim((yaxismin,yaxismax))
plt.grid()
plt.gca().minorticks_off()
if (plotEagle):
    plt.xlabel("Number of V100 GPUs")
    plt.xticks(nodes,labels=ngpuLabels)
else:
    plt.xlabel("Summit: Number of Power9/V100 Nodes")
    plt.xticks(nodes,labels=nlabels)
plt.yticks(yticks,labels=yticklabels)
if (plotEagle):
    plt.savefig("%s_Strong_PerStep_timings_Total_%s_SummitVsEagle.png"%(sim_name,date),bbox_inches='tight')
else:
    plt.savefig("%s_Strong_PerStep_timings_Total_%s.png"%(sim_name,date),bbox_inches='tight')

# NLI
yticks, yticklabels, yaxismin, yaxismax = getNextPowerUp(nli_all,nli_err_all,5)
plt.figure(fig2.number)
plt.gca().plot(x,np.array([min2,min2/(nodes[-1]/nodes[0])]),'k--', label="Perfect Scaling")
plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.ylabel("Average time per time step (seconds)")
handles, labels = plt.gca().get_legend_handles_labels()
if (plotEagle):
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
elif (plotCPU and plotFY20Q4Baseline):
    handles = [handles[1], handles[3], handles[2], handles[0]]
    labels = [labels[1], labels[3], labels[2], labels[0]]
elif (plotCPU):
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
plt.legend(handles,labels)
plt.xlim((nodes[0]-.1,nodes[-1]+1))
plt.ylim((4,yaxismax))
plt.grid()
plt.gca().minorticks_off()
if (plotEagle):
    plt.xlabel("Number of V100 GPUs")
    plt.xticks(nodes,labels=ngpuLabels)
else:
    plt.xlabel("Summit: Number of Power9/V100 Nodes")
    plt.xticks(nodes,labels=nlabels)
plt.yticks(yticks,labels=yticklabels)
if (plotEagle):
    plt.savefig("%s_Strong_PerStep_timings_NLI_%s_SummitVsEagle.png"%(sim_name,date),bbox_inches='tight')
else:
    plt.savefig("%s_Strong_PerStep_timings_NLI_%s.png"%(sim_name,date),bbox_inches='tight')

# PRE
yticks, yticklabels, yaxismin, yaxismax = getNextPowerUp(pre_all,pre_err_all,10)
plt.figure(fig3.number)
plt.gca().plot(x,np.array([min3,min3/(nodes[-1]/nodes[0])]),'k--', label="Perfect Scaling")
plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.ylabel("Average time per time step (seconds)")
handles, labels = plt.gca().get_legend_handles_labels()
if (plotEagle):
    plt.xlabel("Number of V100 GPUs")
    plt.xticks(nodes,labels=ngpuLabels)
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
elif (plotCPU and plotFY20Q4Baseline):
    handles = [handles[1], handles[3], handles[2], handles[0]]
    labels = [labels[1], labels[3], labels[2], labels[0]]
elif (plotCPU):
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
plt.legend(handles,labels)
plt.xlim((nodes[0]-.1,nodes[-1]+1))
plt.ylim((yaxismin,yaxismax))
plt.grid()
plt.gca().minorticks_off() 
if (plotEagle):
    plt.xlabel("Number of V100 GPUs")
    plt.xticks(nodes,labels=ngpuLabels)
else:
    plt.xlabel("Summit: Number of Power9/V100 Nodes")
    plt.xticks(nodes,labels=nlabels)
plt.yticks(yticks,labels=yticklabels)
if (plotEagle):
    plt.savefig("%s_Strong_PerStep_timings_PRE_%s_SummitVsEagle.png"%(sim_name,date),bbox_inches='tight')
else:
    plt.savefig("%s_Strong_PerStep_timings_PRE_%s.png"%(sim_name,date),bbox_inches='tight')
