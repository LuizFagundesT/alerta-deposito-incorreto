
# IMPORTS
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import smtplib
from email.message import EmailMessage

##CREDENCIAIS 
load_dotenv(r'trocaDep\credenciais.env')
userSitrack = os.getenv('USER')
senhaSitrack = os.getenv('PASSWORD')
EMAIL= os.getenv('EMAIL')
SENHA_APP = os.getenv('SENHA_APP')

#OBTENDO PHAPSESID
# endpoint para obter PHPSESSID, o PPHPSESSID vai autenticar as consultas na api que retorna o deposito em que ID se encontra
urlPHPSESSID = (
    f'https://www.sitrack.com.br/site5/sessions/create'
    f'?userName={userSitrack}&password={senhaSitrack}'
)
responsePHPSESSID = requests.get(url=urlPHPSESSID)
obj = responsePHPSESSID.json()
# sessionid necessário para chamadas da API
PHPSESSID = obj['session']['sessionid']

# LEITURA DOS IDS E VALIDAÇÃO
# lendo base de dados com os IDs que seram consultados.
tabelaIds = pd.read_csv(r'trocaDep\ids.csv')

# lista criada que vai armazenar os ids fora do depósito de estoque
idsForaEstoque = []

#for que percorre 'tabelaIds' fazendo a consulta de cada id encontrado e já realizando o filtro se esta ou não no deposito correto.
for linha in tabelaIds.index:
    valorId = tabelaIds.loc[linha, 'id']

    responseDep = requests.get(
        url=f'https://www.sitrack.com.br/site5/device/?deviceid={valorId}&PHPSESSID={PHPSESSID}'
    )
    objDep = responseDep.json()

    # 140773 = depósito de estoque
    if objDep[0]['holderid'] != 140773:
        idsForaEstoque.append(valorId)



# ENVIO DE E-MAIL COM RESULTADOS
def enviar_email(destinatario, assunto, corpo):
    # MONTAGEM DA MENSAGEM 
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg.set_content(corpo)

    # --- ENVIO ---
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, SENHA_APP)
            smtp.send_message(msg)
        print(f"E-mail enviado para {destinatario}!")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

# FORMATANDO A LISTA PARA O CORPO DO E-MAIL 
# Criamos uma string onde cada ID fica em uma nova linha
if idsForaEstoque:
    lista_ids_texto = "\n".join(map(str, idsForaEstoque))
    corpo_mensagem = f"Olá,\n\nOs seguintes IDs foram identificados FORA do depósito de estoque:\n\n{lista_ids_texto}\n\nTotal de itens: {len(idsForaEstoque)}"
else:
    corpo_mensagem = "Nenhum ID foi encontrado fora do depósito de estoque hoje."

#Chamando a função para enviar para o seu e-mail
enviar_email(
    destinatario="luizagustinho032@gmail.com", 
    assunto="Relatório de IDs Fora de Estoque", 
    corpo=corpo_mensagem
)

