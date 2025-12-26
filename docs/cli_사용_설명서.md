# CLI 사용 설명서 (v1.1.0)

| 메타데이터 | 내용 |
| :--- | :--- |
| **최종 수정일** | 2025-12-26 |
| **대상** | 개발자 (Electron 통합용) 및 고급 사용자 |
| **버전** | 1.1.0 (Architecture Refactored) |

---

## 📋 목차

1. [개요](#1-개요)
2. [공통 옵션](#2-공통-옵션)
3. [모드별 상세 사용법](#3-모드별-상세-사용법)
    - [3.1 Betinfo (배당 데이터)](#31-betinfo-배당-데이터)
    - [3.2 Flashscore (경기/메타데이터)](#32-flashscore-경기메타데이터)
4. [IPC 통신 규격 (중요)](#4-ipc-통신-규격-중요)
5. [종료 코드 (Exit Code)](#5-종료-코드-exit-code)
6. [데이터 저장 구조](#6-데이터-저장-구조)

---

## 1. 개요

본 크롤러는 명령줄 인터페이스(CLI)를 통해 제어되며, 모든 출력은 표준 출력(stdout) 및 표준 에러(stderr)를 통해 구조화된 메시지로 전달됩니다. 이 규격은 Electron UI와의 안정적인 결합을 목적으로 설계되었습니다.

---

## 2. 공통 옵션

| 옵션 | 상수명 | 기본값 | 설명 |
| :--- | :--- | :--- | :--- |
| `--mode` | `ARG_MODE` | (필수) | 실행 모드 (`betinfo`, `flashscore`) |
| `--headless` | `ARG_HEADLESS` | `True` | 브라우저 숨김 모드 (표시하려면 `--no-headless`) |
| `--output-dir` | `ARG_OUTPUT_DIR` | `./data` | 데이터 저장 경로 지정 |
| `--timeout` | `ARG_TIMEOUT` | `300` | 프로세스 강제 종료 대기 시간 (초) |
| `--debug` | `ARG_DEBUG` | `False` | 디버그 로그 출력 (stderr로 전달됨) |

---

## 3. 모드별 상세 사용법

### 3.1 Betinfo (배당 데이터)

프로토 배당률 정보를 회차별로 수집합니다.

| 옵션 | 설명 | 예시 |
| :--- | :--- | :--- |
| `--recent` | 최신 N개 회차 자동 수집 | `--recent=5` |
| `--rounds` | 특정 회차 목록 수집 (쉼표 구분) | `--rounds=2025050,2025051` |
| `--start-round`, `--end-round` | 회차 범위 수집 | `--start-round=2025040 --end-round=2025050` |

**실행 예시**
```bash
python main.py --mode=betinfo --recent=5 --headless
```

---

### 3.2 Flashscore (경기/메타데이터)

축구 경기 결과 및 리그/팀 메타데이터를 수집합니다.

| 옵션 | 설명 | 기본값 |
| :--- | :--- | :--- |
| `--task` | 작업 유형 (`matches`, `metadata`) | (필수) |
| `--url` | Flashscore 상세 URL | (추천) |
| `--season` | 수집 시즌 | `2025-2026` |
| `--fs-start-round` | 시작 라운드 (matches 전용) | 전체 |
| `--fs-end-round` | 종료 라운드 (matches 전용) | 전체 |
| `--checkpoint-interval` | 체크포인트 저장 간격 (라운드 단위) | `0` (비활성) |
| `--resume` | 중단 지점(Checkpoint)부터 재개 | `False` |

**실행 예시 (메타데이터 수집)**
```bash
# 순위표 URL에서 ID 자동 추출 지원
python main.py --mode=flashscore --task=metadata --url="https://www.flashscore.co.kr/soccer/england/premier-league/standings/#/OEEq9Yvp/standings/overall/"
```

**실행 예시 (과거 시즌 경기 데이터 수집)**
```bash
# URL에서 리그명과 경로 자동 추출 및 시즌 연도 매칭
python main.py --mode=flashscore --task=matches \
  --url="https://www.flashscore.co.kr/soccer/england/premier-league-2023-2024/results/" \
  --season="2023-2024" \
  --fs-start-round=1 --fs-end-round=17
```

**실행 예시 (최신 라운드 자동 수집 - Betinfo)**
```bash
python main.py --mode=betinfo --recent=3
```

---

## 4. IPC 통신 규격 (중요)

Electron UI는 stdout으로 출력되는 다음 접두사들을 파싱하여 상태를 업데이트해야 합니다.

### 4.1 메시지 접두사 (Prefix)

| 접두사 | 설명 | 데이터 형식 |
| :--- | :--- | :--- |
| `STATUS:` | 현재 작업 상태 변경 | `{TYPE}\|{VALUE}` |
| `PROGRESS:` | 작업 완료율 (%) | `0` ~ `100` |
| `DATA:` | 크롤링 결과 또는 중간 정보 | JSON 스트링 |
| `CHECKPOINT:` | 체크포인트 저장/삭제 알림 | `SAVED\|key` 또는 `CLEARED\|key` |
| `[LOG]` | 디버그 로그 (stderr 출력) | 텍스트 |

### 4.2 주요 상태(STATUS) 타입

| 타입 | 의미 | 예시 |
| :--- | :--- | :--- |
| `START` | 크롤링 전체 프로세스 시작 | `STATUS:START\|1735140000` |
| `COMPLETE` | 모든 작업 정상 완료 | `STATUS:COMPLETE\|1735140500` |
| `MODE` | 현재 실행 중인 상세 모드 | `STATUS:MODE|recent_5` |
| `COLLECTING_ROUND` | 현재 수집 중인 회차/라운드 번호 | `STATUS:COLLECTING_ROUND\|25` |
| `RESUME` | 중단 지점에서 재개됨 알림 | `STATUS:RESUME\|Resuming...` |

### 4.3 에러 형식 (ERROR)

`ERROR:{에러코드}\|{메시지}` 형식으로 출력됩니다.

| 코드 | 상수명 | 의미 |
| :--- | :--- | :--- |
| `1` | `ERROR_CODE_CONFIG` | CLI 인자 누락 또는 설정 파일 오류 |
| `2` | `ERROR_CODE_CRAWLING` | 페이지 파싱 실패 또는 네트워크 오류 |
| `3` | `ERROR_CODE_TIMEOUT` | 프로세스 허용 시간(Watchdog) 초과 |

---

## 5. 종료 코드 (Exit Code)

프로세스 종료 시의 `exitCode`를 사용하여 최종 성공 여부를 판별하세요.

- `0`: **SUCCESS** - 모든 작업이 성공적으로 완료됨.
- `1`: **CONFIG_ERROR** - 실행 인자가 잘못되었거나 설정 오류.
- `2`: **CRAWLING_FAILED** - 크롤링 중 치명적 오류 발생.
- `3`: **TIMEOUT** - 지정된 대기 시간을 초과하여 강제 종료됨.

---

## 6. 데이터 저장 구조

모든 데이터는 프로젝트 루트의 `data/` 디렉토리에 저장됩니다.

- **Betinfo**: `betinfo_proto_rate_{회차}.csv`
- **Flashscore Matches**: `flashscore_matches_{국가}_{리그}_{시즌}.csv`
- **Flashscore Metadata**:
    - `leagues.csv`: 리그 정보 (국가, 리그명, ID 등)
    - `teams.csv`: 팀 정보 (팀명, 이미지 경로 등)
    - `league_teams.csv`: 리그와 팀의 소속 관계 정보

---
*본 문서는 시스템 상수를 변경할 경우 함께 업데이트되어야 합니다.*
