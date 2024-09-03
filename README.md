# Motorshot: 오토바이 헬멧 미착용 및 위협운전 탐지 컴퓨터비전 프로젝트

### 개요

이 프로젝트는 오토바이의 교통법 위반으로 인해 발생하는 사고 문제를 해결하기 위한 목적으로 설계되었습니다. 다양한 뉴스 기사와 데이터를 통해 볼 수 있듯이, 횡단보도에서의 사고, 인도 및 횡단보도 침범, 과속 및 난폭 운전 등 교통법을 위반하는 오토바이 운전으로 인해 심각한 사고들이 빈번하게 발생하고 있습니다. 이러한 문제는 보행자와 다른 운전자들의 안전을 심각하게 위협하고 있습니다.
프로젝트는 이러한 교통법 위반 행위의 심각성을 인식시키고, 법규 준수의 중요성을 강조하기 위한 캠페인이나 솔루션을 개발하는 것을 목표로 합니다. 궁극적으로는 오토바이 운전자들의 법규 준수율을 높이고, 이를 통해 사고를 줄여 보다 안전한 도로 환경을 조성하는 데 기여하고자 합니다.

### 주요 기능

* 헬멧 착용 여부 감지: Yolov8s 모델을 활용하여 오토바이 운전자의 헬멧 착용 상태를 실시간으로 감지합니다. 이를 통해 헬멧 미착용으로 인한 사고 위험을 줄이는 데 기여할 수 있습니다.
* 위험 운전 감지: Yolov8s 모델을 통해 오토바이의 앞바퀴 들기(윌리)와 지그재그 운전 등 위험한 운전 행위를 실시간으로 감지하여 경고합니다. 이 기능은 도로 안전을 향상시키는 데 중요한 역할을 합니다.
* 횡단보도 침범 감지: 오토바이가 횡단보도를 일정 시간 이상 침범했을 때 이를 실시간으로 감지하고 경고를 제공합니다. 이는 보행자의 안전을 보호하고 교통법규 준수를 강화하는 데 도움을 줍니다.

### 특징

* 실시간 감지: 오토바이의 헬멧 착용 여부와 위험 운전 행위를 실시간으로 감지하여 즉각적인 경고를 제공합니다.
* 다양한 위험 행위 감지: 헬멧 미착용뿐만 아니라 앞바퀴 들기, 지그재그 운전, 횡단보도 침범 등 다양한 위험 운전 패턴을 감지할 수 있습니다.
* 적응형 데이터 증강: 다양한 환경과 조건에서 정확한 감지를 위해 데이터 증강 기법을 적용하여 모델의 신뢰성을 높였습니다.

### 요구 사항

- Python 3.7 이상
- MongoDB 인스턴스

### 사용

* 프론트엔드

```bash
# 깃 클론
git clone https://github.com/Heeseon06/Motorshot_frontend_Project

# 프로젝트 루트 폴더에서 아래 실행(패키지 설치)
npm install

# 실행
npm start
```
* 백엔드

```bash
# 깃 클론
git clone https://github.com/Heeseon06/Motorshot_backend

# 실행
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

```


# 포트폴리오

![917ab1cda90918ceb58074243b46922f-0](https://github.com/user-attachments/assets/5979141b-fd1f-4efb-b13a-6c7878a26f4f)

<details>
  <summary>펼치기/접기</summary>

<!-- ![917ab1cda90918ceb58074243b46922f-0](https://github.com/user-attachments/assets/5979141b-fd1f-4efb-b13a-6c7878a26f4f) -->
![917ab1cda90918ceb58074243b46922f-1](https://github.com/user-attachments/assets/e7def550-79fa-47b2-96ef-7706e1aaaf70)
![917ab1cda90918ceb58074243b46922f-2](https://github.com/user-attachments/assets/779a7c6a-1721-454d-b178-d342c49187fe)
![917ab1cda90918ceb58074243b46922f-3](https://github.com/user-attachments/assets/f5881950-d618-4fba-877d-c46b294fd3f9)
![917ab1cda90918ceb58074243b46922f-4](https://github.com/user-attachments/assets/d6ba2e21-185d-4fe3-b86e-55dd7c6ce04a)
![917ab1cda90918ceb58074243b46922f-5](https://github.com/user-attachments/assets/c5055fe4-52a4-4d5a-b616-85d6b9dcfa5c)
![917ab1cda90918ceb58074243b46922f-6](https://github.com/user-attachments/assets/c6adc318-c5c9-4fa1-b1e0-0e21c3c7e406)
![917ab1cda90918ceb58074243b46922f-7](https://github.com/user-attachments/assets/b312deed-7386-4a70-8c4b-abbc396d7fb3)
![917ab1cda90918ceb58074243b46922f-8](https://github.com/user-attachments/assets/13e9240b-7ba2-485b-b1a6-6b7561ad0750)
![917ab1cda90918ceb58074243b46922f-9](https://github.com/user-attachments/assets/7b4a2bf4-7150-4bee-b263-70494b5577d2)
![917ab1cda90918ceb58074243b46922f-10](https://github.com/user-attachments/assets/150c094a-9708-4b2d-98ae-b145a91114e9)
![917ab1cda90918ceb58074243b46922f-11](https://github.com/user-attachments/assets/b8a3b892-07b7-4ef8-abd8-a0fdca573484)
![917ab1cda90918ceb58074243b46922f-12](https://github.com/user-attachments/assets/1c42a12e-8434-4057-ac48-771190fa1651)
![917ab1cda90918ceb58074243b46922f-13](https://github.com/user-attachments/assets/8584455b-7592-469b-ae65-f44651e31e58)
![917ab1cda90918ceb58074243b46922f-14](https://github.com/user-attachments/assets/2b745df2-e2d5-41c7-82e2-12519adf75df)
![917ab1cda90918ceb58074243b46922f-15](https://github.com/user-attachments/assets/7ee7af6c-52f9-4a2c-9ac6-d4f07fba6721)
![917ab1cda90918ceb58074243b46922f-16](https://github.com/user-attachments/assets/fb45a377-141d-4c70-993f-4d14d943dd7c)
![917ab1cda90918ceb58074243b46922f-17](https://github.com/user-attachments/assets/71933b91-fc70-4641-9975-01819cdd980f)
 
 </details>

<br>

# 사용 기술

* 프론트엔드
   * JavaScript
   * React

* 백엔드
   * FastAPI
   * Python

* 모델
   * YOLOv8
   * Pytorch

* 데이터베이스
  * MongoDB

* 협업
   * GitHub
   * Figma

## 파일 구조
```
Backend/
├── src/
│   ├── config/                 # 설정 파일
│   ├── controllers/            # 컨트롤러
│   ├── middleware/             # 미들웨어
│   ├── models/                 # 데이터베이스 모델 및 AI 모델
│   ├── routers/                # 라우트
│   ├── main.py                 # FastAPI 애플리케이션 진입점 파일
├── .env                        # 환경 변수 설정 파일
├── README.md                   # 프로젝트 설명 파일
```

# 작성자의 기여
