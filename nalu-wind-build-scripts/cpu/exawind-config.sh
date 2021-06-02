#!/bin/bash
#
# Exawind-builder configuration file.
# Generated by bootstrap script at 2020-02-08 18:12:53 EST
# Documentation available at https://exawind-builder.readthedocs.io/en/latest/index.html
EXAWIND_NUM_JOBS=36
SPACK_ROOT=${EXAWIND_PROJECT_DIR}/spack
SPACK_COMPILER=${SPACK_COMPILER:-${EXAWIND_COMPILER}}

EXAWIND_MAKE_TYPE=ninja
export PATH=/ccs/proj/cfd116/shreyas/summit/exawind/source/ninja:${PATH}

EXAWIND_MODMAP[netcdf]=netcdf-c

BUILD_TYPE=RELEASE     # [RELEASE, DEBUG, RELWITHDEBINFO]
ENABLE_OPENMP=OFF      # [ON, OFF]
ENABLE_CUDA=OFF

ENABLE_OPENFAST=OFF    # Enable OpenFAST TPL with Nalu-Wind
ENABLE_TIOGA=ON        # Enable TIOGA for overset connectivity
ENABLE_HYPRE=ON        # Enable HYPRE linear solvers with Nalu-Wind
ENABLE_FFTW=OFF        # Enable FFTW for ABL simulations

ENABLE_BIGINT=OFF

HYPRE_ROOT_DIR=/PATH/TO/HYPRE/CPU/INSTALL
TRILINOS_ROOT_DIR=/PATH/TO/TRILINOS/CPU/INSTALL
EXAWIND_MODMAP[cuda]=cuda/10.2.89