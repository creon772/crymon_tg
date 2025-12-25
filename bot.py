from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import httpx
import asyncio

# ================== НАСТРОЙКИ ==================

TOKEN = "8476951928:AAEzX20GUdAnsCy46q9qBDx4hzt8J9gK-Ks"
WEBAPP_URL = "https://crymon-game.onrender.com"
BACKEND_URL = "https://crymon-game.onrender.com/api/users/create_user"
WEBSITE_URL = "https://crymongame.com"
TG_GROUP_URL = "https://t.me/crymon_game"
SUPPORT_URL = "https://t.me/crymon_cat"

# ================== /START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or ""

    # Проверяем аргументы (referral)
    args = context.args
    ref_id = None
    if args:
        for arg in args:
            if arg.startswith("ref"):
                ref_id = arg[3:]

    # Отправляем данные на бэкенд через POST с JSON
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                BACKEND_URL,
                params={
                    "user_id": str(user_id),
                    "username": username,
                    "referrer_id": ref_id
                },
                timeout=10
            )
            if response.status_code == 200:
                print(f"User {user_id} создан/обновлен на бэкенде")
            else:
                print(f"Ошибка при создании пользователя: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Ошибка запроса к бэкенду: {e}")

    # Кнопка START с WebApp
    keyboard = [[InlineKeyboardButton("START", web_app=WebAppInfo(url=WEBAPP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)


    text = (
        "🚀 *Welcome to CRYMON*\n\n"
        "💎 Mine crypto daily\n"
        "🐱 Collect cats with boosts\n"
        "👥 Earn from referrals\n\n"
        "Tap *Launch App* to start 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🚀 Launch App", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
            InlineKeyboardButton("🌐 Links", callback_data="links"),
        ],
    ]

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================== FAQ ==================

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
    "❓ *CRYMON FAQ*\n\n"

    "*🚀 What is CRYMON?*\n"
    "CRYMON is a crypto mining game inside Telegram.\n"
    "You earn tokens by mining daily, collecting cats,\n"
    "and increasing your mining power over time.\n\n"

    "*⚡ How does mining work?*\n"
    "Mining is automatic.\n"
    "Your daily income depends on:\n"
    "• Your level\n"
    "• Active boosts\n"
    "• Owned cats\n"
    "• Referral bonuses\n\n"

    "*🐱 What are Cats?*\n"
    "Cats are special characters that boost your mining.\n"
    "Each cat has unique power, energy and bonus effects.\n"
    "More cats = higher daily rewards.\n\n"

    "*👥 What is the referral system?*\n"
    "Invite friends using your referral link.\n"
    "When friends join, you receive bonuses 1 $CRYM\n"
    "and grow faster inside the game.\n\n"

    "*🔐 Is it safe?*\n"
    "Yes.\n"
    "Login works via Telegram only.\n"
    "No passwords or private keys required.\n\n"

    "*🎮 Is CRYMON free to play?*\n"
    "Yes.\n"
    "You can start for free and earn through gameplay.\n"
    "Additional boosts are optional.\n\n"

    "*🚧 What’s coming next?*\n"
    "• New cats and boosts\n"
    "• Marketplace\n"
    "• Events and bonuses\n\n"

    "_Welcome to CRYMON. Start small, grow smart 🚀_"
)

    await query.message.reply_text(text, parse_mode="Markdown")

# ================== LINKS ==================

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🌐 Website", url=WEBSITE_URL)],
        [InlineKeyboardButton("💬 Telegram Group", url=TG_GROUP_URL)],
        [InlineKeyboardButton("🛠 Support", url=SUPPORT_URL)],
    ]

    await query.message.reply_text(
        "🌐 *CRYMON Links*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================== ЗАПУСК ==================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(faq, pattern="faq"))
    app.add_handler(CallbackQueryHandler(links, pattern="links"))

    print("CRYMON bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
