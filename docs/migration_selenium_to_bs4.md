# BeautifulSoup 마이그레이션 변경 계획 (Feature: replace-selenium-with-bs4)

본 문서는 Selenium 기반의 파싱 로직을 BeautifulSoup(`bs4`) 기반의 순수 파싱 로직으로 분리하기 위한 코드 변경 계획 및 아키텍처 변화를 기술한다.

---

## 1. 아키텍처 변화 (Architecture Changes)

### Before: Selenium 의존적 구조
파서가 직접 브라우저(`driver`)를 제어하며 데이터를 추출한다.

```text
[BetinfoPage (Scraper)]
      │
      │ driver 전달
      ▼
[SeleniumMatchParser]
      │ find_element() 반복 호출 (I/O Blocking)
      ▼
 [Browser DOM]
```

### After: I/O와 CPU의 분리
스크래퍼가 HTML 문자열을 추출하고, 파서는 문자열만 분석한다.

```text
[BetinfoPage (Scraper)]
      │
      │ driver.page_source (HTML String 추출)
      ▼
[BetinfoParser (BS4)]
      │ BeautifulSoup(html, 'lxml') (Memory Parsing)
      ▼
  [Domain Objects]
```

---

## 2. 파일별 변경 계획

### 2.1 의존성 관리
*   **파일**: `requirements.txt`
*   **변경**:
    ```text
    beautifulsoup4>=4.12.0
    lxml>=5.0.0
    ```
    *   `lxml`은 `html.parser`보다 약 5배 빠른 C 기반 파서이므로 필수 권장.

### 2.2 파서 구현 (New)
*   **파일**: `src/infrastructure/scraping/parsers/betinfo_parser.py` (신규 생성)
*   **역할**: 순수 HTML 문자열을 입력받아 `Match` 객체 리스트 반환.
*   **코드 구조 예시**:
    ```python
    from bs4 import BeautifulSoup
    from domain.models.match import Match
    
    class BetinfoParser:
        def parse(self, html_content: str) -> list[Match]:
            soup = BeautifulSoup(html_content, "lxml")
            matches = []
            
            # CSS Selector 사용 (Selenium과 유사)
            rows = soup.select("tr.match-row") 
            for row in rows:
                match = self._parse_row(row)
                if match:
                    matches.append(match)
            return matches
            
        def _parse_row(self, row) -> Match:
            # 순수 텍스트 추출 로직
            home = row.select_one(".home-team").get_text(strip=True)
            ...
    ```

### 2.3 스크래퍼 수정
*   **파일**: `src/infrastructure/scraping/scrapers/betinfo_page.py`
*   **변경**:
    *   `SeleniumMatchParser` import 제거.
    *   `BetinfoParser` import 추가.
    *   `parse()` 호출 시점 변경:
    ```python
    # Before
    matches = self.parser.parse(self.driver)
    
    # After
    html_source = self.driver.page_source  # 스냅샷 캡처
    matches = self.parser.parse(html_source) # 순수 파싱
    ```

### 2.4 단위 테스트 (New)
*   **파일**: `tests/test_betinfo_parser.py`
*   **역할**: 브라우저 없이 파싱 로직 검증.
*   **데이터**: `tests/mock_data/betinfo_sample.html` (실제 사이트 HTML 저장본)

---

## 3. 마이그레이션 체크리스트

1.  [ ] `feature/replace-selenium-with-bs4` 브랜치 생성
2.  [ ] `requirements.txt` 업데이트 (`bs4`, `lxml`)
3.  [ ] `BetinfoParser` 구현 (Selenium 코드 이식)
4.  [ ] `tests/mock_data`에 HTML 샘플 저장
5.  [ ] `test_betinfo_parser.py` 작성 및 Pass 확인
6.  [ ] `BetinfoPage`에서 파서 교체
7.  [ ] 전체 크롤링 실행 확인 (Integration Test)
