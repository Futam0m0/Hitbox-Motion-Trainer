import time

class InputBuffer:
    def __init__(self,maxSize= 20):
        self.buffer = []
        self.maxSize = maxSize

    def addInput(self, direction):
        timestamp = time.time()

        #prevent dupes
        if self.buffer and self.buffer[-1][0] == direction:
            return
        self.buffer.append((direction,timestamp))

        if len(self.buffer) > self.maxSize:
            self.buffer.pop(0)

    def getRecent(self,n):
        return self.buffer[-n:]
