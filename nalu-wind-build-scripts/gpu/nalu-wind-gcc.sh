#!/bin/bash
#
# ExaWind build script for project: nalu-wind
#
# Autogenerated for ornl-summit and gcc
#
# 1. See https://exawind-builder.readthedocs.io for documentation
# 2. Use new-script.sh to regenerate this script
#

#
# Setup variables used by functions
#
export EXAWIND_SRCDIR=/ccs/proj/cfd116/shreyas/summit/exawind-2020-08/exawind-builder
export EXAWIND_COMPILER=gcc
export EXAWIND_SYSTEM=ornl-summit
export EXAWIND_CODE=nalu-wind
export EXAWIND_CFGFILE=exawind-config

#
# Source the core, system, and project specific build scripts
#
source ${EXAWIND_SRCDIR}/core.bash
source ${EXAWIND_SRCDIR}/envs/${EXAWIND_SYSTEM}.bash
source ${EXAWIND_SRCDIR}/codes/${EXAWIND_CODE}.bash

# Path to ExaWind project and install directories
export EXAWIND_PROJECT_DIR=${EXAWIND_PROJECT_DIR:-/ccs/proj/cfd116/shreyas/summit/exawind-2020-08}
export EXAWIND_INSTALL_DIR=${EXAWIND_INSTALL_DIR:-${EXAWIND_PROJECT_DIR}/install/${EXAWIND_COMPILER}}
export EXAWIND_CONFIG=${EXAWIND_CONFIG:-${EXAWIND_PROJECT_DIR}/${EXAWIND_CFGFILE}.sh}

# Source any user specific configuration (see documentation)
exawind_load_user_configs

# Path to the source directory (absolute or relative to build directory)
NALU_WIND_SOURCE_DIR=${NALU_WIND_SOURCE_DIR:-..}
# Path where `make install` will install files for this project
NALU_WIND_INSTALL_PREFIX=${NALU_WIND_INSTALL_PREFIX:-${EXAWIND_INSTALL_DIR}/nalu-wind}

########## BEGIN user specific configuration ###########

########## END user specific configuration   ###########

### Execute main function (must be last line of this script)
if [[ "${BASH_SOURCE[0]}" != "${0}" ]] ; then
    exawind_env && exawind_proj_env
else
    exawind_main "$@"
fi
