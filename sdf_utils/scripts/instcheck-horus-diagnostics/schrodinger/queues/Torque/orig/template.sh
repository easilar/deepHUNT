#!/bin/sh
#PBS -N %PBSNAME%
#PBS -j oe
#PBS -r n
#PBS -l nodes=%NPROC%
#
# Batch-submission script for Torque system
#

PATH=/usr/bin:/bin:/usr/bsd:/usr/sbin:/sbin:/usr/local/bin:$PATH

QPATH=/usr/local/pbs/bin
curdir=`echo $0 | sed -e 's#/[^/]*$##'`
if [ -f "$curdir/config" ]; then
  . $curdir/config
fi

PATH=$QPATH:$PATH

%ENVIRONMENT%

SCHRODINGER_BATCHID="$PBS_JOBID"
export SCHRODINGER_BATCHID

# $TMPDIR is set by the queue, but only if it is configured properly;
# hence, provide a fallback
if [ -z "$TMPDIR" ]; then
  mkdir -p ~/.schrodinger/temp
  TMPDIR=~/.schrodinger/temp
fi

SCHRODINGER_MPI_NODEFILE="$TMPDIR/$SCHRODINGER_BATCHID.mpinodes"
SCHRODINGER_TMP_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
export SCHRODINGER_MPI_NODEFILE SCHRODINGER_TMP_NODEFILE

if [ "%NPROC%" -gt 1 -a -n "$PBS_NODEFILE" ]; then
  SCHRODINGER_NODEFILE="$PBS_NODEFILE"
  SCHRODINGER_MPI_NODEFILE="$PBS_NODEFILE"
  export SCHRODINGER_NODEFILE SCHRODINGER_MPI_NODEFILE
  if [ -n "%GPGPU%" ]; then
    SCHRODINGER_GPGPU=`awk -v ORS=' ' -v OFS=':' '{print $1, "%GPGPU%"}' $PBS_NODEFILE`
    export SCHRODINGER_GPGPU
  fi
else
  hostname > "$SCHRODINGER_MPI_NODEFILE"
  if [ -n "%GPGPU%" ]; then
    HOST=`hostname`
    SCHRODINGER_GPGPU="$HOST:%GPGPU%"
    export SCHRODINGER_GPGPU
  fi
fi

%COMMAND%

