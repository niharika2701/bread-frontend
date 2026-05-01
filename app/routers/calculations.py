from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import CalculationCreate, CalculationRead
from app.calculations import CalculationFactory

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.post("/", response_model=CalculationRead, status_code=201)
def add_calculation(payload: CalculationCreate, db: Session = Depends(get_db)):
    """Add a new calculation. Computes and stores the result."""
    if payload.user_id:
        user = db.query(models.User).filter(models.User.id == payload.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    result = CalculationFactory.compute(payload.type, payload.a, payload.b)

    record = models.Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type.value,
        result=result,
        user_id=payload.user_id
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    """Browse all calculations."""
    return db.query(models.Calculation).all()


@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    """Read a single calculation by ID."""
    record = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return record


@router.put("/{calc_id}", response_model=CalculationRead)
def edit_calculation(calc_id: int, payload: CalculationCreate, db: Session = Depends(get_db)):
    """Edit an existing calculation. Recomputes the result."""
    record = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Calculation not found")

    result = CalculationFactory.compute(payload.type, payload.a, payload.b)

    record.a = payload.a
    record.b = payload.b
    record.type = payload.type.value
    record.result = result
    record.user_id = payload.user_id

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{calc_id}", status_code=204)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    """Delete a calculation by ID."""
    record = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(record)
    db.commit()