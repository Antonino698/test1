from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN: Final = '6330182331:AAGHzlu-MmTk4Bu20Kfc3X-eYDH3YoVTD9s'
BOT_USERNAME: Final ='@TestQD2023bot'
NOME_TAVOLO, NUMERO_PERSONE, ORARIO = range(3)
posti_disponibili = {'20:00': 10, '21:00': 10, '22:00': 10}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Ciao!')

async def prenotazioni_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=f"Ciao {user.mention_markdown_v2()}, inserisci il nome del tavolo:")
    return NOME_TAVOLO

async def handle_nome_tavolo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data[NOME_TAVOLO] = update.message.text

    update.message.reply_text("Ottimo! Ora inserisci il numero di persone (massimo 10):")
    return NUMERO_PERSONE

async def handle_numero_persone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    try:
        numero_persone = int(update.message.text)
        if numero_persone < 1 or numero_persone > 10:
            raise ValueError()
        user_data['numero_persone'] = numero_persone

        # Invia i bottoni per selezionare l'orario
        reply_markup = orari_keyboard()
        update.message.reply_text("Seleziona l'orario desiderato:", reply_markup=reply_markup)
        return ORARIO
    except ValueError:
        update.message.reply_text("Inserisci un numero valido (da 1 a 10).")
        return NUMERO_PERSONE

def orari_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("20:00", callback_data='20:00'),
            InlineKeyboardButton("21:00", callback_data='21:00'),
            InlineKeyboardButton("22:00", callback_data='22:00'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def handle_orario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    orario_scelto = query.data

    if posti_disponibili[orario_scelto] > 0:
        user_data['orario'] = orario_scelto
        posti_disponibili[orario_scelto] -= 1  # Decrementa i posti disponibili
        await query.answer(f"Hai prenotato per le {orario_scelto}.")
        await query.edit_message_text("Prenotazione completata. Grazie!")
        
        # Salva i dati nel database o fai qualsiasi altra operazione necessaria

        return ConversationHandler.END
    else:
        await query.answer("Spiacenti, non ci sono posti disponibili per questo orario.")
        # Invia di nuovo i bottoni per selezionare l'orario
        reply_markup = orari_keyboard()
        await query.message.edit_text("Seleziona un orario disponibile:", reply_markup=reply_markup)
        return ORARIO

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'ciao' in processed:
        return 'MA CHE VUOI?'
    
    return 'non ho capito...'

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restaurant_info = "Numero di telefono: +1234567890\nIndirizzo: Via del Ristorante, 12345, Città"
    await update.message.reply_text(restaurant_info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('il file sta arrivando')
    return await context.bot.send_photo(update.effective_chat.id, photo=open('image1.jpg', 'rb'))

if __name__ == '__main__':
    print('MI STO ACCENDENDO')
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prenotazioni', prenotazioni_command)],
        states={
            NOME_TAVOLO: [MessageHandler(filters.TEXT, handle_nome_tavolo)],
            NUMERO_PERSONE: [MessageHandler(filters.TEXT, handle_numero_persone)],
            ORARIO: [CallbackQueryHandler(handle_orario)]
        },
        fallbacks=[],
    )
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('prenotazioni', prenotazioni_command))
    app.add_handler(CommandHandler('menu', download))
    app.add_handler(CommandHandler('back_to_start', start_command))
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)
    app.add_handler(conv_handler)
    app.run_polling(poll_interval=3)
