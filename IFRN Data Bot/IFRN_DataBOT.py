import telebot
from BotFunctions import *

BOT = telebot.TeleBot(API_TOKEN)


'''comandos /help e /start'''
@BOT.message_handler(commands=['help', 'start'])
def send_welcome(message):
    BOT.reply_to(message, """\
Eai, ta afim de ver dados das notas dos anos passados do IFRN?
Assim você pode ter uma base do quanto tirar

    /dados {campus}_{curso}_{turno}_{*cota*}
         - Mostra dados do curso em gráficos temporais

  OBS: o paramêtro entre * é opcional.
\
""")

# Função pra o comando /dados
@BOT.message_handler(commands=['dados'])
def send_welcome(message):
    chat_id = message.chat.id
    curso = (message.text)[7:]
    curso_split = curso.split('_')
    cota = None

    # Se digitou a cota, pegar dados daquela cota:
    if curso_split[-1] in ['Geral', 'L1', 'L2', 'L5', 'L6', 'L15']:
        cota = curso_split[-1]
        df2 = df.loc[(df['Curso'] == str(curso_split[:-1]))
                     & (df['Cota'] == cota)]

    # Senão, pega do curso todo    
    else:
        df2 = df.loc[df['Curso'] == str(curso_split)]
        
    # Resposta    
    if len(df2) == 0:
        BOT.reply_to(message, '''Não achei seu curso. Escreva com iniciais maiúsculas e com acento.
            Ex: /dados Natal - Central_Informatica para Internet_Matutino_Geral''')
    else:
        BOT.reply_to(message, 'Calculando...')

        BOT.send_document(chat_id, getPhoto(df2, curso_split, cota=cota),
                          reply_to_message_id=message.message_id)

BOT.polling()
