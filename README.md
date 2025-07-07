# 🤖 Gupy Scrapper - Automatizador de Candidaturas

Um sistema automatizado para aplicar em vagas da plataforma Gupy, desenvolvido em Python com interface web Flask.

## 📋 Descrição

Este projeto automatiza o processo de candidatura em vagas da Gupy, permitindo que você:
- Configure seu perfil profissional uma única vez
- Aplique automaticamente em múltiplas vagas
- Acompanhe o status de todas as suas candidaturas
- Tenha uma interface web intuitiva para gerenciar tudo

## 🚀 Funcionalidades

### Frontend (Flask)
- **Interface Web**: Dashboard moderno e responsivo
- **Gerenciamento de Perfil**: Edite seus dados pessoais, formação, experiências e competências
- **Histórico de Candidaturas**: Visualize todas as aplicações realizadas
- **Status em Tempo Real**: Acompanhe o sucesso/falha de cada candidatura

### Backend (Automação)
- **Web Scraping**: Extração automática de dados das vagas
- **Preenchimento Inteligente**: Uso de IA para responder perguntas específicas
- **Automação de Navegador**: Controle automatizado do Chrome via Selenium
- **Processamento de Formulários**: Preenchimento inteligente de campos

## 🛠️ Tecnologias Utilizadas

### Frontend
- **Flask**: Framework web Python
- **Tailwind CSS**: Framework CSS para design responsivo
- **Jinja2**: Template engine
- **HTML5/CSS3/JavaScript**

### Backend
- **Python**: Linguagem principal
- **Selenium**: Automação de navegador
- **OpenAI API**: Processamento inteligente de perguntas
- **Beautiful Soup**: Web scraping
- **Pandas**: Manipulação de dados

### Automação
- **Chrome WebDriver**: Controle do navegador
- **Web Scraping**: Extração de dados das páginas
- **Form Processing**: Preenchimento inteligente de formulários

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Google Chrome instalado
- Conta na OpenAI (para processamento de perguntas)

### Passos para instalação

1. **Clone o repositório**
```bash
git clone <https://github.com/vinibarbieri/gupy-scrapper>
cd gupy-scrapper
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r backend/requirements.txt
pip install flask
```

5. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_api_aqui
```

## 🚀 Como usar

### 1. Iniciar a aplicação
```bash
python app.py
```

### 2. Acessar a interface web
Abra seu navegador e acesse: `http://localhost:5000`

### 3. Configurar seu perfil
- Clique em "Editar Perfil"
- Preencha todos os dados pessoais, formação, experiências e competências
- Salve as alterações

### 4. Aplicar em vagas
- Na página inicial, cole o link da vaga da Gupy
- Clique em "Aplicar"
- O sistema irá automaticamente:
  - Acessar a vaga
  - Preencher seus dados
  - Responder perguntas específicas (se houver)
  - Submeter a candidatura

### 5. Acompanhar candidaturas
- Visualize o histórico de todas as candidaturas
- Veja o status (sucesso/falha) de cada aplicação
- Acesse os links das vagas diretamente

## 📁 Estrutura do Projeto

```
gupy-scrapper/
├── app.py                 # Aplicação Flask principal
├── dados.json            # Dados do perfil do usuário
├── aplicacoes.json       # Histórico de candidaturas
├── templates/            # Templates HTML
│   ├── base.html
│   ├── home.html
│   └── editar_perfil.html
├── backend/              # Módulos de automação
│   ├── bot_aplicar.py    # Lógica principal do bot
│   ├── form_processor.py # Processamento de formulários
│   ├── openai_helper.py  # Integração com OpenAI
│   ├── automation/       # Automação de navegador
│   └── data/            # Gerenciamento de dados
└── venv/                # Ambiente virtual
```

## ⚙️ Configuração

### Configuração do Perfil
O sistema armazena seus dados em `dados.json`:
- Dados pessoais (nome, email, telefone, CPF)
- Endereço completo
- Formação acadêmica
- Experiências profissionais
- Competências técnicas
- Links (LinkedIn, GitHub)

### Configuração da OpenAI
Para processamento inteligente de perguntas, configure sua API key da OpenAI no arquivo `.env`.

## 🔧 Personalização

### Adicionar novos campos
Para adicionar novos campos ao perfil:
1. Edite `templates/editar_perfil.html`
2. Adicione os campos no formulário
3. Atualize a função `editar_perfil()` em `app.py`
4. Atualize a exibição em `templates/home.html`

### Modificar comportamento do bot
O comportamento principal do bot está em `backend/bot_aplicar.py`. Você pode:
- Ajustar seletores CSS para diferentes layouts
- Modificar lógica de preenchimento
- Adicionar novos tipos de campos

## 📝 Licença

Este projeto é desenvolvido para fins educacionais e de automação pessoal.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## ⚠️ Aviso Legal

Este projeto é destinado para uso pessoal e educacional. Respeite os termos de uso da plataforma Gupy e use de forma responsável. O uso de automação pode violar os termos de serviço de algumas plataformas.

---

**Desenvolvido para facilitar o processo de candidatura em vagas** 