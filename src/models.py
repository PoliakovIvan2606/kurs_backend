from typing import List

from sqlalchemy import ForeignKey, Table, Column, MetaData, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_10, str_17


class CarOrm(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str_10] #= mapped_column(unique=True) # TODO Разкоментировать
    full_name: Mapped[str]
    address: Mapped[str] # Адрес проживания
    make: Mapped[str] # Марка машины
    date_of_issue: Mapped[int]  # Дата выпуска
    engine_capacity: Mapped[int] # Объём двигателя
    engine_number: Mapped[str_17] # Номер двигателя. Тоже должен быть уникальным
    color: Mapped[str]
    vehicle_type: Mapped[str] # Тип ТС

    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=True)

    technical_inspection: Mapped[bool] = mapped_column(default=True) # техосмотр

    organization: Mapped['OrganizationOrm'] = relationship()

    hijacking: Mapped['Hijacking'] = relationship()
class OrganizationOrm(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] #= mapped_column(unique=True)
    city: Mapped[str]
    area: Mapped[str] # Район
    address: Mapped[str]
    supervisor: Mapped[str] # Руководитель

    organization: Mapped['CarOrm'] = relationship()

# Дорожно транспортное проишествие
class Accident(Base):
    __tablename__ = "accident"

    id: Mapped[int] = mapped_column(primary_key=True)

    data: Mapped[str] # дата
    type_of_incident: Mapped[str] # тип проишествия
    place: Mapped[str] # место проишествия
    brands_of_affected_cars: Mapped[str] # марки пострадавших машин список марок
    number: Mapped[str] #= mapped_column(unique=True) # государственный номер
    machine_type: Mapped[str] # тип машины
    summary: Mapped[str] # краткое содержание
    number_of_victims: Mapped[int] # число пострадавших
    amount_of_damage: Mapped[int] # сумма ущерба
    cause: Mapped[str] # причина
    road_conditions: Mapped[str] # дорожные условия

# Угон
class Hijacking(Base):
    __tablename__ = "hijacking"

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str_10] = mapped_column(ForeignKey("car.number", ondelete="CASCADE"))# , unique=True)

    hijacking: Mapped['CarOrm'] = relationship()