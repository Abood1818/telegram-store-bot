import telebot
from telebot import types

# بيانات البوت
BOT_TOKEN = "7390710856:AAGgxZKsyg6tL47IA-KwWVwe66dv85eSBdc"
ADMIN_ID = 671524794  # معرفك على تيليجرام

bot = telebot.TeleBot(BOT_TOKEN)

# قائمة السلع المؤقتة (في الذاكرة فقط)
products = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍️ عرض السلع", "💳 طرق الدفع")
    if message.from_user.id == ADMIN_ID:
        markup.add("➕ إضافة سلعة", "❌ حذف السلع")
    bot.send_message(message.chat.id, "مرحبًا بك في متجرنا ✨\nاختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🛍️ عرض السلع")
def show_products(message):
    if not products:
        bot.send_message(message.chat.id, "لا توجد سلع حالياً.")
        return
    for p in products:
        bot.send_message(message.chat.id, f"📦 {p['name']}\n💰 السعر: {p['price']}")

@bot.message_handler(func=lambda m: m.text == "💳 طرق الدفع")
def show_payment(message):
    bot.send_message(message.chat.id, "💳 طرق الدفع:\n- STC Pay\n- Apple Pay\n- حوالة بنكية\n- PayPal")

@bot.message_handler(func=lambda m: m.text == "➕ إضافة سلعة" and m.from_user.id == ADMIN_ID)
def ask_name(message):
    msg = bot.send_message(message.chat.id, "📝 أرسل اسم السلعة:")
    bot.register_next_step_handler(msg, ask_price)

def ask_price(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "💰 أرسل سعر السلعة:")
    bot.register_next_step_handler(msg, lambda m: save_product(m, name))

def save_product(message, name):
    price = message.text
    products.append({'name': name, 'price': price})
    bot.send_message(message.chat.id, f"✅ تم إضافة السلعة: {name} بسعر {price}")

@bot.message_handler(func=lambda m: m.text == "❌ حذف السلع" and m.from_user.id == ADMIN_ID)
def delete_products(message):
    products.clear()
    bot.send_message(message.chat.id, "🗑️ تم حذف جميع السلع.")

# بدء التشغيل
print("✅ البوت يعمل الآن ...")
bot.infinity_polling()
