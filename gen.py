import os
import random
import shutil
import time
from typing import Optional

import utils
from abc import ABC, abstractmethod

class VideoClipper(ABC):
    @abstractmethod
    def clip(self, path: str):
        pass

class RandomClipper(VideoClipper):
    def __init__(self, min_length: int = 15, max_length: int = 30, reencode=True):
        self.min_length = min_length
        self.max_length = max_length
        self.reencode = reencode

    def clip(self, path: str):
        ext = os.path.splitext(path)[1]
        os.makedirs(utils.DIR_CLIPS, exist_ok=True)

        total_length = utils.get_length(path)
        cur_time = 0
        i = utils.get_num_clips()  # for continuing numbering rather than overwriting videos
        while cur_time <= total_length:
            duration = random.uniform(self.min_length, self.max_length)

            if not self.reencode:
                # NOTE: performs output seeking -- times may therefore not be entirely accurate,
                #       but this way, don't need to re-encode
                utils.run("ffmpeg -y -i \"{2}\" -ss {0} -t {1} -c copy \"{3}\"".format(
                    cur_time,  # first time
                    duration,
                    path,
                    os.path.join(utils.DIR_CLIPS, "{:06d}{}".format(i, ext)))  # file path for segment (inherit original file extension)
                )
            else:
                utils.run("ffmpeg -y -i \"{2}\" -ss {0} -t {1} \"{3}\"".format(
                    cur_time,  # first time
                    duration,
                    path,
                    os.path.join(utils.DIR_CLIPS, "{:06d}{}".format(i, ext)))  # file path for segment (inherit original file extension)
                )

            cur_time += duration
            i += 1

class ClipJoiner:
    @abstractmethod
    def join(self, first_file: str, second_file: str, out_file: str):
        pass

class ConcatJoiner(ClipJoiner):
    def join(self, first_file: str, second_file: str, out_file: str):
        utils.ffmpeg_concat([first_file, second_file], out_file)

class CrossFadeJoiner(ClipJoiner):
    def __init__(self, fade_duration: float = 1):
        super().__init__()
        self.fade_duration = fade_duration

    def join(self, first_file: str, second_file: str, out_file: str):
        # https://video.stackexchange.com/a/17504/25336

        first_length = utils.get_length(first_file)
        second_length = utils.get_length(second_file)
        resolution = utils.get_resolution(first_file)

        utils.run(f"ffmpeg -i {first_file} -i {second_file} "
                  f"-filter_complex "
                  f"\"color=black:{resolution}:d={first_length + second_length - self.fade_duration}[base];"
                  f"[0:v]setpts=PTS-STARTPTS[v0];"
                  f"[1:v]format=yuva420p,fade=in:st=0:d={self.fade_duration}:alpha=1,"
                  f"     setpts=PTS-STARTPTS+({first_length - self.fade_duration}/TB)[v1];"
                  f"[base][v0]overlay[tmp];"
                  f"[tmp][v1]overlay,format=yuv420p[fv];"
                  f"[0:a][1:a]acrossfade=d={self.fade_duration}[fa]\" "
                  f"-map \"[fv]\" -map \"[fa]\" {out_file}")

class RandomCrossFadeJoiner(CrossFadeJoiner):
    def __init__(self, min_fade_duration: float = 0.2, max_fade_duration: float = 1):
        super().__init__()
        self.min_fade_duration = min_fade_duration
        self.max_fade_duration = max_fade_duration

    def join(self, first_file: str, second_file: str, out_file: str):
        self.fade_duration = random.randint(self.min_fade_duration, self.max_fade_duration)
        super().join(first_file, second_file, out_file)


class Generator:
    def __init__(self, clipper: Optional[VideoClipper], joiner: ClipJoiner):
        self.clipper = clipper
        self.joiner = joiner

    def _clip(self, folders):
        if self.clipper is not None:
            for folder in folders:
                for file in os.listdir(folder):
                    self.clipper.clip(os.path.join(folder, file))

    def _join(self):
        # default behaviour: just join sequentially
        self._join_by_ranking(range(utils.get_num_clips()))

    def _join_by_ranking(self, ranks):
        with open("ranks.txt", "w") as f:
            f.write(str(ranks))

        os.makedirs(utils.DIR_OUT, exist_ok=True)

        clips = [os.path.join(utils.DIR_CLIPS, file) for file in sorted(os.listdir(utils.DIR_CLIPS))]

        # init: copy the first clip to the out folder
        ext = os.path.splitext(clips[ranks[0]])[1]
        out_file = os.path.join(utils.DIR_OUT, "out"+ext)
        out_tmp_file = os.path.join(utils.DIR_OUT, "out_tmp"+ext)  # used below
        shutil.copy2(clips[ranks[0]], out_file)

        for i in range(1, len(clips)):
            # copy next clip to the out folder
            ext = os.path.splitext(clips[ranks[i]])[1]
            next_file = os.path.join(utils.DIR_OUT, "next"+ext)
            shutil.copy2(clips[i], next_file)

            # rename 'out' file (for ffmpeg)
            os.rename(out_file, out_tmp_file)
            self.joiner.join(out_tmp_file, next_file, out_file)

            # cleanup
            os.remove(out_tmp_file)
            os.remove(next_file)

    def gen(self, *folders):
            self._clip(folders)
            self._join()

class ShuffleGenerator(Generator):
    @staticmethod
    def _get_random_ranking(n):
        """
        Returns a list of numbers [0, n-1] shuffled such that
        no two numbers in the list are consecutive
        """
        buf = []
        values = set(range(n))

        # initial number is any random number
        num = random.choice(list(values))
        buf.append(num)
        values.discard(num)

        # the rest of the numbers...
        for i in range(n-1):
            # next number: select number from the remaining values but NOT num+1
            possible_values = list(values - {num + 1})
            if len(possible_values) > 0:
                num = random.choice(possible_values)
                values.discard(num)
                buf.append(num)
            else:
                # in the unlucky case where the last number that remains
                # is consecutive to the previous number
                buf.append(values.pop())  # oh well, whatever just push it to the buffer anyway

        return buf

    def _join(self):
        super()._join_by_ranking(self._get_random_ranking(utils.get_num_clips()))

# todo: skip generator, shuffle generator


if __name__ == '__main__':
    # os.makedirs(utils.DIR_INPUT, exist_ok=True)
    # Generator(RandomClipper(), ClipJoiner()).gen()

    # debug:
    RandomClipper(5, 30).clip("data/input/small/out.mkv")
    # ConcatJoiner().join("data/clips/0000.mp4", "data/clips/0002.mp4", "data/tmp/out.mp4")

    # initial_time = time.time()
    # ShuffleGenerator(
    #     # RandomClipper(min_length=5, max_length=30),
    #     None,
    #     RandomCrossFadeJoiner(0.2, 1)
    # ).gen("data/input/small/")
    # print(time.time() - initial_time)
