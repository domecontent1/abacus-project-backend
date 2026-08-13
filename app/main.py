import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def generate_abacus_logic(level, rows):
    nums = []
    total = 0

    for i in range(rows):
        if level == "DIRECT":
            # Numbers that don't require carries/formulas
            # Simplified for now: 1-digit numbers that keep total < 9
            val = random.randint(1, 4) if total < 5 else random.randint(-4, -1)
            if total + val < 0 or total + val > 9: val = 1
        else:
            # Random for now, can be expanded with specific "Friend" logic later
            val = random.randint(1, 9) if random.random() > 0.3 else random.randint(-9, -1)
            if total + val < 0: val = abs(val)

        total += val
        nums.append(val)
    return nums, total


@app.get("/api/practice")
async def get_practice(questions: int = 5, rows: int = 3, level: str = "DIRECT"):
    result = []
    for _ in range(questions):
        problem, answer = generate_abacus_logic(level, rows)
        result.append({"problem": problem, "answer": answer})
    return {"questions": result}