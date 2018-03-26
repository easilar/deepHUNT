#!/usr/bin/env python
#
# Wrapper script for Condor job cancellation
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('Condor cancel')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

usage_str = "Usage: cancel.py <batchid(s)>"

batchid_re = r'cluster\s+(\d+)'
cancel_status_re = r'marked for removal|couldn\'t find'

def form_command(keywords, batchids):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; "% keywords["QPROFILE"]
    cmd += "%s %s"% (keywords["QDEL"], ' '.join(batchids))
    logger.debug("Executing cmd: %s"% cmd)
    return cmd

def process_output(qdel_output):
    lines = []
    for line in qdel_output:
        logger.debug("Output: %s"% line)
        line = line.rstrip()
        job  = re.search(batchid_re, line, flags=re.IGNORECASE)
        match = re.search(cancel_status_re, line, flags=re.IGNORECASE)
        if job:
            batchid = job.group(1)
            logger.debug("Batchid: %s Output: %s" % (batchid,line))
            if match:
                lines.append("%s %s" % (batchid, line))
            else:
                lines.append("%s ERROR %s" % (batchid, line))
        else:
            lines.append("- %s" % line)

    return "\n".join(lines) + "\n"

def cancelJobs(batchids):
    """
    Run the QDEL command to cancel given batchids.

    Sample output of command:

    $ condor_rm 5
    Cluster 5 has been marked for removal.

    $ condor_rm 5
    Couldn't find/remove all jobs in cluster 5.
    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords, batchids)
    logger.debug("Executing cmd: %s" % cmd)
    qdel = sp.Popen(cmd, shell=True, stdout = sp.PIPE, stderr = sp.STDOUT)
    message = process_output(qdel.stdout)
    print message
    exit_code = qdel.wait()

    return exit_code

#########################################################################
def main(argv):
    """
    Main routine for the commandline application
    """
    optParser = queueinit.setupOptions(usage_str)
    opts, batchids = optParser.parse_args()
    
    if not batchids:
        raise Exception("No batchids were specified")

    if opts.debug: 
        logger.setLevel(log.DEBUG)

    exit_code = cancelJobs(batchids)
    return exit_code

if __name__ == '__main__':
    try:
        exit_code = main(sys.argv)
    except Exception, err:
        print err
        print usage_str
        sys.exit(1)
    sys.exit(exit_code)
