import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

CONSULTANT = "your_username_here"

PROGRAMS = {
    "shudnennia": {
        "base": "🥤 Formula 1 + чай",
        "mid": "🥤 Formula 1 + чай + Aloe + Protein Drink Mix",
        "max": "🥤 Повний комплекс: Formula 1 + чай + Aloe + Protein"
    },
    "pidtrymka": {
        "base": "🥗 Formula 1 + чай",
        "mid": "🥗 Formula 1 + Aloe + баланс харчування",
        "max": "🥗 Повний wellness-комплекс"
    },
    "masa": {
        "base": "💪 Formula 1 + Protein Drink Mix",
        "mid": "💪 Formula 1 + Protein + перекуси",
        "max": "💪 Повний набір для маси"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Схуднення", callback_data="shudnennia")],
        [InlineKeyboardButton("⚖️ Підтримка", callback_data="pidtrymka")],
        [InlineKeyboardButton("💪 Маса", callback_data="masa")]
    ]

    await update.message.reply_text(
        "Вітаю 👋 Обери мету:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["goal"] = query.data

    keyboard = [
        [InlineKeyboardButton("🥉 Мала", callback_data="base")],
        [InlineKeyboardButton("🥈 Середня", callback_data="mid")],
        [InlineKeyboardButton("🥇 Макс", callback_data="max")]
    ]

    await query.message.reply_text(
        "Оберіть рівень програми:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    goal = context.user_data.get("goal")
    level = query.data

    text = PROGRAMS.get(goal, {}).get(level, "Немає даних")

    keyboard = [
        [InlineKeyboardButton(
            "📲 Консультант",
            url=f"https://t.me/{CONSULTANT.replace('@','')}"
        )]
    ]

    await query.message.reply_text(
        f"📦 Ваша програма:\n\n{text}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    if not TOKEN:
        print("❌ BOT_TOKEN не знайдено в Environment Variables")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_goal, pattern="^(shudnennia|pidtrymka|masa)$"))
    app.add_handler(CallbackQueryHandler(handle_level, pattern="^(base|mid|max)$"))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
