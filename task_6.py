# Дані
items = {
    "pizza":      {"cost": 50, "calories": 300},
    "hamburger":  {"cost": 40, "calories": 250},
    "hot-dog":    {"cost": 30, "calories": 200},
    "pepsi":      {"cost": 10, "calories": 100},
    "cola":       {"cost": 15, "calories": 220},
    "potato":     {"cost": 25, "calories": 350},
}

# 1) ЖАДІБНИЙ АЛГОРИТМ (ratio = calories / cost)

def greedy_algorithm(items: dict, budget: int):
    # Сортуємо за ratio; у разі рівності — за калоріями (більше краще), потім за меншою ціною
    sorted_items = sorted(
        items.items(),
        key=lambda kv: (kv[1]["calories"] / kv[1]["cost"], kv[1]["calories"], -kv[1]["cost"]),
        reverse=True,
    )

    chosen, total_cal, total_cost = [], 0, 0
    for name, info in sorted_items:
        c, cal = info["cost"], info["calories"]
        if total_cost + c <= budget:
            chosen.append(name)
            total_cost += c
            total_cal += cal

    return chosen, total_cal, total_cost


# 2) ДИНАМІЧНЕ ПРОГРАМУВАННЯ 

def dynamic_programming(items: dict, budget: int):
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals  = [items[n]["calories"] for n in names]
    n = len(names)

    # dp розміром (n+1) x (budget+1)
    dp = [[0]*(budget+1) for _ in range(n+1)]

    for i in range(1, n+1):
        cost_i, cal_i = costs[i-1], cals[i-1]
        for b in range(budget+1):
            # варіант без предмета i
            dp[i][b] = dp[i-1][b]
            # варіант з предметом i (якщо поміщається)
            if cost_i <= b:
                dp[i][b] = max(dp[i][b], dp[i-1][b-cost_i] + cal_i)

    # Відновлення вибору (backtracking)
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i-1][b]:  # предмет i було взято
            chosen.append(names[i-1])
            b -= costs[i-1]

    chosen.reverse()  # щоб зберегти природний порядок
    total_cal = dp[n][budget]
    total_cost = sum(items[name]["cost"] for name in chosen)
    return chosen, total_cal, total_cost


# Демонстрація

if __name__ == "__main__":
    BUDGET = 100

    g_items, g_cal, g_cost = greedy_algorithm(items, BUDGET)
    print("Жадібний:", g_items, "| калорії =", g_cal, "| вартість =", g_cost)

    d_items, d_cal, d_cost = dynamic_programming(items, BUDGET)
    print("DP      :", d_items, "| калорії =", d_cal, "| вартість =", d_cost)
