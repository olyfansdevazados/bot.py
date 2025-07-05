# Cyberspace bot

##This source serves as a base for Cyberspace store bots.
##It aims to be as modular as possible, allowing adding new features with minor effort.

## Example config file

##```python
# Your Telegram bot token.
BOT_TOKEN = "7998145772:AAHZj8nDAxneu_7_8h42SHd9VxIvvKj5Tss"

# Telegram API ID and Hash. This is NOT your bot token and shouldn't be changed.
API_ID = 24604162
API_HASH = "b29ef0c9bfb01b6f1af7961c51d82726"

# Chat used for logging errors.
LOG_CHAT = -4718120083

# Chat used for logging user actions (like buy, gift, etc).
ADMIN_CHAT = -4718120083
GRUPO_PUB = -4718120083


# How many updates can be handled in parallel.
# Don't use high values for low-end servers.
WORKERS = 20

# Admins can access panel and add new materials to the bot.
ADMINS = [8135002019 , 7735036614]

# Sudoers have full access to the server and can execute commands.
SUDOERS = [8135002019 , 7735036614]

# All sudoers should be admins too
ADMINS.extend(SUDOERS)

GIFTERS = []

# Bote o Username do bot sem o @
# Exemplo: default
BOT_LINK = "raul01net_bot"



# Bote o Username do suporte sem o @
# Exemplo: suporte
BOT_LINK_SUPORTE = "raul01net_bot"
##```
