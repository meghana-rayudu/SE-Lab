import math
import re
from statistics import mean


def parse_setpoint(text):
    if not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) < 2 or text[-1].upper() not in ('C', 'F'):
        return None
    try:
        value = float(text[:-1])
        if text[-1].upper() == 'F':
            value = (value - 32) * (5 / 9)
        return round(value, 1) if math.isfinite(value) else None
    except (ValueError, OverflowError):
        return None


def average_temperature(readings_csv):
    if not isinstance(readings_csv, str):
        return None
    try:
        values = [float(r) for r in readings_csv.split(',')]
        if not all(math.isfinite(v) for v in values):
            return None
        return mean(values)
    except (ValueError, OverflowError):
        return None


def schedule_slot(time_text):
    if not isinstance(time_text, str):
        return None
    match = re.fullmatch(r'([0-9]{2}):([0-9]{2})', time_text.strip())
    if not match:
        return None
    hour, minute = map(int, match.groups())
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return ('night ' if hour < 6 else 'day ') + (f'{minute:02d}' if hour < 6 else str(minute))

def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result if result is not None else "Invalid input")

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result if result is not None else "Invalid input")

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
