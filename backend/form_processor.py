import time
from selenium.webdriver.common.by import By
from openai_helper import gerar_resposta_openai


def processar_todas_perguntas(driver):
    print("\n🔍 Iniciando captura de perguntas...")

    # 🔥 Captura todos os elementos com ID que contenha "additional-question"
    elementos_pergunta = driver.find_elements(By.XPATH, "//*[contains(@id, 'additional-question')]")

    perguntas_processadas = []

    for elemento in elementos_pergunta:
        try:
            # Detecta se é um label (pergunta) ou input/textarea (campo de resposta)
            if elemento.tag_name in ['label', 'legend']:
                texto = elemento.text.strip()
                if texto and texto not in perguntas_processadas:
                    perguntas_processadas.append(texto)
                    print(f"📝 Pergunta detectada: {texto}")
            else:
                continue
        except Exception as e:
            print(f"❌ Erro capturando pergunta: {e}")

    print(f"\n✅ Total de perguntas encontradas: {len(perguntas_processadas)}\n")

    for idx, pergunta in enumerate(perguntas_processadas, 1):
        print(f"🔄 Processando pergunta {idx}/{len(perguntas_processadas)}")
        try:
            resposta = gerar_resposta_openai(pergunta)
            print(f"✍️ Resposta OpenAI: {resposta}")

            # 📦 Detecta se é input, textarea, radio ou checkbox
            input_element = encontrar_elemento_resposta(driver, pergunta)

            if input_element is None:
                print("⚠️ Nenhum campo de resposta encontrado.")
                continue

            tag = input_element.tag_name.lower()

            if tag == 'input' and input_element.get_attribute('type') in ['text', 'input']:
                input_element.clear()
                input_element.send_keys(resposta)
                print(f"✅ Preencheu input com: {resposta}")

            elif tag == 'textarea':
                input_element.clear()
                input_element.send_keys(resposta)
                print(f"✅ Preencheu textarea com: {resposta}")

            elif tag == 'input' and input_element.get_attribute('type') in ['radio', 'checkbox']:
                label = input_element.find_element(By.XPATH, './ancestor::label')
                label.click()
                print(f"✅ Selecionou opção: {label.text.strip()}")

            else:
                print(f"⚠️ Tipo de input não tratado: {tag}")

            time.sleep(1)

        except Exception as e:
            print(f"❌ Erro processando pergunta: {e}")


def encontrar_elemento_resposta(driver, texto_pergunta):
    try:
        # Encontra input, textarea ou opções que contenham o mesmo ID da pergunta
        id_fragment = texto_pergunta.split('.')[0].strip()  # exemplo: '2' em '2. Qual sua...'

        xpath = f"//*[contains(@id, 'additional-question-input-{id_fragment}')]"
        elementos = driver.find_elements(By.XPATH, xpath)

        if elementos:
            return elementos[0]

        # Tenta pegar textareas
        xpath_textarea = f"//*[contains(@id, 'additional-question-textarea-{id_fragment}')]"
        elementos = driver.find_elements(By.XPATH, xpath_textarea)

        if elementos:
            return elementos[0]

        return None
    except:
        return None
import time
from selenium.webdriver.common.by import By
from openai_helper import gerar_resposta_openai


def processar_todas_perguntas(driver):
    print("\n🔍 Iniciando captura de perguntas...")

    # 🔥 Captura todos os elementos com ID que contenha "additional-question"
    elementos_pergunta = driver.find_elements(By.XPATH, "//*[contains(@id, 'additional-question')]")

    perguntas_processadas = []

    for elemento in elementos_pergunta:
        try:
            # Detecta se é um label (pergunta) ou input/textarea (campo de resposta)
            if elemento.tag_name in ['label', 'legend']:
                texto = elemento.text.strip()
                if texto and texto not in perguntas_processadas:
                    perguntas_processadas.append(texto)
                    print(f"📝 Pergunta detectada: {texto}")
            else:
                continue
        except Exception as e:
            print(f"❌ Erro capturando pergunta: {e}")

    print(f"\n✅ Total de perguntas encontradas: {len(perguntas_processadas)}\n")

    for idx, pergunta in enumerate(perguntas_processadas, 1):
        print(f"🔄 Processando pergunta {idx}/{len(perguntas_processadas)}")
        try:
            resposta = gerar_resposta_openai(pergunta)
            print(f"✍️ Resposta OpenAI: {resposta}")

            # 📦 Detecta se é input, textarea, radio ou checkbox
            input_element = encontrar_elemento_resposta(driver, pergunta)

            if input_element is None:
                print("⚠️ Nenhum campo de resposta encontrado.")
                continue

            tag = input_element.tag_name.lower()

            if tag == 'input' and input_element.get_attribute('type') in ['text', 'input']:
                input_element.clear()
                input_element.send_keys(resposta)
                print(f"✅ Preencheu input com: {resposta}")

            elif tag == 'textarea':
                input_element.clear()
                input_element.send_keys(resposta)
                print(f"✅ Preencheu textarea com: {resposta}")

            elif tag == 'input' and input_element.get_attribute('type') in ['radio', 'checkbox']:
                label = input_element.find_element(By.XPATH, './ancestor::label')
                label.click()
                print(f"✅ Selecionou opção: {label.text.strip()}")

            else:
                print(f"⚠️ Tipo de input não tratado: {tag}")

            time.sleep(1)

        except Exception as e:
            print(f"❌ Erro processando pergunta: {e}")


def encontrar_elemento_resposta(driver, texto_pergunta):
    try:
        # Encontra input, textarea ou opções que contenham o mesmo ID da pergunta
        id_fragment = texto_pergunta.split('.')[0].strip()  # exemplo: '2' em '2. Qual sua...'

        xpath = f"//*[contains(@id, 'additional-question-input-{id_fragment}')]"
        elementos = driver.find_elements(By.XPATH, xpath)

        if elementos:
            return elementos[0]

        # Tenta pegar textareas
        xpath_textarea = f"//*[contains(@id, 'additional-question-textarea-{id_fragment}')]"
        elementos = driver.find_elements(By.XPATH, xpath_textarea)

        if elementos:
            return elementos[0]

        return None
    except:
        return None
