# 십자말풀이 퍼즐 자동생성 서비스

십자말풀이 퍼즐을 국립국어원 우리말샘의 사전 데이터 속 단어를 추출해 자동으로 만들어주는 서비스입니다!

---

## 서비스 제공 기능

- 퍼즐 자동 생성
- 퍼즐 풀이
- 타인이 풀이했던 퍼즐 풀이
- 로그인 및 내가 풀이한 퍼즐 수 확인

<div align="center">
  <img src="https://github.com/user-attachments/assets/8ee628a3-d7e4-4d64-898c-0e015412aa2c" alt="image1" width="30%">
  <img src="https://github.com/user-attachments/assets/729f5b81-f675-472a-ad0b-033a50e91957" alt="image2" width="30%">
  <img src="https://github.com/user-attachments/assets/6cdf598a-929a-4602-a58d-2a123dc89799" alt="image3" width="30%">
</div>

---

## 사용 기술 스택

<div align=left> 
  <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" width=100 height=50/>
</div>

---

### 퍼즐 생성 기능 성능 개선

초기에 작성한 브루트한 퍼즐 생성 기능의 성능이 저조해 개선
1. 로직 개선으로 DB 호출 빈도 ⬇
    - 단어 20개 배치에 4.9초에서 2.6초로 약 45% 성능 개선
3. 쿼리 실행 계획 확인 후 단어 테이블 인덱스 생성
    - 단어 탐색 쿼리 튜닝 추가로 개별 단어 조회 시 0.25초에서 0.015초로 약 94% 성능 향상
    - 인덱스 생성 이후 단어 28~29개 배치에 8.5초에서 3.4초로 약 60% 성능 향상

### 테스트 성능 개선

퍼즐 생성 엔드포인트 테스트에 단어 정보가 필요한 상황 발생. <br>
테스트 케이스 독립성 부여를 위해 TEST DB 초기화 시 단어 테이블은 SKIP하는 로직 도입.
![image](https://github.com/user-attachments/assets/952adb7d-ade2-48ec-bad3-7154b29f09d7)

단어 정보가 필요한 테스트 케이스의 경우 단일 케이스 당 1분 이상 세팅에 소요되던 것을 제거할 수 있었음. <br>

#### 관련 링크

[Blog](https://velog.io/@taegong_s/series/%EC%8B%AD%EC%9E%90%EB%A7%90%ED%92%80%EC%9D%B4-%EA%B2%8C%EC%9E%84)

