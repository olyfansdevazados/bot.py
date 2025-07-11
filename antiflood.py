import time
from functools import partial
from typing import Union

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_CHAT, ADMINS, SUDOERS
from database import cur, save
from utils import create_mention, is_user_banned

cur.execute("CREATE TABLE IF NOT EXISTS antiflood (user_id, unix_time)")


@Client.on_message(
    ~filters.channel & ~filters.user(ADMINS + SUDOERS) & filters.regex(r"^/"), group=-3
)
@Client.on_callback_query(~filters.user(ADMINS + SUDOERS), group=-3)
async def antiflood(c: Client, m: Union[CallbackQuery, Message]):
    # Delete old rows.
    cur.execute("DELETE FROM antiflood WHERE unix_time < ?", [int(time.time()) - 5])

    # Insert antiflood row.
    cur.execute(
        "INSERT INTO antiflood (user_id, unix_time) VALUES (?,?)",
        [m.from_user.id, int(time.time())],
    )

    # Get total rows count.
    msg_count = cur.execute(
        "SELECT COUNT() FROM antiflood WHERE user_id = ?", [m.from_user.id]
    ).fetchone()[0]

    if isinstance(m, CallbackQuery):
        max_count = 10
    else:
        max_count = 10

    if msg_count > max_count:
        return await m.stop_propagation()

    if msg_count == max_count:
        if is_user_banned(m.from_user.id):
            return await m.stop_propagation()

        cur.execute(
            "UPDATE users SET is_blacklisted = 1 WHERE id = ?", [m.from_user.id]
        )
        save()

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "✅ Desbanir", callback_data=f"unban_user {m.from_user.id}"
                    )
                ]
            ]
        )

        mention = create_mention(m.from_user)

        await c.send_message(
            ADMIN_CHAT,
            f"<b>⛔️ {mention} foi banido automaticamente por flood.</b>",
            reply_markup=kb,
        )

        if isinstance(m, CallbackQuery):
            send_text = partial(c.send_message, m.from_user.id)
        else:
            send_text = m.reply_text

        await send_text(
            "<b>⛔️ Você foi automaticamente banido do bot por flood.</b> "
            "Caso ache que isso é um erro, entre em contato com o dono do bot."
        )

        return await m.stop_propagation()
