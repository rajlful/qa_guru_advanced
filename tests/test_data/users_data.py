from dataclasses import dataclass, asdict
from faker import Faker
from pydantic import EmailStr


@dataclass
class User:
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


fake = Faker()


def fake_user():
    return asdict(
        User(
            fake.email(),
            fake.first_name(),
            fake.last_name(),
            fake.image_url()
        )
    )
