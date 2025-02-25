class Destination:
    """
    A class to represent a travel destination.
    """

    def __init__(self, name, climate, activity, budget, popularity, region, duration, cuisine):
        self.name = name.strip()
        self.climate = climate.strip().lower()
        self.activity = activity.strip().lower()
        self.budget = budget.strip().lower()
        self.popularity = popularity.strip().lower()
        self.region = region.strip().lower()
        self.duration = duration.strip().lower()  # short, medium, or long travel duration
        self.cuisine = cuisine.strip().lower()  # local or international cuisine

    def __str__(self):
        return f"{self.name} ({self.climate}, {self.activity}, {self.budget}, {self.popularity}, {self.region}, {self.duration}, {self.cuisine})"

    def get_attributes(self):
        """
        Return a dictionary of the destination's attributes.
        """
        return {
            "climate": self.climate,
            "activity": self.activity,
            "budget": self.budget,
            "popularity": self.popularity,
            "region": self.region,
            "duration": self.duration,
            "cuisine": self.cuisine
        }


# ========================================
# Section 2: Functions for File Management
# ========================================
def load_destinations(filename):
    """
    Loads destination data from a CSV file and returns a list of Destination objects.
    Expected CSV format:
      name,climate,activity,budget,popularity,region,duration,cuisine
    """
    destination_list = []
    try:
        with open(filename, "r") as file:
            # reading the header
            header = file.readline()
            # reading each subsequent line
            for line in file:
                # this is for skiping blank lines
                if line.strip() == "":
                    continue
                parts = line.strip().split(",")
                if len(parts) != 8:
                    print("Skipping invalid line:", line)
                    continue
                dest = Destination(*parts)
                destination_list.append(dest)
    except FileNotFoundError:
        print(f"Error: {filename} not found. No destinations loaded.")
    return destination_list


def save_destinations(filename, destinations):
    """
    Saves the current list of destinations back to the CSV file.
    This function overwrites the file.
    """
    with open(filename, "w") as file:
        # header
        file.write("name,climate,activity,budget,popularity,region,duration,cuisine\n")
        for dest in destinations:
            attributes = dest.get_attributes()
            line = f"{dest.name},{attributes['climate']},{attributes['activity']},{attributes['budget']},{attributes['popularity']},{attributes['region']},{attributes['duration']},{attributes['cuisine']}\n"
            file.write(line)
