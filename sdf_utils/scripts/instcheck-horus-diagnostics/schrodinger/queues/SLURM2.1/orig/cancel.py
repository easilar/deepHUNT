#!/usr/bin/env python
#
# Wrapper script for SLURM job cancellation
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('SLURM cancel')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

batchid_re = r'(\d+)'
cancel_status_re = r'Terminating job'

usage_str = "Usage: cancel.py <batchid(s)>"

def form_command(keywords, batchids):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; "% keywords["QPROFILE"]
    cmd += "%s -v %s"% (keywords["QDEL"], ' '.join(batchids))
    return cmd

def process_output(qdel_output):
    output_lines = []
    for line in qdel_output:
        logger.debug("Output: %s"% line)
        job  = re.search(batchid_re, line)
        match = re.search(cancel_status_re, line)
        if job:
            batchid = job.groups()[0]
            logger.debug("Batchid: %s Output: %s" % (batchid,line))
            if match:
                output_lines.append("%s %s" % (batchid, line))
            else:
                output_lines.append("%s ERROR %s" % (batchid, line))
        else:
            output_lines.append("- %s" % line)

    return "\n".join(output_lines) + "\n"

def cancelJobs(batchids):
    """
    Run the QDEL command to cancel given batchids.

    Sample output of command:
    $ scancel -v 244
    scancel: Terminating job 244
    """

    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords, batchids)
    logger.debug("Executing cmd: %s"% cmd)
    qdel = sp.Popen(cmd, shell=True, stdout = sp.PIPE, stderr = sp.STDOUT)
    message = process_output(qdel.stdout)
    print message
    exit_code = qdel.wait()
    logger.debug("Exit code from command: %d"% exit_code)

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
