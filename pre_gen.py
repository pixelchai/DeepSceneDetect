import os
import utils

def get_timestamps(path):
    with utils.TmpFile(os.path.join(utils.DIR_TMP, "output")) as file_output:
        with utils.TmpFile(os.path.join(utils.DIR_TMP, "timestamps")) as file_timestamps:
            utils.run("ffmpeg -y -i {} -filter:v \"select='gt(scene,0.4)',showinfo\" -f null - 2> {}"
                      .format(path, file_output))
            utils.run("grep showinfo {} | grep \"pts_time:[0-9.]*\" -o | grep \"[0-9.]*\" -o > {}"
                      .format(file_output, file_timestamps))

            with open(file_timestamps) as f:
                print(f.read())

get_timestamps("data/input/test.webm")