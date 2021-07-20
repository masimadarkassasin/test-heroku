from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "1722059977:AAEpKG7MLK4nYSjsqDgM6IBfPhYBo7S2RPc"  # Забираем значение типа str
ADMINS = 997430015 # Тут у нас будет список из админов
