from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from database import session_factory
from models import OrganizationOrm, CarOrm, Hijacking, Accident

from schemas import *

app = FastAPI(
    title="Trading App"
)

def technical_inspection_check():
    with session_factory() as session:
        query = select(CarOrm)
        result = session.execute(query)
        cars = result.scalars().all()
        for car in cars:
            if car.date_of_issue < datetime.now().year:
                car.technical_inspection = False
        session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(technical_inspection_check, 'cron', hour=0)  # Запуск в полночь каждый день
scheduler.start()

# Поиск по гос. номеру
@app.get('/car/{num}')
def get_car(num: str):
    with session_factory() as session:
        query = select(CarOrm).where(CarOrm.number == num).options(joinedload(CarOrm.organization))
        res = session.execute(query)
        res_sqla = res.scalar()
        try:
            res_pd = CarModel.model_validate(res_sqla, from_attributes=True)
        except Exception as e:
            print(e)
            return {'car': 'Машина не была найдена'}
        session.commit()
    return {'car': res_pd}

# Добавление машины с организацией
@app.post('/add_car')
def add_car(car: CarModel):
    print(car.technical_inspection)
    with session_factory() as session:
        if car.organization:
            stmt_org = insert(OrganizationOrm).values(
                [
                    dict(car.organization)
                ]
            )
            session.execute(stmt_org)
            qery = select(OrganizationOrm).where(OrganizationOrm.name == car.organization.name)
            id_org = session.execute(qery).scalar().id
        else:
            id_org = None
        car_dict = dict(car)
        car_dict.pop('organization')
        car_dict['organization_id'] = id_org
        add = AddCarModel(**car_dict)
        stmt_car = insert(CarOrm).values(
            [
                dict(add)
            ]
        )
        session.execute(stmt_car)
        session.commit()
    return {"status": "200 OK"}

######### Разкоментировать когда добавлю в БД техосмотр #########

# Прохождение машины на техобслуживание
@app.get('/undergoing_maintenance/{num}')
def get_car(num: str):
    with session_factory() as session:
        query = select(CarOrm).where(CarOrm.number == num)
        res = session.execute(query)
        res_sqla = res.scalar()
        if res_sqla:
            res_sqla.technical_inspection = True
        else:
            return {'status': 'Машина не найдена'}
        session.commit()
        return {'status': '200 OK'}

# Список всех машин, которые не проишли техобслудивание
@app.get('/technical_inspection_false')
def get_car():
    with session_factory() as session:
        query = select(CarOrm).where(CarOrm.technical_inspection == False)
        res = session.execute(query)
        res_sqla = res.scalars()
        res_pd = [CarModel.model_validate(car, from_attributes=True) for car in res_sqla]
        session.commit()
        return {'cars': res_pd}


# Добавление угнанной машины
@app.post('/add_ugon')
def ugon(number: str):
    with session_factory() as session:
        stmt = insert(Hijacking).values(
            [
                {'number': number}
            ]
        )
        session.execute(stmt)
        session.commit()
        return {'status': '200 OK'}

# Поиск машины которую угнали
@app.get('/ugon/{num}')
def ugon_postam(number: str):
    with session_factory() as session:
        query = select(Hijacking).where(Hijacking.number == number)
        res = session.execute(query)
        res_sqla = res.scalar()
        try:
            query_car = select(CarOrm).where(CarOrm.number == res_sqla.number)
        except Exception as e:
            return {'car': 'Машина не была найдена'}
        res = session.execute(query_car)
        res_sqla = res.scalar()
        res_pd = CarModel.model_validate(res_sqla, from_attributes=True)
        session.commit()

        return {'car': res_pd}


# Добавление ДТП
@app.post('/add_DTP')
def add_DTP(acident: AcidentModel):
    with session_factory() as session:
        stmt = insert(Accident).values(
            [
                dict(acident)
            ]
        )
        session.execute(stmt)
        session.commit()
        return {'status': '200 OK'}

# Поиск участвовали ли машина в ДТП
@app.get('/DTP/{num}')
def ugon_postam(number: str):
    with session_factory() as session:
        query = select(Accident).where(Accident.number == number)
        res = session.execute(query)
        res_sqla = res.scalar()
        res_bd = AcidentModel.model_validate(res_sqla, from_attributes=True)
        return {'DTP': res_bd}