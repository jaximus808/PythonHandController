import tkinter as tk
from tkinter import Canvas, Pack, Scrollbar, StringVar, ttk
from tkinter.constants import CENTER, LEFT, NORMAL, RIGHT, TOP, VERTICAL, Y, X
import requests
import json
import UnityCommunicator as U;
import HandController 
import time;
import cv2;
import mediapipe as mp;

MasterServer = "http://192.168.1.4:3000"

LARGEFONT =("Verdana", 35)
MEDIUMFONT =("Verdana", 25)
NORMALFONT =("Verdana", 15)
class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        self.screen_width = self.winfo_screenwidth();
        self.screen_height = self.winfo_screenheight();
        
        center_x = int(self.screen_width/2 - self.screen_width / 2)
        center_y = int(self.screen_height/2 - self.screen_height / 2)

        self.geometry(f'{self.screen_width}x{self.screen_height}+{center_x}+{center_y}')
         
        self.geometry
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        # canvas =Canvas(container);
        # tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        # initializing frames to an empty array
        self.configure(bg="white")
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
  
            frame = F(container, self)
            # canvas = tk.Canvas(frame)
            # ttk.Scrollbar(frame, orient="vertical",command=canvas.yview)
            # scrollable_frame = ttk.Frame(canvas);

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            #scrollable_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
    def show_frame(self, cont):
        x = self.CheckToken()

        frame = self.frames[self.frames[cont].SpecialCheck(x)]
        frame.tkraise()
    def CheckToken(self):
        x = TxtFileManager.readToken()
        if len(x) > 0:
            rstatus, rbody = HttpCommunicator.PostRequest(MasterServer+"/api/user/accountDetails",{"token":x})
            print(rbody)
            if rbody["error"]:
                TxtFileManager.setToken("")
            else:
                return True
        return False 
class StartPage(tk.Frame):
    def SpecialCheck(self,token):
        if token:
            return Page1 
        return StartPage
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenWidth =self.winfo_screenwidth()
        self.auth = False;
        screenHeight =self.winfo_screenheight()
        centerX = int(screenWidth/2)
        centerY = int(screenHeight/2)
        # label of frame Layout 2

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview);
        self.authFrame = ttk.Frame(canvas); 

        self.authFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        ) 
        canvas.create_window((0, 0), window=self.authFrame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right", fill="y")
        self.usernameRegisterVar = StringVar();
        self.passwordRegisterVar = StringVar();
        self.emailRegisterVar = StringVar();
 
        self.emailLoginVar = StringVar();
        self.passwordLoginVar = StringVar(); 
        # self.authFrame = tk.Frame(self, width=screenWidth, height=screenHeight);
        
        self.statusReg = StringVar();
        self.statusReg.set("Status: ")
        self.statusLog = StringVar();
        self.statusLog.set("Status: ")

        # self.authFrame.place(x=0, y=0)
        # # putting the grid in its place by using
        # grid
        
        
        # if(loginStatus != "-1"):


        ttk.Label(self.authFrame, text ="Login Page", font = LARGEFONT).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame, text="Register", font= MEDIUMFONT).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame,text="username", font=NORMALFONT).pack(side=TOP, fill=X)
        ttk.Entry(self.authFrame,textvariable=self.usernameRegisterVar ).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame,text="email",font = NORMALFONT).pack(side=TOP, fill=X)
        ttk.Entry(self.authFrame,textvariable=self.emailRegisterVar ).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame,text="password",font = NORMALFONT).pack(side=TOP, fill=X)
        tk.Entry(self.authFrame,show="*",textvariable=self.passwordRegisterVar ).pack(side=TOP, fill=X)
        ttk.Button(self.authFrame, text="Register", 
        command=lambda:self.register(self.usernameRegisterVar.get(),self.emailRegisterVar.get(),self.passwordRegisterVar.get(),controller)).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame, textvariable=self.statusReg, font= NORMALFONT, wraplength=200,justify=LEFT).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame, text="Login", font= MEDIUMFONT).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame,text="email",font = NORMALFONT).pack(side=TOP, fill=X)
        ttk.Entry(self.authFrame,textvariable=self.emailLoginVar ).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame,text="password", font = NORMALFONT).pack(side=TOP, fill=X)
        tk.Entry(self.authFrame,textvariable=self.passwordLoginVar,show="*" ).pack(side=TOP, fill=X)
        ttk.Button(self.authFrame, text="Login", 
        command=lambda:self.login(self.emailLoginVar.get(),self.passwordLoginVar.get(),controller)).pack(side=TOP, fill=X)
        ttk.Label(self.authFrame, textvariable=self.statusLog, font= NORMALFONT,wraplength=200,justify=LEFT).pack(side=TOP, fill=X)
    def register(self, _username, _email, _pass,_controller):
        rstatus, rToken = HttpCommunicator.PostRequest(
            MasterServer+"/api/user/createUser", {"username":_username, "email": _email, "password":_pass})
        print("nuts");
        print(rToken);
        if not rToken["error"]:
            TxtFileManager.setToken(rToken["message"]);
            self.statusReg.set("Status: "+ "Success!")
            _controller.show_frame(Page1)
        else:
            print("ERROR!!!!!");
            print(rToken["message"])
            self.statusReg.set("Status: "+rToken["message"])

        print(rToken["error"])
        print(rToken["message"])

    def login(self, _email, _pass,_controller):
        rstatus, rToken = HttpCommunicator.PostRequest(
            MasterServer+"/api/user/loginUser", {"email": _email, "password":_pass})
        print("nuts");
        print(rToken);
        if not rToken["error"]:
            TxtFileManager.setToken(rToken["message"]);
            self.statusLog.set("Status: "+ "Success!")
            _controller.show_frame(Page1)
        else:
            print("ERROR!!!!!");
            print(rToken["message"])
            self.statusLog.set("Status: "+rToken["message"])

        print(rToken["error"])
        print(rToken["message"])
    


# second window frame page1
class Page1(tk.Frame):
    def SpecialCheck(self, token):
        if not token:
            return StartPage
        return Page1 
    
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview);
        self.authFrame = ttk.Frame(canvas); 

        self.authFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        ) 
        canvas.create_window((0, 0), window=self.authFrame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(self.authFrame, text ="Robot Connect Page", font = LARGEFONT).pack(side=TOP,fill=X, anchor=CENTER);
        
        self.controller = controller

        self.robotIdInput = StringVar();
        self.robotPasswordInput = StringVar(); 
        self.statusConnect = StringVar(); 
        self.statusConnect.set("Status: ")

        ttk.Label(self.authFrame,text="Robot ID", font = NORMALFONT).pack(fill=X, anchor=CENTER);
        ttk.Entry(self.authFrame, textvariable=self.robotIdInput, font=NORMALFONT).pack(fill=X, anchor=CENTER);
        ttk.Label(self.authFrame, text="Robot Password", font=NORMALFONT).pack(fill=X, anchor=CENTER);
        tk.Entry(self.authFrame, textvariable=self.robotPasswordInput, font=NORMALFONT,show="*" ).pack( fill=X, anchor=CENTER);
        ttk.Label(self.authFrame, textvariable=self.statusConnect, font=NORMALFONT,wraplength=200,justify=LEFT).pack(fill=X, anchor=CENTER)
        ttk.Button(self.authFrame,text="Connect", 
        command=lambda:self.connect(self.robotIdInput.get(), self.robotPasswordInput.get())).pack(side=TOP,fill=X, anchor=CENTER)

        ttk.Button(self.authFrame, text ="Log out",
                            command = lambda : self.logout()).pack(fill=X, anchor=CENTER)
        # putting the button in its place by
        # using grid
    def connect(self, handId, handPass):
        token = TxtFileManager.readToken()
        rstatus, rBody = HttpCommunicator.PostRequest(MasterServer+"/api/user/connectArm", {"token":token,"id": handId, "password": handPass});
        print(rBody["message"])
        self.statusConnect.set("Status: "+ rBody["message"])
        if rBody["error"]:
           return; 
        self.controller.show_frame(Page2);
        StartHandUDP(rBody["ip"], rBody["port"]); 
        #will read ip and port and save into ram. 
        

    def logout(self):
        TxtFileManager.setToken("");
        self.controller.show_frame(StartPage)
  
  
# third window frame page2
class Page2(tk.Frame):
    def SpecialCheck(self, token):
        return Page2; 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

class HttpCommunicator:
    def GetRequest(address):
        r = requests.get(address);
        return r.status_code, json.loads(r.text)
    def PostRequest(address, body):
        r = requests.post(address, data = body);
        print("cock")
        print(r.text)

        return r.status_code, json.loads(r.text)

class TxtFileManager:
    def setToken(token):
        file = open("localstorage.txt","w")
        file.write(token);
        file.close()
    def readToken():
        file = open("localstorage.txt","r+");
        return file.read()

def StartHandUDP(targetIp, targetPort):
    dataReader = HandController.Hands();
    sock = U.UnityCommunicator("", 8000, 8001,dataReader, targetIp,targetPort,True, True,)

    t = time.time()
    timer = 0
    deltaTime = t;
    cap = cv2.VideoCapture(0)
    while True:
        
        success, img = cap.read()
        img,results = dataReader.handData(img)

        if dataReader.connected:
            data = dataReader.CreateData(results);
            
            sock.SendData(data);
        else:
            t = time.time()
            # print(t)
            # print(deltaTime)
            timer += t - deltaTime; 
            deltaTime = t; 
            if timer > 5:
                print("cock");
                timer = 0; 
                data = dataReader.CreateJoinData();
                sock.SendData(data); 
        if dataReader.connected:
            cv2.putText(img, "connected", (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255), 3);
        elif sock.disconnected:
            cv2.putText(img, "Fleet Server Closed", (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255), 3);
        else:
            cv2.putText(img, "connecting", (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255), 3);
        cv2.imshow("Image",img);
        cv2.waitKey(1);
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) <1:
            break  
        
    

wind=Window();

if __name__ == "__main__":
    # execute only if run as a script
    #main()
    #wind.homepage()
    wind.mainloop()