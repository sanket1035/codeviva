"""Student marks: average, grade and topper."""


def average(marks):
    """Return the mean of a list of marks."""
    total = 0
    for m in marks:
        total += m
    return total / len(marks)


def grade(avg):
    """Convert an average to a letter grade."""
    if avg >= 75:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 40:
        return "C"
    return "F"


def topper(students):
    """Return the name of the student with the best average."""
    best_name, best_avg = None, -1
    for name, marks in students.items():
        avg = average(marks)
        if avg > best_avg:
            best_name, best_avg = name, avg
    return best_name


def report(students):
    for name, marks in students.items():
        avg = average(marks)
        print(name, round(avg, 1), grade(avg))
    print("Topper:", topper(students))


data = {"Asha": [80, 72, 91], "Ravi": [55, 48, 62], "Meera": [38, 41, 35]}
report(data)
