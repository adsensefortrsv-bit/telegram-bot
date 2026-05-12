import json

def get_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_user(user_id):
    users = get_users()

    if user_id not in users:
        users.append(user_id)

        with open("users.json", "w") as f:
            json.dump(users, f)
