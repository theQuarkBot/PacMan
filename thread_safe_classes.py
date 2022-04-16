import threading

class SafeScreen:
    def __init__(self, display):
        self.__display__ = display
        self.mutex = threading.Semaphore(1)

    def get(self):
        self.mutex.acquire()
        return self.__display__

    def release(self):
        self.mutex.release()


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Semaphore(1)

    def lock(self, semaphore):
        with self.mutex:
            self.counter += 1
            if self.counter == 1:
                semaphore.acquire()

    def unlock(self, semaphore):
        with self.mutex:
            self.counter -= 1
            if self.counter == 0:
                semaphore.release()