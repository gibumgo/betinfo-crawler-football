# Electron UI 통합 설계서

| 메타데이터 | 내용 |
| :--- | :--- |
| **최종 수정일** | 2025-12-26 |
| **대상** | Electron 개발자 및 시스템 통합 담당자 |
| **버전** | 1.0.0 |
| **프로젝트 상태** | Python CLI 완성 (90%), Electron 통합 준비 완료 |

---

## 📋 목차

1. [현황 분석](#1-현황-분석)
2. [통합 아키텍처](#2-통합-아키텍처)
3. [UI 설계](#3-ui-설계)
4. [구현 가이드](#4-구현-가이드)
5. [배포 전략](#5-배포-전략)

---

## 1. 현황 분석

### 1.1 Python 크롤러 현재 상태

**✅ 이미 구현 완료된 기능**

```
betinfo-crawler-football/
├── main.py                    # ✅ CLI 진입점 완성 (run_cli_mode 구현)
├── config.py                  # ✅ 시스템 상수 정의 완료
├── src/
│   ├── application/
│   │   └── services/          # ✅ BetinfoService, FlashscoreService, FlashscoreMetaService
│   ├── domain/                # ✅ Match, League, Team, LeagueTeam 도메인 모델
│   ├── infrastructure/
│   │   ├── repositories/      # ✅ CSV 저장 및 중복 제거 로직
│   │   ├── scraping/          # ✅ Selenium 기반 스크래퍼
│   │   └── storage/           # ✅ HistoryManager (실행 이력 관리)
│   ├── presentation/
│   │   └── controllers/       # ✅ CliBetinfoController, CliFlashscoreController
│   └── shared/
│       ├── ipc_messenger.py   # ✅ IPC 통신 프로토콜 구현
│       └── error_handler.py   # ✅ 에러 핸들링
└── docs/                      # ✅ CLI 사용 설명서, 리팩토링 보고서
```

**핵심 강점**
- **완전한 CLI 지원**: `--mode`, `--task`, `--url`, `--season` 등 모든 파라미터를 명령줄로 제어 가능
- **IPC 프로토콜 완비**: `STATUS`, `PROGRESS`, `ERROR`, `LOG` 메시지 구조화
- **환경 이식성**: `lxml` 의존성 제거로 Python 3.x만 있으면 실행 가능
- **데이터 무결성**: CSV 중복 제거, 히스토리 관리 자동화

### 1.2 Electron 통합 시 장점

| 항목 | 상태 | 비고 |
|:---|:---|:---|
| **CLI 인터페이스** | ✅ 완성 | argparse 기반, 모든 옵션 지원 |
| **IPC 통신** | ✅ 완성 | stdout/stderr 분리, 구조화된 메시지 |
| **에러 핸들링** | ✅ 완성 | Exit Code 규약 (0/1/2/3/99) |
| **진행률 보고** | ✅ 완성 | `PROGRESS:0~100` 메시지 전송 |
| **리소스 관리** | ✅ 완성 | finally 블록에서 Selenium 정리 |
| **히스토리 관리** | ✅ 완성 | `data/history.json`에 실행 이력 저장 |

**결론**: **Electron 통합을 위한 모든 기반이 이미 구축되어 있음**. Python 코드 수정 없이 바로 subprocess 연동 가능.

---

## 2. 통합 아키텍처

### 2.1 시스템 구조

```
┌─────────────────────────────────────────────────────────┐
│                   Electron UI Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Crawler Menu │  │ Progress Bar │  │ Result Viewer│  │
│  │              │  │              │  │              │  │
│  │ - Betinfo    │  │ Real-time    │  │ CSV Files    │  │
│  │ - Flashscore │  │ 0-100%       │  │ Preview      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕ child_process.spawn
                          ↕ stdout/stderr parsing
┌─────────────────────────────────────────────────────────┐
│                 Python Crawler Process                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ python3 main.py --mode betinfo --recent 3       │   │
│  │                 --headless --output ./data      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  [IPCMessenger] → stdout: STATUS/PROGRESS/DATA          │
│                → stderr: [LOG][LEVEL] messages          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 IPC 통신 프로토콜 (이미 구현됨)

**Python → Electron 메시지 포맷**

| 메시지 타입 | 포맷 | 예시 | 용도 |
|:---|:---|:---|:---|
| **시작** | `STATUS:START\|{message}` | `STATUS:START\|Betinfo Crawler Started` | 크롤링 시작 알림 |
| **완료** | `STATUS:COMPLETE\|{message}` | `STATUS:COMPLETE\|Task Finished` | 정상 완료 |
| **진행률** | `PROGRESS:{percent}` | `PROGRESS:45.0` | 프로그레스 바 업데이트 |
| **에러** | `ERROR:{code}\|{message}` | `ERROR:2\|Network timeout` | 에러 발생 |
| **로그** | `[LOG][{level}] {message}` | `[LOG][INFO] Collecting round...` | 디버그 로그 (stderr) |

**Exit Code 규약**

```python
# src/infrastructure/constants/error_codes.py (이미 정의됨)
ERR_SUCCESS = 0           # 정상 완료
ERR_INVALID_ARGUMENT = 1  # CLI 인자 오류
ERR_RUNTIME_FAILURE = 2   # 크롤링 실패 (네트워크, 파싱 등)
ERR_INTERRUPTED = 3       # 사용자 중단 (Ctrl+C)
ERR_TIMEOUT = 4           # 타임아웃 (향후 구현 예정)
```

### 2.3 명령어 예시

**Betinfo 수집**
```bash
python3 main.py --mode betinfo --recent 3
python3 main.py --mode betinfo --rounds "2025001,2025002,2025003"
python3 main.py --mode betinfo --start-round 2025001 --end-round 2025010
```

**Flashscore 경기 수집**
```bash
python3 main.py --mode flashscore --task matches \
  --url "https://www.flashscore.co.kr/soccer/england/premier-league/results/" \
  --season "2025-2026" \
  --fs-start-round 1 --fs-end-round 17
```

**Flashscore 메타데이터 수집**
```bash
python3 main.py --mode flashscore --task metadata \
  --url "https://www.flashscore.co.kr/soccer/england/premier-league/standings/#/OEEq9Yvp/standings/overall/" \
  --season "2025-2026"
```

---

## 3. UI 설계

### 3.1 메인 화면 레이아웃

```
┌─────────────────────────────────────────┐
│         Betinfo Crawler Manager          │
├─────────────────────────────────────────┤
│                                          │
│  📊 대시보드                              │
│     - 최근 수집 이력 (history.json 기반)  │
│     - 총 수집 경기 수                     │
│     - 마지막 수집 시간                    │
│                                          │
│  🎯 크롤러 실행                           │
│     ┌─────────────────────────────┐     │
│     │ 사이트 선택                   │     │
│     │  ○ Betinfo (배당 데이터)      │     │
│     │  ○ Flashscore (경기/메타)     │     │
│     └─────────────────────────────┘     │
│                                          │
│     [Betinfo 모드]                       │
│     ┌─────────────────────────────┐     │
│     │ ○ 최신 N개 회차               │     │
│     │   개수: [3]                   │     │
│     │ ○ 특정 회차 목록              │     │
│     │   회차: [2025001,2025002]     │     │
│     │ ○ 회차 범위                   │     │
│     │   시작: [2025001] 끝: [010]   │     │
│     └─────────────────────────────┘     │
│                                          │
│     [Flashscore 모드]                    │
│     ┌─────────────────────────────┐     │
│     │ 작업: ○ 경기  ○ 메타데이터    │     │
│     │ URL: [paste here]             │     │
│     │ 시즌: [2025-2026]             │     │
│     │ 라운드: [1] ~ [17] (선택)     │     │
│     └─────────────────────────────┘     │
│                                          │
│     [▶ 크롤링 시작]  [⏹ 중지]           │
│                                          │
│  📁 데이터 관리                           │
│     - CSV 파일 목록 (./data 스캔)        │
│     - 파일 미리보기                      │
│     - 엑셀 변환                          │
│                                          │
└─────────────────────────────────────────┘
```

### 3.2 실시간 진행 화면

```
┌─────────────────────────────────────────┐
│  크롤링 진행 중...                        │
│  ████████████░░░░░░░░░░░░  45.0%        │
│                                          │
│  📝 실시간 로그                           │
│  ┌────────────────────────────────────┐ │
│  │ STATUS:START|Betinfo Crawler...    │ │
│  │ [LOG][INFO] Auto-detecting top 3...│ │
│  │ [LOG][INFO] Detected latest 3...   │ │
│  │ STATUS:COLLECTING_ROUND|2025152    │ │
│  │ PROGRESS:33.3                      │ │
│  │ [LOG][INFO] ✅ 2025152: 150 saved  │ │
│  │ PROGRESS:66.6                      │ │
│  │ STATUS:COMPLETE|Task Finished      │ │
│  └────────────────────────────────────┘ │
│                                          │
│  [⏹ 중지]                                │
└─────────────────────────────────────────┘
```

### 3.3 데이터 뷰어

```
┌─────────────────────────────────────────┐
│  📁 수집된 데이터 목록                    │
│  ┌────────────────────────────────────┐ │
│  │ ✓ betinfo_proto_rate_2025152.csv   │ │
│  │   150건 | 2025-12-26 14:03         │ │
│  │ ✓ flashscore_matches_england_...   │ │
│  │   320건 | 2025-12-26 13:45         │ │
│  │ ✓ leagues.csv (메타데이터)          │ │
│  │   1건 | 2025-12-26 14:10           │ │
│  │ ✓ teams.csv (메타데이터)            │ │
│  │   20건 | 2025-12-26 14:10          │ │
│  └────────────────────────────────────┘ │
│                                          │
│  📊 미리보기: betinfo_proto_rate_...     │
│  ┌────────────────────────────────────┐ │
│  │ 회차│경기번호│리그    │홈팀  │원정팀│ │
│  │ 152│001    │프리미어│맨시티│리버풀│ │
│  │ 152│002    │라리가  │바르샤│레알  │ │
│  └────────────────────────────────────┘ │
│                                          │
│  [📥 엑셀 변환]  [🗑️ 삭제]  [🔄 새로고침]│
└─────────────────────────────────────────┘
```

---

## 4. 구현 가이드

### 4.1 Electron Main Process (TypeScript)

```typescript
// main.ts
import { spawn, ChildProcess } from 'child_process';
import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';

let crawlerProcess: ChildProcess | null = null;

// 크롤러 실행
ipcMain.handle('crawler:start', async (event, config) => {
  const args = buildCommandArgs(config);
  
  crawlerProcess = spawn('python3', ['main.py', ...args], {
    cwd: path.join(__dirname, '../python-crawler'),
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  // stdout 파싱
  crawlerProcess.stdout?.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.startsWith('STATUS:')) {
        const [type, value] = line.substring(7).split('|');
        event.sender.send('crawler:status', { type, value });
      } else if (line.startsWith('PROGRESS:')) {
        const percent = parseFloat(line.substring(9));
        event.sender.send('crawler:progress', percent);
      } else if (line.startsWith('ERROR:')) {
        const [code, message] = line.substring(6).split('|');
        event.sender.send('crawler:error', { code: parseInt(code), message });
      }
    });
  });

  // stderr 로그
  crawlerProcess.stderr?.on('data', (data) => {
    event.sender.send('crawler:log', data.toString());
  });

  // 종료 처리
  crawlerProcess.on('exit', (code) => {
    event.sender.send('crawler:exit', code);
    crawlerProcess = null;
  });
});

// 크롤러 중지
ipcMain.handle('crawler:stop', () => {
  if (crawlerProcess) {
    crawlerProcess.kill('SIGTERM');
    return true;
  }
  return false;
});

function buildCommandArgs(config: CrawlerConfig): string[] {
  const args = ['--mode', config.mode];
  
  if (config.mode === 'betinfo') {
    if (config.recent) {
      args.push('--recent', config.recent.toString());
    } else if (config.rounds) {
      args.push('--rounds', config.rounds);
    } else if (config.startRound && config.endRound) {
      args.push('--start-round', config.startRound);
      args.push('--end-round', config.endRound);
    }
  } else if (config.mode === 'flashscore') {
    args.push('--task', config.task);
    args.push('--url', config.url);
    args.push('--season', config.season);
    if (config.fsStartRound) args.push('--fs-start-round', config.fsStartRound.toString());
    if (config.fsEndRound) args.push('--fs-end-round', config.fsEndRound.toString());
  }
  
  if (config.headless) args.push('--headless');
  if (config.outputDir) args.push('--output-dir', config.outputDir);
  
  return args;
}

interface CrawlerConfig {
  mode: 'betinfo' | 'flashscore';
  recent?: number;
  rounds?: string;
  startRound?: string;
  endRound?: string;
  task?: 'matches' | 'metadata';
  url?: string;
  season?: string;
  fsStartRound?: number;
  fsEndRound?: number;
  headless?: boolean;
  outputDir?: string;
}
```

### 4.2 Renderer Process (React 예시)

```typescript
// CrawlerPanel.tsx
import React, { useState, useEffect } from 'react';

export function CrawlerPanel() {
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState<string[]>([]);
  const [status, setStatus] = useState<'idle' | 'running' | 'complete' | 'error'>('idle');

  useEffect(() => {
    // IPC 리스너 등록
    window.electron.on('crawler:progress', (percent: number) => {
      setProgress(percent);
    });

    window.electron.on('crawler:status', ({ type, value }) => {
      if (type === 'START') setStatus('running');
      if (type === 'COMPLETE') setStatus('complete');
      addLog(`[STATUS] ${type}: ${value}`);
    });

    window.electron.on('crawler:log', (message: string) => {
      addLog(message);
    });

    window.electron.on('crawler:error', ({ code, message }) => {
      setStatus('error');
      addLog(`[ERROR ${code}] ${message}`);
    });

    window.electron.on('crawler:exit', (code: number) => {
      if (code === 0) setStatus('complete');
      else setStatus('error');
    });

    return () => {
      // cleanup listeners
    };
  }, []);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  const handleStart = async () => {
    const config: CrawlerConfig = {
      mode: 'betinfo',
      recent: 3,
      headless: true
    };
    await window.electron.invoke('crawler:start', config);
  };

  const handleStop = async () => {
    await window.electron.invoke('crawler:stop');
  };

  return (
    <div className="crawler-panel">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
        <span>{progress.toFixed(1)}%</span>
      </div>

      <div className="log-viewer">
        {logs.map((log, i) => (
          <div key={i} className="log-line">{log}</div>
        ))}
      </div>

      <div className="controls">
        <button onClick={handleStart} disabled={status === 'running'}>
          ▶ 시작
        </button>
        <button onClick={handleStop} disabled={status !== 'running'}>
          ⏹ 중지
        </button>
      </div>
    </div>
  );
}
```

### 4.3 히스토리 조회

```typescript
// HistoryViewer.tsx
import fs from 'fs/promises';
import path from 'path';

interface HistoryRecord {
  id: string;
  mode: string;
  args: Record<string, any>;
  status: 'SUCCESS' | 'FAILED' | 'RUNNING';
  start_time: string;
  end_time: string | null;
  log_summary: string | null;
  error_message: string | null;
}

async function loadHistory(): Promise<HistoryRecord[]> {
  const historyPath = path.join(app.getPath('userData'), 'data', 'history.json');
  const content = await fs.readFile(historyPath, 'utf-8');
  return JSON.parse(content);
}

// UI에서 표시
export function HistoryPanel() {
  const [history, setHistory] = useState<HistoryRecord[]>([]);

  useEffect(() => {
    loadHistory().then(setHistory);
  }, []);

  return (
    <div className="history-panel">
      <h2>📊 실행 이력</h2>
      <table>
        <thead>
          <tr>
            <th>시간</th>
            <th>모드</th>
            <th>상태</th>
            <th>요약</th>
          </tr>
        </thead>
        <tbody>
          {history.map(record => (
            <tr key={record.id}>
              <td>{new Date(record.start_time).toLocaleString()}</td>
              <td>{record.mode}</td>
              <td className={`status-${record.status.toLowerCase()}`}>
                {record.status}
              </td>
              <td>{record.log_summary || record.error_message || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 5. 배포 전략

### 5.1 PyInstaller 번들링 (권장)

**장점**
- 사용자 PC에 Python 설치 불필요
- 단일 실행 파일로 간편한 배포
- 의존성 충돌 방지

**빌드 스크립트**
```bash
# build.sh
cd python-crawler

pyinstaller --onefile \
  --add-data "config.py:." \
  --add-data "src:src" \
  --hidden-import selenium \
  --hidden-import pandas \
  --name betinfo-crawler \
  main.py

# 결과물: dist/betinfo-crawler (또는 .exe)
```

**Electron에서 사용**
```typescript
// main.ts
const crawlerPath = app.isPackaged
  ? path.join(process.resourcesPath, 'betinfo-crawler')
  : path.join(__dirname, '../python-crawler/dist/betinfo-crawler');

crawlerProcess = spawn(crawlerPath, args);
```

### 5.2 Electron 패키징

```json
// package.json
{
  "name": "betinfo-crawler-ui",
  "version": "1.0.0",
  "build": {
    "appId": "com.betinfo.crawler",
    "productName": "Betinfo Crawler",
    "files": [
      "dist/**/*",
      "resources/**/*"
    ],
    "extraResources": [
      {
        "from": "python-crawler/dist/betinfo-crawler",
        "to": "betinfo-crawler"
      }
    ],
    "mac": {
      "target": "dmg",
      "icon": "build/icon.icns"
    },
    "win": {
      "target": "nsis",
      "icon": "build/icon.ico"
    }
  }
}
```

### 5.3 배포 체크리스트

- [ ] Python 크롤러 PyInstaller 빌드 테스트
- [ ] Electron 앱 패키징 (Mac/Windows)
- [ ] 실행 파일 권한 설정 (chmod +x)
- [ ] 샘플 데이터 포함 (docs, 예시 CSV)
- [ ] 사용자 매뉴얼 작성
- [ ] 에러 발생 시 로그 수집 메커니즘
- [ ] 자동 업데이트 기능 (선택)

---

## 6. 구현 로드맵

### Phase 1: Electron 기본 구조 (1주)
- [ ] Electron + React/Vue 프로젝트 초기화
- [ ] IPC 통신 레이어 구현 (Main ↔ Renderer)
- [ ] subprocess 통신 테스트 (Python 호출)

### Phase 2: 핵심 UI 구현 (1주)
- [ ] 크롤러 실행 화면 (폼 + 프로그레스)
- [ ] 실시간 로그 뷰어
- [ ] 히스토리 조회 화면

### Phase 3: 데이터 관리 (1주)
- [ ] CSV 파일 목록 표시
- [ ] 파일 미리보기 (테이블)
- [ ] 엑셀 변환 기능

### Phase 4: 배포 준비 (1주)
- [ ] PyInstaller 빌드 자동화
- [ ] Electron 패키징
- [ ] 사용자 테스트 및 버그 수정

---

## 7. 참고 자료

### 관련 문서
- [CLI 사용 설명서](./cli_사용_설명서.md)
- [기능 구현 목록](./기능_구현_목록.md)
- [리팩토링 상세 보고서](./리팩토링_상세_보고서.md)

### Python CLI 명령어 레퍼런스
```bash
# 도움말
python3 main.py --help

# Betinfo 예시
python3 main.py --mode betinfo --recent 5
python3 main.py --mode betinfo --rounds "2025001,2025002"

# Flashscore 예시
python3 main.py --mode flashscore --task matches \
  --url "https://www.flashscore.co.kr/soccer/england/premier-league/results/" \
  --season "2025-2026"

python3 main.py --mode flashscore --task metadata \
  --url "https://www.flashscore.co.kr/soccer/england/premier-league/standings/#/ID/standings/overall/"
```

### Exit Code 참조
| Code | 의미 | 대응 방법 |
|:---|:---|:---|
| 0 | 성공 | 완료 메시지 표시 |
| 1 | 인자 오류 | 사용자에게 입력값 재확인 요청 |
| 2 | 크롤링 실패 | 네트워크 확인 또는 재시도 제안 |
| 3 | 사용자 중단 | 정상 종료 처리 |
| 99 | 예상치 못한 오류 | 로그 수집 후 개발자에게 보고 |

---

**작성일**: 2025-12-26  
**작성자**: Antigravity (AI Assistant)  
**프로젝트 상태**: Python CLI 완성, Electron 통합 준비 완료
