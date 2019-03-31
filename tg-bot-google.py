import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from bs4 import BeautifulSoup
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Preparation
if True:
    token=''
    GOOGLE = range(1)
    ECHO = range(1)

    start_text='I am a bot. Type /help for command list'
    start_google_text='Google search here.'
    start_echo_text = 'What is echo?'
    help_text='\n'.join(['/start - Start the bot.',
                         '/google - Google search.',
                         '/echo - What is echo?',
                         '/help - Command list'])

# Function definition
if True:
    def google_parse(query):
        link='https://www.google.com/search?&q='+query
        res=requests.get(link).text
        soup = BeautifulSoup(res,'html.parser')
        hits=soup.find('div',id='search')
        hittitle = hits.select('h3.r > a')[0].text
        hitlink = hits.select('div > cite')[0].text
        hitdesc = hits.find('span',class_='st').text
        return [hitlink,hittitle,hitdesc]

# Events
if True:
    def start(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=start_text)

    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=help_text)

    def start_google(bot, update):
        user = update.message.from_user
        logger.info(f"User {user.first_name} started Google search.")
        bot.send_message(chat_id=update.message.chat_id, text=start_google_text)
        return GOOGLE

    def google(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='\n\n'.join(google_parse(update.message.text)))

    def start_echo(bot, update):
        user = update.message.from_user
        logger.info("User %s started echo activity.", user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=start_echo_text)
        return ECHO

    def echo(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=f'What is {update.message.text}?')

    def cancel(bot, update):
        user = update.message.from_user
        logger.info(f"User {user.first_name} cancelled the conversation.")
        update.message.reply_text('Activity cancelled.')
        return ConversationHandler.END

    def error(bot, update, error):
        logger.warning(f'Update "{bot}" caused error "{error}"')

# Main
if True:
    def main():
        updater = Updater(token)
        dp = updater.dispatcher

        google_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('google', start_google)],
        states={GOOGLE: [MessageHandler(Filters.text, google)]},
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True)

        echo_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('echo', start_echo)],
        states={ECHO: [MessageHandler(Filters.text, echo)]},
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True)

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(google_conv_handler)
        dp.add_handler(echo_conv_handler)

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
