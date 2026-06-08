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
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (>7.0) should include received messages"
            )


def display_contact_info(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10.0")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {contact.message_received or 'No message received'}")
    print(f"Verified: {contact.is_verified}")


def create_valid_contact() -> AlienContact:
    return AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.fromisoformat("2024-06-15T14:30:00"),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False,
    )


def attempt_invalid_id() -> None:
    try:
        AlienContact(
            contact_id="WRONG_001",
            timestamp=datetime.now(),
            location="Unknown",
            contact_type=ContactType.VISUAL,
            signal_strength=3.0,
            duration_minutes=10,
            witness_count=1,
            message_received=None,
            is_verified=False,
        )
        print("No error raised? Unexpected.")
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'value_error':
                print(f"Business Rule Violation: {error['msg']}")


def attempt_invalid_physical_unverified() -> None:
    try:
        AlienContact(
            contact_id="AC_002",
            timestamp=datetime.now(),
            location="Mars",
            contact_type=ContactType.PHYSICAL,
            signal_strength=6.0,
            duration_minutes=30,
            witness_count=4,
            message_received="Handshake observed",
            is_verified=False,
        )
        print("No error raised? Unexpected.")
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'value_error':
                print(f"Business Rule Violation: {error['msg']}")


def attempt_invalid_telepathic_witnesses() -> None:
    try:
        AlienContact(
            contact_id="AC_003",
            timestamp=datetime.now(),
            location="Andromeda",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=2,
            message_received=None,
            is_verified=False,
        )
        print("No error raised? Unexpected.")
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'value_error':
                print(f"Business Rule Violation: {error['msg']}")


def attempt_invalid_strong_signal_no_message() -> None:
    try:
        AlienContact(
            contact_id="AC_004",
            timestamp=datetime.now(),
            location="Zeta Reticuli",
            contact_type=ContactType.RADIO,
            signal_strength=9.5,
            duration_minutes=60,
            witness_count=10,
            message_received=None,
            is_verified=False,
        )
        print("No error raised? Unexpected.")
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'value_error':
                print(f"Business Rule Violation: {error['msg']}")


def main() -> None:
    print("=" * 50)
    print("Alien Contact Log Validation")
    print("=" * 50)

    print("Valid contact report:")
    contact = create_valid_contact()
    display_contact_info(contact)

    print("Invalid cases:")
    attempt_invalid_id()
    print()
    attempt_invalid_physical_unverified()
    print()
    attempt_invalid_telepathic_witnesses()
    print()
    attempt_invalid_strong_signal_no_message()


if __name__ == "__main__":
    main()
