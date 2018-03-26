#!/usr/bin/env python
#
# Wrapper script for PBS job cancellation
#

import sys
import os
import re
import subprocess as sp

import logging as log
logger = log.getLogger('PBS cancel')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

usage_str = "Usage: cancel.py <batchid(s)>"

def form_command(keywords, batchids):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; "% keywords["QPROFILE"]
    keepnum = lambda x: re.sub(r'\D.+', "", x)
    numbatchids = map(keepnum, batchids)
    cmd += "%s %s"% (keywords["QDEL"], ' '.join(numbatchids))
    return cmd

def cancelJobs(batchids):
    """
    Run the QDEL command to cancel given batchids.

    Sample output of command:

    $ qdel 7938861
    <no output -- exit code is 0 on success, nonzero on failure>
    """
    keywords = queueinit.readConfig(queue_dir=queue_dir)
    cmd = form_command(keywords, batchids)
    logger.debug("Executing cmd: %s"% cmd)

    process = sp.Popen(cmd, shell=True, stdout = sp.PIPE, stderr = sp.STDOUT)
    exit_code = process.wait()
    if exit_code:
        result = "ERROR"
    else:
        result = "cancelled"
    for batchid in batchids:
        print "%s %s" % (batchid, result)

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
    
