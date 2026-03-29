from dataclasses import dataclass


@dataclass
class Car:
    id: str
    link: str
    name: str
    year: int
    CRC: float | None
    USD: float | None
