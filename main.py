from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time
import random
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

class BrowserDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def open_url(self, url):
        self.driver.get(url)

    def wait_and_click(self, selector: str, by="css", timeout=10):
        if by == "css":
            locator = (By.CSS_SELECTOR, selector)
        elif by == "xpath":
            locator = (By.XPATH, selector)
        else:
            raise ValueError("Unsupported selector type. Use 'css' or 'xpath'.")

        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        time.sleep(1)

    def type(self, selector, text):
        input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        input_element.clear()
        input_element.send_keys(text)

    def close(self):
        self.driver.quit()


# 🔥 Gerar resposta com OpenAI
def gerar_resposta_openai(pergunta, opcoes=None):
    if opcoes:
        # Prompt para múltipla escolha
        opcoes_texto = "\n".join([f"- {opcao}" for opcao in opcoes])
        prompt = f"""
        Diante da pergunta: "{pergunta}",
        escolha a alternativa que melhor responde entre estas opções:
        {opcoes_texto}

        Responda apenas com o texto exato da opção.
        """
        temperature = 0.0  # Respostas precisas para múltipla escolha
    else:
        # Prompt para texto livre
        prompt = f"""
        Você é um candidato profissional preenchendo um formulário de vaga de emprego.
        Responda de forma educada, profissional e objetiva a esta pergunta:

        "{pergunta}"
        """
        temperature = 0.7  # Mais criatividade para respostas textuais

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


# 🔍 Capturar e processar perguntas
def processar_perguntas(driver):
    print("🔍 Iniciando captura de perguntas...")

    perguntas = []

    # ✅ 1. Perguntas em labels com for="additional-question"
    labels = driver.find_elements(By.XPATH, '//label[starts-with(@for, "additional-question")]')
    for label in labels:
        texto = label.text.strip()
        if texto:
            print(f"📝 Pergunta detectada (label): {texto}")
            perguntas.append({
                "tipo": "texto",
                "pergunta": texto,
                "input_id": label.get_attribute('for')
            })

    # # ✅ 2. Perguntas em legend (checkbox)
    # legends = driver.find_elements(By.TAG_NAME, 'legend')
    # for legend in legends:
    #     texto = legend.text.strip()
    #     if texto:
    #         print(f"📝 Pergunta detectada (legend): {texto}")
    #         checkbox_inputs = legend.find_elements(By.XPATH, '../../..//input[@type="checkbox"]')
    #         opcoes = []
    #         for checkbox in checkbox_inputs:
    #             label = checkbox.find_element(By.XPATH, "./ancestor::label | ./following-sibling::*")
    #             opcoes.append(label.text.strip())

    #         perguntas.append({
    #             "tipo": "checkbox",
    #             "pergunta": texto,
    #             "opcoes": opcoes,
    #             "inputs": checkbox_inputs
    #         })

    # ✅ 3. Perguntas em fieldsets
    fieldsets = driver.find_elements(By.TAG_NAME, 'fieldset')
    for fs in fieldsets:
        try:
            # Primeiro verifica se há um <legend> (checkbox)
            legends = fs.find_elements(By.TAG_NAME, 'legend')
            if legends:
                texto = legends[0].text.strip()
                if texto:
                    checkbox_inputs = fs.find_elements(By.XPATH, './/input[@type="checkbox"]')
                    opcoes = []
                    for checkbox in checkbox_inputs:
                        label = checkbox.find_element(By.XPATH, './ancestor::label | ./following-sibling::*')
                        opcoes.append(label.text.strip())

                    print(f"📝 Pergunta detectada (fieldset checkbox): {texto}")
                    perguntas.append({
                        "tipo": "checkbox",
                        "pergunta": texto,
                        "opcoes": opcoes,
                        "inputs": checkbox_inputs
                    })
                continue  # Se já processou como checkbox, pula para o próximo fieldset

            # Se não tiver legend, tenta buscar label (radio)
            label = fs.find_element(By.TAG_NAME, 'label')
            texto = label.text.strip()
            if texto:
                radios = fs.find_elements(By.XPATH, './/input[@type="radio"]')
                opcoes = []
                for radio in radios:
                    lbl = radio.find_element(By.XPATH, './ancestor::label')
                    opcoes.append(lbl.text.strip())

                print(f"📝 Pergunta detectada (fieldset radio): {texto}")
                perguntas.append({
                    "tipo": "radio",
                    "pergunta": texto,
                    "opcoes": opcoes,
                    "inputs": radios
                })
        except Exception as e:
            print(f"⚠️ Erro processando fieldset: {e}")


    print(f"✅ Total de perguntas encontradas: {len(perguntas)}")

    # 🚀 Processamento e preenchimento
    for idx, p in enumerate(perguntas):
        print(f"\n🔄 Processando pergunta {idx + 1}/{len(perguntas)}")
        print(f"📄 {p['pergunta']}")

        resposta = gerar_resposta_openai(p['pergunta'], p.get('opcoes'))
        print(f"✍️ Resposta OpenAI: {resposta}")

        try:
            if p['tipo'] == 'texto':
                input_element = driver.find_element(By.ID, p['input_id'])
                input_element.clear()
                input_element.send_keys(resposta)
                print("✅ Preencheu input de texto.")

            elif p['tipo'] == 'radio':
                selecionado = False
                for radio, opcao in zip(p['inputs'], p['opcoes']):
                    if opcao.lower() in resposta.lower():
                        label = radio.find_element(By.XPATH, './ancestor::label')
                        label.click()
                        selecionado = True
                        print(f"✅ Selecionou opção: {opcao}")
                        break
                if not selecionado:
                    radio = p['inputs'][0]
                    radio.find_element(By.XPATH, './ancestor::label').click()
                    print(f"⚠️ Nenhuma opção casou. Selecionou primeira opção: {p['opcoes'][0]}")

            elif p['tipo'] == 'checkbox':
                for checkbox, opcao in zip(p['inputs'], p['opcoes']):
                    if opcao.lower() in resposta.lower():
                        label = checkbox.find_element(By.XPATH, './ancestor::label | ./following-sibling::*')
                        label.click()
                        print(f"✅ Selecionou checkbox: {opcao}")

        except Exception as e:
            print(f"❌ Erro preenchendo pergunta: {e}")


# 🏁 Função principal
def main():
    driver = BrowserDriver()

    try:
        print("🔗 Acessando a vaga...")
        driver.open_url("https://mobi7.gupy.io/job/eyJqb2JJZCI6OTMxMzIzMywic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=gupy_portal")

        driver.wait_and_click('[data-testid="apply-link"]')
        print("✅ Clique no botão 'Candidatar-se' realizado.")
        time.sleep(random.uniform(3.2, 6.7))

        driver.type('input[name="username"]', 'vinicius190702@hotmail.com')
        time.sleep(random.uniform(0.3, 1.1))
        driver.type('input[name="password"]', 'Br0c0l!s')
        time.sleep(random.uniform(0.4, 1.7))
        driver.wait_and_click('button#button-signin')
        print("✅ Login realizado com sucesso.")

        # Ocultar header para evitar erros de clique
        try:
            driver.driver.execute_script("document.querySelector('header').style.display = 'none';")
            print("✅ Header ocultado.")
        except:
            print("⚠️ Header não encontrado.")


        driver.wait_and_click('//button[contains(text(), "Continuar")]', by="xpath")
        print("✅ Clique no botão 'Continuar' realizado.")

        driver.wait_and_click('button[name="saveAndContinueButton"]')
        print("✅ Clique em 'Salvar e continuar' realizado.")

        driver.wait_and_click('button[aria-label="Responder agora"]')
        print("✅ Clique em 'Responder agora' realizado.")

        time.sleep(3)

        processar_perguntas(driver.driver)

        driver.wait_and_click('#dialog-give-up-personalization-step')
        print("🚀 Candidatura finalizada com sucesso!")

        time.sleep(3)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
