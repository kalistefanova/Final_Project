"""
Your Travel Destination Helper
----------------------------
This program asks you a series of questions about your travel preferences and
uses your responses to recommend a travel destination.

Key features:
- Asks questions on climate, preferred activity, budget, and popularity
- Allows users to specify countries/continents to avoid.
- Scores a set of predefined travel destinations based on your answers.
- Provides a recommendation based on the highest total score.
"""
from countries import destinations

# Dictionary of destinations with their attributes.
# Each destination has:
# - climate: tropical, temperate, or cold
# - activity: relaxation, cultural, adventure, or nature
# - budget: low, medium, or high
# - popularity: popular or under the radar
# - country: the country of the destination
# - continent: the continent of the destination

def ask_question(question, options):
    """
    This function asks the user a question and returns their validated response.
    parameters:
    - question: The question to display.
    - options: a list of acceptable responses (lowercase).
    returns: their validated response in lowercase.
    """
    # Show question and options
    while True:
        print("\n" + question)
        print("Options:", ", ".join(options))
        answer = input("Your answer: ").strip().lower()
        if answer in options:
            return answer
        else:
            print("Invalid answer. Please choose one of the options provided.")


def get_user_preferences():
    """
    This function asks the user a series of questions about their travel preferences.
    returns: a dictionary with the user's preferences.
    """
    preferences = {}

    # Question 1: Climate
    preferences['climate'] = ask_question(
        "What type of climate do you prefer?",
        ["tropical", "temperate", "cold"]
    )

    # Question 2: Activities
    preferences['activity'] = ask_question(
        "What type of activity do you prefer on your trip?",
        ["relaxation", "cultural", "adventure", "nature"]
    )

    # Question 3: Budget
    preferences['budget'] = ask_question(
        "What is your budget level?",
        ["low", "medium", "high"]
    )

    # Question 4: Popularity preference
    preferences['popularity'] = ask_question(
        "Do you prefer popular destinations or under the radar locations?",
        ["popular", "under the radar"]
    )

    # Question 5: Specific countries to avoid
    print("\nAre there any specific countries you want to avoid?")
    print("Enter the country names separated by commas, or type 'none':")
    avoid_countries = input("Your answer: ").strip().lower()
    if avoid_countries == "none":
        preferences['avoid_countries'] = []
    else:
        preferences['avoid_countries'] = [country.strip() for country in avoid_countries.split(",")]

    # Question 7: Specific continents to avoid
    print("\nAre there any specific continents you want to avoid?")
    print("Options: Asia, Europe, North America, Oceania, Africa, Central America, South America")
    print("Enter the continent names separated by commas, or type 'none':")
    avoid_continents = input("Your answer: ").strip().lower()
    if avoid_continents == "none":
        preferences['avoid_continents'] = []
    else:
        preferences['avoid_continents'] = [continent.strip() for continent in avoid_continents.split(",")]

    return preferences
