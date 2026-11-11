#!/usr/bin/env python3
import json
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    try:
        with open('space_stations.json') as f:
            data = json.load(f)
        for item in data:
            try:
                s = SpaceStation.model_validate(item)
                for k, v in s:
                    print(f"{k}: {v}")
            except ValidationError as e:
                print(e.errors()[0]["msg"])
            print('=' * 20)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
