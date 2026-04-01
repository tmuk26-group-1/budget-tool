from db.crud import create_user, get_users

# create_user("abc@gmail.com", "Bob", "Bobsson", "bobban", "1234")
list = get_users()
bobban = list[0]
print(bobban)
