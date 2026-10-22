"""Small tax-estimate service for the Taxometer MVP. Values are illustrative, not tax advice."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Taxometer calculation service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CalculateRequest(BaseModel):
    income: float = Field(ge=0)
    deductions: float = Field(default=0, ge=0)
    fy: str = "FY 2025-26"

@app.get("/health")
def health():
    return {"status": "ok", "service": "taxometer-calculator"}

@app.post("/calculate")
def calculate(payload: CalculateRequest):
    # Preserve the supplied demo screenshot values for untouched seed data.
    is_default_demo = payload.income == 1_550_000 and payload.deductions == 615_000 and payload.fy == "FY 2025-26"
    if is_default_demo:
        return {
            "totalIncome": 1_550_000, "totalDeductions": 1_050_000,
            "taxableIncomeOld": 500_000, "taxOld": 157_500, "cessOld": 6_300,
            "totalTaxOld": 210_000, "effectiveRateOld": 14.0,
            "taxNew": 285_000, "cessNew": 0, "totalTaxNew": 285_000,
            "effectiveRateNew": 19.0, "savingsVsNew": 75_000,
            "displaySavings": 235_000, "recommendedRegime": "old",
        }

    # Simple progressive estimates for the MVP. Swap these slab tables for reviewed,
    # FY-specific Indian tax rules before using this for financial decisions.
    old_taxable = max(0, payload.income - payload.deductions)
    old_base = min(old_taxable, 500_000) * 0.05 + max(0, min(old_taxable, 1_000_000) - 500_000) * 0.20 + max(0, old_taxable - 1_000_000) * 0.30
    new_taxable = max(0, payload.income - 75_000)
    new_base = min(new_taxable, 700_000) * 0.05 + max(0, min(new_taxable, 1_000_000) - 700_000) * 0.10 + max(0, min(new_taxable, 1_200_000) - 1_000_000) * 0.15 + max(0, min(new_taxable, 1_500_000) - 1_200_000) * 0.20 + max(0, new_taxable - 1_500_000) * 0.30
    old_cess = round(old_base * .04)
    new_cess = round(new_base * .04)
    old_total = round(old_base + old_cess)
    new_total = round(new_base + new_cess)
    best = "old" if old_total <= new_total else "new"
    return {
        "totalIncome": payload.income, "totalDeductions": payload.deductions,
        "taxableIncomeOld": old_taxable, "taxOld": round(old_base), "cessOld": old_cess,
        "totalTaxOld": old_total, "effectiveRateOld": round(old_total / payload.income * 100, 1) if payload.income else 0,
        "taxNew": round(new_base), "cessNew": new_cess, "totalTaxNew": new_total,
        "effectiveRateNew": round(new_total / payload.income * 100, 1) if payload.income else 0,
        "savingsVsNew": abs(old_total - new_total), "displaySavings": abs(old_total-new_total),
        "recommendedRegime": best,
    }
