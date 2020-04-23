import os
import utils

def get_timestamps(path, thresh=0.2):
    # https://stackoverflow.com/a/38205105/5013267

    timestamps = []
    with utils.TmpFile(os.path.join(utils.DIR_TMP, "output")) as file_output:
        with utils.TmpFile(os.path.join(utils.DIR_TMP, "timestamps")) as file_timestamps:

            utils.run("ffmpeg -y -i \"{0}\" -filter:v \"select='gt(scene,{2})',showinfo\" -f null - 2> \"{1}\""
                      .format(path, file_output, thresh))
            utils.run("grep showinfo \"{}\" | grep \"pts_time:[0-9.]*\" -o | grep \"[0-9.]*\" -o > \"{}\""
                      .format(file_output, file_timestamps))

            with open(file_timestamps) as f:
                buffer = f.readline()
                while buffer != "":
                    timestamps.append(float(buffer))
                    buffer = f.readline()

    return timestamps

def cut_video(path, remove_short=True):
    timestamps = get_timestamps(path)

    new_dir, ext = os.path.splitext(path)
    os.makedirs(new_dir, exist_ok=False)
    for i in range(len(timestamps)-1):
        utils.run("ffmpeg -ss {0} -i \"{2}\" -to {1} -c copy \"{3}\"".format(
            timestamps[i],  # first time
            timestamps[i+1],
            path,
            os.path.join(new_dir, "{:06d}{}".format(i, ext)))  # file path for segment (inherit original file extension)
        )

    if remove_short:
        i = 0
        for file_segment_path in os.listdir(new_dir):
            path = os.path.join(new_dir, file_segment_path)
            if utils.get_length(path) < 5:
                os.remove(path)
                print("Removed short segment: {}".format(path))
            else:
                # rename so that file numberings still sequential
                os.rename(
                    path,
                    os.path.join(new_dir, "{:0d}{}".format(i, os.path.splitext(file_segment_path)[1]))
                )
                i += 1


if __name__ == '__main__':
    # cut up all input videos
    for file in os.listdir(utils.DIR_INPUT):
        name, ext = os.path.splitext(file)
        path = os.path.join(utils.DIR_INPUT, file)

        if ext == '.txt': continue
        if not os.path.isfile(path): continue

        try:
            cut_video(path)
        except OSError:
            # folder already exists, continue
            continue
