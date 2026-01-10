import re
import yaml
from datetime import datetime, timedelta
from pathlib import Path

from lazuz.api_calls import ApiCalls
from lazuz.courts_data import DAYS, COURTS


PREFERENCE_FILE = Path("configs/court_preferences.yaml")


def parse_free_hours(free_clubs: list[str]) -> list[int]:
    free_hours = [re.match(r"([0-9]{2}):00", hour) for hour in free_clubs]
    assert all(free_hours), f"Failed to parse {free_clubs}"

    return [int(hour.group(1)) for hour in free_hours if hour]


def load_preferences() -> dict:
    config = {}
    with open(PREFERENCE_FILE, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config


def create_list_of_days(
    preferences: dict[str, dict[str, list[int]]]
) -> dict[int, dict[int, set[int]]]:
    all_days = {day for category in preferences.values() for day in category["days"]}
    all_days_cartezian = [
        (day, category["hours"], category["courts"])
        for category in preferences.values()
        for day in category["days"]
    ]

    option_per_day = {
        day: [
            options for day_option, *options in all_days_cartezian if day_option == day
        ]
        for day in all_days
    }
    return {
        day: dict(
            (court, {x for x in config[0]})
            for config in days_configs
            for court in config[-1]
        )
        for day, days_configs in option_per_day.items()
    }


def find_courts_on_preference(days_forward: int = 30):
    config = load_preferences()
    all_days = create_list_of_days(config)

    api_calls = ApiCalls()
    next_days = [datetime.now() + timedelta(days=day) for day in range(days_forward)]

    # 4 is Friday, 5 is Saturday, 6 is Sunday.
    next_days = [day for day in next_days if ((day.weekday() + 2) % 7) in all_days]

    for day in next_days:
        spots = all_days[(day.weekday() + 2) % 7]
        court_ids = spots.keys()

        clubs = api_calls.clubs_by_multiple_id(list(court_ids), day)
        assert clubs.status_code == 200

        result = clubs.json()
        result_per_club = {
            club["club_id"]: club["availableSlots"] for club in result["clubs"]
        }
        slots_per_club = {
            club: parse_free_hours(slots) for club, slots in result_per_club.items()
        }
        # hours = parse_free_hours(result['clubs'][0]['availableSlots'])
        wanted_slots = {
            court: hours & set(slots_per_club[court]) for court, hours in spots.items()
        }
        existing_slots = {
            court: hours for court, hours in wanted_slots.items() if hours
        }

        if existing_slots:
            for court, hours in existing_slots.items():
                print(
                    f'{DAYS[(day.weekday() + 2) % 7]} - {day.strftime("%d / %m")} - {COURTS[court]} - {hours}'
                )


if __name__ == "__main__":
    find_courts_on_preference()
