from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Hashavim360")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ---------- דפים קיימים ----------
@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
@app.get("/about.html", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/services", response_class=HTMLResponse)
@app.get("/services.html", response_class=HTMLResponse)
def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
@app.get("/contact.html", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/healthz")
def healthz():
    return PlainTextResponse("ok")

# ---------- דפי מחשבונים חדשים ----------
@app.get("/calc/loan", response_class=HTMLResponse)
def calc_loan_page(request: Request):
    return templates.TemplateResponse("loan.html", {"request": request})

@app.get("/calc/investment", response_class=HTMLResponse)
def calc_invest_page(request: Request):
    return templates.TemplateResponse("investment.html", {"request": request})

@app.get("/calc/mortgage", response_class=HTMLResponse)
def calc_mortgage_page(request: Request):
    return templates.TemplateResponse("mortgage.html", {"request": request})

# ---------- מודלים לחישוב ----------
class LoanInput(BaseModel):
    amount: float
    annual_rate_percent: float
    years: float

class LoanOutput(BaseModel):
    monthly_payment: float
    total_payment: float
    total_interest: float

class InvestInput(BaseModel):
    principal: float
    annual_rate_percent: float
    years: float

class InvestOutput(BaseModel):
    future_value: float

# ---------- API אמיתי ----------
@app.post("/api/calc/loan", response_model=LoanOutput)
def api_calc_loan(body: LoanInput):
    if body.amount <= 0 or body.years <= 0:
        raise HTTPException(status_code=400, detail="amount & years חייבים להיות > 0")
    r = body.annual_rate_percent / 100.0 / 12.0
    n = int(round(body.years * 12))
    if r == 0:
        monthly = body.amount / n
    else:
        x = (1 + r) ** n
        monthly = (body.amount * r * x) / (x - 1)
    total = monthly * n
    interest = total - body.amount
    return LoanOutput(monthly_payment=round(monthly, 2),
                      total_payment=round(total, 2),
                      total_interest=round(interest, 2))

@app.post("/api/calc/investment", response_model=InvestOutput)
def api_calc_invest(body: InvestInput):
    if body.principal < 0 or body.years < 0:
        raise HTTPException(status_code=400, detail="principal & years חייבים להיות ≥ 0")
    r = body.annual_rate_percent / 100.0
    fv = body.principal * ((1 + r) ** body.years)
    return InvestOutput(future_value=round(fv, 2))

@app.post("/api/calc/mortgage", response_model=LoanOutput)
def api_calc_mortgage(body: LoanInput):
    # אותו חישוב כמו הלוואה
    return api_calc_loan(body)
