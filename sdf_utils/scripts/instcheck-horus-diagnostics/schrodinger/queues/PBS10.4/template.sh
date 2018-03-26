#!/bin/sh
#PBS -N %PBSNAME%
#PBS -j oe
#PBS -r n
#PBS -l select=%NPROC%
#
# Batch-submission script for OpenPBS system
#

PATH=/usr/bin:/bin:/usr/bsd:/usr/sbin:/sbin:/usr/local/bin:$PATH

QPATH=/usr/local/pbs/bin
curdir=`echo $0 | sed -e 's#/[^/]*$##'`
if [ -f "$curdir/config" ]; then
  . $curdir/config
fi

PATH=$QPATH:$PATH

SCHRODINGER_BATCHID="$PBS_JOBID"
export SCHRODINGER_BATCHID

%ENVIRONMENT%

NODEFILE_DIR=~/.schrodinger/tmp
if [ ! -d "$NODEFILE_DIR" ]; then
  mkdir -p "$NODEFILE_DIR"
fi

if [ "%NPROC%" -gt 1 -a -n "$PBS_NODEFILE" ]; then
  SCHRODINGER_NODEFILE="$PBS_NODEFILE"
  SCHRODINGER_MPI_NODEFILE="$PBS_NODEFILE"
  export SCHRODINGER_NODEFILE SCHRODINGER_MPI_NODEFILE
  if [ -n "%GPGPU%" ]; then
    SCHRODINGER_GPGPU=`awk -v ORS=' ' -v OFS=':' '{print $1, "%GPGPU%"}' $PBS_NODEFILE`
    export SCHRODINGER_GPGPU
  fi
else
  SCHRODINGER_MPI_NODEFILE="$NODEFILE_DIR/$PBS_JOBID.mpinodes"
  SCHRODINGER_TMP_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
  export SCHRODINGER_MPI_NODEFILE SCHRODINGER_TMP_NODEFILE
  hostname > "$SCHRODINGER_MPI_NODEFILE"
  if [ -n "%GPGPU%" ]; then
    HOST=`hostname`
    SCHRODINGER_GPGPU="$HOST:%GPGPU%"
    export SCHRODINGER_GPGPU
  fi
fi

%COMMAND%

