from telebot import TeleBot, types
from config import TOKEN
from services import services
from currency import get_user_currency, set_user_currency, convert_price
from keyboards import main_menu_keyboard, currency_keyboard, services_keyboard

bot = TeleBot(TOKEN)
user_currency = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    set_user_currency(message.chat.id, "USD")
    bot.send_message(message.chat.id, "أهلاً بك عزيزي/عزيزتي 😊\nاختر من القائمة:", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🎯 اختيار العملة")
def handle_choose_currency(message):
    bot.send_message(message.chat.id, "اختر العملة:", reply_markup=currency_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🇺🇸 USD", "🇸🇦 SAR", "🇾🇪 YER"])
def handle_currency_selection(message):
    currency = message.text.split()[1]
    set_user_currency(message.chat.id, currency)
    bot.send_message(message.chat.id, f"✅ تم تغيير العملة إلى {currency}", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🧾 قائمة الخدمات")
def handle_services(message):
    bot.send_message(message.chat.id, "اختر الخدمة لعرض الأسعار:", reply_markup=services_keyboard())

@bot.message_handler(func=lambda msg: msg.text in services)
def handle_service_selection(message):
    currency = get_user_currency(message.chat.id)
    price_list = services[message.text]
    text = f"💰 الأسعار ({currency})\n\n"
    for item, price_usd in price_list.items():
        converted = convert_price(price_usd, currency)
        text += f"• {item} = {converted} {currency}\n"
    bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "⬅️ العودة")
def handle_back(message):
    bot.send_message(message.chat.id, "رجعناك للقائمة الرئيسية:", reply_markup=main_menu_keyboard())

print("🤖 البوت يعمل...")
bot.infinity_polling()
