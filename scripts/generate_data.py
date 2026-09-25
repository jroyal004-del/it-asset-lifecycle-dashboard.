import os
import random
from datetime import timedelta
import pandas as pd
from faker import Faker

random.seed(42)
Faker.seed(42)
fake = Faker()

DEPTS = ["Engineering", "Finance", "Logistics", "HR", "Operations", "IT"]
TYPES = {"Laptop": (900, 2200), "Desktop": (700, 1800),
         "Monitor": (150, 500), "Docking Station": (100, 300)}
OS_OPTIONS = ["Windows 10", "Windows 11", "macOS 13", "macOS 14", "macOS 15"]
STATUSES = ["In Use", "In Storage", "Retired", "Pending Disposal"]
LOCATIONS = ["Building A", "Building B", "Warehouse", "Remote"]

departments = pd.DataFrame({"dept_id": range(1, len(DEPTS) + 1), "dept_name": DEPTS})
employees = pd.DataFrame({
    "emp_id": range(1, 61),
    "name": [fake.name() for _ in range(60)],
    "dept_id": [random.randint(1, len(DEPTS)) for _ in range(60)],
})

rows = []
for i in range(1, 501):
    atype = random.choice(list(TYPES))
    low, high = TYPES[atype]
    purchase = fake.date_between(start_date="-7y", end_date="-1m")
    rows.append({
        "asset_id": f"A{i:04d}",
        "serial_number": fake.bothify("??#######").upper(),
        "asset_type": atype,
        "purchase_date": purchase,
        "cost": round(random.uniform(low, high), 2),
        "os_version": random.choice(OS_OPTIONS) if atype in ("Laptop", "Desktop") else None,
        "status": random.choice(STATUSES),
        "location": random.choice(LOCATIONS),
        "owner_emp_id": random.randint(1, 60),
        "warranty_expiry": purchase + timedelta(days=365 * random.choice([1, 3, 3, 5])),
        "last_audit_date": fake.date_between(start_date="-3y", end_date="today"),
    })
assets = pd.DataFrame(rows)

# Second system of record (finance), copied BEFORE flaws are injected
finance = assets[["asset_id", "serial_number", "cost", "purchase_date"]].copy()
finance = finance.rename(columns={"cost": "book_cost"})

# --- Inject realistic data problems ---
# 1. Duplicate serial numbers in the IT system
for idx in random.sample(range(1, 500), 12):
    assets.loc[idx, "serial_number"] = assets.loc[idx - 1, "serial_number"]

# 2. Missing owners
assets.loc[random.sample(range(500), 20), "owner_emp_id"] = None

# 3. Assets missing from finance's list
finance = finance.drop(finance.sample(15, random_state=1).index)

# 4. Cost mismatches between systems
for idx in random.sample(list(finance.index), 10):
    finance.loc[idx, "book_cost"] = round(finance.loc[idx, "book_cost"] * random.uniform(0.8, 1.2), 2)

# 5. "Ghost" assets that finance has but IT doesn't
ghosts = pd.DataFrame([{
    "asset_id": f"F{9000 + n}",
    "serial_number": fake.bothify("??#######").upper(),
    "book_cost": round(random.uniform(500, 2000), 2),
    "purchase_date": fake.date_between(start_date="-6y", end_date="-1y"),
} for n in range(8)])
finance = pd.concat([finance, ghosts], ignore_index=True)

# --- Save ---
os.makedirs("data/raw", exist_ok=True)
assets.to_csv("data/raw/it_assets.csv", index=False)
finance.to_csv("data/raw/finance_assets.csv", index=False)
departments.to_csv("data/raw/departments.csv", index=False)
employees.to_csv("data/raw/employees.csv", index=False)
print("Done. Files saved to data/raw/")
