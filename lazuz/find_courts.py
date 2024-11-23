import re
from datetime import datetime, timedelta

from lazuz.api_calls import ApiCalls

def parse_free_hours(free_clubs: list[str]) -> list[int]:
    return [int(re.match(r'([0-9]{2}):00', hour).group(1)) for hour in free_clubs]


def find_evening_court() -> None:
    api_calls = ApiCalls()

    next_days = [datetime.now() + timedelta(days=day) for day in range(30)] 
    week_days = [day for day in next_days if not (4 <= day.weekday() < 6)]
    for court in [66, 139]:
        for day in week_days:
            clubs = api_calls.clubs_by_id(court, day)
            assert clubs.status_code == 200

            result = clubs.json()
            hours = parse_free_hours(result['clubs'][0]['availableSlots'])
            free = False

            for hour in [19, 20, 21]:
                if hour in hours:
                    free = True
                    print(f'court {court} - {(day.weekday() + 1) % 7 + 1} - {day.date()} {hour}')
            # if not free:
            #     print(f'{(day.weekday() + 1) % 7 + 1} - {day} No free hours')


if __name__ == '__main__':
    find_evening_court()