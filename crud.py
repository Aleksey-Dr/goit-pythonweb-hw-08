from typing import List
from datetime import date, timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from . import models, database


def get_contact(db: Session, contact_id: int):
    return (
        db.query(database.ContactDB).filter(database.ContactDB.id == contact_id).first()
    )


def get_contacts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
):
    query = db.query(database.ContactDB)
    if first_name:
        query = query.filter(database.ContactDB.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(database.ContactDB.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(database.ContactDB.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


def create_contact(db: Session, contact: models.ContactCreate):
    db_contact = database.ContactDB(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: models.ContactUpdate):
    db_contact = (
        db.query(database.ContactDB).filter(database.ContactDB.id == contact_id).first()
    )
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = (
        db.query(database.ContactDB).filter(database.ContactDB.id == contact_id).first()
    )
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False


def get_upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []
    contacts = db.query(database.ContactDB).all()
    for contact in contacts:
        birthday_month = contact.birthday.month
        birthday_day = contact.birthday.day

        # Processing February 29 in a non-leap year
        if birthday_month == 2 and birthday_day == 29 and not isleap(today.year):
            birthday_this_year = date(today.year, 2, 28)
        else:
            try:
                birthday_this_year = date(today.year, birthday_month, birthday_day)
            except ValueError:
                continue

        if today <= birthday_this_year <= next_week:
            upcoming_birthdays.append(contact)
        else:
            next_year = today.year + 1
            if birthday_month == 2 and birthday_day == 29 and not isleap(next_year):
                birthday_next_year = date(next_year, 2, 28)
            else:
                try:
                    birthday_next_year = date(next_year, birthday_month, birthday_day)
                except ValueError:
                    continue

            if today <= birthday_next_year <= next_week:
                upcoming_birthdays.append(contact)
    return upcoming_birthdays
