from driver.chrome_driver_factory import ChromeDriverFactory
from scraper.betinfo_page import BetinfoPage
from repository.csv_repository import CSVRepository
from service.proto_service import ProtoService


def run(start_round: int, end_round: int):
    driver = ChromeDriverFactory.create()

    try:
        page = BetinfoPage(driver)
        repository = CSVRepository()

        service = ProtoService(
            page=page,
            repository=repository
        )

        for round_num in range(start_round, end_round + 1):
            round_value = str(round_num)
            print(f"🔄 {round_value} 회차 처리 중...")

            service.collect_round(round_value)

    except Exception as e:
        print(f"[치명적 오류] 실행 중단: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    start_round = int(input("시작 회차 (예: 2025040): "))
    end_round = int(input("끝 회차 (예: 2025045): "))

    run(start_round, end_round)
