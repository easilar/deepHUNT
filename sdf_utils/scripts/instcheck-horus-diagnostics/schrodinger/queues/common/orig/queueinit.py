import os
import sys
import os.path
import optparse

queues_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_dir = os.path.join(queues_dir, "common")

def setupOptions(usage=None):
    """ 
    Setup basic options for queue action script and return parser

    Parameters
    
    usage (str)
        Usage string to add in help message
    """
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="turn on debugging")

    return parser 

def readConfig(config_file=None, queue_dir=None):
    """
    Read configuration file and set up environment to run queue commands.
    Return dictionary of queue variables and values.

    Parameters
 
    config_file (pathname) optional
        Configuration file pathname
    queue_dir (pathname) optional
        Directory in which the script that loaded this module is located
    """
    keywords = {'QPATH': '', 'QPROFILE': ''}

    os.environ['PATH'] = os.environ['PATH'] + os.pathsep + "/usr/bin:/bin:/usr/sbin:/usr/bsd:/usr/local/bin"
    if not config_file:
        config_file = os.path.join(queue_dir, "config")
    if not os.path.isfile(config_file):
        raise IOError("The %s file is missing."% config_file)
    fh = open(config_file)

    try:
        for line in fh.read().splitlines():
            line = line.strip()
            if not line.startswith("#") and "=" in line:
                keyword_list = line.split('=', 1)
                if len(keyword_list) == 2:
                    keywords[keyword_list[0]] = keyword_list[1]
                else:
                    keywords[keyword_list[0]] = ""
    finally:
        fh.close()

    if keywords["QPATH"]:
            os.environ["PATH"] = keywords["QPATH"] + os.pathsep + os.environ["PATH"]

    return keywords
