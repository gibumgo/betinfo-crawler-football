# 데이터 매핑 전략: 파편화된 문자열을 도메인 모델로 변환하기

크롤링으로 긁어온 파편화된 문자열들이 시스템 내에서 어떻게 의미 있는 `Match` 객체로 안착하는지 그 과정에서의 고민을 정리했습니다.

## 1. 문제: 파싱과 로직의 혼재

처음에는 `parse_game_row`라는 함수 하나가 HTML 추출부터 날짜 변환, 배당 계산까지 모든 일을 처리했습니다. 사이트 구조가 조금이라도 바뀌면 함수 전체를 뒤져야 했고, 인덱스 하나만 틀려도 데이터 전체가 오염되는 상황이었습니다.

### Before: 모든 로직이 섞인 파싱 함수
```python
def parse_game_row(row, round_info, weekday_kr, game_type_mapping):
    cols = row.find_all('td')
    
    # 날짜 추출 및 변환이 파싱 로직 중간에 끼어 있음
    match = re.search(r'(\d{2}/\d{2}) \(.\)(\d{2}:\d{2})', cols[1].text.strip())
    # ... 날짜 처리 ...
    
    # 하드코딩된 인덱스로 배당 추출
    win_odds = cols[13].find('span').text.strip()
    
    # 결과 딕셔너리를 직접 조립하여 반환
    return {
        '회차': round_info,
        '홈': home_team,
        '결과 배당': get_result_odds(result, win_odds, draw_odds, lose_odds),
        # ... 수십 개의 키-값 쌍 ...
    }
```

이 방식은 각 데이터 항목이 어떤 기준(Policy)으로 만들어지는지 파악하기 어려웠습니다.

## 2. 해결 방법: 도메인 팩토리와 정책 분리

단순히 `dict`를 넘기는 게 아니라, **"추출은 파서가, 조립은 모델이"** 담당하도록 역할을 나눴습니다. 파서는 순수한 문자열 데이터만 모으고 실제 객체화는 `Match` 클래스의 팩토리 메서드에서 수행합니다.

### After: Match 객체 스스로 데이터를 정제하도록 변경
```python
@classmethod
def create_from_extracted_data(cls, data: dict, round_val: str):
    # 배당 계산처럼 복잡한 룰은 정책 객체(OddsPolicy)에 맡깁니다.
    result_odds = OddsPolicy.calculate_result_odds(
        data.get("result"), 
        data.get("win_domestic"), 
        data.get("draw_domestic"), 
        data.get("lose_domestic")
    )
    # 정제된 데이터만 생성자로 넘깁니다.
    return cls(round=round_val, result_odds=result_odds, **data)
```

## 3. OddsPolicy: 복잡한 매핑 로직의 격리

"승/무/패", "U/O" 같은 다양한 결과에 따라 배당 인덱스를 찾아야 하는 로직은 별도의 정책 클래스로 떼어냈습니다.

**Before (전역 함수 방식)**
```python
def get_result_odds(result: str, win_odds: str, draw_odds: str, lose_odds: str):
    # 전역에 흩어져 있던 매핑 로직
    odds_map = {"승": win_odds, "무": draw_odds, "패": lose_odds, ...}
    return odds_map.get(result.strip(), "")
```

**After (OddsPolicy 클래스 활용)**
```python
class OddsPolicy:
    MAP = {
        "승": "win", "무": "draw", "패": "lose",
        "U": "win", "O": "lose",
        "홀": "win", "짝": "lose",
    }
    
    @classmethod
    def calculate_result_odds(cls, result, win, draw, lose):
        # 문자열을 내부 표준 키값으로 먼저 변환한 뒤 값을 찾습니다.
        key = cls.MAP.get(result.strip())
        return {"win": win, "draw": draw, "lose": lose}.get(key, "")
```

이렇게 정책을 분리하니 사이트의 결과 표시 문구가 바뀌더라도 `OddsPolicy.MAP` 하나만 수정하면 코드가 안전하게 유지됩니다.

## 4. 마무리
데이터가 파서에서 모델로 넘어가는 병목 구간을 정책 객체로 뚫어냈습니다. 파싱 로직이 단순해진 덕분에 사이트 변화에 더 기민하게 대응할 수 있을 것 같습니다.