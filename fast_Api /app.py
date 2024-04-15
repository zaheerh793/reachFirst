from fastapi import APIRouter, HTTPException, Depends, FastAPI
import models
from validator import EmployeeSerializer, ShiftSerializer
from database import engine, get_db
from sqlalchemy.orm import Session
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
import uvicorn


@app.post("/employees/")
async def create_employee(employee: EmployeeSerializer, db: Session = Depends(get_db)):
    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@app.get("/employees/")
def retrieve_employee(db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).all()
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}")
async def update_employee(employee_id: int, employee_data: EmployeeSerializer, db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.name = employee_data.name
    employee.email = employee_data.email
    db.commit()
    db.refresh(employee)

    return employee


@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {}

@app.get("/employees/{employee_id}/shifts")
async def get_employee_shifts(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
        if not employee:
            return HTTPException(status_code=404, detail="Employee not found")
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")

    # employee = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    shifts = db.query(models.Shift).filter(models.Shift.employee_id==employee.id)
    return shifts


@app.post("/shifts/")
async def create_shift(shift: ShiftSerializer, db: Session = Depends(get_db)):
    employee_exists = db.query(models.Employee).filter(models.Employee.id==shift.employee_id).first()
    if not employee_exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    new_shift = models.Shift(
        start_time=shift.start_time,
        end_time=shift.end_time,
        shift_date=shift.shift_date,
        employee_id=shift.employee_id
    )
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift


@app.get("/shifts/")
async def get_shifts(shift_date: str = None, db: Session = Depends(get_db)):
    queryset = db.query(models.Shift).all()
    if shift_date:
        queryset = queryset.filter(shift_date=shift_date)
    # shifts = [ShiftSerializer(shift).dict() for shift in queryset]
    return queryset


@app.put("/shifts/{shift_id}")
async def update_shift(shift_id: int, shift_data: ShiftSerializer, db: Session = Depends(get_db)):
    try:
        shift = db.query(models.Shift).filter(models.Shift.id==shift_id).first()
    except models.Shift.DoesNotExist:
        raise HTTPException(status_code=404, detail="Shift not found")

    shift.start_time = shift_data.start_time
    shift.end_time = shift_data.end_time
    db.commit()
    db.refresh(shift)

    return shift


@app.delete("/shifts/{shift_id}")
async def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    try:
        shift = db.query(models.Shift).filter(models.Shift.id==shift_id).first()
    except models.Shift.DoesNotExist:
        raise HTTPException(status_code=404, detail="Shift not found")

    db.delete(shift)
    db.commit()
    return {}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8000")
