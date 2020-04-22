import os
import utils

def get_timestamps(path):
    # https://stackoverflow.com/a/38205105/5013267

    timestamps = []
    with utils.TmpFile(os.path.join(utils.DIR_TMP, "output")) as file_output:
        with utils.TmpFile(os.path.join(utils.DIR_TMP, "timestamps")) as file_timestamps:

            utils.run("ffmpeg -y -i {} -filter:v \"select='gt(scene,0.2)',showinfo\" -f null - 2> {}"
                      .format(path, file_output))
            utils.run("grep showinfo {} | grep \"pts_time:[0-9.]*\" -o | grep \"[0-9.]*\" -o > {}"
                      .format(file_output, file_timestamps))

            with open(file_timestamps) as f:
                buffer = f.readline()
                while buffer != "":
                    timestamps.append(float(buffer))
                    buffer = f.readline()

    return timestamps

def cut_video(path):
    timestamps = get_timestamps(path)

    new_dir, ext = os.path.splitext(path)
    os.makedirs(new_dir, exist_ok=False)
    for i in range(len(timestamps)-1):
        utils.run("ffmpeg -ss {} -i {} -t {} -c copy {}".format(
            timestamps[i],  # first time
            path,
            timestamps[i+1] - timestamps[i],  # duration
            os.path.join(new_dir, "{:04d}{}".format(i, ext)))  # file path for segment (inherit original file extension)
        )

cut_video("data/input/test.webm")
