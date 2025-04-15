import tkinter as tk
import random

# === Configuration ===
NOMBRE_MAX = 10
TEMPS_PAR_QUESTION = 10
NOMBRE_DE_QUESTIONS = 10

# === Variables globales ===
score = 0
total = 0
current_answer = 0
current_question = ""
chrono = None
temps_restant = TEMPS_PAR_QUESTION

# === Fonctions ===

def nouvelle_operation():
    global current_answer, total, current_question, temps_restant

    if total >= NOMBRE_DE_QUESTIONS:
        fin_du_jeu()
        return

    a = random.randint(1, NOMBRE_MAX)
    b = random.randint(1, NOMBRE_MAX)
    op = '+'  # pour simplifier

    current_answer = a + b
    current_question = f"{a} {op} {b}"
    question_label.config(text=f"{current_question} = ?")
    total += 1
    update_score_label()

    temps_restant = TEMPS_PAR_QUESTION
    update_timer()
    demarrer_chrono()
    status_label.config(text="Choisis la bonne réponse :")
    generer_boutons_reponses()

def generer_boutons_reponses():
    for widget in reponses_frame.winfo_children():
        widget.destroy()

    for i in range(1, (NOMBRE_MAX * 2) + 1):
        btn = tk.Button(reponses_frame, text=str(i), font=("Comic Sans MS", 16), width=4,
                        command=lambda val=i: traiter_reponse(val))
        btn.grid(row=(i - 1) // 5, column=(i - 1) % 5, padx=5, pady=5)

def fin_du_jeu():
    arret_chrono()
    question_label.config(text="🎉 Bravo ! 🎉")
    status_label.config(text="Fin du jeu ! Tu peux recommencer.")
    timer_label.config(text="")
    ajouter_historique(f"\n🎯 Score final : {score}/{total}")
    bouton_recommencer.pack(pady=10)
    for widget in reponses_frame.winfo_children():
        widget.destroy()

def traiter_reponse(reponse):
    global score
    arret_chrono()
    if reponse == current_answer:
        score += 1
        ajouter_historique(f"{current_question} = {reponse} ✅")
    else:
        ajouter_historique(f"{current_question} = {reponse} ❌ (attendu : {current_answer})")
    nouvelle_operation()

def update_score_label():
    score_label.config(text=f"Score : {score}/{total}")

def ajouter_historique(texte_brut):
    historique_text.config(state="normal")

    if "attendu" in texte_brut:
        # Exemple : 14 + 3 = 16 ❌ (attendu : 17)
        partie, attendu = texte_brut.split(" ❌ ")
        historique_text.insert(tk.END,
            f"{partie.ljust(18)} ❌ {attendu.strip()}\n")
    elif "✅" in texte_brut:
        partie = texte_brut.replace(" ✅", "")
        historique_text.insert(tk.END,
            f"{partie.ljust(22)} ✅\n")
    else:
        # en cas de message libre
        historique_text.insert(tk.END, texte_brut + "\n")

    historique_text.see(tk.END)
    historique_text.config(state="disabled")


def update_timer():
    timer_label.config(text=f"⏱ {temps_restant} sec")
    if temps_restant > 5:
        timer_label.config(fg="green", font=("Arial Rounded MT Bold", 28))
    elif temps_restant > 3:
        timer_label.config(fg="orange", font=("Arial Rounded MT Bold", 32))
    else:
        timer_label.config(fg="red", font=("Arial Rounded MT Bold", 36))

def compte_a_rebours():
    global temps_restant
    temps_restant -= 1
    update_timer()
    if temps_restant <= 0:
        status_label.config(text="⏱ Temps écoulé")
        traiter_reponse("Temps")
    else:
        global chrono
        chrono = fenetre.after(1000, compte_a_rebours)

def demarrer_chrono():
    global chrono
    arret_chrono()
    chrono = fenetre.after(1000, compte_a_rebours)

def arret_chrono():
    global chrono
    if chrono is not None:
        fenetre.after_cancel(chrono)
        chrono = None

def recommencer_jeu():
    global score, total
    score = 0
    total = 0
    historique_text.config(state="normal")
    historique_text.delete("1.0", tk.END)
    historique_text.config(state="disabled")
    bouton_recommencer.pack_forget()
    status_label.config(text="")
    nouvelle_operation()

# === Interface ===
fenetre = tk.Tk()
fenetre.title("🎉 Jeu de maths magique 🎲")
fenetre.geometry("700x700")
fenetre.configure(bg="#ffeef8")

main_frame = tk.Frame(fenetre, bg="#ffeef8")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_frame = tk.Frame(fenetre, bg="#fffaf0", width=350, height=300)
right_frame.pack(side=tk.RIGHT, anchor='n')
right_frame.pack_propagate(False)  # Désactive l’auto-ajustement à son contenu
 

question_label = tk.Label(main_frame, text="", font=("Comic Sans MS", 28), bg="#ffeef8", fg="#333")
question_label.pack(pady=10)

timer_label = tk.Label(main_frame, text="", font=("Arial Rounded MT Bold", 32), bg="#ffeef8")
timer_label.pack()

score_label = tk.Label(main_frame, text="Score : 0/0", font=("Comic Sans MS", 16), bg="#ffeef8")
score_label.pack(pady=10)

status_label = tk.Label(main_frame, text="", font=("Comic Sans MS", 14), fg="gray", bg="#ffeef8")
status_label.pack(pady=5)

reponses_frame = tk.Frame(main_frame, bg="#ffeef8")
reponses_frame.pack(pady=10)



# Conteneur avec marges internes
historique_container = tk.Frame(right_frame, bg="#ffeef8", padx=20, pady=20)
historique_container.pack(fill=tk.BOTH, expand=True)

# Titre de l'historique
historique_title = tk.Label(historique_container, text="📜 Historique", font=("Comic Sans MS", 14, "bold"), bg="#ffeef8")
historique_title.pack(pady=(10, 5))

# Zone de texte dans le conteneur
historique_text = tk.Text(historique_container,
                          width=30,
                          height=20,
                          state="disabled",
                          font=("Courier", 10),
                          bg="#ffeef0",
                          relief="flat",
                          bd=0)
historique_text.pack(fill=tk.BOTH, expand=True)



bouton_recommencer = tk.Button(main_frame, text="🔄 Recommencer", font=("Comic Sans MS", 14), bg="#ffd", command=recommencer_jeu)

# Lancement
nouvelle_operation()
fenetre.mainloop()
# Fin du code