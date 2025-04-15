import requests

def envoyer_resultat_whatsapp(score, total, numero_parent):
    url = "https://graph.facebook.com/v19.0/599165689952317/messages"

    headers = {
        "Authorization": "Bearer EAAR18KhFZCCsBOZCnhTOZCPySQMKndUfYAv899dIVuIZC6Bm0gzLL5xqmVQBrvW6Q3jZAPMV7WWESkeFyn7boUdfjqrJQsDY5pvb9cUbZA9haHFwg98Snc6cmd7xO9A3cK2ZChKwJynN9tRAGOemWzG5IH4bhOg0vdbryoRfvRR1LQSAm5kdEXAlcqZBU79jGVGwAHVHLPwNx3M65VHZAbu7sDOTdvCMZD",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero_parent,
        "type": "text",
        "text": {
            "body": f"🎉 Résultats du jeu de maths 🎲\nScore : {score}/{total}\nBravo à ton enfant !"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ Message envoyé avec succès")
    else:
        print(f"❌ Erreur d'envoi : {response.status_code} — {response.text}")


# Exemple d'utilisation
if __name__ == "__main__":
    score = 8
    total = 10
    numero_parent = "41787199620"  # Remplacez par le numéro de téléphone du parent
    envoyer_resultat_whatsapp(score, total, numero_parent)