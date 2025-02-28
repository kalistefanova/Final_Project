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
# - climate: hot, tropical, temperate, or cold
# - activity: relaxation, cultural, adventure, or nature
# - budget: low, medium, or high
# - popularity: popular or off-beaten
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
        Returns:
    - dict: User preferences.
    """
    preferences = {}
    weights = {}

    def ask_priority(question):
        """
        Asks the user to assign a priority level (low, medium, high) for each preference.
        Parameters:
        - question (str): The prompt for priority.
        Returns:
        - int: A numeric weight (1 for low, 2 for medium, 3 for high).
        """
        while True:
            print("\n" + question)
            print("Priority Levels: low, medium or high")
            priority = input("Your priority level: ").strip().lower()
            if priority in ["low", "medium", "high"]:
                return {"low": 1, "medium": 2, "high": 3}[priority]
            else:
                print("Invalid choice. Please select low, medium, or high.")

    # Question 1: Climate
    preferences['climate'] = ask_question(
        "What type of climate do you prefer?",
        ["hot","tropical", "temperate", "cold"]
    )
    preferences['climate_priority'] = ask_priority("How important is climate to you?")

    # Question 2: Activities
    preferences['activity'] = ask_question(
        "What type of activity do you prefer on your trip?",
        ["cultural", "urban", "adventure", "relaxation"]
    )
    preferences['activity_priority'] = ask_priority("How important is the activity to you?")
    # Question 3: Budget
    preferences['budget'] = ask_question(
        "What is your budget level?",
        ["low", "medium", "high"]
    )
    preferences['budget_priority'] = ask_priority("How important is budget to you?")
    # Question 4: Popularity preference
    preferences['popularity'] = ask_question(
        "Do you prefer popular destinations or under the radar locations?",
        ["popular", "under the radar"]
    )
    preferences['popularity_priority'] = ask_priority("How important is popularity to you?")
    #Question 5: Vibe preferences
    preferences['vibe'] = ask_question(
        "What is the vibe that you are looking for?",
        ["modern", "historic", "exotic", "cozy"]
    )
    preferences['vibe_priority'] = ask_priority("How important is the vibe to you?")
    # Question 6: Language Preferences
    preferences['language'] = ask_question(
        "If you need to communicate easily and prefer an English-friendly environment, choose English-Friendly. If you don’t mind managing without knowing the local language, choose Language Barrier Doesn’t Matter.",
        ["english-friendly", "language barrier doesn’t matter"]
    )
    preferences['language_priority'] = ask_priority("How important is the language to you?")

    # Question 7: Specific countries to avoid
    print("\nAre there any specific countries you want to avoid?")
    print("Enter the country names separated by commas, or type 'none':")
    avoid_countries = input("Your answer: ").strip().lower()
    if avoid_countries == "none":
        preferences['avoid_countries'] = []
    else:
        preferences['avoid_countries'] = [country.strip() for country in avoid_countries.split(",")]

    # Question 8: Specific continents to avoid
    print("\nAre there any specific continents you want to avoid?")
    print("Options: Asia, Europe, North America, Oceania, Africa, Central America, South America")
    print("Enter the continent names separated by commas, or type 'none':")
    avoid_continents = input("Your answer: ").strip().lower()
    if avoid_continents == "none":
        preferences['avoid_continents'] = []
    else:
        preferences['avoid_continents'] = [continent.strip() for continent in avoid_continents.split(",")]

    return preferences

def score_destination(destination_attributes, user_preferences):
    """
    Computes a score for a destination based on how its attributes match the user's preferences.

    Each matching attribute adds a weighted point.

    Parameters:
    - destination_attributes (dict): A dictionary of attributes for a destination.
    - user_preferences (dict): A dictionary of the user's preferences (including priorities).

    Returns:
    - int: The computed score.
    """
    score = 0
    weight_factors = ["climate", "activity", "popularity", "vibe", "language"]

    # Score based on matching factors (excluding budget)
    for factor in weight_factors:
        user_pref = user_preferences.get(factor)
        user_priority = user_preferences.get(f"{factor}_priority", 1)

        if not isinstance(user_priority, int):
            user_priority = 1

        if factor in destination_attributes:
            destination_value = destination_attributes[factor]

            # If the attribute is a list (e.g., multiple activities), check if user's choice is in the list
            if isinstance(destination_value, list):
                if user_pref in destination_value:
                    score += user_priority  # Assign priority weight if at least one match is found
            elif destination_value == user_pref:
                score += user_priority  # Add priority weight for direct matches

    # Handle budget separately to allow hierarchical inclusion
    user_budget = user_preferences.get("budget")
    budget_priority = user_preferences.get("budget_priority", 1)
    destination_budget = destination_attributes.get("budget")

    budget_hierarchy = {"low": 1, "medium": 2, "high": 3}

    # Check if both user and destination budgets exist in the hierarchy
    if user_budget in budget_hierarchy and destination_budget in budget_hierarchy:
        if budget_hierarchy[destination_budget] <= budget_hierarchy[user_budget]:
            score += budget_priority  # Assign budget priority score
    # EXCEPTION TO --> Handle language separately:
    language_priority = user_preferences.get("language_priority", 1)
    user_language_pref = user_preferences.get("language")
    # This works if user indicates "language barrier doesn’t matter", add full weight regardless
    if user_language_pref == "language barrier doesn’t matter":
        score += language_priority
    else:
        if destination_attributes.get("language", "") == user_language_pref:
            score += language_priority
    return score

def recommend_destination(user_preferences):
    """
    Evaluates all destinations and recommends the one with the highest score.

    Parameters:
    - user_preferences (dict): A dictionary of the user's travel preferences.

    Returns:
    - A tuple containing the recommended destination (or destinations if tied) and its score.
    """
    best_score = -1
    top_destinations = []
    recommendation = None
    scores = {}

    # Iterate over each destination
    for destination, attributes in destinations.items():
        # Skip if the destination is in the avoid list
        if (attributes['country'].lower() in user_preferences['avoid_countries'] or
            attributes['continent'].lower() in user_preferences['avoid_continents']):
            continue

        # Compute the score for the destination
        current_score = score_destination(attributes, user_preferences)
        scores[destination] = current_score
        if current_score > best_score:
            best_score = current_score
            top_destinations = [destination]  # Reset list with new best score destination
        elif current_score == best_score:
            top_destinations.append(destination)  # Add to the list if it ties
    # For detailed debugging, you might print all scores:
    print("\n--- Destination Scores ---")
    for dest, sc in scores.items():
        print(f"{dest}: {sc}")

    return top_destinations, best_score


def display_recommendation(recommendation, score, user_preferences):
    """
    Displays the recommended destination and a summary of the user's preferences.

    Parameters:
    - recommendation (list of str): The recommended destination(s).
    - score (int): The score of the recommended destination(s).
    - user_preferences (dict): The user's travel preferences.
    """
    print("\n=== Your Travel Recommendations ===")
    if recommendation:
        print("Based on your preferences:")
        for key, value in user_preferences.items():
            if "_priority" not in key and key not in ["avoid_countries", "avoid_continents"]:
                print(f"  {key.capitalize()}: {value}")

        print(f"\n🏆 The best destinations for you (Score: {score}):")
        for dest in recommendation:
            print(f"   - {dest}")
    else:
        print("Sorry, we couldn't find a destination that matches your preferences.")

def display_intro():
    """
    Displays the introduction and instructions for the travel destination chooser.
    """
    print("-" * 50)
    print(" Welcome to the Travel Destination Chooser!")
    print("-" * 50)
    print("Answer a few questions about your travel preferences, and we'll recommend")
    print("a destination that matches what you're looking for.")
    print("Let's get started!")
    print("-" * 50)

def main():
    """
    Main function that drives the travel destination chooser program.
    """
    display_intro()
    preferences = get_user_preferences()
    destination, score = recommend_destination(preferences)
    display_recommendation(destination, score, preferences)

    # THIS PART ASKS THE USER IF THEY WANT TO PLAY AGAIN!!
    while True:
        retry = input("\nWould you like to try again? (yes/no): ").strip().lower()
        if retry == "yes":
            print("\nRestarting the Travel Destination Chooser...")
            preferences = get_user_preferences()
            destination, score = recommend_destination(preferences)
            display_recommendation(destination, score, preferences)
        elif retry == "no":
            print("\nThank you for using the Travel Destination Chooser. Have a great trip!")
            break
        else:
            print("Please answer 'yes' or 'no'.")

if __name__ == "__main__":
    main()