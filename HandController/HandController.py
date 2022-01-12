import cv2;
import mediapipe as mp;
import time;
import UnityCommunicator as U;
import struct;
import tkinter as tk; 

#need to thread this shit 
class Hands:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode;
        self.maxHands = maxHands;
        self.detectionCon = detectionCon;
        self.trackCon = trackCon;

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode,maxHands,1,detectionCon,trackCon);
        self.mpDraw = mp.solutions.drawing_utils
        self.connected = False; 
        self.clientId = -1; 

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

    def CreateJoinData(self,targetId):
        bytepacket = bytearray(struct.pack("i",0))
        bytepacket += bytearray(struct.pack("i",-1));

        bytepacket += bytearray(struct.pack("i",int(targetId)));
        return bytepacket
    def CreateData(self, results):
        #if results.multi_hand_landmarks:
            #hand data landmarks is a float
            #print(type( results.multi_hand_landmarks[0].landmark[0].x))
        
        bytepacket = bytearray(struct.pack("i",1));
        bytepacket += bytearray(struct.pack("i",self.clientId));
        #print(bytepacket)
        bytepacket += bytearray(struct.pack("i",1));
        if results.multi_hand_landmarks:
            #byte array structure:
            #hands?, two hands?, right?, land marks, if hand count 2 then print next values 
            # size should always be 20 vectors (so 60 floats) per hand 
            bytepacket += bytearray(struct.pack("?",True));
            #print(bytepacket);
            bytepacket += bytearray(struct.pack("i",len(results.multi_hand_landmarks)));
            #print(bytepacket);
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
        bytepacket += struct.pack("?",False);
        return bytepacket;



def main():
    window_width = 500
    window_height = 500

    

    root = tk.Tk(); 
    

    screen_width = root.winfo_screenwidth();
    screen_height = root.winfo_screenheight();
    
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{screen_width}x{screen_height}+{center_x}+{center_y}')
    

    label = tk.Label(root, text="hello",font=("Helvetica", 14)).place(x = 5, y =2);
    label2 = tk.Label(root, text="balls",font=("Helvetica", 14));
    

    
    root.title("Internet Robot Window");
    root.mainloop();
    # t = time.time()
    # timer = 0
    # deltaTime = t;
    # cap = cv2.VideoCapture(0)
    # while True:
        
    #     success, img = cap.read()
    #     img,results = dataReader.handData(img)

    #     if dataReader.connected:
    #         data = dataReader.CreateData(results);
            
    #         sock.SendData(data);
    #     else:
    #         t = time.time()
    #         # print(t)
    #         # print(deltaTime)
    #         timer += t - deltaTime; 
    #         deltaTime = t; 
    #         if timer > 5:
    #             print("cock");
    #             timer = 0; 
    #             data = dataReader.CreateJoinData();
    #             sock.SendData(data); 
    #     if dataReader.connected:
    #         cv2.putText(img, "connected", (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255), 3);
    #     else:
    #         cv2.putText(img, "connecting", (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255), 3);
    #     cv2.imshow("Image",img);
    #     cv2.waitKey(1);  
