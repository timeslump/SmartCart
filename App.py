from PIL import Image, ImageTk
import tkinter as tk
import SmartCart
import cv2
import time
import qrcode
import pyzbar.pyzbar as pyzbar
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class App(object):
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.attributes("-fullscreen", True)
        self.tk.bind("<F11>", lambda event: self.tk.attributes("-fullscreen", not self.tk.attributes("-fullscreen")))
        self.tk.bind("<Escape>", lambda event: self.tk.destroy())
        self.tk.title("Test")

        # Video Part, Make qrcode
        self.cartnum = 1
        self.qr = qrcode.make(str(self.cartnum))
        self.qr.save('qrcode.png')
        self.cap = cv2.VideoCapture(-1)
        self.item = {}

         #firebase
        self.cred = credentials.Certificate('/home/pi/smartcart-94000-firebase-adminsdk-pkypl-72ca0b7711.json')
        self.default_app = firebase_admin.initialize_app(cred, {'databaseURL':'https://smartcart-94000-default-rtdb.firebaseio.com/'})
        tmp = db.reference('Item').get()
        self.itemprice = { x:tmp[x]['price'] for x in tmp}
        
        self.FPage()

    # Destory All grid in current Frame 
    def switch_frame(self):
        mylist = self.tk.grid_slaves()
        for i in mylist:
            i.destroy()

    # First page press Start to start
    def FPage(self):
        tk.Button(self.tk , text="Start",command= lambda : [self.switch_frame(), self.Spage()]).grid(row = 0)


    def Spage(self):
        self.image1 = tk.PhotoImage(file="qrcode.png")
        tk.Label(self.tk, image = self.image1).grid(row = 0)
        tk.Button(self.tk , text="next",command= lambda : [self.switch_frame(), self.Tpage()]).grid(row = 1)

    def camThread(self):
        color = []
        panel = None
        while True:
            ret, color = self.cap.read()
            gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
            decoded = pyzbar.decode(gray)
            for d in decoded:
                x, y, w, h = d.rect
                barcode_data = d.data.decode("utf-8")
                barcode_type = d.type
                print(barcode_data, barcode_type)
                #go to certify page with info
                cv2.destroyAllWindows()
                self.switch_frame()
                self.Certify(barcode_data)
                return
            image = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            if panel is None:
                panel = tk.Label(self.tk,image = image)
                panel.grid(column =  1)
                panel.image = image
            else:
                panel.configure(image = image)
                panel.image = image
    def Tpage(self):
        tk.Label(self.tk, text = "ITEMS").grid(column = 0)
        thread_cap = threading.Thread(target=self.camThread, args = ())
        thread_cap.start()
        tk.Button(self.tk , text="FINISH SHOPPING ",command= lambda : [self.switch_frame(), self.Lpage()]).grid(row = 1)
    
    def Certify(self, data):
        tk.Button(self.tk , text="Confirm",command= lambda : [self.switch_frame(), self.AppendItem(data),self.Tpage()]).grid(column = 0)
        tk.Button(self.tk , text="NO",command= lambda : [self.switch_frame(), self.Tpage()]).grid(row = 1)
    
    def AppendItem(self, data):
        if data not in self.item:
            self.item[data] = 0
        else:
            self.time[data] += 1

    def Lpage(self):
        #결제하는 부분을  여따 달고 
        #결제가 끝났으면 다시 처음 화면으로 돌아가게 하기
        pass 

if __name__ == "__main__":
    app = App()
    app.tk.mainloop()

