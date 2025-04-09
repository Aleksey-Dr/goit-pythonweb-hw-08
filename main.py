from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Залежність для отримання сесії бази даних
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=models.Contact)
def create_contact(contact: models.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[models.Contact])
def read_contacts(skip: int = 0, limit: int = 100, first_name: str = None,
                  last_name: str = None, email: str = None, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit, first_name=first_name, last_name=last_name, email=email)
    return contacts


@app.get("/contacts/{contact_id}", response_model=models.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=models.Contact)
def update_contact(contact_id: int, contact: models.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=dict)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    if crud.delete_contact(db, contact_id=contact_id):
        return {"message": f"Contact with id {contact_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Contact not found")


@app.get("/contacts/birthdays/upcoming", response_model=List[models.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    upcoming_birthdays = crud.get_upcoming_birthdays(db)
    return upcoming_birthdays