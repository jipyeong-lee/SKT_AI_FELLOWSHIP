# OCR

## Text Detection
### TextSnake
- MMOCR 라이브러리 활용
- 해당 모델의 아웃풋이 NER 모델의 인풋으로 들어가야하므로 맥락 부여를 위해 상대적으로 긴 텍스트가 들어가는 것이 좋다고 판단
- 라이브러리 기준 최신모델(DBNet++) 대비 긴 텍스트 형태 잘 잡아냄
![image](https://user-images.githubusercontent.com/77089771/200468695-4cd71875-d0f6-44b1-91a1-b72e90097160.png)


## Text Recognition
### PARSeq
- Scene Text Recognition 분야 SOTA
- 라틴어 계열 사전학습 모델만 존재
- AI HUB 야외 실제 촬영 한글 이미지 + AI HUB 공공행정문서 OCR 데이터 활용 한글 데이터셋 생성(약 180만건)
- 모델 구조 활용 한국어 데이터셋으로 학습
![image](https://user-images.githubusercontent.com/77089771/200469890-df2688b3-8e1c-45e7-83cc-cd9999e7975c.png)


## 아쉬운 점
### Text Detection
- Detection 모델 라이브러리 활용한 점
- inference time 상대적으로 느림 -> one-stage 기반 모델 구조 개선 및 SOTA 모델 구조 활용(YOLO 계열 구조 개선 목표)
### Text Recognition
- PARSeq 모델 구조 그대로 활용 -> ViT Encoder Layer 구조 : Swin Transformer Encoder 구조로 변경
- 데이터 수 사전학습 모델에 비해 적음 -> 데이터 셋 추가 
