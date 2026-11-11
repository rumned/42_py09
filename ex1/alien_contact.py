#!/usr/bin/env python3
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
import json


class ContactType(str, Enum):
    RADIO = 'radio'
    VISUAL = 'visual'
    PHYSICAL = 'physical'
    TELEPATHIC = 'telepathic'


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

    @model_validator(mode='after')
    def extra_validator(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError('Contact ID must start with "AC"')
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError('Physical contact reports must be verified')
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                'Telepathic contact requires at least 3 witnesses'
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                'Strong signals (> 7.0) must include a received message'
            )
        return self


def main() -> None:
    try:
        with open('alien_contacts.json') as f:
            data = json.load(f)
        for item in data:
            try:
                s = AlienContact.model_validate(item)
                for k, v in s:
                    print(f"{k}: {v}")
            except ValidationError as e:
                print(e.errors()[0]["msg"])
            print('=' * 20)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
