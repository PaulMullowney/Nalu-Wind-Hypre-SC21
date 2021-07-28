# Nalu-Wind-Hypre-SC21
This repository stores key information regarding the compute artifacts for the Nalu-Wind/Hypre SC21 paper submission. Reproducing the paper results assumes that you have gained access to the CFD116 project on ORNL Summit. These instructions will NOT work if that has not occured. Contact Paul Mullowney (pmullown@nrel.gov) for help regarding the information in this wiki or getting access to CFD116.

# Contents
- [Machine Characterization](#machine-characterization)
- [Building Software](#building-software)
  - [Trilinos](#trilinos)
  - [Hypre](#hypre)
  - [Nalu-Wind](#nalu-wind)
- [Input Files](#input-files)
- [Job Scripts](#job-scripts)
- [Python Tools](#python-tools)
  - [Plot Generation](#plot-generation)
- [Meshes](#meshes)

# Machine Characterization

Results from the [the SC Tech Program Author Kit](https://github.com/SC-Tech-Program/Author-Kit):

- [NREL Eagle compute node description](eagle-system.txt), more details at the [website](https://www.nrel.gov/hpc/eagle-system-configuration.html)
- [ORNL Summit compute node description](summit-system.txt), more details at the [website](https://docs.olcf.ornl.gov/systems/summit_user_guide.html#summit-documentation-resources)


# Building Software

### Trilinos
 - git clone git@github.com:trilinos/Trilinos.git
 - cd Trilinos
 - git checkout 937c9ae018b
   We're gonna use the checkpoint associated with generating our results.

##### CPU
 - mkdir build_cpu
 - copy the files from  - [Trilinos CPU Build Scripts](trilinos-build-scripts/cpu/) into build_cpu
 - cd build_cpu
 - in trilinos-gcc.sh, you will need to edit the line below to be your desired location

   TRILINOS_INSTALL_PREFIX=/PATH/TO/CPU/INSTALL/trilinos-master-$(date +%Y-%m-%d)
   

 - ./trilinos-gcc.sh cmake_full -DTPL_ENABLE_ParMETIS=ON
 - ./trilinos-gcc.sh make -j4 (or -j42 if on an interactive shell)
 - ./trilinos-gcc.sh make install

##### GPU
 - mkdir build_gpu
 - copy the files from  - [Trilinos GPU Build Scripts](trilinos-build-scripts/gpu/) into build_gpu
 - cd build_gpu
 - in trilinos-gcc.sh, you will need to edit the line below to be your desired location

   TRILINOS_INSTALL_PREFIX=/PATH/TO/GPU/INSTALL/trilinos-master-$(date +%Y-%m-%d)

 - ./trilinos-gcc.sh cmake_full
 - ./trilinos-gcc.sh make -j4 (or -j42 if on an interactive shell)
 - ./trilinos-gcc.sh make install
 
Note, it is not necessary to enable ParMETIS with the GPU build since we will be using stk_balance.exe outside of our Nalu-Wind simulations,
i.e. we can use the CPU build of stk_balance.exe to repartition meshes. See the section on [Meshes](#meshes) below for more detail.

### Hypre
 - wget https://zenodo.org/record/4899892/files/PaulMullowney/hypre-v1.0.0.zip
 - Follow the instructions on the README to build Hypre
 - Modify the generic paths in the configure line appropriately
 - To do a CPU build, set --without-cuda or remove all cuda-related flags from the configure line

### Nalu-Wind
 - wget https://zenodo.org/record/4899910/files/PaulMullowney/nalu-wind-v1.0.0.zip

##### CPU
 - mkdir build_cpu
 - copy the files from  - [Nalu-Wind CPU Build Scripts](nalu-wind-build-scripts/cpu/) into build_cpu
 - cd build_cpu
 - you will need to edit 2 variables in exawind-config.sh to point to your CPU installation directories of Trilinos and Hypre

   HYPRE_ROOT_DIR=/PATH/TO/HYPRE/CPU/INSTALL

   TRILINOS_ROOT_DIR=/PATH/TO/TRILINOS/CPU/INSTALL

 - ./nalu-wind-gcc.sh cmake_full
 - ./nalu-wind-gcc.sh make -j4 (or -j42 if on an interactive shell)

Once finished, this directory will have the CPU naluX executable. In the scripts that follow, change all instances of
/PATH/TO/NALU/CPU/BUILD/naluX to this path.

##### GPU
 - mkdir build_gpu
 - copy the files from  - [Nalu-Wind GPU Build Scripts](nalu-wind-build-scripts/gpu/) into build_gpu
 - cd build_gpu
 - you will need to edit 2 variables in exawind-config.sh to point to your GPU installation directories of Trilinos and Hypre

   HYPRE_ROOT_DIR=/PATH/TO/HYPRE/GPU/INSTALL

   TRILINOS_ROOT_DIR=/PATH/TO/TRILINOS/GPU/INSTALL 

 - ./nalu-wind-gcc.sh cmake_full
 - ./nalu-wind-gcc.sh make -j4 (or -j42 if on an interactive shell)

Once finished, this directory will have the GPU naluX executable. In the scripts that follow, change all instances of
/PATH/TO/NALU/GPU/BUILD/naluX to this path.


# Input Files

RCB and ParMETIS input files are listed for the three turbine meshes. For each of the ParMETIS versions listed, Nalu-Wind requires that Trilinos be built with ParMETIS and that stk_balance.exe tool is executed, as described in the [Meshes](#meshes) section below.

### NREL 5 MW : Low Resolution, Single Turbine

The input files can be found at:
- [Input File with RCB decompositions](nrel5mw/nrel5mw_rcb.yaml)
- [Input File with ParMETIS decompositions](nrel5mw/nrel5mw.yaml)

### NREL 5 MW : Low Resolution, Dual Turbine

The input files can be found at:
- [Input File with RCB decompositions](nrel5mw2t/nrel5mw2t_rcb.yaml)
- [Input File with ParMETIS decompositions](nrel5mw2t/nrel5mw2t.yaml)

### NREL 5 MW : High Resolution, Single Turbine

The input files can be found at:
- [Input File with RCB decompositions](nrel5mw_refined/nrel5mw_refined_rcb.yaml)
- [Input File with ParMETIS decompositions](nrel5mw_refined/nrel5mw_refined.yaml)


# Job Scripts

Sample job scripts for the low resolution, single turbine mesh with RCB Decomposition are given at:
- CPU : [Single Job Template](job_scripts/bsub_cpu.sh.i), [All Jobs Strong Scaling](job_scripts/script_cpu.sh)
- GPU : [Single Job Template](job_scripts/bsub_gpu.sh.i), [All Jobs Strong Scaling](job_scripts/script_gpu.sh)

The templates must be modified to point to your Nalu-Wind build, i.e. "/PATH/TO/NALU/CPU/BUILD/naluX" and "/PATH/TO/NALU/GPU/BUILD/naluX" must be modified appropriately.

If ParMETIS decompositions are desired, one must follow the instructions in [Meshes](#meshes). The paths must be appropriately adjusted.
In addition, the jsrun command in the templates must be adjust to:

/sw/summit/xalt/1.2.1/bin/jsrun --smpiargs="-gpu" -n ${ranks} -a 1 -c 1 -g 1 ${nalu} -i nrel5mw.yaml -o timings_${date}/nrel5mw_${name}.log

These job scripts can be adjusted appropriately for the dual turbine and high resolution, single turbine cases. 


# Python Tools

Python tools for generating the plots in the submitted paper have also been added. The necessary python packages are listed in [requirements](python_tools/requirements.txt).
We've also added the output of our runs, used to generate the plots, in:

### NREL 5 MW : Low Resolution, Single Turbine

 - [Summit](nrel5mw/timings_5-28-2021/)
 - [Summit F420Q4 Baseline](nrel5mw/fy20q4baseline/)
 - [Eagle](nrel5mw/timings_eagle/)

### NREL 5 MW : Low Resolution, Dual Turbine

 - [Summit](nrel5mw2t/timings_3-9-2021/)

### NREL 5 MW : High Resolution, Single Turbine

 - [Summit](nrel5mw_refined/timings_3-26-2021/)

### Plot Generation

The tools assume that results are stored in directories of form /PATH/TO/timings_DATE/, i.e. ../nrel5mw/timings_5-28-2021/.
Strong scaling figures can be generated by going into the python_tools subdir and doing:
 - Figure 3 : python plotPerStepTimingsStrong.py ../nrel5mw/ 5-28-2021 1 1 0
 - Figure 11 : python plotPerStepTimingsStrong.py ../nrel5mw/ 5-28-2021 0 0 1
 - Figure 8 : python plotPerStepTimingsStrong.py ../nrel5mw2t/ 3-9-2021 1 0 0
 - Figure 9 : python plotPerStepTimingsStrong.py ../nrel5mw_refined/ 3-26-2021 1 0 0

Per equation breakdowns can be generated by doing:
 - Figure 6 :  python plotEquationTimingsGPU.py ../nrel5mw/ ContinuityEQS 5-28-2021 30 0 1
 - Figure 7 :  python plotEquationTimingsGPU.py ../nrel5mw/ ContinuityEQS 5-28-2021 30 0 0

One could swap ContinuityEQS with MomentumEQS, TurbKineticEnergyEQS, or SpecDissRateEQS to generate plots for the other
equation systems. One could also use these scripts to plot the per equation breakdowns for the dual turbine or the refined model.


# Meshes

Exodus files for the meshes for various computational results are stored on Summit in the /hpss/prod/cfd116/proj-shared/ directory. 

- Low Resolution, Single Turbine : /hpss/prod/cfd116/proj-shared/nrel5mw/nrel5mw.exo
- Low Resolution, Dual Turbine : /hpss/prod/cfd116/proj-shared/nrel5mw2t/nrel5mw2t.exo
- High Resolution, Single Turbine : /hpss/prod/cfd116/proj-shared/nrel5mw_refined/nrel5mw_refined.exo

These files can be retrieved using the [hsi](https://docs.olcf.ornl.gov/data/archiving.html#using-hsi) interface.
The exodus files can be used directly within a Nalu-Wind simulation using RCB domain decomposition. Or, one can rebalance the low resolution, single turbine mesh using Trilinos tools via:

 - jsrun -n ${ranks} /PATH/TO/TRILINOS/INSTALL/bin/stk_balance.exe /PATH/TO/MESH/nrel5mw.exo --decomp-method=parmetis --output-directory /PATH/TO/MESH/temp_exo/

It is sufficient to use the CPU build of Trilinos with ParMETIS to repartition the meshes for GPU runs.
See the instructions above for building Trilinos or [website](https://trilinos.github.io/) for more details.

