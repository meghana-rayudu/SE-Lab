import math
import os
from hypothesis import given, example, strategies as st

# Set THERMOSTAT_ORIGINAL=1 to reproduce failures on the original code.
if os.getenv('THERMOSTAT_ORIGINAL') == '1':
    from original_thermostat_control import parse_setpoint, average_temperature, schedule_slot
else:
    from thermostat_control import parse_setpoint, average_temperature, schedule_slot

inputs = st.text() | st.none() | st.integers() | st.lists(st.integers(), max_size=5)

@given(inputs)
@example('')
@example('NaNC')
@example('21X')
def test_parse_setpoint_no_crash(s):
    result = parse_setpoint(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))
    if s in ('', 'NaNC', '21X'):
        assert result is None

@given(inputs)
@example('')
@example('1,,2')
@example('inf,2')
def test_average_temperature_no_crash(s):
    result = average_temperature(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))
    if s in ('', '1,,2', 'inf,2'):
        assert result is None

@given(inputs)
@example('')
@example('25:70')
@example('02:xx')
def test_schedule_slot_no_crash(s):
    result = schedule_slot(s)
    assert result is None or result.startswith(('night ', 'day '))
    if s in ('', '25:70', '02:xx'):
        assert result is None

@given(st.integers(-1000, 1000), st.sampled_from(['C', 'F', 'c', 'f']))
def test_valid_setpoint(value, unit):
    expected = value if unit.upper() == 'C' else (value - 32) * 5 / 9
    assert math.isclose(parse_setpoint(f'{value}{unit}'), round(expected, 1))

@given(st.lists(st.integers(-1000, 1000), min_size=1, max_size=30))
def test_valid_average(values):
    assert math.isclose(average_temperature(','.join(map(str, values))), sum(values)/len(values))

@given(st.integers(0, 23), st.integers(0, 59))
def test_valid_schedule(hour, minute):
    expected = f'night {minute:02d}' if hour < 6 else f'day {minute}'
    assert schedule_slot(f'{hour:02d}:{minute:02d}') == expected
