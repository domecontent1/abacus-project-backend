import random
from typing import List, Dict


class MathEngine:
    @staticmethod
    def generate_questions(count: int, digits: int, rows: int) -> List[Dict]:
        questions = []
        for _ in range(count):
            nums = []
            # Generate first number based on digits (e.g., 2 digits = 10 to 99)
            low = 10 ** (digits - 1)
            high = (10 ** digits) - 1

            current_total = random.randint(low, high)
            nums.append(current_total)

            for _ in range(rows - 1):
                # 70% chance of addition, 30% subtraction to keep it positive
                op = "+" if random.random() > 0.3 else "-"
                val = random.randint(low, high)

                if op == "+":
                    current_total += val
                    nums.append(val)
                else:
                    # Safety check for abacus: no negative results
                    if current_total - val >= 0:
                        current_total -= val
                        nums.append(-val)
                    else:
                        current_total += val
                        nums.append(val)

            questions.append({
                "problem": nums,  # Example: [10, -5, 20]
                "answer": current_total
            })
        return questions