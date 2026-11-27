"""
Demo script showing expected learning path output format.
Run: python demo_output.py
"""

from prompt import user_goal_prompt


def generate_sample_learning_path(goal: str) -> str:
    """Return a sample learning path matching the agent's expected output format."""
    return f"""User Goal: {goal}

## Sample Learning Path Output (Demo)

Here is your learning path document link: https://docs.google.com/document/d/sample-doc-id/edit
Here is your YouTube playlist link: https://www.youtube.com/playlist?list=sample-playlist-id (with relevant content)

---

# Python Programming Basics — 5-Day Learning Path

## Day 1:
**Topic:** Introduction to Python & Setup
**YouTube Link:** https://www.youtube.com/watch?v=sample-day1

## Day 2:
**Topic:** Variables, Data Types & Control Flow
**YouTube Link:** https://www.youtube.com/watch?v=sample-day2

## Day 3:
**Topic:** Functions & Modules
**YouTube Link:** https://www.youtube.com/watch?v=sample-day3

## Day 4:
**Topic:** Data Structures (Lists, Dicts, Sets)
**YouTube Link:** https://www.youtube.com/watch?v=sample-day4

## Day 5:
**Topic:** Algorithms & Problem Solving
**YouTube Link:** https://www.youtube.com/watch?v=sample-day5

---

### Top Channels or Institutes to Follow
- Corey Schafer
- freeCodeCamp
- Programming with Mosh
"""


if __name__ == "__main__":
    goal = "I want to learn Python programming basics in 5 days, focusing on data structures and algorithms."
    print("=" * 60)
    print("MCP Learning Path Generator — Demo Output")
    print("=" * 60)
    print()
    print(generate_sample_learning_path(goal))
    print()
    print("=" * 60)
    print("Agent prompt template loaded:", len(user_goal_prompt), "chars")
    print("=" * 60)
