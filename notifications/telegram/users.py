import telegram
from django.conf import settings
from django.urls import reverse

from bot.common import Chat, ADMIN_CHAT, send_telegram_message, render_html_message


def notify_profile_needs_review(user, intro):
    user_profile_url = settings.APP_HOST + reverse("profile", kwargs={"user_slug": user.slug})
    send_telegram_message(
        chat=ADMIN_CHAT,
        text=render_html_message("moderator_new_member_review.html", user=user, intro=intro),
        reply_markup=telegram.InlineKeyboardMarkup([
            [
                telegram.InlineKeyboardButton("👍 Впустить", callback_data=f"approve_user:{user.id}"),
                telegram.InlineKeyboardButton("❌️ Отказать", callback_data=f"reject_user:{user.id}"),
            ],
            [
                telegram.InlineKeyboardButton("😏 Посмотреть", url=user_profile_url),
            ]
        ])
    )


def notify_user_profile_approved(user):
    user_profile_url = settings.APP_HOST + reverse("profile", kwargs={"user_slug": user.slug})

    if user.telegram_id:
        send_telegram_message(
            chat=Chat(id=user.telegram_id),
            text=f"🌴 Подравляем! Вы теперь участник Phangan Club!"
                 f"\n\nЧтобы другие участники узнали о вас еще больше, заполните оставшиеся поля в профиле:"
                 f"\n\n{user_profile_url}"
        )


def notify_user_profile_rejected(user):
    user_profile_url = settings.APP_HOST + reverse("profile", kwargs={"user_slug": user.slug})

    if user.telegram_id:
        send_telegram_message(
            chat=Chat(id=user.telegram_id),
            text=f"😐 К сожалению, ваш профиль не прошел модерацию. Вот, почему так бывает:\n\n"
                 f"- 📜 Маленькое #intro. Расскажите о себе побольше, хотя бы пару абзацев. Для примера посмотрите чужие интро, "
                 f"там есть ссылочки. <a href=\"https://vas3k.club/docs/about/#rules\">Наши правила</a>, "
                 f"с которыми вы согласились, запрещают анонимные профили в Клубе.\n"
                 f"- 🤐 Вымышленное имя или вы не указали фамилию. \n"
                 f"- 🙊 Наличие фраз типа «не скажу», «не люблю писать о себе», «потом заполню». \n\n"
                 f"\n\nПо этой ссылке вы можете исправить свою анкету и податься еще раз: {user_profile_url}"
        )
