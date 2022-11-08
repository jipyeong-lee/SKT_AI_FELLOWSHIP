# NER(Name Entity Recognition)

## Dataset
1. KLUE-NER Dataset
- 사람(PS), 위치(LC), 기관(OG), 날짜(DT), 시간(TI), 수량(QT)
- 총 13가지 tag
![image](https://user-images.githubusercontent.com/77089771/200480987-3589538e-69fd-4df0-a951-0441586a935d.png)

2. 한국해양대학교 자연연어처리연구실 NER Dataset
- 개체이름 / 시간표현 / 수량표현
- 인명, 지명, 기관명, 기타 / 날짜, 시간, 기간 / 통화, 비율, 기타 수량 표현
- 총 21가지 tag
![image](https://user-images.githubusercontent.com/77089771/200483945-90ff50f3-1c2b-4d78-b961-6a05bfdca698.png)


## Model
### KoELECTRA
![image](https://user-images.githubusercontent.com/77089771/200484907-cbb57131-4f1e-4900-934b-481f1e60e19f.png)
1. 기존 Pre-trained 모델을 사용한 Tokenizing이 아닌 음절 단위로 Tokenizing 후 학습
   - Pre-trained Tokenizer에서 OOV 문제 최소화 (음절 단위는 대부분 Corpus에 포함되기 때문)
2. 데이터 셋의 모든 라벨을 사용한 경우(13, 21개)와 필요한 라벨(5개)만을 사용한 경우 두 가지로 나눠서 실험 진행
   - 필요한 라벨만을 사용한 경우가 모델의 예측 난이도를 낮출 것으로 판단
   - 여러 실험 후 성능이 가장 좋았던 KoELECTRA 모델 사용
![image](https://user-images.githubusercontent.com/77089771/200487309-e300dbd2-4643-4868-9458-ab80d3cdbd36.png)

### PER
- 이름 태그는 별도의 전처리 안함

### LOC
- 장소 태그는 일정 장소를 유추할 수 있는 경우에만 장소 태그로 사용
- 개인 정보로 인식하기 전 수준은 주소로 인식되지 않도록 자세한 주소 구조에 집중하도록 학습
- Dataset에 장소(LOC) 태그 데이터  주소 구조(주소 / 지번주소 / 도로명주소 / 관할주민센터)로 랜덤 대체
  ex) 00도 000시 000로 000 (개인 정보라고 인식할 수 있는 단위)
  - 전처리 용이성 차이로 한국해양대학교 자연언어처리연구실 NER Dataset 최종 데이터셋 선정
  - KLUE-NER 데이터셋은 벤치마크 데이터로 사용
  ![image](https://user-images.githubusercontent.com/77089771/200487826-89d54756-0e22-460a-bcae-e41d4b03d319.png)

