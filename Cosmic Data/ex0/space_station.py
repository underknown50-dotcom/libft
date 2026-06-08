from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def display_station_info(station: SpaceStation) -> None:
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Last maintenance: {station.last_maintenance}")
    status = 'Operational' if station.is_operational else 'Non-operational'
    print(f"Status: {status}")
    print(f"Notes: {station.notes}")


def create_valid_station() -> SpaceStation:
    return SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.fromisoformat("2024-06-15T10:30:00"),
        is_operational=True,
        notes="Main module replacement scheduled",
    )


def attempt_invalid_station_creation() -> None:
    try:
        SpaceStation(
            station_id="MARS01",
            name="Mars Base Alpha",
            crew_size=50,
            power_level=95.0,
            oxygen_level=88.0,
            last_maintenance=datetime(2024, 7, 1, 12, 0, 0),
        )
        print("No error raised? Unexpected.")
    except ValidationError as e:
        print(f"ValidationError caught:\n{e}")


def main() -> None:
    print("=" * 50)
    print("Space Station Data Validation")
    print("=" * 50)

    print("Valid station created:")
    station = create_valid_station()
    display_station_info(station)

    print("Expected validation error (crew_size > 20):")
    attempt_invalid_station_creation()


if __name__ == "__main__":
    main()
