from flask import Flask, render_template, request
import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

app = Flask(__name__)

# 모델 로드
model = joblib.load('../model_pipeline.pkl')

# 전체 성적 데이터 로드
data = pd.read_csv('../dataset/student-mat.csv', sep=';')
data['G_avg'] = data[['G1', 'G2', 'G3']].mean(axis=1)

# 입력 변수 이름 업데이트
feature_names = [
    'age', 'sex', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob',
    'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures',
    'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
    'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc',
    'Walc', 'health', 'absences', 'school'
]

# 수치형 변수 목록 업데이트
numeric_features = [
    'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
    'famrel', 'freetime', 'goout', 'Dalc', 'Walc',
    'health', 'absences'
]

# 성적 분포 시각화 함수
def create_distribution_plot(predicted_score):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['G_avg'], bins=20, kde=True, color='skyblue', label='성적 분포')
    plt.axvline(x=predicted_score, color='red', linestyle='--', label='예측된 성적')
    plt.title('전체 성적 분포에서의 예측된 성적 위치')
    plt.xlabel('성적')
    plt.ylabel('학생 수')
    plt.legend()
    plt.savefig('static/prediction_plot.png')
    plt.close()

# 백분위 계산 함수
def calculate_percentile(predicted_score):
    percentile = stats.percentileofscore(data['G_avg'], predicted_score, kind='rank')
    return percentile

# 홈 페이지
@app.route('/')
def home():
    return render_template('index.html')

import time

def create_distribution_plot(predicted_score):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['G_avg'], bins=20, kde=True, color='skyblue', label='Grade Distribution')
    plt.axvline(x=predicted_score, color='red', linestyle='--', label='Predicted Grade')
    plt.title('Position of Predicted Grade within Overall Grade Distribution')
    plt.xlabel('Grade')
    plt.ylabel('Number of Students')
    plt.legend()
    timestamp = int(time.time())
    filename = f'prediction_plot_{timestamp}.png'
    plt.savefig(f'static/{filename}')
    plt.close()
    return filename



# 예측 처리
@app.route('/predict', methods=['POST'])
def predict():
    input_data = {}
    for feature in feature_names:
        value = request.form.get(feature)
        if value is None or value == '':
            value = 0 if feature in numeric_features else 'unknown'
        input_data[feature] = value

    # 입력 데이터를 DataFrame으로 변환
    input_df = pd.DataFrame([input_data])

    # 수치형 변수 변환
    input_df[numeric_features] = input_df[numeric_features].apply(pd.to_numeric)

    # 예측 수행
    prediction = model.predict(input_df)[0]
    prediction = round(prediction, 2)

    # 백분위 계산
    percentile = calculate_percentile(prediction)
    percentile = round(percentile, 2)
   
    # 시각화 생성
    plot_filename = create_distribution_plot(prediction)

    return render_template('result.html', prediction=prediction, percentile=percentile, plot_filename=plot_filename)

    

if __name__ == '__main__':
    app.run(debug=True)
