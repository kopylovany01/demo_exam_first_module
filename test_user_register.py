import re
from datetime import datetime, date
import pytest


class UserRegistration:
    def register(self, data):
        name = data.get("name", "")
        birthdate = data.get("birthdate", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        inn = data.get("inn", "")
        passport = data.get("passport", "")

        # Валидация имени
        if not name:
            return {"status": False}
        elif len(name) > 40:
            return {"status": False}
        elif not re.match(r'^[A-Za-zА-Яа-яёЁ\s]+$', name):
            return {"status": False}

        # Валидация возраста
        birth = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        sixteen_birthday = date(birth.year + 16, birth.month, birth.day)

        if today < sixteen_birthday:
            return {"status": False}

        # Валидация почты
        if not email:
            return {"status": False}
        elif len(email) > 64:
            return {"status": False}
        elif "@" not in email:
            return {"status": False}

        # Валидация номера телефона
        if not phone:
            return {"status": False}
        elif not re.match(r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$', phone):
            return {"status": False}
        
        # Валидация ИНН
        if not inn:
            return {"status": False}
        elif not inn.isdigit():
            return {"status": False}
        elif len(inn) != 12:
            return {"status": False}
        elif inn.startswith("00"):
            return {"status": False}

        # Валидация паспорта
        if not passport:
            return {"status": False}
        elif not passport.isdigit():
            return {"status": False}
        elif len(passport) != 10:
            return {"status": False}
        elif passport.startswith("00"):
            return {"status": False}
        
        
        return {"status": True}



class TestUserRegistration:
    positive_test_data_cases = [
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "1234567890"
         }, True),
        ({
             "name": "a" * 40,
             "birthdate": "2009-12-09",
             "email": "a" * 55 + "@mail.ru",
             "phone": "+7-999-888-77-32",
             "inn": "123456789012",
             "passport": "0134567890"
         }, True),
        ({
             "name": "a" * 39,
             "birthdate": "2009-12-08",
             "email": "a" * 56 + "@mail.ru",
             "phone": "+7-999-888-77-27",
             "inn": "123456789012",
             "passport": "0934567890"
         }, True),
        ({
             "name": "Ян",
             "birthdate": "1999-12-11",
             "email": "ivan-ivanoff@mail.ru",
             "phone": "+7-999-888-77-01",
             "inn": "123456789012",
             "passport": "0234567890"
         }, True),
        ({
             "name": "А",
             "birthdate": "2000-01-01",
             "email": "ivan.true123@mail.ru",
             "phone": "+7-999-888-77-11",
             "inn": "123456789012",
             "passport": "1234567890"
         }, True),
    ]
    negative_test_data_cases = [
        # Длина имени больше 40 символов
        ({
            "name": "a" * 41,
            "birthdate": "2000-01-01",
            "email": "ivan@mail.ru",
            "phone": "+7-999-888-77-66",
            "inn": "123456789012",
            "passport": "1234567890"
        }, False),
        # Длина почты более 64 символов
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "a" * 58 + "mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "1234567890"
         }, False),
        # Невалидный формат почты
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivanmail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "1234567890"
         }, False),
        # Невалидный формат номера телефона
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "8-999-888-77-66",
             "inn": "123456789012",
             "passport": "1234567890"
         }, False),
        # ИНН начинающийся с 00
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "003456789012",
             "passport": "1234567890"
         }, False),
        # Длина паспорта меньше 10 символов
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "123456789"
         }, False),
        # Длина паспорта больше 10 символов
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "12345678911"
         }, False),
        # Длина ИНН меньше 12 символов
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "12345678901",
             "passport": "1234567891"
         }, False),
        # Длина ИНН больше 12 символов
        ({
             "name": "Иван Иванов",
             "birthdate": "2000-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "12345678901",
             "passport": "123456789111"
         }, False),
        # Возраст меньше 16 лет
        ({
             "name": "Иван Иванов",
             "birthdate": "2011-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "123456789"
         }, False),
        # Паспорт начинается с 00
        ({
             "name": "Иван Иванов",
             "birthdate": "2011-01-01",
             "email": "ivan@mail.ru",
             "phone": "+7-999-888-77-66",
             "inn": "123456789012",
             "passport": "003456789"
         }, False),
    ]

    @pytest.fixture()
    def service(self):
        return UserRegistration()

    @pytest.mark.parametrize("data,expected", positive_test_data_cases)
    def test_successful_registration(self, service, data, expected):
        form_data = data

        result = service.register(data)
        assert result["status"] == expected

    @pytest.mark.parametrize("data,expected", negative_test_data_cases)
    def test_negative_registration(self, service, data, expected):
        form_data = data

        result = service.register(data)
        assert result["status"] == expected