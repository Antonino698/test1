from typing import Final
from telegram import Update
import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from datetime import datetime, timedelta
from dateutil import parser


TOKEN: Final = '6330182331:AAGHzlu-MmTk4Bu20Kfc3X-eYDH3YoVTD9s'
BOT_USERNAME: Final ='@TestQD2023bot'


##FUNZ START
#messaggio di benvenuto e intro ai comandi del bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Ciao!')


##FUNZ DI VISUALIZZAZIONE MENU
# visualizza il menu in formato jpeg e se lo vuoi come poster autografato richiedi la versione png a soli 9,95$
async def menu_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('il file sta arrivando')
    #return context.bot.send_document(update.effective_chat.id, document=open('menu-completo.pdf' , 'rb'))
    #return context.bot.send_document(update.effective_chat.id, "https://palermo.prezzemoloevitale.it/media/downloadable/menu/_menu_completo.pdf")
    return await context.bot.send_photo(update.effective_chat.id, photo=open('image1.jpg' , 'rb'))

##FUNZ DI VISUALIZZAZIONE SPECIAL NIGHTS EVENTS
# visualizza le locandine degli eventi (mar:'Cena con delitto', giov:'giovedì gnocco', sab:'discoDinner')
async def eventi_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('il file sta arrivando')
    #return context.bot.send_document(update.effective_chat.id, document=open('menu-completo.pdf' , 'rb'))
    #return context.bot.send_document(update.effective_chat.id, "https://palermo.prezzemoloevitale.it/media/downloadable/menu/_menu_completo.pdf")
    return await context.bot.send_photo(update.effective_chat.id, photo=open('image1.jpg' , 'rb'))

##FUNZ DI VISUALIZZAZIONE INFO
# visualizza le info del ristorante cioè via(con link a maps),orari,numeri.
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restaurant_info = "Numero di telefono: +1234567890\nIndirizzo: Via del Ristorante, 12345, Città"
    await update.message.reply_text(restaurant_info)
  

""" async def select_date(update, context):
    button_list = []
    current_date = datetime.now()
    for i in range(7):
        date = current_date + timedelta(days=i)
        button_list.append([InlineKeyboardButton(date.strftime('%Y-%m-%d'), callback_data=str(date))])

    reply_markup = InlineKeyboardMarkup(button_list)
    await update.message.reply_text('Seleziona una data:', reply_markup=reply_markup) """




""" async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print (f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
     response: str =handle_response(text)

    print ('Bot' , response)
    await update.message.reply_text(response)

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'ciao' in processed:
        return 'MA CHE VUOI?'
    
    #if 'prenota' in processed:

       # return 'ANCORA CO STA PRENOTAZIONE'
    
    return 'non ho capito...' """

##FUNZ PER PRENOTARE IL TAVOLO '/prenota'
#1.chiede il numero di persone (>1 && <=10)
#2.mostra le fasce orarie disponibili(button), permette di selezionarne una tra quelle con numero_dip>=num-pers. (20:00 || 21:00 || 22:00). altrimenti mostra testo di scuse 'ritenta più tardi o domani'
#3.memorizza la prenotazione su db e assegna id_prenotazione (chiave primaria)
async def prenotazioni_command(update, context):
    button_list = []
    current_date = datetime.now()
    for i in range(7):
        date = current_date + timedelta(days=i)
        button_list.append([InlineKeyboardButton(date.strftime('%Y-%m-%d'), callback_data=str(date))])

async def date_button_click(update, context):
    selected_date = update.callback_query.data
    parsed_date = parser.parse(selected_date)
    await update.callback_query.message.reply_text(f'Hai selezionato la data: {parsed_date.strftime("%Y-%m-%d")}')

##FUNZ PER GESTIRE LA PRENOTAZIONE '/le_mie_prenotazioni'
#permette di visualizzare la prenotazione corrente, se esiste, e di disdirla(button) 
#disdire la prenotazione consiste in:
#-cercare la prenotazione dell'utente(tramite id_prenotazione) nel db
#-ripristinare i posti disponibili nella fascia oraria di riferimento

if __name__ == '__main__':
    print('MI STO ACCENDENDO')
    app= Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('prenota', prenotazioni_command))
    app.add_handler(CommandHandler('menu', menu_command))
    # app.add_handler(CommandHandler('back_to_start', start_command))
    #app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(CommandHandler('eventi', eventi_command))
    #app.add_handler(CommandHandler('info', select_date))
    app.add_handler(CallbackQueryHandler(date_button_click))

                      
    #app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #app.add_error_handler(error)

    app.run_polling(poll_interval=3)