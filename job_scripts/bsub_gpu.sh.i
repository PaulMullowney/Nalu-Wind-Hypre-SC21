#!/bin/bash
# Begin LSF Directives
#BSUB -P CFD116
#BSUB -W 1:00
#BSUB -nnodes %NODES%
#BSUB -J nrel5mw_gpu_%CORES%

export CUDA_LAUNCH_BLOCKING=1
export HDF5_DISABLE_VERSION_CHECK=1

ranks=%CORES%
name=${ranks}GPUs

module load DefApps
module load cuda/10.2.89
module load gcc/7.4.0
module load spectrum-mpi/10.3.1.2-20200121

#
# Tried these but saw no benefit
#
#export PAMI_IBV_ADAPTER_AFFINITY=1
#export PAMI_IBV_DEVICE_NAME=mlx5_0:1,mlx5_3:1
#export PAMI_IBV_DEVICE_NAME_1=mlx5_3:1,mlx5_0:1
#export PAMI_ENABLE_STRIPING=1

#jsrun -n ${ranks} /PATH/TO/TRILINOS/INSTALL/bin/stk_balance.exe /PATH/TO/MESH/nrel5mw.exo --decomp-method=parmetis --output-directory temp_exo/

date=$(date +%Y-%m-%d)
nalu=/PATH/TO/NALU/GPU/BUILD/naluX
/sw/summit/xalt/1.2.1/bin/jsrun --smpiargs="-gpu" -n ${ranks} -a 1 -c 1 -g 1 ${nalu} -i nrel5mw_rcb.yaml -o timings_${date}/nrel5mw_rcb_${name}.log
mv *EQS_decomp_${ranks}GPUs.txt timings_${date}

