# PBL0602 — Web Service Car CRUD (REST API)

## Framework
**Python[1]** — Flask

## Deskripsi
REST API CRUD data mobil menggunakan Flask dan SQLite (`carsweb.db`). Semua response dalam format JSON.

## Database: carsweb.db
Tabel: `tbcars (id, carname, carbrand, carmodel, carprice)`

## Instalasi
```bash
cd pbl0602-webservice-car
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Run
```bash
python app.py
```
Server: `http://localhost:5002`

## Endpoint REST

| Method | Route | Fungsi | Response |
|---|---|---|---|
| GET | `/api/cars` | List semua mobil | `200` JSON array |
| GET | `/api/cars/<id>` | Detail 1 mobil | `200` / `404` |
| POST | `/api/cars` | Tambah mobil | `201` |
| PUT | `/api/cars/<id>` | Update mobil | `200` / `404` |
| DELETE | `/api/cars/<id>` | Hapus mobil | `200` / `404` |
| GET | `/api/cars/search?q=` | Cari mobil | `200` |

## Contoh curl

```bash
# List
curl http://localhost:5002/api/cars

# Create
curl -X POST http://localhost:5002/api/cars -H "Content-Type: application/json" \
  -d '{"carname":"Blue Sedan","carbrand":"Toyota","carmodel":"Camry","carprice":"300000"}'

# Update
curl -X PUT http://localhost:5002/api/cars/1 -H "Content-Type: application/json" \
  -d '{"carname":"Red Sports","carbrand":"Ferrari","carmodel":"F40","carprice":"500000"}'

# Delete
curl -X DELETE http://localhost:5002/api/cars/1

# Search
curl "http://localhost:5002/api/cars/search?q=Toyota"
```
