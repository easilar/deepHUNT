#!/bin/sh
#SUBMIT Requirements = ((Arch =?= "INTEL") || (Arch =?= "X86_64")) && (OpSys =?= "LINUX")  && (Memory * 2048 > ImageSize) && ((%NPROC% == 1) || (SingleSlotMultiCore =?= True))
#SUBMIT +RequestCpus = %NPROC%
#SUBMIT notification = never
#
# Batch-submission script for Condor system
#

PATH=/usr/bin:/bin:/usr/bsd:/usr/sbin:/sbin:/usr/local/bin:$PATH

SCHRODINGER_BATCHID=$CONDOR_JOBID
export SCHRODINGER_BATCHID

%ENVIRONMENT%

# set $HOME, as a workaround for Ev:89945
if [ -z "$HOME" ]; then
  HOME=`echo ~`
  export HOME
fi

if [ -n "$_CONDOR_SCRATCH_DIR" ]; then
  NODEFILE_DIR="$_CONDOR_SCRATCH_DIR"
else
  USER=`whoami`
  NODEFILE_DIR="/tmp/$USER"
fi
if [ ! -d "$NODEFILE_DIR" ]; then
  mkdir -p "$NODEFILE_DIR"
fi

SCHRODINGER_MPI_NODEFILE="$NODEFILE_DIR/$SCHRODINGER_BATCHID.nodefile"
SCHRODINGER_TMP_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
export SCHRODINGER_MPI_NODEFILE SCHRODINGER_TMP_NODEFILE

HOST=`hostname`
if [ "%NPROC%" -gt 1 ]; then
  # create nodefile for single-slot 8-core node
  echo $HOST  > "$SCHRODINGER_MPI_NODEFILE" # 1
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 2
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 3
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 4
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 5
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 6
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 7
  echo $HOST >> "$SCHRODINGER_MPI_NODEFILE" # 8
  SCHRODINGER_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
  export SCHRODINGER_NODEFILE
  if [ -n "%GPGPU%" ]; then
    SCHRODINGER_GPGPU="$HOST:8%GPGPU%"
    export SCHRODINGER_GPGPU
  fi
else
  echo $HOST > "$SCHRODINGER_MPI_NODEFILE"
  if [ -n "%GPGPU%" ]; then
    SCHRODINGER_GPGPU="$HOST:%GPGPU%"
    export SCHRODINGER_GPGPU
  fi
fi

%COMMAND%
