import os
import subprocess

DIR_ROOT = "data"
DIR_INPUT = os.path.join(DIR_ROOT, "input")
DIR_CLIPS = os.path.join(DIR_ROOT, "clips")
DIR_OUT = os.path.join(DIR_ROOT, "out")
DIR_TMP = os.path.join(DIR_ROOT, "tmp")

def run(command):
    subprocess.run(command, shell=True)

class TmpFile:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        # create containing directory if not already exist
        os.makedirs(os.path.split(self.path)[0], exist_ok=True)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete temp file
        os.remove(self.path)
