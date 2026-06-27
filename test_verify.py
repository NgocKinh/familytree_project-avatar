from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

print(
    pwd.verify(
        "Admin@123",
        "$2b$12$A3/aYnwlCag4n//KCCWYdOcC0Gpll/9ztkY3jmsPxBFmpzsJr8fSa",
    )
)