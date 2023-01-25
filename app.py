import pandas as pd
import numpy as np
from flask import Flask, request, render_template


app = Flask(__name__)


def getPredict():

    order = request.form['orderdate']
    print(order)
    data = pd.read_csv(
        'dataset/orders.csv')

    X = data.iloc[:, 2]  # mengambil data jumlah order
    Y = data.iloc[:, 4]  # mengambil data order lined number
    data = data.drop(labels=2, axis=0)

    # Building the model
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)

    num = 0
    den = 0

    # perulangan perhitungan XY dan X^2
    for i in range(len(X)):
        num += (X[i] - X_mean)*(Y[i] - Y_mean)
        den += (X[i] - X_mean)**2

    # perhitungan a dan b
    m = num / den
    c = Y_mean - m*X_mean
    order = int(order)

    Y_pred =1*(m*order + c)
    print(round(Y_pred))
    return render_template('index.html', prediction_text='jumlah order {} adalah  {}'.format(order, round(Y_pred)))

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        return render_template('index.html')


@app.route('/prediksi', methods=['POST'])
def predict():
    if (request.method == 'POST'):
        return getPredict()



if __name__ == '__main__':
     app.run(debug=True)