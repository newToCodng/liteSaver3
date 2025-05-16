# LiteSaver 💸

LiteSaver is a **personal finance tracking app** designed to be simple for users but robust under the hood. It allows users to **track income and expenses**, **set budgets**, **create savings goals**, and **generate reports** — all while keeping the user interface clean and intuitive.

---

## 📌 Features

### Backend (FastAPI)
- User Registration and Login (JWT Auth)
- Manage Accounts (Multi-currency support)
- Create and View Transactions (Income/Expense)
- Set Budgets and Monitor Progress
- Define and Track Savings Goals
- Generate Reports (JSONB based, future export support planned)
- CORS-enabled for frontend integration
- Modular architecture with separate routers, services, and models

### Frontend (Flutter)
- User Authentication (Login/Register)
- Dashboard Overview (Balances, Transactions)
- Accounts Page
- Add/View Transactions
- (Planned) Reports and Settings Pages

---

## 🛠️ Tech Stack

| Layer        | Technology      |
|--------------|-----------------|
| Backend      | FastAPI (Python)|
| Database     | PostgreSQL      |
| Frontend     | Flutter (Dart)  |
| DB Driver    | asyncpg         |
| Auth         | JWT (HS256)     |

---

## 📁 Project Structure (Backend)

