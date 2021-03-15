from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox
import tkinter.filedialog
import os
import uuid
import face_recognition
import cv2


class Picture(object):
    def __init__(self, init_window_name):
        self.window = init_window_name
        self.image_path = []
        self.img_num = 0
        self.welcome_path = './welcome.png'  # 初始化图片

    def init_window(self):
        self.window.geometry('800x520+500+100')
        self.window.resizable(0, 0)  # 防止用户调整尺寸
        self.window.title("人脸比对")
        self.menubar = Menu(self.window)
        self.aboutmenu = Menu(self.window, tearoff=0)
        self.menubar.add_cascade(label='关于', menu=self.aboutmenu)
        self.aboutmenu.add_command(label='版本号: 1.0')
        self.aboutmenu.add_command(label='作者: Humy')

        self.welcome = Label(self.window, text='人脸比对', fg='white', bg='#000000', font=('Arial', 12), width=34,
                             height=2).place(x=230, y=10)

        self.img_open1 = Image.open(self.welcome_path).resize((258, 258))
        self.image1 = ImageTk.PhotoImage(self.img_open1)
        self.label_img1 = Label(self.window, image=self.image1)
        self.label_img1.place(x=110, y=100)

        self.img_open2 = Image.open(self.welcome_path).resize((258, 258))
        self.image2 = ImageTk.PhotoImage(self.img_open2)
        self.label_img2 = Label(self.window, image=self.image2)
        self.label_img2.place(x=420, y=100)

        self.btn1 = Button(self.window, text='请选择图片', font=('Arial', 12), fg='white', width=10, height=1,
                           command=self.select_file1, bg='#000000')
        self.btn1.place(x=190, y=390)

        self.btn2 = Button(self.window, text='请选择图片', font=('Arial', 12), fg='white', width=10, height=1,
                           command=self.select_file2, bg='#000000')
        self.btn2.place(x=500, y=390)

        self.submit = Button(self.window, text='提交', font=('Arial', 12), fg='white', width=10, height=1,
                             command=self.submit_cmd, bg='#000000')
        self.submit.place(x=350, y=390)

        self.show = StringVar()

        self.show_info = Label(self.window, textvariable=self.show,
                               fg='black', font=('Arial', 12), height=1).place(x=190, y=450)

        self.window.config(menu=self.menubar)
        self.window.mainloop()

    def select_file1(self):
        self.filename1 = tkinter.filedialog.askopenfilename()
        print(self.filename1)
        img_open = Image.open(self.filename1).resize((258, 258))
        image = ImageTk.PhotoImage(img_open)
        self.label_img1.configure(image=image)
        self.label_img1.image = image

    def select_file2(self):
        self.filename2 = tkinter.filedialog.askopenfilename()
        print(self.filename2)
        img_open = Image.open(self.filename2).resize((258, 258))
        image = ImageTk.PhotoImage(img_open)
        self.label_img2.configure(image=image)
        self.label_img2.image = image

    @staticmethod
    def resize_img(filename):
        img = cv2.imread(filename)
        h, w = img.shape[:2]
        ratio_w = w / 1280
        ratio_h = h / 720
        if ratio_w > 1 or ratio_h > 1:
            ratio = max(ratio_w, ratio_h)
            new_w = int(w / ratio)
            new_h = int(h / ratio)
            img = cv2.resize(img, (new_w, new_h))
            cv2.imwrite(filename, img)

    def submit_cmd(self):
        path1 = self.filename1
        path2 = self.filename2

        img1 = Image.open(path1).convert('RGB')
        img2 = Image.open(path2).convert('RGB')
        new_path1 = os.path.join(save_face_dir, self.random_name())
        new_path2 = os.path.join(save_face_dir, self.random_name())
        img1.save(new_path1)
        img2.save(new_path2)

        self.resize_img(new_path1)
        self.resize_img(new_path2)

        cmp_img1 = face_recognition.load_image_file(new_path1)
        cmp_img2 = face_recognition.load_image_file(new_path2)

        cmp_img1_encode = face_recognition.face_encodings(cmp_img1)[0]
        cmp_img2_encode = face_recognition.face_encodings(cmp_img2)[0]

        known_encode = [cmp_img1_encode]

        distance = face_recognition.face_distance(known_encode, cmp_img2_encode)

        prob = "%.2f" % distance
        info = "人脸距离为:{}，在阈值为0.5时，是否是同一个人：{}".format(str(prob), str(distance < 0.5))
        # info = "人脸距离为:" + str(prob)
        self.show.set(info)

    @staticmethod
    def random_name():
        filename = str(uuid.uuid4()) + '.jpg'
        return filename


if __name__ == "__main__":

    save_face_dir = './face_data'
    if not os.path.exists(save_face_dir):
        os.makedirs(save_face_dir)

    windows = Tk()
    picture = Picture(windows)
    picture.init_window()
