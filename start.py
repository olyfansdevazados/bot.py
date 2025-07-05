from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet, dobrosaldo
from config import BOT_LINK
from config import BOT_LINK_SUPORTE


@Client.on_message(filters.command(["start", "menu"]))
@Client.on_callback_query(filters.regex("^start$"))
async def start(c: Client, m: Union[Message, CallbackQuery]):
    user_id = m.from_user.id


    rt = cur.execute(
        "SELECT id, balance, balance_diamonds, refer FROM users WHERE id=?", [user_id]
    ).fetchone()

    if isinstance(m, Message):
        """refer = (
            int(m.command[1])
            if (len(m.command) == 2)
            and (m.command[1]).isdigit()
            and int(m.command[1]) != user_id
            else None
        )

        if rt[3] is None:
            if refer is not None:
                mention = create_mention(m.from_user, with_id=False)

                cur.execute("UPDATE users SET refer = ? WHERE id = ?", [refer, user_id])
                try:
                    await c.send_message(
                        refer,
                        text=f"<b>O usuário {mention} se tornou seu referenciado.</b>",
                    )
                except BadRequest:
                    pass"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("💳 Comprar", callback_data="shop"),
              # InlineKeyboardButton("🎲 Cassino", callback_data="cassino"),
            ],
            
            [
                InlineKeyboardButton("💸 Adicionar saldo", callback_data="add_saldo"),
                InlineKeyboardButton("👤 Suas informações", callback_data="user_info"),
                
            ],
             [InlineKeyboardButton("✅ Trocas", callback_data="exchange"),],
            
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""‌<a href='{bot_logo}'>&#8204</a><b>Olá</b> {m.from_user.first_name}, <i>Seja bem-vindo!</i>

<a href="t.me/PuxadasGratis7">👥 Grupo</a>
<a href="t.me/rickstoreref">📢 Canal</a>
<a href="t.me/suporterick">👤 Atendimento</a>

💵 | Saldo em dobro: {dobrosaldo()}
"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
