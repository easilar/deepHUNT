#!/bin/sh
#$ -N '%PBSNAME%'
#$ -notify
#$ -j y
#$ -r n
#
# For parallel mpi jobs, the "-pe mp <ncpu>" option is used to
# specify the number of processors to reserve.  It should be added
# to the "qargs:" line of the hosts file, rather than here, to
# avoid specifying a parallel environment for serial jobs.
#
# -pe mp %NPROC%
#
# Batch-submission script for Sun Grid Engine 
#
# set -x
PATH=/usr/bin:/bin:/usr/bsd:/usr/sbin:/sbin:/usr/local/bin:$PATH

## Write the batch script in your home directory
# cp $JOB_SCRIPT ~/%JOBID%.batch

requeue_job () { exit 99; }

QPATH=$SGE_BINARY_PATH
PATH=$QPATH:$PATH

SCHRODINGER_SIGUSR1="STOP"
export SCHRODINGER_SIGUSR1

SCHRODINGER_JOBDIR=""
export SCHRODINGER_JOBDIR;

# BatchId and TaskId are used to define other env vars,
# so these settings must precede ENVIRONMENT section.
SCHRODINGER_BATCHID="$JOB_ID"
export SCHRODINGER_BATCHID

if [ -n "$SGE_TASK_ID" -a "$SGE_TASK_ID" != "undefined" ]; then
  SCHRODINGER_TASKID="$SGE_TASK_ID"
  export SCHRODINGER_TASKID
fi

SCHRODINGER_QUEUE_TMPDIR="$TMPDIR"
export SCHRODINGER_QUEUE_TMPDIR

%ENVIRONMENT%

%LICENSE_CHECK%

SCHRODINGER_MPI_NODEFILE="$TMPDIR/$JOB_ID.mpinodes"
SCHRODINGER_TMP_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
export SCHRODINGER_MPI_NODEFILE SCHRODINGER_TMP_NODEFILE

if [ "%NPROC%" -gt 1 -a -n "$PE_HOSTFILE" ]; then
  #nodefile from sge is with 4 columns (hostname procs user queue), so we crop it
  awk '{for(i=0;i<$2;i++) print $1}' $PE_HOSTFILE > "$SCHRODINGER_MPI_NODEFILE"
  SCHRODINGER_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
  export SCHRODINGER_NODEFILE
  if [ -n "%GPGPU%" ]; then
    SCHRODINGER_GPGPU=`awk -v ORS=' ' -v OFS=':' '{for(i=0;i<$2;i++) print $1, "%GPGPU%"}' $PE_HOSTFILE`
    export SCHRODINGER_GPGPU
  fi

  #mpirun still tries to use rsh so we set some extra env.
  P4_RSHCOMMAND=ssh; export P4_RSHCOMMAND
  RSHCOMMAND=ssh; export RSHCOMMAND
else
  hostname > "$SCHRODINGER_MPI_NODEFILE"
  if [ -n "%GPGPU%" ]; then
    HOST=`hostname`
    SCHRODINGER_GPGPU="$HOST:%GPGPU%"
    export SCHRODINGER_GPGPU
  fi
fi

%COMMAND%

