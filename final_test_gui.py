import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk,Image 
import imutils
import pygame
import os 
import datetime
import cv2

pygame.mixer.init()

alarm_sound = pygame.mixer.Sound("alarm_main_1001.wav")

tracker = cv2.TrackerCSRT_create()
app = ctk.CTk()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app.geometry("720x480")
app.minsize(720,480)
app.title("Main_Windows")

imgg = Image.open("pattern.png")
imgg = imgg.resize((100,100),Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(imgg)


def start_webcam():
    camera = True  #set this True for webcam
    testt = 'Meet_Bard.mp4'
    alarm_on = False

    if camera:
        video = cv2.VideoCapture(0)
    else:
        video = cv2.VideoCapture(testt)

    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    timer = 1
    count = 0
    alarm_start_time = None

    # Create a log file for alarms
    log_file = open("alarm_log.txt", "w")

    # Read the first frame and select the ROI
    _, frame = video.read()
    frame = imutils.resize(frame, width=1024)
    BB = cv2.selectROI(frame, False)
    tracker.init(frame, BB)

    while True:
        _, frame = video.read()
        frame = imutils.resize(frame, width=1024)

        track_success, BB = tracker.update(frame)

        if track_success:
            top_left = (int(BB[0]), int(BB[1]))
            bottom_right = (int(BB[0] + BB[2]), int(BB[1] + BB[3]))
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 5)

            window_size = cv2.getWindowImageRect('Output')[2:4]
            if top_left[0] < 0 or top_left[1] < 0 or bottom_right[0] > window_size[0] or bottom_right[1] > window_size[1]:
                if not alarm_on:
                    alarm_sound.play(loops=-1)
                    alarm_on = True
                    alarm_start_time = datetime.datetime.now()
                    log_file.write("Alarm started at video timestamp: {}\n".format(video.get(cv2.CAP_PROP_POS_MSEC)))

            else:
                if alarm_on:
                    alarm_sound.stop()
                    alarm_on = False
                    alarm_stop_time = datetime.datetime.now()
                    log_file.write("Alarm stopped at video timestamp: {}\n".format(video.get(cv2.CAP_PROP_POS_MSEC)))
        
        if timer == 0:
            roi = frame[int(BB[1]):int(BB[1] + BB[3]), int(BB[0]):int(BB[0] + BB[2])]
            cv2.imwrite('dataset/roi{}.png'.format(count), roi)
            count += 1

            timer = 1

            timer -= cv2.waitKey(1) & 0xff == ord('q')


        cv2.imshow('Output', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    log_file.close
    video.release()
    pygame.quit()
    cv2.destroyAllWindows()

file_path = ""

def browse_video_file():
    file_path = filedialog.askopenfilename()
    print("selected_file_path",file_path)
    dialogue_for_selection(file_path)


def dialogue_for_selection(file_dict):
    camera = False  #set this True for webcam
    testt = file_dict
    alarm_on = False

    if camera:
        video = cv2.VideoCapture(0)
    else:
        video = cv2.VideoCapture(testt)

    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    timer = 1
    count = 0
    alarm_start_time = None

    # Create a log file for alarms
    log_file = open("alarm_log.txt", "w")

    # Read the first frame and select the ROI
    _, frame = video.read()
    frame = imutils.resize(frame, width=1024)
    BB = cv2.selectROI(frame, False)
    tracker.init(frame, BB)

    while True:
        _, frame = video.read()
        frame = imutils.resize(frame, width=1024)

        track_success, BB = tracker.update(frame)

        if track_success:
            top_left = (int(BB[0]), int(BB[1]))
            bottom_right = (int(BB[0] + BB[2]), int(BB[1] + BB[3]))
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 5)

            window_size = cv2.getWindowImageRect('Output')[2:4]
            if top_left[0] < 0 or top_left[1] < 0 or bottom_right[0] > window_size[0] or bottom_right[1] > window_size[1]:
                if not alarm_on:
                    alarm_sound.play(loops=-1)
                    alarm_on = True
                    alarm_start_time = datetime.datetime.now()
                    log_file.write("Alarm started at video timestamp: {}\n".format(video.get(cv2.CAP_PROP_POS_MSEC)))

            else:
                if alarm_on:
                    alarm_sound.stop()
                    alarm_on = False
                    alarm_stop_time = datetime.datetime.now()
                    log_file.write("Alarm stopped at video timestamp: {}\n".format(video.get(cv2.CAP_PROP_POS_MSEC)))
        
        if timer == 0:
            roi = frame[int(BB[1]):int(BB[1] + BB[3]), int(BB[0]):int(BB[0] + BB[2])]
            cv2.imwrite('dataset/roi{}.png'.format(count), roi)
            count += 1

            timer = 1

            timer -= cv2.waitKey(1) & 0xff == ord('q')


        cv2.imshow('Output', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    log_file.close
    video.release()
    pygame.quit()
    cv2.destroyAllWindows()


def main_new_windows():
    
    topl = ctk.CTkToplevel()
    topl.geometry("600x400")
    topl.title("Second_Window")

    testframe_main = ctk.CTkFrame(master = topl)
    testframe_main.pack(padx = 10,pady=20,fill = "both",expand = True)

    #labell = ctk.CTkLabel(testframe_main,image=bg_image)
    #labell.pack(fill="both",expand = True)

    testbuttonI = ctk.CTkButton(master=testframe_main,text = "On Webcam",command = start_webcam,hover = True)
    testbuttonI.pack(side='left',expand = True)
    testbuttonII = ctk.CTkButton(master=testframe_main,text = "Over Existing Video",command = browse_video_file,hover = True)
    testbuttonII.pack(side='left',expand = True)

    topl.mainloop()


my_image = ctk.CTkImage(light_image = Image.open("pattern.png"),dark_image=Image.open("pattern.png"),size = (720,480))

testframebehind = ctk.CTkFrame(master=app)
testframebehind.place(x=0,y=0)

imagelabel = ctk.CTkLabel(master = testframebehind,image=my_image)
imagelabel.pack()

testframe = ctk.CTkFrame(app,fg_color="transparent",bg_color="transparent")
testframe.pack(padx=10,pady=20,fill="both",expand = True)


label1 = ctk.CTkLabel(master=testframe,text = "Object Tracker",font = ("Times 24",36, "bold"),underline = 1,fg_color = "transparent",bg_color="transparent")
label1.pack(padx=10,pady=20,expand = True)

fakelabel = ctk.CTkLabel(master=testframe,text = "Welcome!",font=("Helvetica",18,"bold"))
fakelabel.pack(padx=10,pady=20,fill="x",expand = True)


button1 = ctk.CTkButton(master = testframe,text="Press Me to open new window",command=main_new_windows,hover=True)
button1.pack(padx=10,pady=20,expand = True)


app.mainloop()