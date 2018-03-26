#!/usr/bin/env python
#
# Wrapper script to find the status of a submitted job for PBS
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('PBS status')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

usage_str = "Usage: status.py [batchid(s)]"

batchid_re = r'(\d+\S+)'

def jobcontrol_status(pbs_status):
    jc_status = {
        'E' : 'exited',
        'H' : 'submitted',  # held
        'Q' : 'submitted',
        'R' : 'running',
        'T' : 'submitted',  # moved (??)
        'W' : 'submitted',  # waiting
        'S' : 'submitted'   # suspended
        }
    return jc_status.get(pbs_status, "submitted")

def form_command(keywords):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; " % keywords["QPROFILE"]
    cmd += "%s " % keywords["QSTAT"]
    return cmd

def process_output(qstat_output):
    pbs_status = {}
    for line in qstat_output:
        line.rstrip()
        logger.debug("Output: %s"% line)
        fields = line.split()
        job = re.search(batchid_re, fields[0])
        if job:
            pbsid = job.group(0)
            status = fields[4]
            # pbsid can be truncated, so save just the numerical part
            numid = re.sub(r'\D.+', "", pbsid)
            logger.debug("PBSId: %s numid: %s status: %s" % (pbsid, numid, status))
            pbs_status[numid] = jobcontrol_status(status)
    return pbs_status

def run(batchids):
    """
    Run the QSTAT command to get the status of given batchids.

    Sample output of command (note the batch id can be truncated):

    $ qstat
    Job id            Name             User              Time Use S Queue
    ----------------  ---------------- ----------------  -------- - -----
    97.pdx-pbspro-lv0 job300-muriel-4  mashkevi          00:00:00 R workq         

    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords)
    logger.debug("Executing cmd: %s"% cmd)
    qstat = sp.Popen(cmd, shell=True, stdout = sp.PIPE)
    pbs_status = process_output(qstat.stdout)
    exit_code = qstat.wait()

    if not batchids:
        batchids = sorted(pbs_status.keys())
    for batchid in batchids:
        numid = re.sub(r'\D.+', "", batchid)
        status = pbs_status.get(numid, "unknown")
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
