from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        self._check_id_prefix()
        self._check_physical_verification()
        self._check_telepathic_witnesses()
        self._check_strong_signal_message()
        return self

    def _check_id_prefix(self) -> None:
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

    def _check_physical_verification(self) -> None:
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

    def _check_telepathic_witnesses(self) -> None:
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

    def _check_strong_signal_message(self) -> None:
        if (
            self.signal_strength > 7.0
            and self.message_received is None
        ):
            raise ValueError(
                "Strong signals (>7.0) must include a received message"
            )


def process_alien_data(json_data: str) -> None:
    try:
        contact = AlienContact.model_validate_json(json_data)

        print("Successfully parsed and validated incoming JSON telemetry!")
        print(f"Contact ID: {contact.contact_id}")
        timestamp_info = f"{type(contact.timestamp)} -> {contact.timestamp}"
        print(
            "Timestamp parsed into Python datetime:",
            timestamp_info,
        )
        print(f"Message: '{contact.message_received}'")

    except ValidationError as e:
        print(f"Validation failed for incoming JSON data:\n{e}")


if __name__ == "__main__":
    raw_json_input = """
    {
        "contact_id": "AC_2026_999",
        "timestamp": "2026-06-07T09:15:00",
        "location": "Deep Space Sector 4",
        "contact_type": "radio",
        "signal_strength": 8.8,
        "duration_minutes": 120,
        "witness_count": 5,
        "message_received": "Signal detected from Kepler-186f",
        "is_verified": false
    }
    """

    process_alien_data(raw_json_input)
