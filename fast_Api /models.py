from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from database import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    # shifts = relationship("Shift", back_populates="employee")


class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    shift_date = Column(Date)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    # employee = relationship("Employee", back_populates="shifts")

