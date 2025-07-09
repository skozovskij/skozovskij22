import json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import Message
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import CreateAccountParams, create_account
from solders.instruction import Instruction, AccountMeta
import os

# Ініціалізація клієнта Solana
client = Client("https://api.devnet.solana.com")

# Створення гаманців
payer = Keypair()
data_account = Keypair()
print("payer pubkey:", payer.pubkey())
print("data_account pubkey:", data_account.pubkey())

# Зчитування даних з локального файлу
file_path_1 = "local_data.json"
file_path_2 = "comparison_data.json"
comparison_data = {}
if os.path.exists(file_path_1) and os.path.getsize(file_path_1) > 0:
    with open(file_path_1, "r", encoding="utf-8") as file:
        try:
            local_data = json.load(file)
        except json.JSONDecodeError:
            print("Помилка: Файл містить некоректні JSON-дані.")
            local_data = {}
else:
    print("Помилка: Файл порожній або не існує.")
    local_data = {}


# **Порівняння даних та відсіювання різниці**
filtered_data = {key: value for key, value in local_data.items() if key not in comparison_data}

if filtered_data:
    # **Запис у Solana**
    text_data = json.dumps(filtered_data).encode("utf-8")
    instruction_store = Instruction(
        accounts=[
            AccountMeta(pubkey=data_account.pubkey(), is_signer=False, is_writable=True)
        ],
        program_id=Pubkey.from_string("9xQeWvGJavGWX6McsZpuZm3wVnN3Ki53CW2KycsM6XHt"),
        data=text_data
    )
    message = Message(instructions=[instruction_store])
    transaction_store = Transaction(
        from_keypairs=[payer],
        message=message,
        recent_blockhash=client.get_latest_blockhash().value.blockhash
    )
    transaction_store.sign([payer])
    client.send_transaction(transaction_store, payer)

    # **Оновлення файлу з яким порівнювали**
    comparison_data.update(filtered_data)
    with open(file_path_2, "w", encoding="utf-8") as file:
        json.dump(comparison_data, file, ensure_ascii=False, indent=4)

print("Дані успішно оновлені та записані в Solana!")

account_info = client.get_account_info(data_account.pubkey())
stored_data = bytes(account_info.value.data[0]).decode("utf-8")

print("Збережені дані в Solana:", stored_data)