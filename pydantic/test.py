from typing import Annotated, Literal

from annotated_types import Gt

from pydantic import BaseModel, ValidationError, Field, field_validator
from annotated_types import Annotated
from typing import List, Optional


#Написать вложенную схему валидации данных, получить ошибки валидации


class Fruit(BaseModel):
    name: str  
    color: Literal['red', 'green']  
    weight: Annotated[float, Gt(0)]  
    

class Basket(BaseModel):
    name: str
    fruits: List[Fruit] = Field(min_items=1) 



data = {
    "name": "корзина1",
    "fruits": [
        {"name": "абрикос", "color": "red", "weight":"22 кг"},  # Ошибка: zip_code должен быть 5 цифр
        {"name": 123, "color": "red", "weight":0.2}  # Ошибка: city не должен быть пустым
    ]
}
'''
try:
    basket = Basket(**data)
except ValidationError as e:
    print(e.json(indent=2)) 


[
  {
    "type": "float_parsing",
    "loc": [
      "fruits",
      0,
      "weight"
    ],
    "msg": "Input should be a valid number, unable to parse string as a number",
    "input": "22 кг",
    "url": "https://errors.pydantic.dev/2.10/v/float_parsing"
  },
  {
    "type": "string_type",
    "loc": [
      "fruits",
      1,
      "name"
    ],
    "msg": "Input should be a valid string",
    "input": 123,
    "url": "https://errors.pydantic.dev/2.10/v/string_type"
  }
]'''


#Написать метод с кастомным post-валидатором к полю


class User(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=99)

    # Кастомный пост-валидатор для поля age
    @field_validator("age", mode="after")
    def check_age(cls, value):
        if value == 21:  
            raise ValueError("Age cannot be 21!")
        return value

'''
try:
    user = User(name="Alice", age=21)
except ValidationError as e:
    print(e.json(indent=2))
'''


#Навесить кастомный пост-валидатор к полю с помощью Annotated без объявления метода модели (не получилось)


def validate_age(value: int) -> int:
    if value == 21:
        raise ValueError("Age cannot be 21!")
    return value

class User(BaseModel):
    # Навешиваем кастомный валидатор через Annotated
    age: Annotated[int, Field(ge=18, le=99), field_validator("age", mode="after")(validate_age)]

'''
# Пример использования
try:
    user = User(age=21)
except ValidationError as e:
    print(e.json(indent=2))
'''

#Экспортировать данные в формат JSON с помощью Pydantic без библиотеки json

class User(BaseModel):
    id: int
    name: str
    is_active: bool

user = User(id=1, name="John Doe", is_active=True)

# Экспортируем данные в JSON
json = user.model_dump_json(indent=2)  
print(json)

# Экспортируем данные в плоский формат
model = user.model_dump()  
print(model)

#Написать скрипт, считывающий значения из переменных окружения с помощью pydantic-settings

from pydantic_settings import BaseSettings

class DatabaseSettings(BaseModel):
    url: str
    port: int = 5432  # Значение по умолчанию


class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(levelname)s - %(message)s"


class AppSettings(BaseSettings):
    app_name: str
    debug: bool = False
    database: DatabaseSettings  
    logging: Optional[LoggingSettings] = None  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = AppSettings()
except ValidationError as e:
    print(e.json(indent=2)) 

