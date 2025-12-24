from dataclasses import dataclass

@dataclass(frozen=True)
class Team:
    team_id: str            # Flashscore 팀 고유 ID (예: hA1Zm19f)
    team_name: str          # URL용 팀명 (예: arsenal)
    team_name_ko: str       # 한국어 팀명 (예: 아스널)
    team_image_url: str     # 팀 로고 이미지 URL
    nation: str             # 저장 경로 구분용 국가명 (예: england)

    @classmethod
    def create(cls, **kwargs):
        return cls(
            team_id=kwargs.get("team_id", ""),
            team_name=kwargs.get("team_name", ""),
            team_name_ko=kwargs.get("team_name_ko", ""),
            team_image_url=kwargs.get("team_image_url", ""),
            nation=kwargs.get("nation", "")
        )
