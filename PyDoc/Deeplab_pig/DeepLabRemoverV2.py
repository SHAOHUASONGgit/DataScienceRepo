#基于python3.8.7
#pip install tensorflow==2.5.0
#pip install keras-preprocessing
#pip install numpy
#pip install opencv-python
#pip install pillow
import tensorflow._api.v2.compat.v1 as tf
from keras.preprocessing.image import img_to_array, array_to_img
import numpy
import cv2
import os
import tkinter
from tkinter import filedialog
import threading
tf.disable_v2_behavior()

#窗口
window = tkinter.Tk()
window.title("Remover")
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

#提取
def Remove():
    filein = DirectoryGetter(1)
    fileout = DirectoryGetter(2)
    for Photo in os.listdir(filein):
        print(Photo)
        rawimg = cv2.imread(str(filein) + "/" + Photo)
        height, width, channels = rawimg.shape
        img = cv2.resize(rawimg,(640,480))
        img = img_to_array(img)
        img = numpy.expand_dims(img, axis=0).astype(numpy.uint8)
        sess = tf.Session()
        output = tf.import_graph_def(graph_def, input_map={"ImageTensor:0": img}, return_elements=["SemanticPredictions:0"])
        result = sess.run(output)[0]
        result = numpy.swapaxes(result, 0, 2)
        result = numpy.swapaxes(result, 0, 1)
        result = array_to_img(numpy.uint8(result*100))
        result = cv2.cvtColor(numpy.asarray(result),cv2.COLOR_RGB2BGR)
        result = cv2.resize(result,(width,height))
        result = cv2.bitwise_and(result, rawimg)
        cv2.imwrite(str(fileout) + "/" + Photo, result)#输出图像路径(初步)

#提取线程
def RemoveFun():
    thread = threading.Thread(target=Remove)
    thread.setDaemon(True)
    thread.start()

#读模型
f = open("frozen_inference_graph_pig.pb", "rb")
graph_def = tf.GraphDef()
graph_def.ParseFromString(f.read())

#输入栏
InputBar = tkinter.Entry(window, show = None)
InputBar.grid(row = 0, column = 0)
OutputBar = tkinter.Entry(window, show = None)
OutputBar.grid(row = 1, column = 0)

#按钮
InputButton = tkinter.Button(window, text='输入文件夹', font=('Arial', 12), width=10, command = lambda : DirectoryReader(1))
InputButton.grid(row = 0,column = 1)
OutputButton = tkinter.Button(window, text='输出文件夹', font=('Arial', 12), width=10, command = lambda : DirectoryReader(2))
OutputButton.grid(row = 1,column = 1)
RemoveButton = tkinter.Button(window, text='提取', font=('Arial', 12), command = RemoveFun)
RemoveButton.grid(row = 2,column = 0, columnspan = 2)
window.mainloop()