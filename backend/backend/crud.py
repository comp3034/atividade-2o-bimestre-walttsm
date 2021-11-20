from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_user(db: Session, user_id: int, values: schemas.UserEdit):
    print(values)
    db_user_to_update = get_user(db, user_id)
    if db_user_to_update:
        if values.name != None:
            db_user_to_update.name = values.name
        
        if values.email != None:
            db_user_to_update.email = values.email
            
        if values.birth_date != None:
            db_user_to_update.birth_date = values.birth_date
    
        db.add(db_user_to_update)
        db.commit()
        db.refresh(db_user_to_update)
        
    return db_user_to_update

def get_measures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Measure).offset(skip).limit(limit).all()

def create_user_measure(db: Session, measure: schemas.MeasureBase, user_id: int):
    db_measure = models.Measure(**measure.dict(), user_id=user_id)
    print(db_measure)
    db.add(db_measure)
    db.commit()
    db.refresh(db_measure)
    return db_measure

def get_user_measures(db: Session, user_id: int):
    return db.query(models.Measure).filter(models.Measure.user_id == user_id).all()
