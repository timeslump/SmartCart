import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyzbar.pyzbar as pyzbar
import cv2
import time
import qrcode
class Main(object):
    def __init__(self):
        #camera
        self.cartnum = 1
        self.qr = qrcode.make(str(self.cartnum))
        self.cap = cv2.VideoCapture(-1)
        #firebase
        self.cred = cred = credentials.Certificate('/home/pi/smartcart-94000-firebase-adminsdk-pkypl-72ca0b7711.json')
        self.default_app = firebase_admin.initialize_app(cred, {'databaseURL':'https://smartcart-94000-default-rtdb.firebaseio.com/'})
        # y[0] should barcodeURL
        self.code = {y[0] : x for x, y in db.reference('Product').get().items()}
    def searchQR(self):
        while self.cap.isOpened():
            ret, img = self.cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            decoded = pyzbar.decode(gray)
            for d in decoded:
                x, y, w, h = d.rect
                barcode_data = d.data.decode("utf-8")
                barcode_type = d.type
            if barcode_data in self.code.keys():
                #go to certify page with info
                self.cap.release()
                cv2.destroyAllWindows()
                self.Certify(barcode_data, self.code[barcode-data])
                return
            # Make function about Click to quit
            #
            time.sleep(0.1)
        self.cap.release()
        cv2.destroyAllWindows()


main = Main()
main.init()