#!/usr/bin/env python
#
# Wrapper script to find the status of a submitted job for Condor
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('Condor status')
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

def jobcontrol_status(condor_status):
    jc_status = {
        'C'  : 'completed',  # completed
        'U'  : 'submitted',  # unexpanded
        'H'  : 'submitted',  # hold
        'I'  : 'submitted',  # idle
        'R'  : 'running',
        'X'  : 'killed'   # removed
        }
    return jc_status.get(condor_status, "submitted")

def form_command(keywords):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; " % keywords["QPROFILE"]
    cmd += "%s " % keywords["QSTAT"]
    return cmd

def process_output(qstat_output):
    batch_status = {}
    for line in qstat_output:
        line.rstrip()
        logger.debug("Output: %s"% line)
	if re.match(r'^\s*$', line):
            continue
        fields = line.split()
        job = re.search(batchid_re, fields[0])
        if job:
            id = fields[0]
            id = re.sub(r'\..*', "", id);
            status = fields[5]
            logger.debug("Id: %s status: %s" % (id, status))
            batch_status[id] = jobcontrol_status(status)
    return batch_status

def run(batchids):
    """
    Run the QSTAT command to get the status of given batchids.

    Sample output of command:

    $ condor_q

    -- Submitter: Q1@ip-10-159-23-56 : <10.159.23.56:39213> : ip-10-159-23-56.ec2.internal
     ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD               
      2.0   smashkevich    12/5  15:40   0+00:00:52 C  0   122.1 inscript_26041.sh 
      3.0   smashkevich    12/5  16:39   0+00:00:00 I  0   0.0  inscript_5445.sh  

    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords)
    logger.debug("Executing cmd: %s"% cmd)
    qstat = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    batch_status = process_output(qstat.stdout)
    exit_code = qstat.wait()

    if not batchids:
        batchids = sorted(batch_status.keys())
    for batchid in batchids:
        status = batch_status.get(batchid, "unknown")
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
