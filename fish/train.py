import os
from dataclasses import dataclass
import base64
from io import BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score, roc_curve


@dataclass
class Data:
    X_train : np.ndarray
    X_test : np.ndarray
    Y_train : np.ndarray
    Y_test : np.ndarray

    @classmethod
    def load(DataClass, filename):
        return Data(**np.load(filename))


def train(data):
    model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1_000)
    model.fit(data.X_train, data.Y_train)

    return model


def evaluate(model, data):
    # Prepare ROC data
    Y_train_hat = model.predict_proba(data.X_train)[:, 1]
    Y_test_hat = model.predict_proba(data.X_test)[:, 1]
    train_auc = roc_auc_score(data.Y_train, Y_train_hat)
    test_auc = roc_auc_score(data.Y_test, Y_test_hat)

    # Create ROC plot
    fig, ax = plt.subplots()
    fpr, tpr, _ = roc_curve(data.Y_train, Y_train_hat)
    ax.plot(fpr, tpr)
    fpr, tpr, _ = roc_curve(data.Y_test, Y_test_hat)
    ax.plot(fpr, tpr)
    ax.plot([0, 1], [0, 1], c='grey', linestyle='dotted')
    ax.set_title('ROC Curve')
    ax.legend([
        f'Train AUC {train_auc:0.3f}',
        f'Test AUC {test_auc:0.3f}',
    ], loc='lower right')

    # Encode ROC plot as base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img1 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    # Scatter plot for samples
    fig, ax = plt.subplots()
    colors = np.array(["#377eb8", "#ff7f00"])
    ax.scatter(data.X_train[:100, 0], data.X_train[:100, 1], color=colors[data.Y_train[:100]])
    
    # Encode scatter plot as base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img2 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    # Prepare HTML document
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Evaluation Results</title>
    </head>
    <body>
        <h1>Model Evaluation</h1>
        <h2>ROC Curve</h2>
        <img src="data:image/png;base64,{img1}" alt="ROC Curve">
        <h2>Data Sample</h2>
        <img src="data:image/png;base64,{img2}" alt="Data Sample">
        <h3>Test AUC: {test_auc:0.3f}</h3>
    </body>
    </html>
    """

    # Save HTML to a file
    filename = 'data/evaluation.html'
    with open(filename, 'w') as f:
        f.write(html_content)
    print(f"saved evaluation report to {filename}")

def save(model):
    filename = 'data/moon_model.v1.joblib'
    joblib.dump(model, filename)
    print(f"saved model to {filename}")

if __name__ == '__main__':
    data = Data.load("data/moon_data_1000_500.npz")
    model = train(data)
    evaluate(model, data)
    save(model)
