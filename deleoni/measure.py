from os.path import join 
from subprocess import run
from typing import Dict

from tempfile import TemporaryDirectory

# note that the bat file is only suitable for windows systems
# but an alternative is avaiable in the same folder for linux.
JAR_EXE = join(".","java", "build", "install", "PromExecutables", "bin", 
               "PromExecutables.bat")

def test_for_executables() -> bool:
    """
    Checks for the executables needed to run the technique from ProM.
    """
    import os 
    if not os.path.exists(JAR_EXE):
        return False 
    return True

def handle_output(tmpdir):
    """
    A quick shortcut to process the measurement from the run of the java
    executable.
    """
    with open(join(tmpdir, "scores.csv")) as f:
        columns = f.readline().split(",")
        data = f.readline().split(",")
        return dict(
            (key,val)
            for key,val 
            in zip(columns,data)
        )

def call_java(log, model) -> Dict[str,str]:
    """
    Calls the java executable with the parameters need to trigger de Leoni,
    returns a dict of measurements for the java call.
    """
    import sys
    with TemporaryDirectory() as tmpdir:
        out = run([ 
            JAR_EXE,
            "--job",
            "deleoni",
            "--model",
            model,
            "--log",
            log,
            "--output",
            tmpdir
        ],
        stdout=sys.stdout)
        print(f"returned value : {out}")
        processed = handle_output(tmpdir)
        print(f"{processed}")
        print(f"outcome :: {processed['mean']}")
        return processed
        
def guard_recall(logfile:str, modelfile:str) -> float:
    """
    Computes the recall notion from "Aligning Event Logs and Process Models for 
    Multi-perspective Conformance Checking" by de Leoni and Aalst in 2013.

    However, PromExecutables (see java dir) needs to be compiled before
    this function can return a value.
    """
    # check for executables
    if not test_for_executables():
        raise Exception(
            "Unable to compute recall notion as PromExecutables"+
            "have not been compiled, see java directory to compile.")
    run_data = call_java(logfile,modelfile)
    return float(run_data["mean"])