import turtle
import math

def draw_pythagoras_tree(t, branch_length, level, angle=30):
    """Рекурсивно малює дерево Піфагора (Y-подібне симетричне дерево)."""
    if level == 0:
        return

    # Малюємо основну гілку
    t.forward(branch_length)

    # Ліва гілка
    t.left(angle)
    draw_pythagoras_tree(t, branch_length * 0.7, level - 1, angle)

    # Права гілка
    t.right(2 * angle)
    draw_pythagoras_tree(t, branch_length * 0.7, level - 1, angle)

    # Повертаємося до початкового положення
    t.left(angle)
    t.backward(branch_length)


def main():
    level = int(input("Введіть рівень рекурсії (наприклад, 9): "))

    screen = turtle.Screen()
    screen.title("Фрактал: дерево Піфагора (симетричне)")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.color("brown")
    t.speed(0)
    t.left(90)

    # Початкова позиція
    t.penup()
    t.goto(0, -250)
    t.pendown()

    # Малюємо фрактал
    draw_pythagoras_tree(t, 100, level)

    t.hideturtle()
    turtle.done()


if __name__ == "__main__":
    main()
