from data.profile_manager import ProfileManager
from data.csv_logger import CSVLogger
from data.job_application import JobApplication

from automation.browser_driver import BrowserDriver


def main():
    profile = ProfileManager.load_profile("data/profile.json")
    print(profile)
    logger = CSVLogger("data/log.csv")

    driver = BrowserDriver()

    try:
        driver.open_url("https://gupy.io/")
        # Aqui você começa a navegar, preencher etc.

        # Exemplo de log de uma candidatura fictícia
        job = JobApplication(
            company="Empresa Fictícia",
            job_title="Desenvolvedor Python",
            job_url="https://gupy.io/vagas/123"
        )
        logger.log(job)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
