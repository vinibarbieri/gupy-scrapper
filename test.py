from automation.browser_driver import BrowserDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
import random

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

def gerar_resposta_openai(pergunta, opcoes=None):
    """Gera resposta usando OpenAI baseada no tipo de pergunta"""
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

def capturar_perguntas_labels(driver):
    """Captura perguntas que estão diretamente em labels ligadas a inputs de texto"""
    perguntas_labels = []
    
    try:
        # Encontrar labels com atributo 'for'
        labels = driver.find_elements(By.CSS_SELECTOR, "label[for]")
        
        for label in labels:
            try:
                for_id = label.get_attribute("for")
                if not for_id:
                    continue
                
                # Encontrar o input correspondente
                input_element = driver.find_element(By.ID, for_id)
                input_type = input_element.get_attribute("type")
                
                # Verificar se é um input de texto ou número
                if input_type in ["text", "number", "email", "tel", "url"]:
                    pergunta_texto = label.text.strip()
                    if pergunta_texto:  # Só adiciona se a pergunta não estiver vazia
                        perguntas_labels.append({
                            "tipo": "texto",
                            "pergunta": pergunta_texto,
                            "input_element": input_element,
                            "label_element": label
                        })
                        print(f"📝 Encontrou pergunta em label: {pergunta_texto}")
                        
            except Exception as e:
                print(f"⚠️ Erro processando label: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Erro capturando perguntas em labels: {e}")
    
    return perguntas_labels

def extrair_opcoes_fieldset(fieldset):
    """Extrai as opções disponíveis de um fieldset"""
    opcoes = []
    
    try:
        # Tentar encontrar opções em labels diretos
        labels = fieldset.find_elements(By.TAG_NAME, "label")
        
        for label in labels:
            texto = label.text.strip()
            if texto and texto not in opcoes:  # Evita duplicatas
                opcoes.append(texto)
        
        # Se não encontrou opções em labels diretos, procurar em divs wrapper
        if not opcoes:
            wrapper_labels = fieldset.find_elements(By.CSS_SELECTOR, ".checkbox-label-wrapper label, .radio-label-wrapper label")
            for label in wrapper_labels:
                texto = label.text.strip()
                if texto and texto not in opcoes:
                    opcoes.append(texto)
        
        # Se ainda não encontrou, procurar por spans dentro de labels
        if not opcoes:
            spans = fieldset.find_elements(By.CSS_SELECTOR, "label span")
            for span in spans:
                texto = span.text.strip()
                if texto and texto not in opcoes:
                    opcoes.append(texto)
                    
    except Exception as e:
        print(f"⚠️ Erro extraindo opções do fieldset: {e}")
    
    return opcoes

def capturar_perguntas_fieldsets(driver):
    """Captura perguntas que estão em fieldsets"""
    perguntas_fieldsets = []
    
    try:
        fieldsets = driver.find_elements(By.TAG_NAME, "fieldset")
        
        for fieldset in fieldsets:
            try:
                pergunta_texto = None
                
                # 🔍 Estratégia 1: Tentar encontrar a pergunta no legend
                try:
                    legend = fieldset.find_element(By.TAG_NAME, "legend")
                    pergunta_texto = legend.text.strip()
                    if pergunta_texto:
                        print(f"📝 Pergunta capturada do legend: {pergunta_texto}")
                except:
                    print("⚠️ Legend não encontrado, tentando outros métodos...")
                
                # 🔍 Estratégia 2: Procurar por label não associado a input (sem atributo 'for')
                if not pergunta_texto:
                    try:
                        labels = fieldset.find_elements(By.TAG_NAME, "label")
                        for label in labels:
                            # Verificar se o label não tem atributo 'for' (não está associado a input)
                            for_attr = label.get_attribute("for")
                            if not for_attr:
                                texto_label = label.text.strip()
                                if texto_label and len(texto_label) > 3:  # Texto deve ter pelo menos 3 caracteres
                                    pergunta_texto = texto_label
                                    print(f"📝 Pergunta capturada de label não associado: {pergunta_texto}")
                                    break
                    except Exception as e:
                        print(f"⚠️ Erro buscando labels não associados: {e}")
                
                # 🔍 Estratégia 3: Procurar por divs ou spans descritivos
                if not pergunta_texto:
                    try:
                        # Buscar por divs com classes comuns de perguntas
                        divs_pergunta = fieldset.find_elements(By.CSS_SELECTOR, "div.question, div.pergunta, div.field-label, div.form-label")
                        for div in divs_pergunta:
                            texto_div = div.text.strip()
                            if texto_div and len(texto_div) > 3:
                                pergunta_texto = texto_div
                                print(f"📝 Pergunta capturada de div descritiva: {pergunta_texto}")
                                break
                    except Exception as e:
                        print(f"⚠️ Erro buscando divs descritivas: {e}")
                
                # 🔍 Estratégia 4: Procurar por spans com texto descritivo
                if not pergunta_texto:
                    try:
                        spans = fieldset.find_elements(By.TAG_NAME, "span")
                        for span in spans:
                            texto_span = span.text.strip()
                            if texto_span and len(texto_span) > 3 and not texto_span.isdigit():
                                # Verificar se não é apenas um número ou texto muito curto
                                pergunta_texto = texto_span
                                print(f"📝 Pergunta capturada de span: {pergunta_texto}")
                                break
                    except Exception as e:
                        print(f"⚠️ Erro buscando spans: {e}")
                
                # 🔍 Estratégia 5: Procurar por elementos com atributos específicos
                if not pergunta_texto:
                    try:
                        # Buscar por elementos com atributos que indicam perguntas
                        elementos_pergunta = fieldset.find_elements(By.CSS_SELECTOR, "[data-question], [data-label], [aria-label]")
                        for elemento in elementos_pergunta:
                            texto_elemento = elemento.text.strip()
                            if texto_elemento and len(texto_elemento) > 3:
                                pergunta_texto = texto_elemento
                                print(f"📝 Pergunta capturada de elemento com atributo: {pergunta_texto}")
                                break
                    except Exception as e:
                        print(f"⚠️ Erro buscando elementos com atributos: {e}")
                
                # 🔍 Estratégia 6: Fallback final - usar texto padrão
                if not pergunta_texto:
                    pergunta_texto = "Pergunta não identificada"
                    print("⚠️ Usando texto padrão para pergunta não identificada")
                
                # Verificar tipos de input
                radios = fieldset.find_elements(By.XPATH, ".//input[@type='radio']")
                checkboxes = fieldset.find_elements(By.XPATH, ".//input[@type='checkbox']")
                inputs = fieldset.find_elements(By.XPATH, ".//input[@type='text']")
                
                if radios:
                    opcoes = extrair_opcoes_fieldset(fieldset)
                    perguntas_fieldsets.append({
                        "tipo": "radio",
                        "pergunta": pergunta_texto,
                        "opcoes": opcoes,
                        "fieldset": fieldset
                    })
                    print(f"📝 Encontrou pergunta radio: {pergunta_texto}")
                    
                elif checkboxes:
                    opcoes = extrair_opcoes_fieldset(fieldset)
                    perguntas_fieldsets.append({
                        "tipo": "checkbox",
                        "pergunta": pergunta_texto,
                        "opcoes": opcoes,
                        "fieldset": fieldset
                    })
                    print(f"📝 Encontrou pergunta checkbox: {pergunta_texto}")
                    
                elif inputs:
                    perguntas_fieldsets.append({
                        "tipo": "texto",
                        "pergunta": pergunta_texto,
                        "input_element": inputs[0],
                        "fieldset": fieldset
                    })
                    print(f"📝 Encontrou pergunta texto em fieldset: {pergunta_texto}")
                    
            except Exception as e:
                print(f"⚠️ Erro processando fieldset: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Erro capturando perguntas em fieldsets: {e}")
    
    return perguntas_fieldsets

def selecionar_opcao_radio(fieldset, resposta_openai):
    """Seleciona uma opção de radio baseada no texto retornado pela OpenAI"""
    try:
        radios = fieldset.find_elements(By.XPATH, ".//input[@type='radio']")
        
        # Procura por correspondência exata (ignorando maiúsculas/minúsculas)
        for radio in radios:
            try:
                # Tentar encontrar o label associado
                label = radio.find_element(By.XPATH, "./ancestor::label")
                texto_opcao = label.text.strip()
                
                if texto_opcao.lower() == resposta_openai.lower():
                    label.click()
                    print(f"✅ Selecionou opção radio: {texto_opcao}")
                    return True
                    
            except:
                # Se não encontrar label direto, procurar por label com for
                radio_id = radio.get_attribute("id")
                if radio_id:
                    try:
                        label = fieldset.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                        texto_opcao = label.text.strip()
                        
                        if texto_opcao.lower() == resposta_openai.lower():
                            label.click()
                            print(f"✅ Selecionou opção radio: {texto_opcao}")
                            return True
                    except:
                        continue
        
        # Fallback: seleciona a primeira opção
        if radios:
            try:
                radios[0].find_element(By.XPATH, "./ancestor::label").click()
                print(f"⚠️ Nenhuma correspondência exata. Selecionando primeira opção radio.")
                return True
            except:
                radios[0].click()
                print(f"⚠️ Nenhuma correspondência exata. Selecionando primeira opção radio.")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erro selecionando opção radio: {e}")
        return False

def selecionar_checkbox(fieldset, resposta_openai):
    """Seleciona checkboxes baseado no texto retornado pela OpenAI"""
    try:
        checkboxes = fieldset.find_elements(By.XPATH, ".//input[@type='checkbox']")
        selecionados = 0
        
        # Procura por correspondência exata (ignorando maiúsculas/minúsculas)
        for checkbox in checkboxes:
            try:
                # Tentar encontrar o label associado
                label = checkbox.find_element(By.XPATH, "./ancestor::label")
                texto_opcao = label.text.strip()
                
                if texto_opcao.lower() == resposta_openai.lower():
                    label.click()
                    print(f"✅ Selecionou checkbox: {texto_opcao}")
                    selecionados += 1
                    
            except:
                # Se não encontrar label direto, procurar por label com for
                checkbox_id = checkbox.get_attribute("id")
                if checkbox_id:
                    try:
                        label = fieldset.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
                        texto_opcao = label.text.strip()
                        
                        if texto_opcao.lower() == resposta_openai.lower():
                            label.click()
                            print(f"✅ Selecionou checkbox: {texto_opcao}")
                            selecionados += 1
                    except:
                        continue
        
        # Fallback: seleciona o primeiro checkbox se nenhum foi selecionado
        if selecionados == 0 and checkboxes:
            try:
                checkboxes[0].find_element(By.XPATH, "./ancestor::label").click()
                print(f"⚠️ Nenhuma correspondência exata. Selecionando primeiro checkbox.")
                return True
            except:
                checkboxes[0].click()
                print(f"⚠️ Nenhuma correspondência exata. Selecionando primeiro checkbox.")
                return True
        
        return selecionados > 0
        
    except Exception as e:
        print(f"❌ Erro selecionando checkbox: {e}")
        return False

def processar_pergunta_texto(pergunta_info):
    """Processa uma pergunta de texto"""
    try:
        pergunta = pergunta_info["pergunta"]
        input_element = pergunta_info["input_element"]
        
        print(f"📄 Pergunta de texto: {pergunta}")
        
        # Gerar resposta com OpenAI
        resposta = gerar_resposta_openai(pergunta)
        print(f"✍️ Resposta OpenAI: {resposta}")
        
        # Preencher o input
        input_element.clear()
        input_element.send_keys(resposta)
        print(f"✅ Resposta preenchida: {resposta}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro processando pergunta de texto: {e}")
        return False

def processar_pergunta_radio(pergunta_info):
    """Processa uma pergunta de múltipla escolha (radio)"""
    try:
        pergunta = pergunta_info["pergunta"]
        opcoes = pergunta_info["opcoes"]
        fieldset = pergunta_info["fieldset"]
        
        print(f"📄 Pergunta de múltipla escolha (radio): {pergunta}")
        print(f"📋 Opções disponíveis: {opcoes}")
        
        # Gerar resposta com OpenAI usando as opções
        resposta = gerar_resposta_openai(pergunta, opcoes)
        print(f"✍️ Resposta OpenAI: {resposta}")
        
        # Selecionar a opção correspondente
        return selecionar_opcao_radio(fieldset, resposta)
        
    except Exception as e:
        print(f"❌ Erro processando pergunta radio: {e}")
        return False

def processar_pergunta_checkbox(pergunta_info):
    """Processa uma pergunta de múltipla escolha (checkbox)"""
    try:
        pergunta = pergunta_info["pergunta"]
        opcoes = pergunta_info["opcoes"]
        fieldset = pergunta_info["fieldset"]
        
        print(f"📄 Pergunta de múltipla escolha (checkbox): {pergunta}")
        print(f"📋 Opções disponíveis: {opcoes}")
        
        # Gerar resposta com OpenAI usando as opções
        resposta = gerar_resposta_openai(pergunta, opcoes)
        print(f"✍️ Resposta OpenAI: {resposta}")
        
        # Selecionar o checkbox correspondente
        return selecionar_checkbox(fieldset, resposta)
        
    except Exception as e:
        print(f"❌ Erro processando pergunta checkbox: {e}")
        return False

def processar_todas_perguntas(driver):
    """Processa todas as perguntas encontradas no formulário"""
    print("🔍 Iniciando captura de perguntas...")
    
    # Capturar perguntas em labels
    perguntas_labels = capturar_perguntas_labels(driver)
    print(f"📝 Encontrou {len(perguntas_labels)} perguntas em labels")
    
    # Capturar perguntas em fieldsets
    perguntas_fieldsets = capturar_perguntas_fieldsets(driver)
    print(f"📝 Encontrou {len(perguntas_fieldsets)} perguntas em fieldsets")

    # Capturar 
    
    # Combinar todas as perguntas
    todas_perguntas = perguntas_labels + perguntas_fieldsets
    print(f"📝 Total de perguntas encontradas: {len(todas_perguntas)}")
    
    # Processar cada pergunta
    for i, pergunta_info in enumerate(todas_perguntas, 1):
        print(f"\n🔄 Processando pergunta {i}/{len(todas_perguntas)}")
        
        try:
            if pergunta_info["tipo"] == "texto":
                processar_pergunta_texto(pergunta_info)
            elif pergunta_info["tipo"] == "radio":
                processar_pergunta_radio(pergunta_info)
            elif pergunta_info["tipo"] == "checkbox":
                processar_pergunta_checkbox(pergunta_info)
            
            # Pequena pausa entre perguntas
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Erro processando pergunta {i}: {e}")
            continue
    
    print(f"\n✅ Processamento de {len(todas_perguntas)} perguntas concluído!")

def main():
    driver = BrowserDriver()

    try:
        print("🔗 Acessando a vaga...")
        driver.open_url("https://mobi7.gupy.io/job/eyJqb2JJZCI6OTMxMzIzMywic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=gupy_portal")

        # Fluxo inicial de candidatura
        driver.wait_and_click('[data-testid="apply-link"]')
        print("✅ Clique no botão 'Candidatar-se' realizado.")
        time.sleep(random.uniform(3.2, 6.7))

        # Login
        driver.type('input[name="username"]', 'vinicius190702@hotmail.com')
        time.sleep(random.uniform(0.3, 1.1))
        driver.type('input[name="password"]', 'Br0c0l!s')
        time.sleep(random.uniform(0.4, 1.7))
        driver.wait_and_click('button#button-signin')
        print("✅ Login realizado com sucesso.")

        # Iniciando a candidatura
        driver.wait_and_click('//button[contains(text(), "Continuar")]', by="xpath")
        print("✅ Clique no botão 'Continuar' realizado.")

        # Respostas padrão
        try:
            driver.wait_and_click('//label[contains(., "Não")]', by="xpath")
            print("✅ Respondeu 'Não' para indicação.")
        except:
            print("⚠️ Pergunta sobre indicação não encontrada.")

        try:
            driver.wait_and_click('//label[contains(., "Não")]', by="xpath")
            print("✅ Respondeu 'Não' para trabalhar na empresa.")
        except:
            print("⚠️ Pergunta sobre trabalhar na empresa não encontrada.")

        # try:
        #     driver.type('input[name="howDidYouHearAboutUs"]', 'LinkedIn')
        #     print("✅ Preencheu 'Onde encontrou a vaga' como LinkedIn.")
        # except:
        #     print("⚠️ Campo 'Onde encontrou a vaga' não encontrado.")

        driver.wait_and_click('button[name="saveAndContinueButton"]')
        print("✅ Clique em 'Salvar e continuar' realizado.")

        driver.wait_and_click('button[aria-label="Responder agora"]')
        print("✅ Clique em 'Responder agora' realizado.")

        time.sleep(3)

        # Processar todas as perguntas dinâmicas
        processar_todas_perguntas(driver.driver)

        # Finalizar candidatura
        try:
            driver.wait_and_click('#dialog-give-up-personalization-step')
            print("🚀 Candidatura finalizada com sucesso!")
        except:
            print("⚠️ Botão de finalizar candidatura não encontrado.")

        time.sleep(3)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
