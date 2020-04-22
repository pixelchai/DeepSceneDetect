import os
import utils
from abc import ABC, abstractmethod

class VideoCutter(ABC):
    @abstractmethod
    def cut(self, path: str):
        pass

class RandomCutter(VideoCutter):
    def __init__(self, min_length: int = 5, max_length: int = 120):
        self.min_length = min_length
        self.max_length = max_length

    def cut(self, path: str):
        utils.run("wow")


class ClipJoiner:
    @abstractmethod
    def join(self, first_video: str, second_video: str) -> str:
        pass


class Generator:
    def __init__(self, cutter, joiner):
        self.cutter = cutter
        self.joiner = joiner

    def gen(self):
        pass  # todo


if __name__ == '__main__':
    os.makedirs(utils.DIR_INPUT, exist_ok=True)
    Generator(RandomCutter(), ClipJoiner()).gen()
