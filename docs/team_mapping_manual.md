# 🧠 지능형 팀 매핑 시스템 사용 설명서

## 1. 개요
Betinfo의 팀명(한글/약어)과 Flashscore의 팀 ID(영문 정규화)를 자동으로 연결해주는 시스템입니다. 
단순한 이름 유사도뿐만 아니라 **"같은 날짜에 같은 상대와 경기를 했는가?"** 라는 경기 맥락(Context) 정보를 사용하여 정확도를 획기적으로 높였습니다.

---

## 2. 작동 원리

### 단계 1: 학습된 매핑 확인 (Memory)
- `config/team_mappings.json` 파일에 이미 저장된 결과가 있는지 확인합니다.
- 예: "맨체스U"가 이미 "manchester-united" ID로 저장되어 있다면 즉시 반환합니다.

### 단계 2: 경기 맥락 추론 (Context Inference)
- **가장 강력한 기능**입니다.
- Betinfo 데이터: `2025-05-12`일 `맨체스U` vs `첼시`
- Flashscore 데이터 검색: `2025-05-12`일 경기 중 `첼시`와 유사한 상대(`Chelsea`)와 경기한 팀을 찾습니다.
- 발견! `Manchester United` vs `Chelsea`
- 결론: `맨체스U` = `Manchester United` (ID: ... )

### 단계 3: 이름 유사도 추론 (Similarity Fallback)
- 맥락 정보가 없을 경우, 문자열 유사도(Levenshtein Distance)를 분석합니다.
- 예: `맨체스U` vs `Manchester Utd` (유사도 80% 이상 시 매핑)

---

## 3. 사용 방법

### 자동 매핑 도구 실행
현재 `tools/map_teams.py` 스크립트를 통해 실행 가능합니다. (추후 CLI 통합 예정)

```bash
python tools/map_teams.py
```

### 매핑 파일 관리
- 위치: `config/team_mappings.json`
- 형식:
  ```json
  {
    "맨체스U": "ppjDR086",
    "첼시": "4fGZN2oK"
  }
  ```
- 이 파일은 Git으로 관리하여 팀원들과 공유할 수 있습니다.

---

## 4. 주의 사항
- **날짜 정보 필수**: 경기 맥락 추론을 위해 Betinfo 수집 시 날짜 정보가 정확해야 합니다.
- **초기 데이터 필요**: Flashscore의 경기 데이터(`flashscore_matches_*.csv`)가 많이 쌓여있을수록 매핑 정확도가 높아집니다.
