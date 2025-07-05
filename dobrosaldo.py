from functools import partial as partial

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMINS
from database import cur, save
from gates import *

GATES = {
    "5": 5,
    "10": 10,
    "20": 20,
    "30": 30,
    "40": 40,
    "50": 50,
    "60": 60,
     "70": 70,
     "80": 80,
     "90": 90,
     "100": 100,
    "0": 0,
}  # fmt: skip


# Copiando o GATES (que é uma constante) para uma variável,
# na qual poderá ser modificada posteriormente.
gates = GATES.copy()


@Client.on_callback_query(filters.regex(r"^dobro$") & filters.user(ADMINS))
async def type_chk(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Configuração porcentagem bonus", callback_data="dobro dobro"),
                
            ],
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="painel"),
            ],
        ]
    )
    


    await m.edit_message_text(
        "<b>🔃 Bonus de saldo</b>\n"
        "<i>- Esta opção permite da bonus ao usuario, caso ele recarregue</i>\n\n"
        "<b>Selecione abaixo a opção desejada:</b>",
        reply_markup=kb,
    )



@Client.on_callback_query(
    filters.regex(r"^dobro (?P<chk_type>.+)$") & filters.user(ADMINS)
)
async def options_gates(c: Client, m: CallbackQuery):
    type_exchange = m.matches[0]["chk_type"]
    bt_list = []
    for opt in gates:
        bt_list.append(
            InlineKeyboardButton(
                text=f"✦ {opt}", callback_data=f"set_dobro {type_exchange} {opt}"
            )
        )

    orgn = (lambda data, step: [data[x : x + step] for x in range(0, len(data), step)])(
        bt_list, 2
    )
    orgn.append([InlineKeyboardButton(text="🔙 Voltar", callback_data="dobro")])
    kb = InlineKeyboardMarkup(inline_keyboard=orgn)

    await m.edit_message_text(
        "<b>🔃 Selecione a gate para operar checagem no bot</b>", reply_markup=kb
    )


@Client.on_callback_query(
    filters.regex(r"^set_dobro (?P<chk_type>.+) (?P<gate>.+)") & filters.user(ADMINS)
)
async def dobro(c: Client, m: CallbackQuery):
    var_alt = m.matches[0]["chk_type"]
    gate = m.matches[0]["gate"]

    if var_alt == "exchange":
        cur.execute("UPDATE dobrosaldo SET valordobro = ?", [gate])
    else:
        cur.execute("UPDATE dobrosaldo SET valordobro = ?", [gate])
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Voltar", callback_data="dobro")]
        ]
    )
    save()
    await m.edit_message_text(
        f"<b>✅ dobro de porcentagem alterado com sucesso. Porcentagem:→ {gate.title()}</b>", reply_markup=kb
    )


@Client.on_callback_query(filters.regex(r"^refresh_gates$") & filters.user(ADMINS))
async def refresh(c: Client, m: CallbackQuery):
    global gates
    gates = GATES.copy()
    await m.answer("Gates reestabelecidas com sucesso.", show_alert=True)











