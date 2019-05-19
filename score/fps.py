import datetime


class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        self._end = datetime.datetime.now()
        return self

    def update(self):
        self._numFrames += 1
        return self

    def elapsed(self):
        end = self._end if self._end is not None else datetime.datetime.now()
        return (end - self._start).total_seconds()

    def fps(self):
        return self._numFrames / self.elapsed()
