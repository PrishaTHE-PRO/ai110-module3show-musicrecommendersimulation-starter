# Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

Suggest songs that match what a user is in the mood for right now. The user tells the system their preferred genre, mood, energy level, and whether they like acoustic music. The system finds the best matches from a 20-song catalog and explains why each one was picked.

---

## 3. Data Used

- 20 songs in a CSV file
- Each song has: genre, mood, energy (0–1), tempo, valence, danceability, and acousticness
- 17 different genres, 14 different moods
- The original 10 songs came with the project starter. 10 more were added for variety.
- All artist names and song titles are made up
- Mood and genre labels were applied by one person, so they reflect one set of opinions about what "chill" or "intense" means

---

## 4. Algorithm Summary

Every song gets a score out of 5 points. Higher score = better match.

- **+2 points** if the genre matches exactly
- **+1 point** if the mood matches exactly
- **Up to +1.5 points** based on how close the song's energy is to what the user wants — closer = more points
- **Up to +0.5 points** based on acoustic texture — closer = more points

The songs are sorted by score, and the top 5 are returned with a plain-English explanation for each one.

The key idea: for energy and acousticness, a song isn't rewarded for being loud or quiet — only for being *close to what was asked for*.

---

## 5. Observed Behavior / Biases

**Genre dominates.** A genre match is worth 2 points — more than energy and acousticness combined. This means a mediocre song in the right genre usually beats a great song in the wrong genre. That doesn't always feel right.

**Mood labels have no nuance.** "Chill" and "focused" can sound nearly identical, but a mismatch costs the full 1 point with nothing in between. The system can't tell the difference between a close miss and a total mismatch.

**The system lives in a filter bubble.** The same preferences always return the same songs. There's no way for it to surprise you or show you something you didn't know you'd like.

**The "average" profile exposed a hidden bias.** Setting all preferences to 0.5 (the midpoint) was supposed to be neutral. It wasn't — it consistently surfaced low-energy ambient tracks because those happen to cluster near the middle of the dataset. There's no such thing as a truly neutral default.

---

## 6. Evaluation Process

Six user profiles were tested:

| Profile | What it tested |
|---|---|
| High-Energy Pop | Normal, clear preferences — expected to work well |
| Chill Lofi | Another normal profile — expected to work well |
| Deep Intense Rock | Clear preferences in a specific genre |
| Conflicting: High Energy + Sad | Can high energy overcome a mood match? |
| No Genre or Mood Match | What happens when nothing matches? |
| Perfectly Average | What does "neutral" actually produce? |

The standard profiles worked as expected. The adversarial ones were more revealing. "No Genre or Mood Match" showed the system barely differentiates when it has no categorical signal — the top 5 scores were all within 0.2 points of each other.

A weight experiment was also run: genre was cut in half (2.0 → 1.0) and energy was doubled (1.5 → 3.0). The rankings shifted noticeably. Songs in closely related genres (like "indie pop" when searching "pop") moved up significantly, which actually felt more musically accurate.

---

## 7. Intended Use and Non-Intended Use

**This system is for:**
- Learning how content-based recommendation logic works
- Classroom exploration and experimentation
- Understanding how weights and features shape results

**This system is NOT for:**
- Real music recommendations for real users
- Any situation where fairness across genres or cultures matters
- Users who can't describe their preferences in four specific terms
- Replacing systems that learn from actual listening behavior

---

## 8. Ideas for Improvement

1. **Add tempo as a scored feature.** The dataset spans 60–168 BPM and the system ignores it entirely. Tempo is something you feel immediately — it should matter.

2. **Make genre matching less binary.** "Indie pop" and "pop" are closer than "pop" and "metal," but the system treats all mismatches the same. A genre similarity table would make this smarter.

3. **Add a diversity rule.** The top 3 results for "Chill Lofi" are always 3 lofi songs. Capping results at one song per artist or genre would push more variety into the list.

---

## 9. Personal Reflection

**Biggest learning moment:**
Seeing the "Perfectly Average" profile output. I assumed setting all preferences to 0.5 would be neutral — like asking for nothing specific. But it surfaced a very specific corner of the catalog (low-energy ambient). That made it click that every default is a choice, and every choice favors someone.

**How AI tools helped, and when I had to double-check:**
AI was useful for generating the initial dataset and boilerplate structure quickly. But it couldn't tell me whether the *weights* were right — that required actually running profiles and asking "does this feel correct?" The math was easy to generate. Deciding what the math *should* say took more judgment.

**What surprised me about simple algorithms:**
The output genuinely *feels* like a recommendation. When Storm Runner came back as #1 for "Deep Intense Rock" with a 4.98 score, it felt satisfying — even though the whole system is just four arithmetic operations. That gap between "it's just addition" and "it feels intelligent" is smaller than I expected.

**What I'd try next:**
I'd add collaborative filtering — even a simple version where the system notices "users who liked Library Rain also added Focus Flow to playlists." That would let the system recommend things users didn't know to ask for, which is what makes Spotify's Discover Weekly feel genuinely useful rather than just accurate.
