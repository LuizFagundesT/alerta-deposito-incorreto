# 📦 Verificador de Depósito – Sitrack <img align="center" alt="Luiz-py" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">

##  <img width="30" height="40" alt="image" src="https://github.com/user-attachments/assets/78890552-eb1e-484d-bc5f-492230271bab" /> Descrição
Este projeto em Python tem como objetivo verificar se dispositivos estão
alocados no **depósito correto de estoque** no sistema **Sitrack**. Um projeto de escopo mais fechado no entando explora pontos importantes quanto ao uso do Python na automação de tarefas no setor de produção.

A partir de uma lista de IDs fornecida em um arquivo CSV, o script:
- autentica na API do Sitrack;
- consulta o depósito atual de cada dispositivo;
- identifica quais IDs estão fora do depósito de estoque;
- envia automaticamente um **relatório por e-mail** com os resultados.

---

## 🧠 Contexto
Atualmente, no sistema, os IDs representam equipamentos físicos.
Durante o processo de produção, esses equipamentos precisam ser movimentados para o depósito de estoque, o que faz parte de uma rotina operacional da empresa.

O sistema Sitrack utiliza autenticação via PHPSESSID para permitir o acesso à sua API.
Este script automatiza o processo de obtenção do PHPSESSID, eliminando a necessidade de autenticação manual e reduzindo significativamente erros operacionais.

Com o PHPSESSID válido, é possível consumir os endpoints da API do Sitrack, informando o ID do equipamento junto ao session ID. A API retorna uma resposta em formato JSON contendo diversos metadados relacionados ao equipamento.

Dentre esses dados, o script utiliza especificamente o campo holderid, que indica em qual depósito o equipamento se encontra.
Essas informações são então filtradas para identificar quais equipamentos não estão alocados no depósito de estoque, permitindo a geração de um relatório automatizado e confiável.

---

## 🛠 Tecnologias Utilizadas
- **Python 3.10+**
- **Pandas** (leitura de CSV)
- **Requests** (consumo da API)
- **SMTP (Gmail)** (envio de e-mails)
- **python-dotenv** (gerenciamento de credenciais)

---

## 📂 Estrutura do Projeto
```text
trocaDep/
├── verificador_deposito_sitrack.py
├── ids.csv
├── credenciais.env
├── requirements.txt
└── README.md
```

---
## ⚙️ Configuração do Ambiente

### 1️ Criar o arquivo `.env`

As credenciais **não ficam no código**.  
Crie um arquivo chamado `credenciais.env` com o seguinte conteúdo:

```env
USER=seu_usuario_sitrack
PASSWORD=sua_senha_sitrack
EMAIL=seu_email@gmail.com
SENHA_APP=sua_senha_de_app_do_google
```
---
## Instalação de dependências
```text
  pip install pandas
  pip install requests
  pip install python-dotenv
  ```

---
## Como utilizar ??
O arquivo deve conter uma coluna chamada id, com os identificadores que serão consultados:
````csv
123456
789012
345678
````
---
## 📊 Regra de Negócio
O depósito de estoque é identificado pelo código:
**140773**

Qualquer dispositivo com holderid diferente desse valor é considerado
fora do depósito correto
---

## 🔐 Segurança

Nenhuma credencial sensível está hardcoded no código
O projeto utiliza variáveis de ambiente
O arquivo .env deve estar listado no .gitignore

---

## <img width="30" height="40" alt="image" src="https://github.com/user-attachments/assets/057d8c57-70c0-445a-ba09-2166d01a0a4c"/> Observações Importantes



O script depende da disponibilidade da API do Sitrack
Não há tratamento de retry para falhas de rede
O envio de e-mail depende da configuração correta do Gmail

---
## <img width="30" height="40" alt="image" src="https://github.com/user-attachments/assets/af624cf8-1723-4078-b0aa-d031f06a8f38" /> Autor

Luiz Gustavo F Teixeira

---
## 🚀 Possíveis Melhorias Futuras

- Separação do código em funções e módulos
- Implementação de logs
- Tratamento de exceções da API
- Agendamento automático (cron / task scheduler)
- Implementação de automação via WEB para realizar automaticamente a troca de deposito de Ids fora do estoque correto
