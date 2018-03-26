#!/usr/bin/env python
#
# Wrapper script to find the status of a submitted job for SLURM
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('SLURM status')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

usage_str = "Usage: status.py [batchid(s)]"

batchid_re = r'(\d+)'

def jobcontrol_status(slurm_status):
    jc_status = {
        'COMPLETING' : 'exited',
        'COMPLETED'  : 'exited',
        'PENDING'    : 'submitted',
        'RUNNING'    : 'running',
        'FAILED'     : 'exited',  # Job dead, not resubmitted (as of slurm 1.2.13)
        'NODE_FAIL'  : 'exited',  # Job dead, not resubmitted (as of slurm 1.2.13)
        'CANCELLED'  : 'exited',  # User stopped job
        'SUSPENDED'  : 'running'  # suspended
    }
    return jc_status.get(slurm_status, "unknown")

def form_command(keywords):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; " % keywords["QPROFILE"]
    cmd += "%s -l" % keywords["QSTAT"]
    return cmd

def process_output(qstat_output, batchids):
    result_dict = {}
    output_lines = []
    for line in qstat_output:
        logger.debug("Output: %s"% line)
        result = line.split()
        if len(result) < 6:
            continue
        batchid, partition, name, user, state = result[0:5]
        if not re.search(batchid_re, batchid):
            continue
        logger.debug("BatchId: %s" % batchid)
        # key => batchid value => state:name:user
        result_dict[batchid] = "%s:%s:%s" % (state, name, user)

    if not batchids:
        batchids = sorted(result_dict.keys())
    for batchid in batchids:
        value = result_dict.get(batchid, "")
        if value:
            (state, name, user) = value.split(":")
            jc_status = jobcontrol_status(state)
        if jc_status == "unknown":
            output_lines.append("%s %s" % (batchid, jc_status))
        else:
            output_lines.append("%s %s - %s %s" % (batchid, jc_status, name, user))

    return "\n".join(output_lines) + "\n"

def run(batchids):
    """
    Run the QSTAT command to get the status of given batchids.

    Sample output of command:

    $ squeue 
    JOBID PARTITION     NAME     USER  ST       TIME  NODES NODELIST(REASON)
      244     batch job100-m mashkevi   R      12:36      1 pdx-slurm1-lv01
    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords)
    logger.debug("Executing cmd: %s"% cmd)
    qstat = sp.Popen(cmd, shell=True, stdout = sp.PIPE)
    message = process_output(qstat.stdout, batchids)
    print message
    exit_code = qstat.wait()

    return exit_code

#########################################################################
def main(argv):
    """
    Main routine for the commandline application
    """
    optParser = queueinit.setupOptions(usage_str)
    opts, batchids = optParser.parse_args()

    if opts.debug:
        logger.setLevel(log.DEBUG)

    exit_code = run(batchids)
    return exit_code

if __name__ == '__main__':
    try:
        exit_code = main(sys.argv)
    except Exception, err:
        print err
        print usage_str
        sys.exit(1)
    sys.exit(exit_code)
