# RFC-004: 외부 프로세스 연동을 위한 안정성 및 통신 규약

| 메타데이터 | 내용 |
| :--- | :--- |
| **작성일** | 2025-12-25 |
| **상태** | Draft (제안) |
| **관련 이슈** | Electron Integration, Process Reliability |
| **키워드** | IPC, Timeout, Cleanup, Exit Code |

---

## 1. 개요 (Summary)
본 제안서는 파이썬 크롤러를 Electron 또는 Java 백엔드에서 **"신뢰할 수 있는 독립 프로세스(Reliable Sub-process)"**로 호출하기 위한 인터페이스 및 안전장치를 정의한다.
핵심 목표는 **"반드시 종료된다(Guaranteed Termination)"**와 **"명확하게 소통한다(Explicit Communication)"**는 보장을 제공하는 것이다.

---

## 2. 배경 및 문제점 (Motivation)

### 2.1 "블랙박스" 프로세스의 위험성
현재 `main.py`는 내부적으로 어떻게 동작하는지 외부에서 알 수 없다.
Electron 입장에서 파이썬 스크립트를 실행했을 때 다음과 같은 문제가 발생할 수 있다.

1.  **Zombie Process**: 어떤 이유로 크롤러가 멈추었을 때(Hanging), Electron은 무한정 기다려야 한다.
2.  **Resource Leak**: 강제 종료 시 브라우저 인스턴스가 닫히지 않고 메모리에 남는다.
3.  **Silent Failure**: 에러가 발생했을 때 로그만 찍고 종료되면, Electron은 이것이 성공인지 실패인지 구분하기 어렵다.

---

## 3. 제안 상세 (Detailed Design)

### 3.1 프로세스 안정성 (Process Safety)

외부 시스템이 안심하고 호출할 수 있도록 2중 안전장치를 도입한다.

#### A. 타임아웃 Watchdog (Guaranteed Termination)
OS 종속적인 `signal` 대신, **별도의 Watchdog 스레드**를 사용하여 일정 시간이 지나면 프로세스를 강제로 종료시킨다.

```python
# 개념 증명 코드 (Watchdog)
def watchdog(timeout_sec):
    time.sleep(timeout_sec)
    sys.stderr.write("FATAL: Timeout reached. Force killing process.\n")
    os._exit(3) # 강제 종료 코드 3 반환
```

#### B. 리소스 정리 보장 (Cleanup Guarantee)
정상 종료든 에러 종료든, 브라우저 리소스는 반드시 반환되어야 한다.

```python
try:
    crawler.run()
finally:
    try:
        if 'driver' in locals(): driver.quit()
    except Exception:
        pass # 이미 죽은 드라이버는 무시
```

---

### 3.2 통신 프로토콜 (Communication Protocol)

표준 출력(stdout)을 파싱 가능한 형태의 메시지 버스로 사용한다.

| 메시지 타입 | 포맷 (Format) | 설명 |
| :--- | :--- | :--- |
| **상태** | `STATUS:START\|{timestamp}` | 작업 시작 알림 |
| **상태** | `STATUS:COMPLETE\|{timestamp}` | 작업 완료 알림 |
| **진행률** | `PROGRESS:{percent}` | 0~100 사이 정수 (UI 표시용) |
| **데이터** | `DATA:{json_string}` | 최종 결과 데이터 (JSON) |
| **에러** | `ERROR:{code}\|{message}` | 치명적 오류 발생 시 |

> **규칙**: 일반 디버깅 로그(`print`)는 이 포맷을 따르지 않으므로, Electron 파서는 위 접두어(Prefix)가 없는 라인은 무시하거나 일반 로그로 처리한다.

---

### 3.3 종료 코드 규약 (Exit Codes)

프로세스의 종료 상태를 명확히 구분하여 Electron이 후속 조치를 취할 수 있게 한다.

| 코드 | 의미 | Electron 대응 가이드 |
| :--- | :--- | :--- |
| **0** | **성공 (Success)** | 결과 데이터(`DATA:...`) 파싱 후 처리 |
| **1** | **일반 에러** | 설정 오류, 파일 없음 등. 사용자에게 알림. |
| **2** | **크롤링 실패** | 네트워크 오류, DOM 변경 등. 재시도 로직 수행 가능. |
| **3** | **타임아웃 (Timeout)** | Watchdog에 의한 강제 종료. 리소스 정리 확인 필요. |

---

## 4. 환경 설정 및 인자 (Configuration)

### 4.1 우선순위 (Priority)
설정값은 다음 우선순위에 따라 적용된다.

1.  **CLI Arguments**: 실행 시 전달된 인자 (최우선)
2.  **Environment Variables**: `os.environ` (Docker/CI 환경)
3.  **Config File**: `config.json` 또는 `config.py` (기본값)

### 4.2 CLI 인자 예시
`argparse`를 사용하여 표준화된 인자를 받는다.

```bash
python main.py --mode=daily --date=2024-01-01 --timeout=300 --headless
```

---

## 5. 결론
이 문서는 파이썬 크롤러와 외부 시스템(Electron/Java) 간의 **"계약서(Contract)"**이다.
이 규약을 준수함으로써, 파이썬 프로세스는 언제든 호출하고 버릴 수 있는 안전한 마이크로서비스 모듈이 된다.
