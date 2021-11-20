from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = crud.create_user(db=db, user=user)
    
    return user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}/", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    return user

@app.put("/users/{user_id}/", response_model=schemas.User)
def edit_user(user_id: int, values: schemas.UserEdit, db: Session = Depends(get_db)):
    edited_user = crud.edit_user(db, user_id, values=values)
    return edited_user

@app.get("/measures/", response_model=List[schemas.Measure])
def get_all_medidas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_measures(db, skip, limit)

@app.get("/users/{user_id}/measures/", response_model=List[schemas.Measure])
def get_user_measures(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        measure = crud.get_user_measures(db, user_id)
        return measure
    
    return HTTPException(status_code=400, detail="Usuário não encontrado!")


@app.post("/users/{user_id}/measures/", response_model=schemas.Measure)
def create_measures(user_id: int, measures: schemas.MeasureBase, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        measure = crud.create_user_measure(db, measures, user_id)
        return measure
    
    return HTTPException(status_code=400, detail="Usuário não encontrado!")