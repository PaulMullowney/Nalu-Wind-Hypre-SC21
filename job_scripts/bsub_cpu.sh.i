#!/bin/bash
# Begin LSF Directives
#BSUB -P CFD116
#BSUB -W 2:00
#BSUB -nnodes %NODES%
#BSUB -J nrel5mw_cpu_%CORES%

export CUDA_LAUNCH_BLOCKING=1
export HDF5_DISABLE_VERSION_CHECK=1

ranks=%CORES%
name=${ranks}CPUs

module load DefApps
module load cuda/10.2.89
module load gcc/7.4.0
module load spectrum-mpi/10.3.1.2-20200121

#jsrun -n ${ranks} /PATH/TO/TRILINOS/INSTALL/bin/stk_balance.exe /PATH/TO/MESH/nrel5mw.exo --decomp-method=parmetis --output-directory temp_exo/

date=$(date +%Y-%m-%d)
nalu=/PATH/TO/NALU/CPU/BUILD/naluX
/sw/summit/xalt/1.2.1/bin/jsrun -n ${ranks} ${nalu} -i nrel5mw_rcb.yaml -o timings_${date}/nrel5mw_rcb_${name}.log
mv *EQS_decomp*txt timings_${date}
