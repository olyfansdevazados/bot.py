import re

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from config import ADMINS
from database import cur, db


def set_pricefull(price_type: str, price_name: str, price_value: int):
    # Obtém se o item já existe na tabela. Se ele existir, faz o update, caso contrário insere.
    if price_value > 0:
        if cur.execute(
            "SELECT price FROM pricesfull WHERE price_type = ? AND price_name = ?",
            (price_type, price_name),
        ).fetchone():
            cur.execute(
                "UPDATE pricesfull SET price = ? WHERE price_name = ? AND price_type = ?",
                (price_value, price_name, price_type),
            )
            db.commit()
        else:
            cur.execute(
                "INSERT INTO pricesfull(price_name, price_type, price) VALUES(?,?,?)",
                (price_name, price_type, price_value),
            )
            db.commit()
    else:
        # Deleta o valor da table caso ele seja 0.
        cur.execute(
            "DELETE FROM pricesfull WHERE price_type = ? AND price_name = ?",
            (price_type, price_name),
        )
    db.commit()


def get_prices_by_categoryfull(price_type: str):
    q = cur.execute(
        "SELECT price_name, price FROM pricesfull WHERE price_type = ?",
        (price_type,),
    )
    return q.fetchall()




@Client.on_callback_query(
    filters.regex(r"^change_pricefull (?P<ptype>.+)") & filters.user(ADMINS)
)
async def change_price(c: Client, m: CallbackQuery):
    price_type = m.matches[0]["ptype"]

    if price_type == "full":
        exemplo = "gold 12\nplatinum 15\nblack 25"
    elif price_type == "binnull":
        exemplo = "550209 10\n544731 16\n553636 40"
    elif price_type == "mixnull":
        exemplo = "5 20\n10 35\n20 60"
    else:
        raise TypeError(f"Price type is not supported: '{price_type}'.")

    prices = get_prices_by_categoryfull(price_type)

    prices_list = "\n".join([f"{price[0]} {price[1]}" for price in prices])
    
    if len(prices_list) == 0:
         prices_list = "No momento não tem nenhuma categoria, defina seus respectivos valores, igual ao exemplo acima"

    await m.message.delete()

    received = await m.message.ask(
    f"<b>💵 Alterando preços de <i>{price_type}</i></b>\n"
        "<i> - Envie uma tabela com os preços no formato <code>item preço</code>, ex.:</i>\n"
        f"<code>{exemplo}</code>\n\n"
        "<b>Dicas:</b>\n"
        "<i> - Você pode enviar somente os que deseja alterar, não é necessário enviar todos.\n"
        "- Para remover um item, defina o seu valor para <b>0</b>.\n"
        '- Caso seja preço unitário, você pode definir o valor "padrão" de níveis não especificados definindo um valor para <b>indefinido</b>.\n'
        "Para cancelar, envie /cancel.</i>\n\n"
        "<b>Preços atuais desta caregoria:</b>\n"
        f"<code>{prices_list}</code>",
        reply_markup=ForceReply(),
    )

    if received.text.startswith("/"):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔙 Voltar", callback_data="change_pricesfull")],
            ]
        )

        # Utilizando o ReplyKeyboardRemove() para remover o teclado anterior.
        await m.message.reply_text(
            "✔ Comando cancelado.", reply_markup=ReplyKeyboardRemove()
        )

        await m.message.reply_text(
            "✅ Pressione o botão abaixo para voltar.", reply_markup=kb
        )

        return

    # Esse regex retorna uma lista com tuplas contendo o nome e valor dos itens.
    for values in re.finditer(
        r"^(?P<price_name>.+?)\s+(?P<price_value>\d+)$", received.text, flags=re.M
    ):
        price_name = values["price_name"]
        price_value = values["price_value"]

        price_name = price_name.upper()
        price_value = int(price_value)

        set_pricefull(price_type, price_name, price_value)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("✅ Ok", callback_data="change_pricesfull")],
        ]
    )

    await m.message.reply_text(
        f"✅ Preços de <b>{price_type}</b> alterados com sucesso.", reply_markup=kb
    )
