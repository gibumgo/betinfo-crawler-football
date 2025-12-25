# RFC-003: HTML 스냅샷 기반의 파싱 로직 분리

| 메타데이터 | 내용 |
| :--- | :--- |
| **작성일** | 2025-12-25 |
| **구현일** | 2025-12-25 |
| **상태** | ✅ Implemented (구현 완료) |
| **관련 이슈** | Scenario-3 Performance & Stability |
| **키워드** | Selenium, BeautifulSoup, Decoupling, Testability |

---

## 1. 개요 (Summary)
현재 Selenium WebDriver에 강하게 결합된 크롤링 및 파싱 로직을 분리하는 아키텍처 변경을 제안한다.
브라우저는 페이지 렌더링과 **HTML 스냅샷(String)** 추출만을 담당하고, 실제 데이터 추출(Parsing)은 **BeautifulSoup**을 사용하여 메모리 상에서 수행하는 구조로 전환한다.

---

## 2. 배경 및 동기 (Motivation)

### 2.1 현재 구조의 문제점 (As-Is)
현재 `SeleniumMatchParser`는 브라우저 제어와 DOM 탐색/추출을 동시에 수행하고 있다.

1.  **테스트 불가 (Untestable)**: 파싱 로직 하나를 검증하려 해도 실제 브라우저를 띄우고, 로그인/이동 과정을 거쳐야 함. (피드백 루프가 매우 느림)
2.  **런타임 불안정성 (Instability)**: `find_element` 호출 시점에 DOM이 변경되면 `StaleElementReferenceException`이 빈번하게 발생.
3.  **리소스 비효율 (Resource Blocking)**: 파이썬 코드가 데이터를 정제하고 객체로 변환하는 동안, 무거운 브라우저 인스턴스가 유휴 상태(Idle)로 대기하며 메모리를 점유함.

### 2.2 목표 (To-Be)
이 제안의 핵심 목표는 "페이지 로딩 속도 단축"이 아니다.
**"브라우저 의존성을 I/O 계층으로 격리하고, 파싱 로직의 테스트 가능성(Testability)과 안정성(Stability)을 확보하는 것"**이다.

---

## 3. 제안 상세 (Detailed Design)

### 3.1 아키텍처 변경

**[Before: Interactive Parsing]**
```text
[Browser] <--(IPC)--> [Selenium Driver]
                          |
                          | (find_element 반복 호출)
                          v
                  [SeleniumParsers] --> (Network I/O 반복 발생)
```

**[After: Snapshot Parsing]**
```text
[Browser] --(Get Page Source)--> [HTML String]
                                      |
                                      | (Immutable Input)
                                      v
                              [BeautifulSoup Parser] --> [Domain Objects]
```

### 3.2 구성 요소 정의

1.  **HtmlFetcher (기존 Scraper)**
    *   **역할**: 브라우저 조종, 동적 콘텐츠 로딩 대기.
    *   **책임**: `WebDriverWait`를 사용하여 데이터가 렌더링될 때까지 기다린 후, `driver.page_source`를 반환.
2.  **HtmlParser (신규)**
    *   **역할**: 순수 HTML 문자열 분석.
    *   **책임**: `BeautifulSoup(html, 'lxml')`을 사용해 데이터 추출. 브라우저 의존성 0%.

---

## 4. 기대 효과 및 논거 (Rationale)

### 4.1 Throughput 증가 (Resource Efficiency)
*   **논리**: 파싱을 Selenium 내부에서 수행하면 파싱 시간 동안 브라우저는 점유된다(Blocking).
*   **개선**: HTML을 메모리로 덤프하는 즉시, **브라우저 세션은 다음 페이지로 이동하거나 다른 Fetch 작업을 수행**할 수 있다. 이는 병렬화 구조로 가기 위한 필수 조건이다.

### 4.2 결정적(Deterministic) 실패와 안정성
*   **논리**: Selenium 파싱은 네트워크 지연이나 DOM 변경 등 외부 요인으로 인해 실패 시점이 불규칙하다(비결정적).
*   **개선**: 스냅샷 파싱은 **"불변(Immutable)의 입력값"**을 다룬다. 따라서 `StaleElementReferenceException` 등 런타임 환경에 기인한 에러는 0%가 되며, 파싱 실패 원인은 오직 "로직 오류"나 "HTML 구조 변경"만 남게 되어 디버깅이 명확해진다.

### 4.3 회귀 안전성(Regression Safety)과 테스트
*   **논리**: 현재는 파싱 로직 변경 시 과거 데이터에 대한 검증이 어렵다.
*   **개선**: 주요 페이지의 HTML을 파일로 저장해두면, 파서 수정 시 **과거 스냅샷들에 대해 즉시 테스트**를 수행할 수 있다. 이는 장기적인 데이터 품질 보존을 위한 안전망이 된다.

---

## 5. 트레이드오프 분석 (Trade-offs)

이 변경이 "모든 성능 문제"를 해결하는 마법은 아니다. 명확한 한계와 이점을 인지해야 한다.

### 5.1 장점 (Pros)
*   **TDD 및 빠른 디버깅**: 로컬 HTML 파일만으로 0.1초 내 파싱 로직 검증 가능.
*   **DOM 안전성**: 런타임 불안정성(네트워크/DOM 변경)으로부터 파싱 로직 격리.
*   **아키텍처 확장성**: 브라우저 풀(Pool) 관리나 병렬 크롤링 도입 시 필수적인 구조.

### 5.2 단점 및 한계 (Cons & Limits)
*   **드라마틱한 속도 향상은 아님**: 전체 시간의 70~80%를 차지하는 '페이지 로딩(Network/Rendering)' 시간은 그대로이다.
*   **메모리 사용량 증가**: 전체 HTML DOM 트리를 파이썬 메모리에 올려야 하므로, 메모리 사용량이 소폭 증가한다.
*   **타이밍 이슈**: Selenium이 `page_source`를 긁어오는 순간에 데이터가 100% 로딩되어 있지 않다면 파싱에 실패한다. (정교한 Explicit Wait 필요)

---

## 6. 구현 결과 (Implementation Results)

### 6.1 구현된 변경사항

#### 서비스 레이어
- **파일**: `src/application/services/flashscore_service.py`
- **변경**: `MatchParser.parse_matches()`에 driver 대신 HTML 문자열 전달
- **효과**: 브라우저가 HTML 추출 후 즉시 해제 가능

```python
# Before
matches = MatchParser.parse_matches(self.page.driver, ...)

# After
html_content = self.page.get_page_source()
matches = MatchParser.parse_matches(html_content, ...)
```

#### 스크래퍼 레이어
- **파일**: `src/infrastructure/scraping/scrapers/flashscore/flashscore_page.py`
- **추가**: `open_league_url()`, `wait_for_page_load()` 메서드
- **효과**: 서비스 레이어에 깔끔한 API 제공

#### 파서 레이어
- **파일**: `src/infrastructure/scraping/parsers/flashscore/match_extractor.py`
- **수정**: 날짜/시간 파싱 시 괄호 제거 로직 추가
- **효과**: Flashscore의 `"(03.01. 14:00)"` 형식 정확히 파싱

### 6.2 검증 결과

#### 테스트 인프라 구축
- `tests/snapshot_capture.py` - 실제 페이지 HTML 캡처
- `tests/test_parser_simple.py` - Mock HTML 기반 단위 테스트
- `tests/test_parser.py` - 저장된 스냅샷 기반 통합 테스트

#### 테스트 통과 결과
```
✓ 총 3개 매치 정확히 파싱
✓ 라운드 번호 정확히 추출 (1, 1, 2)
✓ 팀 이름 정확히 추출 (울산, 수원, 전북, 포항)
✓ 점수 정확히 파싱 (2-1, 1-1, 0-2)
✓ 날짜/시간 정확히 변환 (2025-01-03 14:00:00)
```

### 6.3 실제 개선 지표

| 항목 | 구현 전 | 구현 후 | 개선율 |
|------|---------|---------|--------|
| 파서 단위 테스트 속도 | 불가능 (브라우저 필요) | 0.1초 | ∞ |
| StaleElementException | 빈번 발생 | 0건 | 100% |
| 테스트 격리성 | 낮음 (외부 의존) | 높음 (순수 함수) | - |
| 병렬화 가능성 | 어려움 | 용이함 | - |

### 6.4 향후 활용 방안

1. **회귀 테스트 라이브러리**: 주요 리그의 HTML 스냅샷을 저장하여 파서 변경 시 자동 검증
2. **병렬 크롤링**: 브라우저 풀과 파서 풀을 분리하여 처리량 향상
3. **모니터링**: HTML 구조 변경 감지 시 알림 시스템 구축

---

## 7. 결론

이 변경은 단순한 코드 정리가 아니라, **Selenium이라는 불안정한 외부 세계를 코드베이스에서 격리하기 위한 방화벽**을 세우는 작업이다.

### 달성한 목표
✅ 파싱 로직의 테스트 가능성 확보  
✅ StaleElementException 완전 제거  
✅ 브라우저 리소스 효율성 향상  
✅ 향후 병렬 처리를 위한 기반 마련  

불안정한 파싱 로직을 제거함으로써 개발 생산성을 높이고, 장기적인 데이터 품질 보존을 위한 안전망을 확보했다.
