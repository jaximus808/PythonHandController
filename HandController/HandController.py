import cv2;
import mediapipe as mp;
import time;
import UnityCommunicator as U;
import struct;

sock = U.UnityCommunicator("127.0.0.1", 8000, 8001, True, True)


class Hands:
    
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode;
        self.maxHands = maxHands;
        self.detectionCon = detectionCon;
        self.trackCon = trackCon;

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode,maxHands,detectionCon,trackCon);
        self.mpDraw = mp.solutions.drawing_utils


    def handData(self, img):
        #multi_handedness 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB);
        results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img,results;

    def toBytes(self, data):
        return struct.pack(">f",data)
    def toBytesFloat(self, data):
        return struct.pack("f",data)
    
    def intToBytes(self, data):
        return data.to_bytes(2,"big");

    def CreateData(self, results):
        #if results.multi_hand_landmarks:
            #hand data landmarks is a float
            #print(type( results.multi_hand_landmarks[0].landmark[0].x))
        
        if results.multi_hand_landmarks:
            #byte array structure:
            #hands?, two hands?, right?, land marks, if hand count 2 then print next values 
            # size should always be 20 vectors (so 60 floats) per hand 
            bytepacket = bytearray(struct.pack("?",True));
            print(bytepacket);
            bytepacket += bytearray(struct.pack("i",len(results.multi_hand_landmarks)));
            print(bytepacket);
            bytepacket += bytearray(struct.pack("?",results.multi_handedness == "Right"));
            size = 0;
            for handList in results.multi_hand_landmarks:
                for handLms in handList.landmark:
                    bytepacket += bytearray(self.toBytesFloat(handLms.x));
                    bytepacket += bytearray(self.toBytesFloat(handLms.y));
                    bytepacket += bytearray(self.toBytesFloat(handLms.z));
                    size+=1;
            #print(bytepacket);
            #print(size);
            return bytepacket;
        bytepacket = struct.pack("?",False);
        return bytepacket;


def main():
    dataReader = Hands();
    cap = cv2.VideoCapture(0)
    while True:
        
        success, img = cap.read()
        img,results = dataReader.handData(img)

        data = dataReader.CreateData(results);
        
        sock.SendData(data);
        


        cv2.imshow("Image",img);
        cv2.waitKey(1);  
if __name__ == "__main__":
    # execute only if run as a script
    main()