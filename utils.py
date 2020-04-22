import os
import subprocess

DIR_ROOT = "data"
DIR_INPUT = os.path.join(DIR_ROOT, "input")
DIR_CLIPS = os.path.join(DIR_ROOT, "clips")
DIR_OUT = os.path.join(DIR_ROOT, "out")
DIR_TMP = os.path.join(DIR_ROOT, "tmp")

def run(command):
    print("> " + str(command))
    subprocess.run(command, shell=True)

def run_out(command):
    print("> " + str(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8')
    print("= " + str(output))
    return output

def get_length(path):
    # https://superuser.com/a/945604/581663
    return float(run_out("ffprobe -v error -show_entries "
                         "format=duration -of default=noprint_wrappers=1:nokey=1 \"{}\""
                         .format(path)))

class TmpFile:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        # create containing directory if not already exist
        os.makedirs(os.path.split(self.path)[0], exist_ok=True)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete temp file if exists
        if os.path.isfile(self.path):
            os.remove(self.path)
