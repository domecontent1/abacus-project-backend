import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 1. Add this variable at the very top of main.py
# total_games = 120 # Start with a baseline so it doesn't look empty!

def generate_math(level: str, rows: int, digits: int):
    nums = []
    total = 0

    # 2 digits means 10 to 99
    low = 10 ** (digits - 1)
    high = (10 ** digits) - 1

    for _ in range(rows):
        found = False
        for _ in range(100):  # Try many times to find a valid number
            val = random.randint(low, high)
            if random.random() > 0.7: val = -val

            if total + val < 0: continue

            if level == "DIRECT":
                # Check for carry-over in every digit column
                # We check: can we add these two numbers without "friends" or "carries"?
                s_total = str(total).zfill(digits)
                s_val = str(abs(val)).zfill(digits)

                is_direct = True
                for t_char, v_char in zip(s_total, s_val):
                    t_digit = int(t_char)
                    v_digit = int(v_char)

                    if val > 0:  # Addition check
                        if t_digit + v_digit > 9: is_direct = False
                    else:  # Subtraction check
                        if t_digit - v_digit < 0: is_direct = False

                if is_direct:
                    total += val
                    nums.append(val)
                    found = True
                    break
            else:
                # Level 2 or 3: Just ensure it doesn't go below zero
                total += val
                nums.append(val)
                found = True
                break

        # If no 2-digit number fits the "Direct" rule,
        # fallback to a safe 1-digit number so the game doesn't break
        if not found:
            safe_val = random.randint(1, 4)
            if total - safe_val < 0:
                total += safe_val; nums.append(safe_val)
            else:
                total -= safe_val; nums.append(-safe_val)

    return nums, total


# Create a simple counter (In a real app, you'd use a Database or File)
# For now, this will count until the server restarts
stats = {
    "total_games_played": 100 # Starting with a base number looks better!
}

# 3. Add this new endpoint so the frontend can ask for the number
@app.get("/api/stats")
async def get_stats():
    return {"total_games_played": total_games}




@app.get("/api/practice")
async def get_practice(questions: int = 5, rows: int = 3, level: str = "DIRECT", digits: int = 1):
    # 2. Add this line inside the function to count every game
    global total_games
    total_games += 1

    result = []
    for _ in range(questions):
        problem, answer = generate_math(level, rows, digits)
        result.append({"problem": problem, "answer": answer})
    return {"questions": result}