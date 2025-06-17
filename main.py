from automation.browser_driver import BrowserDriver
from selenium.webdriver.common.by import By
import openai
import time


openai.api_key = 'SUA_API_KEY'


def gerar_resposta_openai(pergunta):
    prompt = f"""
    Você é um candidato profissional preenchendo um formulário de candidatura de emprego.
    Responda de forma objetiva, educada e profissional a esta pergunta:

    "{pergunta}"
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return resposta['choices'][0]['message']['content'].strip()


def main():
    driver = BrowserDriver()

    try:
        driver.open_url("URL_DA_PAGINA_DE_PERGUNTAS")
        time.sleep(3)

        # Encontra todos os fieldsets da página
        fieldsets = driver.driver.find_elements(By.TAG_NAME, "fieldset")
        print(f"Encontrou {len(fieldsets)} perguntas no formulário.")

        for fieldset in fieldsets:
            try:
                pergunta_element = fieldset.find_element(By.TAG_NAME, "label")
                pergunta_texto = pergunta_element.text.strip()
                print(f"📄 Pergunta: {pergunta_texto}")

                if not pergunta_texto:
                    continue

                # 🔥 Gera resposta com OpenAI
                resposta = gerar_resposta_openai(pergunta_texto)
                print(f"✍️ Resposta: {resposta}")

                # 🔍 Verifica se é radio (opções) ou input (texto)
                radios = fieldset.find_elements(By.XPATH, ".//input[@type='radio']")
                inputs = fieldset.find_elements(By.XPATH, ".//input[@type='text']")

                if radios:
                    print("➡️ Pergunta de múltipla escolha (radio). Buscando melhor opção...")
                    encontrou = False

                    for radio in radios:
                        label = radio.find_element(By.XPATH, "./ancestor::label")
                        texto_opcao = label.text.strip()

                        if texto_opcao.lower() in resposta.lower():
                            label.click()
                            print(f"✅ Selecionou opção: {texto_opcao}")
                            encontrou = True
                            break

                    if not encontrou:
                        print("⚠️ Nenhuma opção casou exatamente. Selecionando primeira opção.")
                        radios[0].find_element(By.XPATH, "./ancestor::label").click()

                elif inputs:
                    print("➡️ Pergunta de texto. Preenchendo...")
                    inputs[0].send_keys(resposta)
                    print(f"✅ Resposta preenchida: {resposta}")

                else:
                    print("⚠️ Nenhum input encontrado neste fieldset.")

                time.sleep(1)

            except Exception as e:
                print(f"❌ Erro processando fieldset: {e}")

        # Botão para salvar e continuar
        driver.wait_and_click('button[name="saveAndContinueButton"]')
        print("🚀 Formulário enviado com sucesso!")

        time.sleep(3)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
