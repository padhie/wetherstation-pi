import requests

def get_state(home_assistant, entity_id):
    url = f"{home_assistant.url}/api/states/{entity_id}"
    headers = {"Authorization": f"Bearer {home_assistant.token}", "Content-Type": "application/json"}

    r = requests.get(url, headers=headers, timeout=5)
    r.raise_for_status()

    return float(r.json()["state"])