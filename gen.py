import os
from abc import ABC, abstractmethod

DIR_ROOT = "data"
DIR_INPUT = os.path.join(DIR_ROOT, "input")
DIR_CLIPS = os.path.join(DIR_ROOT, "clips")
DIR_OUT = os.path.join(DIR_ROOT, "out")


class VideoCutter(ABC):
    def __init__(self, path):
        self.path = path

    def cut(self):
        pass


class ClipJoiner(ABC):
    def __init__(self, first_video: str, second_video: str):
        self.first_video = first_video
        self.second_video = second_video

    @abstractmethod
    def join(self) -> str:
        pass


class Generator:
    def __init__(self, cutter: VideoCutter, joiner: ClipJoiner):
        self.cutter = cutter
        self.joiner = joiner

    def gen(self):
        pass  # todo


if __name__ == '__main__':
    os.makedirs(DIR_INPUT, exist_ok=True)
