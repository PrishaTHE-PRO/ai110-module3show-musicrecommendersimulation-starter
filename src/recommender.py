from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initializes the recommender with a catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for a given UserProfile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of song dicts with correctly typed fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Returns a (score, reasons) tuple rating how well a song matches user preferences."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 (binary)
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0 (binary)
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity: up to +1.5 — closer to target = more points
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = 1.5 * (1 - abs(song["energy"] - target_energy))
    score += energy_pts
    reasons.append(f"energy fit (+{energy_pts:.2f})")

    # Acousticness proximity: up to +0.5 — closer to target = more points
    acoustic_target = 0.9 if user_prefs.get("likes_acoustic", False) else user_prefs.get("acousticness", 0.5)
    acoustic_pts = 0.5 * (1 - abs(song["acousticness"] - acoustic_target))
    score += acoustic_pts
    reasons.append(f"acoustic fit (+{acoustic_pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song in the catalog and returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
