from hellofresh.recipes.data_preparation import _time_string_to_minutes


def test_should_calculate_correct_time_for_hours_and_minutes():
    assert 80 == _time_string_to_minutes('PT1H20M')


def test_should_calculate_correct_time_for_minutes_only():
    assert 90 == _time_string_to_minutes('PT90M')


def test_should_calculate_correct_time_for_hours_only():
    assert 240 == _time_string_to_minutes('PT4H')


def test_should_return_zero_if_nothing_provided():
    assert 0 == _time_string_to_minutes('PT')
