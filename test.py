from automation.browser_driver import BrowserDriver


def main():
    driver = BrowserDriver()

    try:
        # Abre a página da vaga
        driver.open_url("https://essentiagroup.gupy.io/job/eyJqb2JJZCI6OTM1OTM2Nywic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=gupy_portal")

        # Clica no botão "Candidatar-se"
        driver.click('[data-testid="apply-link"]')

        print("Clique realizado com sucesso!")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
