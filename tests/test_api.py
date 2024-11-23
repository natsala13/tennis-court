from datetime import datetime, timedelta

import pytest

from lazuz.api_calls import ApiCalls


@pytest.fixture(scope='module')
def api_calls():
    return ApiCalls()

def test_authentication(api_calls):
    assert len(api_calls.token) > 1

def test_available_court(api_calls):
    slots = api_calls.available_slots(1)
    assert slots.status_code == 200
    print(slots.json())

def test_rokah4(api_calls):
    clubs = api_calls.clubs_by_id(66, datetime.now())
    assert clubs.status_code == 200
    print(clubs.json())
    import ipdb;ipdb.set_trace()

def test_all_available_courts_in_week(api_calls):
    next_days = [datetime.now() + timedelta(days=day) for day in range(14)] 
    week_days = [day for day in next_days if not (4 <= day.weekday() < 6)]

    for day in week_days:
        clubs = api_calls.clubs_by_id(139, day)
        assert clubs.status_code == 200
        print(f'{day} - {clubs.json()}')
