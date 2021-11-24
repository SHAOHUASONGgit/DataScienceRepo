import torch
import pandas as pd
from flask import Flask, render_template, request
app = Flask(__name__)

def getLabels(labels):
    allLabels = []
    for data in labels:
        if data not in allLabels:
            allLabels.append(data)
    return allLabels
def classfy(input, allLabels):
    output = allLabels[input.index(max(input))]
    return output
def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset

@app.route('/',methods = ['POST', 'GET'])
def student():
   return render_template('input.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        toClassify = []
        for data in request.form.to_dict().items():
            if(data[1])=="":
                return render_template('input.html')
            else:
                toClassify.append(float(data[1]))
        net = torch.load("model.pkl")
        raw = list(net(torch.tensor(toClassify).float()))
        predction = classfy(raw, allLabels)
        result = str("这个品种应该是：" + predction)
        return render_template("result.html", result=result)
    return render_template('input.html')

if __name__ == '__main__':
    allData = dataReader('iris.csv')
    allLabels = getLabels((allData[:, 4]))
    net = torch.load("model.pkl")
    app.run()