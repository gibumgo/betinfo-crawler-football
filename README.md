# Football Data Crawler (Betinfo & Flashscore)

**Football Data Crawler**는 국내 'Betinfo'와 글로벌 'Flashscore'의 축구 경기 데이터 및 배당률, 리그 메타데이터를 안정적으로 수집하기 위한 고성능 Python 크롤러입니다.

최근 **Layered Architecture** 리팩토링을 통해 유지보수성을 극대화했으며, **Electron 애플리케이션 등 외부 프로세스와의 연동(IPC)**을 지원하는 강력한 CLI 인터페이스를 제공합니다.

---

## ✨ 주요 기능 (Features)

- **이중 수집 모드**:
  - **Betinfo**: 프로토(Proto) 회차별 배당률 및 경기 정보 수집
  - **Flashscore**: 전 세계 축구 리그의 경기 결과, 순위표, 팀 정보 등 상세 메타데이터 수집
- **하이브리드 파싱 아키텍처**:
  - `Selenium`: 동적 페이지 렌더링 및 네비게이션
  - `BeautifulSoup4`: 고속 정적 HTML 파싱 (기존 대비 속도 대폭 향상)
- **강력한 CLI 및 IPC**:
  - 자동화 파이프라인 구축을 위한 명령줄 인터페이스(CLI)
  - 외부 GUI(Electron 등) 연동을 위한 표준화된 IPC 통신 규약 준수 (RFC-004)
- **데이터 정합성**:
  - 도메인 주도 설계(DDD)에 기반한 엄격한 데이터 모델링 (`Match`, `League`, `Team`)
  - CSV 기반의 구조화된 데이터 저장

---

## 🛠️ 설치 방법 (Installation)

### 전제 조건
- Python 3.9 이상
- Google Chrome 브라우저 설치

### 1. 프로젝트 클론
```bash
git clone https://github.com/gibumgo/betinfo-crawler-football.git
cd betinfo-crawler-football
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

---

## 🚀 사용 방법 (Usage)

본 프로그램은 **대화형 모드(Interactive)**와 **CLI 모드(Command Line Interface)** 두 가지 방식을 지원합니다.

### 1. 대화형 모드 (Interactive Mode)
초보자나 단발성 수집에 적합합니다. 메뉴를 선택하여 간편하게 실행할 수 있습니다.

```bash
python main.py
```
*실행 후 화면의 안내에 따라 1(Betinfo) 또는 2(Flashscore)를 선택하고 필요한 정보를 입력하세요.*

### 2. CLI 모드 (Automation)
스크립트나 외부 프로그램에서 호출할 때 사용합니다. `--mode` 옵션으로 수집 대상을 지정합니다.

#### A. Betinfo 수집 (배당률)

**최신 5개 회차 자동 수집:**
```bash
python main.py --mode=betinfo --recent=5 --headless
```

**특정 회차 범위 수집:**
```bash
python main.py --mode=betinfo --start-round=2025040 --end-round=2025050
```

#### B. Flashscore 수집 (경기 및 메타데이터)

**리그/팀 메타데이터 수집:**
순위표 URL을 입력하면 리그 정보와 소속 팀 정보를 자동으로 추출합니다.
```bash
python main.py --mode=flashscore --task=metadata --url="https://www.flashscore.co.kr/soccer/england/premier-league/standings/#/OEEq9Yvp/standings/overall/"
```

**경기 결과 수집 (시즌별):**
과거 시즌 데이터를 수집할 때 유용합니다.
```bash
python main.py --mode=flashscore --task=matches \
  --url="https://www.flashscore.co.kr/soccer/england/premier-league-2023-2024/results/" \
  --season="2023-2024"
```

---

## 🔌 IPC 연동 가이드 (For Developers)

Electron 등 외부 프로세스에서 이 크롤러를 `subprocess`로 실행할 때, **표준 출력(stdout)**을 통해 진행 상황과 상태를 실시간으로 모니터링할 수 있습니다.

**출력 메시지 예시:**
```text
STATUS:START|1735140000
STATUS:MODE|betinfo
STATUS:COLLECTING_ROUND|2025040
PROGRESS:25
DATA:{"match_id": "12345", "home_team": "Arsenal", ...}
STATUS:COMPLETE|1735140500
```
*상세한 통신 규약은 [RFC-004 문서](./docs/rfc_004_process_integration.md)와 [CLI 매뉴얼](./docs/cli_사용_설명서.md)을 참고하세요.*

---

## 📂 프로젝트 구조

- `src/domain/`: 비즈니스 로직 및 데이터 모델
- `src/infrastructure/scraping/`: Selenium 및 BeautifulSoup 파싱 로직
- `src/presentation/`: CLI 파서 및 컨트롤러
- `docs/`: 상세 기술 문서 및 RFC

---

## 📝 라이선스

This project is for educational and research purposes.