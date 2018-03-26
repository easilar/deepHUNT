#!/usr/bin/env python
#
# Wrapper script to find the status of a submitted job for LSF
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('LSF status')
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

def jobcontrol_status(lsf_status):
    jc_status = {
        'PEND'  : 'submitted',
        'PSUSP' : 'submitted',
        'RUN'   : 'running',
        'USUSP' : 'paused',   # although our 'paused' won't lead to this, as of now
        'SSUSP' : 'paused',
        'DONE'  : 'completed'
        }
    return jc_status.get(lsf_status, "submitted")

def form_command(keywords):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; " % keywords["QPROFILE"]
    cmd += "%s " % keywords["QSTAT"]
    return cmd

def process_output(qstat_output):
    lsf_status = {}
    for line in qstat_output:
        line.rstrip()
        logger.debug("Output: %s"% line)
        fields = line.split()
        if len(fields) < 3:
            continue
        job = re.search(batchid_re, fields[0])
        if job:
            batchid = fields[0]
            status = fields[2]
            logger.debug("LSFId: %s status: %s" % (batchid, status))
            lsf_status[batchid] = jobcontrol_status(status)
    return lsf_status

def run(batchids):
    """
    Run the QSTAT command to get the status of given batchids.

    Sample output of command:

    $ bjobs
    JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
    1722    mashkev RUN   normal     pdx-lsf-lv0 pdx-lsf-lv0 job300-m   Sep 13 17:43

    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords)
    logger.debug("Executing cmd: %s"% cmd)
    qstat = sp.Popen(cmd, shell=True, stdout = sp.PIPE)
    lsf_status = process_output(qstat.stdout)
    exit_code = qstat.wait()

    if not batchids:
        batchids = sorted(lsf_status.keys())
    for batchid in batchids:
        status = lsf_status.get(batchid, "unknown")
        print batchid, status

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
