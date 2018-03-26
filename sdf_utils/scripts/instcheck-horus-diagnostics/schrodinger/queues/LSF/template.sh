#!/bin/bash
#BSUB -J %NAME%
#BSUB -n %NPROC%
#BSUB -Q 99
#
# Batch-submission script for LSF system
#

PATH=/usr/bin:/bin:/usr/bsd:/usr/sbin:/sbin:/usr/local/bin:$PATH

%ENVIRONMENT%

export SCHRODINGER_BATCHID
SCHRODINGER_BATCHID=$LSB_JOBID

NODEFILE_DIR=~/.schrodinger/tmp
if [ ! -d "$NODEFILE_DIR" ]; then
  mkdir -p "$NODEFILE_DIR"
fi

SCHRODINGER_MPI_NODEFILE="$NODEFILE_DIR/$LSB_JOBID.mpinodes"
SCHRODINGER_TMP_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
export SCHRODINGER_MPI_NODEFILE SCHRODINGER_TMP_NODEFILE

if [ "%NPROC%" -gt 1 -a -n "$LSB_MCPU_HOSTS" ]; then
  # Format of $LSB_MCPU_HOSTS: "host1 numproc1 host2 numproc2 ..."
  switch=0 
  for field in $LSB_MCPU_HOSTS; do
    if [ $switch -eq 0 ]; then
      # field = hostname
      hostname=$field
      switch=1
    else
      # field = number
      for i in `eval echo {1..$field}`; do
        echo $hostname >> $SCHRODINGER_MPI_NODEFILE
        if [ -n "%GPGPU%" ]; then
          SCHRODINGER_GPGPU="$SCHRODINGER_GPGPU$hostname:%GPGPU% "
          export SCHRODINGER_GPGPU
        fi
      done 
      switch=0
    fi
  done

  SCHRODINGER_NODEFILE="$SCHRODINGER_MPI_NODEFILE"
  export SCHRODINGER_NODEFILE

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

LICTEST_EXITCODE=0
export LICTEST_EXITCODE

if [ -n "$LICENSE_CHECKING" -a -n "%$LICTEST_ARGS%" ]; then
  LICTEST="$SCHRODINGER/utilities/lictest"
  if [ -f "$LICTEST" ]; then
    SCHRODINGER_LICENSE_PID=`sh "$LICTEST" -d %$LICTEST_ARGS% -p 600 -b`
    LICTEST_EXITCODE=$?
    # Exit code 15 or 16 means a retriable license error.
    # Return exit code 99 to tell LSF to reschedule the job.
    if [ "$LICTEST_EXITCODE" = 15 -o "$LICTEST_EXITCODE" = 16 ]; then
      exit 99
    fi
  else
    # jmonitor will recognize this value as "Couldn't execute lictest",
    # and fizzle the job with the corresponding error message.
    SCHRODINGER_LICENSE_PID=0
    LICTEST_EXITCODE=127
  fi
  export SCHRODINGER_LICENSE_PID 
fi

%COMMAND%
