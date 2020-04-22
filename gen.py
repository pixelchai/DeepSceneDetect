import os
import random
import utils
from abc import ABC, abstractmethod

class VideoClipper(ABC):
    @abstractmethod
    def clip(self, path: str):
        pass

class RandomClipper(VideoClipper):
    def __init__(self, min_length: int = 15, max_length: int = 30):
        self.min_length = min_length
        self.max_length = max_length

    def clip(self, path: str):
        ext = os.path.splitext(path)[1]
        os.makedirs(utils.DIR_CLIPS, exist_ok=True)

        total_length = utils.get_length(path)
        cur_time = 0
        i = 0
        while cur_time <= total_length:
            duration = random.uniform(self.min_length, self.max_length)

            utils.run("ffmpeg -y -ss {0} -i \"{2}\" -t {1} -c copy \"{3}\"".format(
                cur_time,  # first time
                duration,
                path,
                os.path.join(utils.DIR_CLIPS, "{:04d}{}".format(i, ext)))  # file path for segment (inherit original file extension)
            )

            cur_time += duration
            i += 1

class ClipJoiner:
    @abstractmethod
    def join(self, first_video: str, second_video: str) -> str:
        pass


class Generator:
    def __init__(self, cutter, joiner):
        self.cutter = cutter
        self.joiner = joiner

    def gen(self, *paths):
        pass  # todo

# todo: skip generator, shuffle generator, mix video sources generator


if __name__ == '__main__':
    # os.makedirs(utils.DIR_INPUT, exist_ok=True)
    # Generator(RandomClipper(), ClipJoiner()).gen()

    # debug:
    RandomClipper().clip("data/input/heidelberg/0000.mp4")
