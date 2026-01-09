class ActivitySuggester:
    
    def __init__(self):
        pass
    
    def suggest_activity(self, energy, time, location):
        return self._suggest_rule_based(energy, time, location)
    
    def _suggest_rule_based(self, energy, time, location):
        activities = {
            ("high", "+5min", "outside"): {
                "activity": "Go for a brisk walk or jog",
                "description": "Get your heart rate up and enjoy the fresh air"
            },
            ("high", "+5min", "inside"): {
                "activity": "Do a quick workout or dance",
                "description": "Move your body to release energy and stress"
            },
            ("high", "<5min", "outside"): {
                "activity": "Step outside and breathe deeply",
                "description": "Take 10 deep breaths while standing in the fresh air"
            },
            ("high", "<5min", "inside"): {
                "activity": "Quick desk stretches",
                "description": "Stand up and do 5-10 stretches to release tension"
            },
            ("low", "+5min", "outside"): {
                "activity": "Nature walk or sit in a park",
                "description": "Find a peaceful spot and observe nature around you"
            },
            ("low", "+5min", "inside"): {
                "activity": "Guided meditation or breathing exercise",
                "description": "Find a quiet space and do a 5-minute meditation"
            },
            ("low", "<5min", "outside"): {
                "activity": "Fresh air break",
                "description": "Step outside, close your eyes, and take 5 slow breaths"
            },
            ("low", "<5min", "inside"): {
                "activity": "Box breathing exercise",
                "description": "Breathe in for 4 counts, hold for 4, out for 4, hold for 4. Repeat 3 times."
            }
        }
        
        key = (energy, time, location)
        return activities.get(key, {
            "activity": "Take a moment to breathe",
            "description": "Pause, close your eyes, and take 3 deep breaths"
        })


def main():
    suggester = ActivitySuggester()
    
    test_cases = [
        ("high", "+5min", "outside"),
        ("low", "<5min", "inside"),
        ("high", "<5min", "inside"),
        ("low", "+5min", "outside"),
    ]
    
    print("Testing Activity Suggester:\n")
    for energy, time, location in test_cases:
        suggestion = suggester.suggest_activity(energy, time, location)
        print(f"Input: {energy} energy, {time}, {location}")
        print(f"Activity: {suggestion['activity']}")
        print(f"Description: {suggestion['description']}\n")


if __name__ == "__main__":
    main()
