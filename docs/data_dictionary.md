# Data Dictionary

## it_assets.csv
| Column | Type | Description |
|---|---|---|
| asset_id | string | Unique ID for each asset (A0001-A0500) |
| serial_number | string | Manufacturer serial number |
| asset_type | string | Laptop, Desktop, Monitor, or Docking Station |
| purchase_date | date | Date the asset was purchased |
| cost | float | Purchase cost in USD |
| os_version | string | Operating system (laptops/desktops only) |
| status | string | In Use, In Storage, Retired, Pending Disposal |
| location | string | Building A, Building B, Warehouse, or Remote |
| owner_emp_id | int | Links to employees.csv |
| warranty_expiry | date | Warranty expiration date |
| last_audit_date | date | Last physical audit date |

## finance_assets.csv
| Column | Type | Description |
|---|---|---|
| asset_id | string | Links to it_assets.csv (where matched) |
| serial_number | string | Serial number as recorded by finance |
| book_cost | float | Cost as recorded in the finance system |
| purchase_date | date | Purchase date as recorded by finance |

## departments.csv
| Column | Type | Description |
|---|---|---|
| dept_id | int | Unique department ID |
| dept_name | string | Department name |

## employees.csv
| Column | Type | Description |
|---|---|---|
| emp_id | int | Unique employee ID |
| name | string | Employee name (synthetic) |
| dept_id | int | Links to departments.csv |

## Known Data Issues (intentionally injected)
1. **Duplicate serial numbers** — 12 assets in it_assets.csv share a serial number with another asset.
2. **Missing owners** — 20 assets have no owner_emp_id assigned.
3. **Missing from finance** — 15 assets exist in IT's system but not in finance's records.
4. **Cost mismatches** — 10 assets have a different cost recorded in finance vs. IT.
5. **Ghost assets** — 8 assets exist in finance's records but not in IT's system (asset_id starts with "F9").