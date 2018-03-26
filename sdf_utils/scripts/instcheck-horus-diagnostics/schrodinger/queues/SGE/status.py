#!/usr/bin/env python
#
# Wrapper script to find the status of a submitted job for SGE
#

import sys
import os
import re
import getpass
import subprocess as sp

import logging as log
logger = log.getLogger('SGE status')
logger.setLevel(log.WARNING)
handler = log.StreamHandler(sys.stdout)
logger.addHandler(handler)

queue_dir = os.path.dirname(os.path.abspath(__file__))
queues_dir = os.path.dirname(queue_dir)
common_dir = os.path.join(queues_dir, "common")
sys.path.insert(0, common_dir)
import queueinit

usage_str = "Usage: status.py [-tasks] [batchid(s)]"
jobs = dict()

def parse_tasklist(tasklist):
    tasks = []
    for taskrange in tasklist.split(","):
        match = re.match(r"(\d+)(?:-(\d+)(?::(\d+))?)?$", taskrange)
        if match:
            (start, stop, step) = match.groups()
            if step is None:
                 step = 1
            if stop is None:
                 stop = start
            tasks.extend(range(int(start), int(stop)+1, int(step)))
    return tasks

class Job(object):
    def __init__(self, batchid):
        self.batchid = batchid
        self.status = None
        self.tasks = dict()

    def set_status(self, status, tasks=None):
        if tasks is None:
            self.status = status
        else:
            for taskid in parse_tasklist(tasks):
                self.tasks[taskid] = status

    def get_status(self, show_tasks):
        if not self.tasks:
            if self.status is None:
                return "unknown"
            else:
                return self.status
        status_count = dict()
        for status in self.tasks.itervalues():
            status_count[status] = status_count.get(status, 0) + 1
        if show_tasks:
            return " ".join(["%s:%d" % (s,status_count[s])
               for s in status_count.keys()])
        if "paused" in status_count:
            return "paused"
        elif "running" in status_count:
            return "running"
        elif "submitted" in status_count:
            return "submitted"
        return "unknown"

def record_status(batchid, status, taskid=None):
    job = jobs.get(batchid, Job(batchid))
    job.set_status(status, taskid)
    jobs[batchid] = job

def jobcontrol_status(sge_status):
    if "q" in sge_status:
        return "submitted"
    elif "w" in sge_status:
        return "submitted"
    elif "h" in sge_status:
        return "submitted"
    elif "s" in sge_status.lower():
        return "paused"
    elif 'r' in sge_status.lower():
        return "running"
    elif 't' in sge_status:
        return "submitted"
    elif 'T' in sge_status:
        return "paused"
    else:
        return "submitted"

def form_command(keywords, username):
    cmd = ""
    if keywords["QPROFILE"] and os.path.isfile(keywords["QPROFILE"]):
        cmd = ". \"%s\"; " % keywords["QPROFILE"]
    cmd += "%s -u %s" % (keywords["QSTAT"], username)
    return cmd

def process_output(qstat_output):
    for line in qstat_output:
        line = line.rstrip()
        logger.debug("Output: %s" % line)
        if "ja-task-ID" in line:
            tid_pos = line.index("ja-task-ID")
            next
        try:
            fields = line.split()
            tasks = line[tid_pos:]
            sgeid = int(fields[0])
            sgeid = str(sgeid)
            sge_status = fields[4]
            if tasks:
                logger.debug("SGEId: %s [task %s] status: %s" % (sgeid, tasks, sge_status))
                record_status(sgeid, jobcontrol_status(sge_status), tasks)
            else:
                logger.debug("SGEId: %s status: %s" % (sgeid, sge_status))
                record_status(sgeid, jobcontrol_status(sge_status))
        except (UnboundLocalError, ValueError, IndexError):
            pass

def run(batchids, opt):
    """
    Run the QSTAT command to get the status of given batchids.

    Sample output of command:

    $ qstat
    job-ID  prior   name       user         state submit/start at     queue                          slots ja-task-ID
    -----------------------------------------------------------------------------------------------------------------
    7938584 0.90450 j3eml_stp1 selvan       r     09/04/2012 12:15:21 urgent.q@robin-0-24.local         64        
    7938583 0.90453 j2rh1_stp7 selvan       r     09/04/2012 12:01:06 urgent.q@robin-0-28.local         64        

    """
    keywords = queueinit.readConfig(queue_dir=queue_dir)
    username = getpass.getuser()
    cmd = form_command(keywords, username)

    logger.debug("Executing cmd: %s" % cmd)
    qstat = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    process_output(qstat.stdout)
    exit_code = qstat.wait()

    if not batchids:
        batchids = sorted(jobs.keys())
    for batchid in batchids:
        job = jobs.get(batchid, Job(batchid))
        print batchid, job.get_status(opt.tasks)

    return exit_code

#########################################################################
def main(argv):
    """
    Main routine for the commandline application
    """
    optParser = queueinit.setupOptions(usage_str)
    optParser.add_option("-t", "--tasks", action="store_true", dest="tasks",
                      default=False, help="show status of job array tasks")
    opt, batchids = optParser.parse_args()

    if opt.debug:
        logger.setLevel(log.DEBUG)

    exit_code = run(batchids, opt)
    return exit_code

if __name__ == '__main__':
    try:
        exit_code = main(sys.argv)
        sys.exit(exit_code)
    except Exception as err:
        print "ERROR:", err
        sys.exit(1)
