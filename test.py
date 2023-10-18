from typing import Final
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from datetime import datetime, timedelta
from dateutil import parser

TOKEN: Final = '6330182331:AAGHzlu-MmTk4Bu20Kfc3X-eYDH3YoVTD9s'
BOT_USERNAME: Final ='@TestQD2023bot'

# Funzione per iniziare la prenotazione
async def start_booking(update, context):
    await update.message.reply_text("Benvenuto nel servizio di prenotazione tavoli. Usa /selectdate per selezionare una data.")

# Funzione per selezionare una data
async def select_date(update, context):
    button_list = []
    current_date = datetime.now()
    
    for i in range(7):
        date = current_date + timedelta(days=i)
        button_list.append([InlineKeyboardButton(date.strftime('%Y-%m-%d'), callback_data=str(date))])

    reply_markup = InlineKeyboardMarkup(button_list)
    await update.message.reply_text('Seleziona una data per la prenotazione:', reply_markup=reply_markup)

# Funzione per gestire il clic su una data
async def button_click(update, context):
    selected_date = update.callback_query.data
    parsed_date = parser.parse(selected_date)
    context.user_data['selected_date'] = parsed_date
    await update.callback_query.message.reply_text(f'Hai selezionato la data: {parsed_date.strftime("%Y-%m-%d")}. Ora, quanti posti desideri prenotare?')

# Funzione per gestire il numero di posti e completare la prenotazione
async def confirm_booking(update, context):
    num_seats = update.message.text
    try:
        num_seats = int(num_seats)
        if num_seats > 0:
            selected_date = context.user_data.get('selected_date')
            if selected_date:
                await update.message.reply_text(f'Hai prenotato {num_seats} posti per il {selected_date.strftime("%Y-%m-%d")}. Grazie per la prenotazione!')
            else:
                await update.message.reply_text('Si è verificato un problema con la data. Riprova.')
        else:
            await update.message.reply_text('Il numero di posti deve essere maggiore di zero. Riprova.')
    except ValueError:
        await update.message.reply_text('Per favore, inserisci un numero valido di posti.')

# Funzione principale
if __name__ == '__main__':
    print('MI STO ACCENDENDO')
    app= Application.builder().token(TOKEN).build()
    #updater = Updater(TOKEN)
    #dp = updater.dispatcher

    app.add_handler(CommandHandler("start", start_booking))
    app.add_handler(CommandHandler("prenota", select_date))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT, confirm_booking))

    app.run_polling(poll_interval=3)


