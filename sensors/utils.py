import subprocess

def getListFromShellCmd(cmd):
    """ Executes a given {cmd} in a shell and returs output as a list (each line is a new item)"""
    """"""
    try:
        out = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        out = out.split("\n")
        # get rid of empty lines
        return [line.strip() for line in out if len(line) > 0]
    except subprocess.CalledProcessError as e:
        return []

def callCmd(cmd_args):
    process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr