import numpy as np
import cv2
import os
import tkinter
import threading
from tkinter import filedialog

#窗口
window = tkinter.Tk()
window.title("DarkGetter")
window.resizable(width=False, height=False)

#读取文件夹
def DirectoryReader(tag):
    global file_path
    if tag == 1 :
        file_path = tkinter.filedialog.askdirectory()
        InputBar.delete(0, len(str(file_path)))
        InputBar.insert(0, file_path)
    if tag == 2 :
        file_path = tkinter.filedialog.askdirectory()
        OutputBar.delete(0, len(str(file_path)))
        OutputBar.insert(0, file_path)

#获取文件夹
def DirectoryGetter(tag):
    if tag == 1 :
        return str(InputBar.get())
    if tag == 2 :
        return str(OutputBar.get())

def darkGetter():
    filein = DirectoryGetter(1)
    fileout = DirectoryGetter(2)
    for Photo in os.listdir(filein):
        image = cv2.imread(str(filein) + "/" + Photo)
        B, G, R = cv2.split(image)
        totalAverage = (np.average(B) + np.average(G) + np.average(R)) / 3
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
        output = []
        for channel in [B, G, R]:
            if(np.average(channel)>totalAverage):
                afterChannel = cv2.erode(channel, kernel, iterations=1)
            else:
                afterChannel = cv2.dilate(channel, kernel, iterations=1)
            output.append(afterChannel)
        cv2.imwrite(str(fileout) + "/B" + Photo, output[0])
        cv2.imwrite(str(fileout) + "/G" + Photo, output[1])
        cv2.imwrite(str(fileout) + "/R" + Photo, output[2])


def darkGetterFun():
    thread = threading.Thread(target=darkGetter)
    thread.setDaemon(True)
    thread.start()

#输入栏
InputBar = tkinter.Entry(window, show = None)
InputBar.grid(row = 0, column = 0)
OutputBar = tkinter.Entry(window, show = None)
OutputBar.grid(row = 1, column = 0)

#按钮
InputButton = tkinter.Button(window, text='Input Folder', font=('Arial', 12), width=10, command = lambda : DirectoryReader(1))
InputButton.grid(row = 0,column = 1)
OutputButton = tkinter.Button(window, text='Output Folder', font=('Arial', 12), width=10, command = lambda : DirectoryReader(2))
OutputButton.grid(row = 1,column = 1)
RemoveButton = tkinter.Button(window, text='Start', font=('Arial', 12), command = darkGetterFun)
RemoveButton.grid(row = 2,column = 0, columnspan = 2)
window.mainloop()