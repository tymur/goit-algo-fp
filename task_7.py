import random
import matplotlib.pyplot as plt
import pandas as pd

# 1. ПАРАМЕТРИ СИМУЛЯЦІЇ

N = 1_000_000  # кількість кидків кубиків (чим більше, тим точніше)


# 2. АНАЛІТИЧНІ ЙМОВІРНОСТІ

analytical_probs = {
    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
    8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
}

# 3. СИМУЛЯЦІЯ МЕТОДОМ МОНТЕ-КАРЛО

results = {s: 0 for s in range(2, 13)}

for _ in range(N):
    dice_sum = random.randint(1, 6) + random.randint(1, 6)
    results[dice_sum] += 1


# 4. РОЗРАХУНОК ЙМОВІРНОСТЕЙ

monte_probs = {s: count / N for s, count in results.items()}


# 5. ПОРІВНЯЛЬНА ТАБЛИЦЯ

data = []
for s in range(2, 13):
    data.append({
        "Сума": s,
        "Аналітична імовірність (%)": analytical_probs[s] * 100,
        "Монте-Карло імовірність (%)": monte_probs[s] * 100,
        "Різниця (%)": abs(monte_probs[s] - analytical_probs[s]) * 100
    })

df = pd.DataFrame(data)
print(df.round(3))

# 6. ВІЗУАЛІЗАЦІЯ

plt.figure(figsize=(10, 5))
plt.bar(df["Сума"] - 0.2, df["Аналітична імовірність (%)"], width=0.4, label="Аналітична", color="#89CFF0")
plt.bar(df["Сума"] + 0.2, df["Монте-Карло імовірність (%)"], width=0.4, label="Монте-Карло", color="#4169E1")
plt.xlabel("Сума на двох кубиках")
plt.ylabel("Ймовірність (%)")
plt.title(f"Порівняння аналітичних і симуляційних результатів ({N:,} кидків)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
