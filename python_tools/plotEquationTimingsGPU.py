#
# This script makes a stacked bar chart of equation timing breakdowns. This script makes the following assumptions
# 
# To run the script, do the following:
#   python plotEquationTimingsGPU.py PATH_TO EQUATION_NAME DATE Y_AXIS_MAX USELOGLOG PLOTCPURESULTS (1==CPU, 0==GPU)
#
#  python plotEquationTimingsGPU.py ../nrel5mw/ ContinuityEQS 5-28-2021 30 0 1
#  python plotEquationTimingsGPU.py ../nrel5mw/ ContinuityEQS 5-28-2021 30 0 0
#  python plotEquationTimingsGPU.py ../nrel5mw2t/ ContinuityEQS 3-9-2021 30 0 1
#  python plotEquationTimingsGPU.py ../nrel5mw2t/ ContinuityEQS 3-9-2021 30 0 0
#  python plotEquationTimingsGPU.py ../nrel5mw_refined/ ContinuityEQS 3-26-2021 30 0 0
#  python plotEquationTimingsGPU.py ../nrel5mw_refined/ ContinuityEQS 3-26-2021 30 0 1
#

from common import *

path_to =  sys.argv[1]
equation_name = sys.argv[2]
date = sys.argv[3]
yaxismax = int(sys.argv[4])
loglog = int(sys.argv[5])
plotCPU = int(sys.argv[6])

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

print(nodes)

nlabels=[]
for node in nodes:
    nlabels.append(str(node))

nGPUs = 6*np.array(nodes)
nCPUs = 7*nGPUs


if (plotCPU):
    y1, y2, y3, y4, y5, y6, y7 = getEquationData(path_to,date,nodes,nCPUs,'CPUs',sim_name,[],1,equation_name)
else:
    y1, y2, y3, y4, y5, y6, y7 = getEquationData(path_to,date,nodes,nGPUs,'GPUs',sim_name,[],1,equation_name)

fig = plt.figure(figsize=(10,10))

if (sim_name=="nrel5mw"):
    NODES = nodes
elif (sim_name=="nrel5mw2t"):
    NODES = (nodes/2).astype(np.int32)
elif (sim_name=="nrel5mw_refined"):
    NODES = (nodes/30).astype(np.int32)

print(NODES)
plt.bar(NODES, y1, bottom=0, width=.8, label="Hypre Precon Setup")
plt.bar(NODES, y2, bottom=y1, width=.8, label="Hypre GMRES Solve")
plt.bar(NODES, y3, bottom=y1+y2,  width=.8, label="Nalu-Wind Assemble")
plt.bar(NODES, y4, bottom=y1+y2+y3, width=.8, label="Hypre Assemble")
plt.bar(NODES, y5+y6, bottom=y1+y2+y3+y4, width=.8, label="Nalu-Wind Other")
        
ax = plt.gca()
if (loglog):
    ax.set_xscale("log")
    ax.set_yscale("log")
plt.ylim((0,yaxismax))
plt.grid()
plt.legend()

plt.ylabel("Average time per timestep (seconds)")
plt.xlabel("Summit: Number of Power9/V100 Nodes")
plt.xticks(NODES,labels=nlabels)
#plt.xticks([2,3,4,6,8,10,12,16,20,24],labels=["2","3","4","6","8","10","12","16","20","24"])
if (plotCPU):
    plt.savefig("%s_HypreCPU_Strong_%s_timings_%s.png"%(sim_name,equation_name,date),bbox_inches='tight')
else:
    plt.savefig("%s_HypreGPU_Strong_%s_timings_%s.png"%(sim_name,equation_name,date),bbox_inches='tight')
