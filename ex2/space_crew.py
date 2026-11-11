#!/usr/bin/env python3
import json
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    CADET = 'cadet',
    OFFICER = 'officer',
    LIEUTENANT = 'lieutenant',
    CAPTAIN = 'captain',
    COMMANDER = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default='planned')
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def extra_validator(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError('Mission ID must start with "M"')
        has_leader = False
        for member in self.crew:
            if member.rank in ('captain', 'commander'):
                has_leader = True
        if not has_leader:
            raise ValueError('Mission needs at least one Captain/Commander')
        for member in self.crew:
            if not member.is_active:
                raise ValueError('All crew must be active for missions')
        if self.duration_days > 365:
            crew_headcount = len(self.crew)
            has_experience = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    has_experience += 1
            if not has_experience >= crew_headcount/2:
                raise ValueError('Long missions need 50%% experienced crew')
        return self


def main() -> None:
    try:
        with open('space_missions.json') as f:
            data = json.load(f)
        for item in data:
            for member in item['crew']:
                try:
                    CrewMember.model_validate(member)
                except ValidationError as ce:
                    print(ce.errors()[0]["msg"])

            try:
                s = SpaceMission.model_validate(item)
                for k, v in s:
                    if isinstance(v, list):
                        for member in v:
                            print('*' * 20)
                            for i, j in member:
                                print(f"  {i}: {j}")
                        print('*' * 20)
                    else:
                        print(f" {k}: {v}\n")
            except ValidationError as e:
                print(e.errors()[0]["msg"])
            print('=' * 50)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
