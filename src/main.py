"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# --- User Profiles ---

PROFILES = {
    # Standard profiles
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.85, "acousticness": 0.1
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.38, "acousticness": 0.8
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.92, "acousticness": 0.1
    },

    # Adversarial / edge case profiles
    "Conflicting: High Energy + Sad": {
        # Tests whether numeric energy score can override a mood mismatch
        "genre": "shoegaze", "mood": "sad", "energy": 0.95, "acousticness": 0.1
    },
    "No Genre or Mood Match": {
        # No song in the catalog has genre "country" or mood "bittersweet"
        # Forces the recommender to rank purely on numeric proximity
        "genre": "country", "mood": "bittersweet", "energy": 0.5, "acousticness": 0.5
    },
    "Perfectly Average": {
        # All values at the midpoint — should produce a flat, undifferentiated ranking
        "genre": "ambient", "mood": "chill", "energy": 0.5, "acousticness": 0.5
    },
}


def print_recommendations(label: str, recommendations: list) -> None:
    """Prints a formatted block of top-k results for one profile."""
    print("\n" + "=" * 52)
    print(f"  Profile: {label}")
    print("=" * 52)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "█" * int(score * 2)
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f} / 5.0  {bar}")
        print(f"       Genre : {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
