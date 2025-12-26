# 프로젝트 구조 (DDD)

이 프로젝트는 도메인 주도 설계(DDD) 원칙을 따르도록 재구성되었습니다.

## 디렉토리 구조

### `src/domain`
**핵심 비즈니스 로직 (Core Business Logic).**
- 엔티티(`models`), 값 객체(Value Objects), 리포지토리 인터페이스(`repositories`)를 포함합니다.
- **규칙**:
  - 다른 계층(Infrastructure, Application, Presentation)에 절대 의존하지 않습니다.
  - 문제 도메인을 정의하는 순수 파이썬(Pure Python) 코드로만 구성됩니다.

### `src/application`
**애플리케이션 계층 (Application Layer).**
- 유스케이스(Use Cases)와 애플리케이션 서비스(`services`)를 포함합니다.
- 도메인 객체와 리포지토리 인터페이스를 사용하여 데이터 흐름을 조정(Orchestration)합니다.
- **규칙**:
  - `domain` 계층에 의존합니다.
  - `presentation`이나 `infrastructure` 계층에는 의존하지 않아야 합니다.

### `src/infrastructure`
**기술적 구현 (Technical Capabilities).**
- `domain`에서 정의된 인터페이스의 실제 구현체를 담당합니다.
- 포함 내용:
  - `repositories`: 리포지토리 인터페이스의 구체적인 구현 (CSV 저장, DB 연동 등).
  - `scraping`: 모든 크롤링 관련 로직을 통합 관리:
    - `drivers`: Selenium/WebDriver 설정.
    - `parsers`: HTML/Text를 데이터 구조로 변환하는 로직.
    - `scrapers`: 브라우징 및 수집 흐름을 제어하는 스크립트.
- **규칙**:
  - 외부 라이브러리(Selenium, Pandas 등)에 의존할 수 있습니다.

### `src/presentation`
**사용자 인터페이스 / API (User Interface).**
- 애플리케이션의 진입점(Entry Point)입니다.
- 포함 내용:
  - `controllers`: 사용자 입력을 처리하고 적절한 `application/services`로 위임합니다.
  - `views`: 출력 결과(콘솔, GUI 응답 등)를 담당합니다.

### `src/shared`
**공통 유틸리티 (Shared Utilities).**
- 에러 처리, 로깅, 헬퍼 함수 등 여러 계층에서 공통적으로 사용되는 기능을 포함합니다.

---

## 향후 이관 참고사항 (Electron/Java)

이 구조는 관심사를 효과적으로 분리하여 향후 이관 작업을 돕습니다:
- **도메인 로직** (`src/domain`): Java 백엔드의 핵심 데이터 구조 및 모델(Entity)의 레퍼런스로 사용됩니다.
- **애플리케이션 로직** (`src/application`): 백엔드가 지원해야 할 "명령(Commands)"이나 서비스 로직의 목록을 제시합니다.
- **크롤링 인프라** (`src/infrastructure/scraping`): 독립적으로 격리되어 있어, 비즈니스 로직에 영향을 주지 않고 구현체를 교체하거나 업그레이드하기 쉽습니다.
