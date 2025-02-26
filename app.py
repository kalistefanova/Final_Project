from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from __init__ import *

from countries import destinations

def ask_question(question, options, frame):
    label = ttk.Label(frame, text=question, style="TLabel")
    label.pack(pady=10)

    response = StringVar()
    dropdown = ttk.Combobox(frame, textvariable=response, values=options, state="readonly", style="TCombobox")
    dropdown.pack(pady=5)
    dropdown.current(0)

    return response

def ask_priority(question, frame):
    label = ttk.Label(frame, text=question, style="TLabel")
    label.pack(pady=10)

    priority = StringVar()
    dropdown = ttk.Combobox(frame, textvariable=priority, values=["low", "medium", "high"], state="readonly", style="TCombobox")
    dropdown.pack(pady=5)
    dropdown.current(0)

    return priority

def get_user_preferences():
    preferences = {}

    pref_window = Toplevel(root)
    pref_window.title("Travel Preferences")
    pref_window.geometry("500x400")
    pref_window.configure(bg="#2196F3")

    canvas = Canvas(pref_window, bg="#2196F3")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = ttk.Scrollbar(pref_window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = ttk.Frame(canvas, padding="20", style="TFrame")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    style.configure("TFrame", background="#2196F3")
    style.configure("TLabel", background="#2196F3", font=("Helvetica", 10))
    style.configure("TCombobox", font=("Helvetica", 10))
    style.configure("TEntry", font=("Helvetica", 10))

    # Question 1: Climate
    preferences['climate'] = ask_question("What type of climate do you prefer?", ["hot", "tropical", "temperate", "cold"], frame)
    preferences['climate_priority'] = ask_priority("How important is climate to you?", frame)

    # Question 2: Activity
    preferences['activity'] = ask_question("What type of activity do you prefer on your trip?", ["cultural", "urban", "adventure", "relaxation"], frame)
    preferences['activity_priority'] = ask_priority("How important is the activity to you?", frame)

    # Question 3: Budget
    preferences['budget'] = ask_question("What is your budget level?", ["low", "medium", "high"], frame)
    preferences['budget_priority'] = ask_priority("How important is budget to you?", frame)

    # Question 4: Popularity
    preferences['popularity'] = ask_question("Do you prefer popular destinations or under the radar locations?", ["popular", "under the radar"], frame)
    preferences['popularity_priority'] = ask_priority("How important is popularity to you?", frame)

    # Question 5: Vibe
    preferences['vibe'] = ask_question("What is the vibe that you are looking for?", ["modern", "historic", "exotic", "cozy"], frame)
    preferences['vibe_priority'] = ask_priority("How important is the vibe to you?", frame)

    # Question 6: Language
    preferences['language'] = ask_question("If you need to communicate easily and prefer an English-friendly environment, choose English-Friendly. If you don’t mind managing without knowing the local language, choose Language Barrier Doesn’t Matter.", ["english-friendly", "language barrier doesn’t matter"], frame)
    preferences['language_priority'] = ask_priority("How important is the language to you?", frame)

    # Question 7: Countries to avoid
    label = ttk.Label(frame, text="Are there any specific countries you want to avoid?", style="TLabel")
    label.pack(pady=10)

    avoid_countries = StringVar()
    entry = ttk.Entry(frame, textvariable=avoid_countries, width=30, style="TEntry")
    entry.pack(pady=5)
    preferences['avoid_countries'] = avoid_countries

    # Question 8: Continents to avoid
    label = ttk.Label(frame, text="Are there any specific continents you want to avoid?", style="TLabel")
    label.pack(pady=10)

    avoid_continents = StringVar()
    entry = ttk.Entry(frame, textvariable=avoid_continents, width=30, style="TEntry")
    entry.pack(pady=5)
    preferences['avoid_continents'] = avoid_continents

    def submit_preferences():
        pref_window.destroy()

    submit_button = Button(frame, text="Submit", command=submit_preferences, **button_style)
    submit_button.pack(pady=20)

    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    pref_window.wait_window()

    preferences['avoid_countries'] = (
        [] if preferences['avoid_countries'].get().strip().lower() == "none"
        else [country.strip().lower() for country in preferences['avoid_countries'].get().split(",")]
    )
    preferences['avoid_continents'] = (
        [] if preferences['avoid_continents'].get().strip().lower() == "none"
        else [continent.strip().lower() for continent in preferences['avoid_continents'].get().split(",")]
    )

    for key in preferences:
        if isinstance(preferences[key], StringVar):
            preferences[key] = preferences[key].get()

    for key in preferences:
        if "_priority" in key:
            preferences[key] = {"low": 1, "medium": 2, "high": 3}[preferences[key]]

    return preferences

def score_destination(destination_attributes, user_preferences):
    score = 0
    weight_factors = ["climate", "activity", "budget", "popularity", "vibe", "language"]

    for factor in weight_factors:
        user_pref = user_preferences.get(factor)
        user_priority = user_preferences.get(f"{factor}_priority", 1)

        if factor in destination_attributes and destination_attributes[factor] == user_pref:
            score += user_priority  # Multiply by weight

    return score

def recommend_destination(user_preferences):
    best_score = -1
    top_destinations = []
    scores = {}

    for destination, attributes in destinations.items():
        if (attributes['country'].lower() in user_preferences['avoid_countries'] or
            attributes['continent'].lower() in user_preferences['avoid_continents']):
            continue

        current_score = score_destination(attributes, user_preferences)
        scores[destination] = current_score
        if current_score > best_score:
            best_score = current_score
            top_destinations = [destination]  # Reset list with new best score destination
        elif current_score == best_score:
            top_destinations.append(destination)  # Add to the list if it ties

    return top_destinations, best_score

def display_recommendation(recommendation, score, user_preferences):
    if recommendation:
        message = (
            "Based on your preferences:\n"
            f"Climate: {user_preferences['climate']}\n"
            f"Activity: {user_preferences['activity']}\n"
            f"Budget: {user_preferences['budget']}\n"
            f"Popularity: {user_preferences['popularity']}\n"
            f"Vibe: {user_preferences['vibe']}\n"
            f"Language: {user_preferences['language']}\n\n"
            f"🏆 The best destinations for you (Score: {score}):\n"
        )
        for dest in recommendation:
            message += f"   - {dest}\n"
    else:
        message = "Sorry, we couldn't find a destination that matches your preferences."

    messagebox.showinfo("Travel Recommendation", message)

def main():
    preferences = get_user_preferences()
    destination, score = recommend_destination(preferences)
    display_recommendation(destination, score, preferences)

root = Tk()
root.title("Travel Destination Helper")
root.geometry("400x300")
root.configure(bg="#e0f7fa")  # Light blue background

style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
style.configure("TCombobox", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))

button_style = {
    "bg": "#1976D2",
    "fg": "black",
    "font": ("Helvetica", 12, "bold"),
    "bd": 0,
    "relief": "flat",
    "activebackground": "#1565C0",
    "activeforeground": "white",
    "padx": 30,
    "pady": 15,
    "highlightthickness": 0,
    "borderwidth": 0,
    "highlightbackground": "#1976D2",
    "highlightcolor": "#1976D2",
}

label = ttk.Label(root, text="Welcome to the Travel Destination Helper!", style="TLabel")
label.pack(pady=20)

start_button = Button(root, text="Start", command=main, **button_style)
start_button.pack(pady=10)

exit_button = Button(root, text="Exit", command=root.quit, **button_style)
exit_button.pack(pady=10)

root.mainloop()