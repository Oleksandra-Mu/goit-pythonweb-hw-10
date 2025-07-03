from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.contact import ContactUpdate, ContactCreate, Contact
from src.repository import contact as repository_contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/",
    response_model=List[Contact],
)
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contact.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: Session = Depends(get_db)):
    owner = await repository_contact.create_contact(body, db)
    return owner


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(
    body: ContactUpdate, contact_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    contact = await repository_contact.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search/", response_model=List[Contact])
def search_contacts_by_query(query: str, db: Session = Depends(get_db)):
    search_result = repository_contact.search_contacts(db, query)
    if not search_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contacts found"
        )
    return search_result


@router.get("/birthdays/", response_model=List[Contact])
async def get_birthdays(db: Session = Depends(get_db)):
    upcoming_birthdays = await repository_contact.get_upcoming_birthdays(db)
    if not upcoming_birthdays:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No upcoming birthdays found"
        )
    return upcoming_birthdays
