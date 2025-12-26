# Repository 패턴 마이그레이션 회고

### BaseRepository에서 CsvRepository로: 구조적 개선의 기록

## 1. 시작은 합리적인 선택이었다

처음 `BaseRepository`를 만들었을 때의 목적은 단순했습니다.
CSV로 데이터를 저장하는 코드가 반복되었고, 이를 공통화하면 초기 개발 속도를 높일 수 있다고 판단했습니다.

실제로 초반에는 효과가 있었습니다.
`LeagueRepository`, `TeamRepository`는 상속만으로 저장 기능을 사용할 수 있었고, 새로운 리포지토리를 추가하는 데 부담이 크지 않았습니다.

**[Before: 초기 BaseRepository]**
```python
class BaseRepository:
    def __init__(self, column_map: dict):
        self.column_map = column_map
    
    def save_to_csv(self, items: list, filename: str) -> None:
        # 단순 반복문으로 데이터 처리
        # Pydantic/Dataclass 구분 로직 부재 -> 호출자가 변환해야 함
        # '덮어쓰기'만 지원 -> 이어쓰기(Append) 불가
        dataframe.to_csv(filename, index=False)
```

문제는 크롤링 로직과 데이터 전처리가 추가되면서부터였습니다.
데이터의 형태와 저장 요구사항이 다양해지자, 처음에는 단순했던 구조가 점점 제약으로 작용하기 시작했습니다.

---

## 2. 구조적인 불편함을 인지하게 된 계기들

문제는 한 번에 드러나지 않았고, 여러 작업을 거치며 반복적으로 나타났습니다.

### 2-1. 저장 리포지토리가 지나치게 많은 것을 알고 있었다

`BetinfoRepository`를 작성하면서 가장 먼저 느낀 점은 역할의 과도함이었습니다.
데이터를 저장하는 클래스가 `pandas`를 직접 사용하고, `DataFrame`을 구성하며, CSV 인코딩 방식까지 결정하고 있었습니다.

**[Before: 책임이 과도한 BetinfoRepository]**
```python
class BetinfoRepository:
    COLUMN_MAP = { ... } 

    def save(self, filename: str, matches: list[Match]) -> None:
        # 1. 도메인 객체를 딕셔너리로 변환
        # 2. 컬럼 매핑 적용
        # 3. Pandas DataFrame 생성
        match_data_rows = [
            {self.COLUMN_MAP[field]: value for field, value in match.model_dump().items()}
            for match in matches
        ]
        
        # 4. CSV 저장 옵션 설정 (인코딩, 인덱스 등)
        matches_dataframe = pd.DataFrame(match_data_rows)
        matches_dataframe.to_csv(filename, index=False, encoding="utf-8-sig")
```
> **문제점**: 저장 방식(CSV -> DB)을 바꾸려면 비즈니스 로직이 있는 이 파일을 뜯어고쳐야 합니다.

### 2-2. 타입 처리 책임이 호출부로 전가되고 있었다

프로젝트에는 Pydantic 모델(`Match`), Dataclass(`Team`), 일반 딕셔너리가 혼재해 있었습니다.
하지만 `BaseRepository`는 입력 타입을 고려하지 않았기 때문에, 호출부에서 미리 변환해야 했습니다.

```python
# 호출하는 쪽에서 저장소의 사정을 맞춰줘야 함 (Leakage of Concern)
repo.save(filename, [m.model_dump() for m in matches])
```

결과적으로 저장 로직을 사용하는 쪽에서 저장 구현의 세부 사항을 알고 있어야 했고,
리포지토리는 이를 도와주지 못하는 상태였습니다.

### 2-3. 변경이 두려운 코드가 되어가고 있었다

`Flashscore` 크롤링 중 "이어쓰기(Append)" 요구사항이 생겼을 때 문제가 명확해졌습니다.
`BaseRepository`를 수정하면 이를 사용하는 다른 3개의 리포지토리에 영향을 줄 가능성이 컸고,
결국 리포지토리 내부에 별도의 `_append_to_csv_safe`라는 중복 메서드를 만드는 선택을 했습니다.

이 시점부터 동일한 CSV 처리 코드가 여러 위치에 복제되기 시작했습니다.

---

## 3. 단순한 개선이 아니라 구조 문제라는 판단

이 문제는 특정 메서드의 구현 방식이나 코드 스타일의 문제가 아니었습니다.
**'저장 메커니즘(Infrastructure)'과 '데이터 정의(Domain)'가 하나의 클래스에 강하게 결합**되어 있었습니다.

이 구조에서는 저장 방식이 바뀔 때마다 도메인 코드가 영향을 받을 수밖에 없었습니다.
그래서 기존 구조를 보완(Patch)하는 대신,
**저장 기술을 별도의 계층으로 완전히 분리하는 방향으로 재설계**하기로 결정했습니다.

---

## 4. 접근 방식: CsvRepository로 책임 분리

재설계 과정에서 기준으로 삼은 원칙은 두 가지였습니다.

1.  **CsvRepository는 저장 기술만 다룬다**: 파일 I/O, 디렉토리 생성, 중복 제거 등.
2.  **도메인 리포지토리는 데이터 정의만 가진다**: 무엇을 저장할지만 선언.

### 4-1. CsvRepository의 구조 (단일 책임 원칙 적용)

`CsvRepository`는 거대한 하나의 함수가 아니라, 기능별로 세분화된 메서드들의 조합으로 구성했습니다.

**[After: CsvRepository 내부]**
```python
class CsvRepository:
    # Facade 메서드: 전체 저장 흐름을 조율
    def save_to_csv(self, items: List[Any], filename: str, append: bool = False, ...) -> None:
        # 1. 데이터 준비 (변환 + 매핑)
        new_df = self._prepare_dataframe(items, column_map)
        
        # 2. 저장 경로 확보 (폴더가 없으면 생성)
        self._ensure_directory(filename)

        # 3. 저장 전략 실행 (이어쓰기 vs 덮어쓰기)
        if append and os.path.exists(filename):
            self._save_append(new_df, filename, deduplicate)
        else:
            self._save_overwrite(new_df, filename)

    # 세부 구현 메서드들 (각자 하나의 일만 담당)
    def _prepare_dataframe(self, items, map): ...
    def _ensure_directory(self, filename): ...
    def _save_append(self, df, filename): ...
```

### 4-2. 제네릭 타입 변환 (Type Agnostic)

가장 핵심적인 개선 사항은 **"무엇을 넣든 알아서 변환해주는"** 로직입니다.
`_convert_item_to_dict` 메서드를 통해 Pydantic, Dataclass, Dict 등 다양한 타입을 일관되게 처리합니다.

```python
    def _convert_item_to_dict(self, item: Any) -> dict:
        # 라이브러리 의존성 격리: 입력된 객체의 타입을 확인하여 적절히 변환
        if hasattr(item, 'model_dump'): return item.model_dump() # Pydantic v2
        if is_dataclass(item): return asdict(item)               # Dataclass
        if isinstance(item, dict): return item                   # Dict
        return item.__dict__                                     # General Object
```

### 4-3. 도메인 리포지토리의 단순화

실제 구현체인 `BetinfoRepository`는 이제 데이터 매핑 정의만 남기고, 모든 구현을 부모에게 위임합니다.

**[After: 가벼워진 BetinfoRepository]**
```python
class BetinfoRepository(MatchRepository, CsvRepository):
    # [What] "나는 이런 데이터를 저장할거야" 정의
    COLUMN_MAP = {
        "home": "홈팀",
        "away": "원정팀",
        ...
    }

    def save(self, filename: str, matches: list[Match]) -> None:
        # [How] "저장은 네가 알아서 해" (CsvRepository의 기능 사용)
        self.save_to_csv(matches, filename, column_map=self.COLUMN_MAP)
```

---

## 5. 마이그레이션 이후의 변화

이번 리팩토링 이후 수정과 확장이 훨씬 수월해졌습니다.
이전에는 CSV 저장 방식과 관련된 변경이 생기면 여러 리포지토리를 함께 살펴봐야 했지만, 이제는 인코딩이나 저장 방식 같은 이슈가 발생해도 CsvRepository만 확인하면 충분합니다.

또한 각 리포지토리에 흩어져 있던 pandas 기반 저장 로직과 디렉터리 생성 코드가 하나의 위치로 모이면서, 같은 기능을 여러 번 구현해야 하는 상황도 자연스럽게 사라졌습니다. 이 덕분에 코드 흐름을 따라가기도 훨씬 쉬워졌습니다.

이 구조 덕분에 저장 방식이 바뀌더라도 도메인 코드에는 영향을 주지 않을 수 있겠다는 확신도 생겼습니다. 이후에 다른 저장소 구현이 필요해지더라도 기존 코드를 크게 손대지 않고 새로운 리포지토리를 추가하는 방향으로 확장할 수 있을 것이라고 판단했습니다.

이 과정을 통해 초기에는 편리해 보였던 상속 구조도 역할과 책임이 모호해지면 기술 부채가 된다는 것, 그리고 이를 **"관심사의 분리(Separation of Concerns)"**를 통해 해결할 수 있음을 확인했습니다.
