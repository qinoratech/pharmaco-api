# PharmaCo API

A REST API that allows citizens to find on-duty pharmacies.

---

## Purpose

This API allows users to:

- Retrieve on-duty pharmacies by country and city
- Find nearby pharmacies using geolocation
- Get detailed pharmacy information
- Power PharmaCo Web and Mobile applications

---

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **MongoDB**
- **Uvicorn**
- **JWT Authentication**

---

## Project Structure

```
app/
├── main.py
├── database/
│   └── mongodb.py
├── models/
├── schemas/
├── routers/
├── services/
├── core/
│   ├── config.py
│   └── security.py
└── utils/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/qinoratech/pharmaco-api.git
cd pharmaco-api
```

---

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
fastapi
uvicorn
python-dotenv
```

---

### Run the Server

```bash
uvicorn app.main:app --reload
```

