from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

current_expression = ""


class Operation(BaseModel):
    a: float
    b: float
    op: str


class Expression(BaseModel):
    expression: str


@app.post("/add")
def add(op: Operation):
    return {"result": op.a + op.b}


@app.post("/subtract")
def subtract(op: Operation):
    return {"result": op.a - op.b}


@app.post("/multiply")
def multiply(op: Operation):
    return {"result": op.a * op.b}


@app.post("/divide")
def divide(op: Operation):
    if op.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": op.a / op.b}


@app.post("/add-expression")
def add_expression(expr: Expression):
    global current_expression
    current_expression = expr.expression
    return {"message": "Expression saved", "expression": current_expression}


@app.get("/get-expression")
def get_expression():
    return {"current_expression": current_expression}


@app.get("/evaluate")
def evaluate_expression():
    global current_expression
    try:
        # Безопасное выполнение выражения
        allowed = re.fullmatch(r"[\d\s+\-*/().]+", current_expression)
        if not allowed:
            raise HTTPException(status_code=400, detail="Invalid characters in expression")
        result = eval(current_expression)
        return {"result": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expression")
