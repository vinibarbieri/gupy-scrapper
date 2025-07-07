import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def processar_perguntas(driver, gerar_resposta_openai):
    print("\n🔍 Iniciando captura de perguntas...")

    perguntas_processadas = []

    # Captura todos os labels com id que contenha 'additional-question'
    labels = driver.find_elements(By.XPATH, "//label[contains(@id, 'additional-question')]")

    for label in labels:
        try:
            pergunta_texto = label.text.strip()
            input_id = label.get_attribute("for")

            if not input_id:
                continue

            print(f"\n📄 Pergunta detectada: {pergunta_texto}")

            # Tenta localizar o campo associado
            campo = None
            try:
                campo = driver.find_element(By.ID, input_id)
            except NoSuchElementException:
                pass

            # Se for campo de texto ou textarea
            if campo and campo.tag_name in ["input", "textarea"]:
                resposta = gerar_resposta_openai(pergunta_texto)
                campo.clear()
                campo.send_keys(resposta)
                print(f"✅ Respondeu campo de texto/textarea: {resposta}")

                perguntas_processadas.append(pergunta_texto)
                continue

            # Se não for campo direto, verifica se é grupo de opções (radio ou checkbox)
            opcoes = driver.find_elements(By.XPATH, f"//input[contains(@id, '{input_id}-option')]")

            if opcoes:
                textos_opcoes = []
                for opcao in opcoes:
                    try:
                        label_opcao = opcao.find_element(By.XPATH, "./ancestor::label")
                        texto_opcao = label_opcao.text.strip()
                        textos_opcoes.append((opcao, texto_opcao))
                    except NoSuchElementException:
                        continue

                lista_opcoes_texto = [texto for _, texto in textos_opcoes]
                print(f"📋 Opções detectadas: {lista_opcoes_texto}")

                resposta = gerar_resposta_openai(pergunta_texto + f"\nOpções: {', '.join(lista_opcoes_texto)}")
                print(f"✍️ Resposta escolhida: {resposta}")

                selecionou = False

                for opcao_element, texto in textos_opcoes:
                    if texto.lower() in resposta.lower():
                        try:
                            opcao_element.find_element(By.XPATH, "./ancestor::label").click()
                            print(f"✅ Selecionou: {texto}")
                            selecionou = True
                            break
                        except (NoSuchElementException, ElementClickInterceptedException):
                            pass

                if not selecionou:
                    print("⚠️ Nenhuma opção casou perfeitamente. Selecionando a primeira.")
                    textos_opcoes[0][0].find_element(By.XPATH, "./ancestor::label").click()

                perguntas_processadas.append(pergunta_texto)
                continue

            print("⚠️ Não foi possível determinar o tipo da pergunta.")

        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {e}")

    # Agora tenta localizar textareas ou inputs que não tenham label
    campos_texto_extra = driver.find_elements(By.XPATH, "//textarea[contains(@id, 'additional-question')]")
    campos_input_extra = driver.find_elements(By.XPATH, "//input[contains(@id, 'additional-question')]")

    for campo in campos_texto_extra + campos_input_extra:
        try:
            campo_id = campo.get_attribute("id")
            label = driver.find_element(By.XPATH, f"//label[@for='{campo_id}']")
            pergunta_texto = label.text.strip()

            if pergunta_texto not in perguntas_processadas:
                resposta = gerar_resposta_openai(pergunta_texto)
                campo.clear()
                campo.send_keys(resposta)
                print(f"✅ Respondeu campo extra: {pergunta_texto} -> {resposta}")
                perguntas_processadas.append(pergunta_texto)

        except NoSuchElementException:
            continue

    print(f"\n✅ Processamento concluído! Total de perguntas respondidas: {len(perguntas_processadas)}")
