# 인스타그램 콘텐츠 다운로더

엑셀/CSV 파일로 인스타그램 게시물을 일괄 다운로드하는 웹 애플리케이션

## 주요 기능

- 📊 **엑셀/CSV/Numbers 파일 지원** - 여러 파일 형식 지원
- 📸 **이미지 & 비디오 다운로드** - 모든 미디어 타입 지원
- 📝 **게시물 텍스트 저장** - 캡션을 `게시물.txt`로 저장
- 📁 **자동 폴더 정리** - `인스타 아이디/날짜/` 구조로 정리
- 📦 **ZIP 압축** - 모든 결과물을 ZIP 파일로 제공
- 📊 **실시간 진행률** - 다운로드 진행 상황 확인
- ⚠️ **실패 링크 추적** - 실패한 링크를 별도 파일로 저장

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd instagram_downloader
```

### 2. Python 패키지 설치

```bash
cd backend
pip install -r requirements.txt
pip install gallery-dl browser-cookie3
```

### 3. 인스타그램 쿠키 추출 (최초 1회)

**중요**: Chrome 브라우저에서 instagram.com에 로그인한 상태여야 합니다.

```bash
cd backend
python3 export_cookies.py
```

성공하면 `instagram_cookies.txt` 파일이 생성됩니다.

### 4. 서버 실행

```bash
# 백엔드 서버
cd backend
python3 app.py
```

서버가 `http://localhost:5001`에서 실행됩니다.

### 5. 프론트엔드 접속

브라우저에서 `frontend/index.html` 파일을 열거나:

```bash
cd frontend
python -m http.server 8000
```

그 후 `http://localhost:8000` 접속

## 사용 방법

### 1. 엑셀 파일 준비

다음 3개의 컬럼이 필요합니다:

| Link                                | Id    | Date         |
| ----------------------------------- | ----- | ------------ |
| https://www.instagram.com/p/ABC123/ | user1 | 2024-01-01   |
| https://www.instagram.com/p/XYZ789/ | user2 | 2024/01/02   |
| https://www.instagram.com/reel/...  | user3 | 2024년1월3일 |

**지원하는 날짜 형식:**

- `2024-01-01`, `2024/01/01`, `2024.01.01`
- `2024년01월01일`, `2024년 01월 01일`
- `24-01-01`, `01/01/2024`
- `20240101`

모든 날짜는 자동으로 `yy.mm.dd` 형식으로 변환됩니다.

### 2. 파일 업로드

1. 웹 페이지에서 파일 선택
2. "업로드 및 다운로드" 버튼 클릭
3. 진행 상황 확인
4. 완료되면 자동으로 ZIP 파일 다운로드

### 3. 결과물 확인

```
instagram_download_20241109_123456.zip
├── 실패한_링크.txt (실패한 경우에만)
├── user1/
│   └── 24.01.01/
│       ├── ABC123_1.jpg
│       ├── ABC123_2.jpg
│       └── 게시물.txt
└── user2/
    └── 24.01.02/
        ├── XYZ789_1.mp4
        └── 게시물.txt
```

## 문제 해결

### 쿠키 추출 실패

**증상**: `export_cookies.py` 실행 시 에러

**해결 방법**:

1. Chrome에서 instagram.com에 로그인되어 있는지 확인
2. `browser-cookie3` 재설치: `pip install --upgrade browser-cookie3`
3. Chrome을 완전히 종료 후 다시 시도

### 다운로드 실패

**증상**: 모든 링크가 실패

**원인 및 해결**:

1. **쿠키 만료**: `python3 export_cookies.py` 다시 실행
2. **Rate Limit**: 잠시 후 다시 시도 (인스타그램 제한)
3. **비공개 계정**: 공개 게시물만 다운로드 가능

### 진행률이 멈춤

**해결 방법**:

1. 브라우저 새로고침
2. 서버 재시작: `Ctrl+C` 후 `python3 app.py`

## 기술 스택

**Backend:**

- Flask (웹 서버)
- gallery-dl (인스타그램 다운로더)
- openpyxl (엑셀 파일 처리)
- browser-cookie3 (쿠키 추출)

**Frontend:**

- HTML/CSS/JavaScript
- Vanilla JS (프레임워크 없음)

## 제한 사항

- **비공개 계정**: 다운로드 불가
- **Rate Limit**: 시간당 약 200-500개 (계정에 따라 다름)
- **쿠키 유효기간**: 약 2-4주 (만료 시 재추출 필요)
- **파일 크기**: 대용량 다운로드 시 시간 소요

## 라이선스

개인 사용 목적으로만 사용하세요. 인스타그램 이용 약관을 준수해야 합니다.

## 주의사항

⚠️ 이 도구는 개인적인 백업 목적으로만 사용하세요.
⚠️ 타인의 콘텐츠를 무단으로 사용하거나 재배포하지 마세요.
⚠️ 인스타그램 이용 약관을 위반하지 않도록 주의하세요.
