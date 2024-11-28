import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
#import matplotlib.pyplot as plt
from tkinter import font
import numpy as np
import time
import os


class Application(tk.Frame):
    def __init__(self, master, video_source=0):
        super().__init__(master)

        os.makedirs('./image', exist_ok=True)

        self.master.geometry("1400x700")
        self.master.title("Tkinter with Video Streming and Capture")

        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=15, weight="bold" )

        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )

        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        self.create_widgets()

        self.delay = 15
        self.update()

    def create_widgets(self):
        self.frame_cam = tk.LabelFrame(self.master, text = '起動中', font=self.font_frame)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid_propagate(0)

        self.frame_cam2 = tk.LabelFrame(self.master, text = '取込画像', font=self.font_frame)
        self.frame_cam2.place(x = 700, y = 10)
        self.frame_cam2.configure(width = self.width+30, height = self.height+50)
        self.frame_cam2.grid_propagate(1)

        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)

        self.canvas2 = tk.Canvas(self.frame_cam2)
        self.canvas2.configure(width=self.width, height=self.height)
        self.canvas2.grid(column=0, row=0, padx=10, pady=10)

        self.frame_btn = tk.LabelFrame( self.master, font=self.font_frame )
        self.frame_btn.place( x=10, y=540 )
        self.frame_btn.configure( width=200, height=100 )
        self.frame_btn.grid_propagate( 0 )

        """
        self.btn_snapshot = tk.Button( self.frame_btn, text='トリガー', font=self.font_btn_big)
        self.btn_snapshot.configure(width = 10, height = 1, command=self.press_snapshot_button, anchor=tk.CENTER )
        self.btn_snapshot.grid(column=0, row=0, padx=10, pady=15)
        """

        self.frame_btn = tk.LabelFrame( self.master, font=self.font_frame )
        self.frame_btn.place( x=10, y=540 )
        self.frame_btn.configure( width=200, height=100 )
        self.frame_btn.grid_propagate( 0 )

        self.btn_snapshot = tk.Button( self.frame_btn, text='トリガー', font=self.font_btn_big)
        self.btn_snapshot.configure(width = 10, height = 1, command=self.press_snapshot_button, anchor=tk.CENTER )
        self.btn_snapshot.grid(column=0, row=0, padx=10, pady=15)

        self.slider = tk.LabelFrame( self.master, font=self.font_frame )
        self.slider.place( x=1100, y=540)
        self.slider.configure( width=310, height=110 )
        self.slider.grid_propagate( 0 )

        self.btn_fillter = tk.Button( self.slider, text='フィルター', font=self.font_btn_big)
        self.btn_fillter.configure(width = 15, height = 1, command=self.press_fillter_button)
        self.btn_fillter.grid(column=0, row=0, padx=0, pady= 0)

        #領域範囲を選択するために数値を入力出来る箇所を作成
        self.region1_x = tk.Entry(self.master, width=5, font=20)
        self.region1_x.place(x=1000,y=540)

        self.region1_y = tk.Entry(self.master, width=5, font=20)
        self.region1_y.place(x=1050,y=540)

        self.region2_x = tk.Entry(self.master, width=5, font=20)
        self.region2_x.place(x=1000,y=570)

        self.region2_y = tk.Entry(self.master, width=5, font=20)
        self.region2_y.place(x=1050,y=570)



    def update(self):
        #Get a frame from the video source
        a, frame = self.vcap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)

        self.master.after(self.delay, self.update)


    def press_snapshot_button(self):
        path = 'image'
        dir = './image'
        now = time.strftime('%y%m%d_%H%M%S')
        self.base_name = os.path.join(path, now)

        _, frame = self.vcap.read()
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        self.canvas2.create_image(0, 0, image=self.photo2, anchor=tk.NW)

        image_value = sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir))
        image_value += 1
        print(image_value)

        if image_value > 20:
            directry = os.listdir(path)
            directry.sort()
            filename = directry.pop(0)
            os.remove(f'{dir}/{filename}')
            cv2.imwrite(f'{self.base_name}.jpg', cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

        cv2.imwrite(f'{self.base_name}.jpg', cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()


    def press_fillter_button(self):
        #import matplotlib.pyplot as plt
        #path = 'image'
        #dir = './image'
        #directry = os.listdir(path)
        #filename = directry.pop(0)
        #img = cv2.imread(f'{dir}/{filename}')

        x_1 = int(self.region1_x.get())
        y_1 = int(self.region1_y.get())
        x_2 = int(self.region2_x.get())
        y_2 = int(self.region2_y.get())

        self.canvas2.create_rectangle(x_2, y_2, x_1, y_1, fill="", outline='black')
        
        path = 'image'
        dir = '/image'
        directry = os.listdir(path)
        image = directry.pop(0)
        print(image)
        image = cv2.imread(f'./image/{image}')
        #img = image[200:100, 10:20]
        #image[400:300, 210:220] = img
        #b,g,r = cv2.split(image)
        #print(b,g,r)
    
        
        
        '''
        img_trim = image[10:20, 200:100]
        img_trim = cv2.cvtColor(img_trim, cv2.COLOR_BGR2RGB)
        plt.imshow(img_trim)
        plt.show()
        '''
        
        #cv2.imshow('original', img)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()


