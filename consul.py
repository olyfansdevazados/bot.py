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


@Client.on_message(filters.command(["consul", "consul"]))
@Client.on_callback_query(filters.regex("^consul$"))
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
                InlineKeyboardButton(
                    "🏳️ Pesquisar Consul",
                    switch_inline_query_current_chat="consul_buy RENNER",
                ),
            ],
[
                InlineKeyboardButton("🔸 Voltar",callback_data="start"),
            ],
            ]
    )
    table_name = "consul"
    ccs = cur.execute(
        f"SELECT nomebanco, count() FROM {table_name} GROUP BY nomebanco ORDER BY count() DESC"
    ).fetchall()

    stock = (
        "\n".join([f"<b>{it[0]}</b>: {it[1]}" for it in ccs])
        or "<b>Sem consul no momento</b>"
    )
    total = f"\n\n<b>Total</b>: {sum([int(x[1]) for x in ccs])}" if ccs else ""

    
    
    start_message = f"""OLÁ {m.from_user.first_name},
<a href='https://cdn.dribbble.com/users/2657768/screenshots/15420992/media/7854e227fa9c24f716be63d4a2f35fd9.mp4'>&#8204</a>
Seja Bem - Vindo a aba de consultaveis.
{get_info_wallet(user_id)}



<b>💳 Consultaveis Disponiveis - </b>\n\n{stock}{total}

🎗 Leia as regras e termo de troca se não for de acordo não compre 🎗


⌛️ 15 Minutos para acesso
⏳ 2 Hora para troca por CVV ou VALIDADE errado Fazendo uma gravação comprando no app, Rotativo digital BH 

🔁  Nao havera troca por mateirial com senha suspensa todas sao consultada certa
💳 Compre o  material e acesse pelo 4g fixo se vier com print de acesso com wifi perde a troca
🔁 Nao havera troca por material com saldo inferior vai ser mandado um gift na percentagem
"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
