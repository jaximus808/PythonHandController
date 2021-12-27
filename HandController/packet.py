class packet():
    def __init__(self, initBytes = bytearray()):
        self.buffer = initBytes;
        self.readPos = 0; 
    def ReadInt(self): 
        if self.readPos+4 > len(self.buffer):
            print("Cannot read int");
            return; 
        self.readPos += 4;
        return int.from_bytes(self.buffer[(self.readPos-4): self.readPos], "little", signed=True)
        