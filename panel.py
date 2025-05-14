from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random
import string
import subprocess

app = Flask(__name__)
DATA_FILE = "used_variants.json"

# Charger les données depuis le fichier JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Sauvegarder les données dans le fichier JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Fonction pour générer des variantes d'email
def generate_email_variants(base_email, count):
    email_prefix, email_domain = base_email.split('@')
    variants = []
    for _ in range(count):
        variant = email_prefix + '.' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)) + '@' + email_domain
        variants.append(variant)
    return variants

@app.route("/")
def index():
    data = load_data()  # Charger les données pour afficher les variantes d'email
    return render_template("panel.html", data=data)

@app.route("/reset", methods=["POST"])
def reset():
    email = request.form.get("email")  # Récupérer l'email à réinitialiser
    data = load_data()
    if email in data:
        del data[email]  # Supprimer l'email du fichier
        save_data(data)  # Sauvegarder les changements
    return redirect(url_for("index"))

# Route pour générer des variantes et enregistrer l'email
@app.route("/generate", methods=["POST"])
def generate():
    email = request.form.get("email")  # Récupérer l'email de base
    variant_count = int(request.form.get("variant_count"))  # Récupérer le nombre de variantes à générer
    variants = generate_email_variants(email, variant_count)  # Générer les variantes
    
    # Sauvegarder les variantes dans le fichier
    data = load_data()
    data[email] = variants  # Ajouter les variantes générées sous l'email de base
    save_data(data)  # Sauvegarder les nouvelles données
    
    return redirect(url_for("index"))

# Route pour lancer le bot (exemple de bot en subprocess)
@app.route("/start_bot", methods=["POST"])
def start_bot():
    try:
        # Exemple de lancement du bot
        # Remplace cette commande par le lancement réel de ton bot
        subprocess.Popen(["python", "Bot Gen Mail.py"])  # Remplace "Bot Gen Mail.py" par le nom réel du fichier bot
        return redirect(url_for("index"))
    except Exception as e:
        # Si une erreur se produit lors du lancement du bot, afficher l'erreur
        return f"Erreur lors du lancement du bot: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
