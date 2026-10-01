from pathlib import Path
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Library Dashboard API",
    description="REST API untuk mini dashboard perpustakaan UTS",
    version="1.0.0",
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# PYDANTIC
# =========================

class BookBase(BaseModel):
    judul: str = Field(..., min_length=1)
    penulis: str = Field(..., min_length=1)
    kategori: str = Field(..., min_length=1)
    stok: int = Field(..., ge=0)


class Book(BookBase):
    id: int


class BookCreate(BookBase):
    pass


# =========================
# SEED DATA
# =========================

SEED_DATA = [
    {
        "id": 1,
        "judul": "Langit di Balik Jendela",
        "penulis": "Arga Pratama",
        "kategori": "Fiksi",
        "stok": 8,
    },
    {
        "id": 2,
        "judul": "Jejak Sang Penjelajah",
        "penulis": "Nadia Putri",
        "kategori": "Petualangan",
        "stok": 5,
    },
    {
        "id": 3,
        "judul": "Belajar Python dari Nol",
        "penulis": "Raka Wijaya",
        "kategori": "Teknologi",
        "stok": 4,
    },
    {
        "id": 4,
        "judul": "Dasar-Dasar Jaringan Komputer",
        "penulis": "Dimas Saputra",
        "kategori": "Teknologi",
        "stok": 2,
    },
    {
        "id": 5,
        "judul": "Misteri Rumah Tua",
        "penulis": "Salsa Maharani",
        "kategori": "Misteri",
        "stok": 0,
    },
    {
        "id": 6,
        "judul": "Pemrograman Web Modern",
        "penulis": "Fajar Nugraha",
        "kategori": "Teknologi",
        "stok": 7,
    },
    {
        "id": 7,
        "judul": "Cerita dari Ujung Kota",
        "penulis": "Alya Ramadhani",
        "kategori": "Fiksi",
        "stok": 3,
    },
    {
        "id": 8,
        "judul": "Pengantar Basis Data",
        "penulis": "Rizky Kurniawan",
        "kategori": "Teknologi",
        "stok": 6,
    },
    {
        "id": 9,
        "judul": "Rahasia Pulau Senja",
        "penulis": "Kevin Mahendra",
        "kategori": "Petualangan",
        "stok": 1,
    },
    {
        "id": 10,
        "judul": "Sejarah Nusantara",
        "penulis": "Bima Adinata",
        "kategori": "Sejarah",
        "stok": 9,
    },
    {
        "id": 11,
        "judul": "Kopi dan Percakapan",
        "penulis": "Nabila Sari",
        "kategori": "Fiksi",
        "stok": 4,
    },
    {
        "id": 12,
        "judul": "Algoritma untuk Pemula",
        "penulis": "Andi Setiawan",
        "kategori": "Teknologi",
        "stok": 3,
    },
    {
        "id": 13,
        "judul": "Perjalanan Menuju Timur",
        "penulis": "Yoga Firmansyah",
        "kategori": "Petualangan",
        "stok": 5,
    },
    {
        "id": 14,
        "judul": "Ensiklopedia Sains Dasar",
        "penulis": "Maya Lestari",
        "kategori": "Sains",
        "stok": 2,
    },
    {
        "id": 15,
        "judul": "Hujan di Bulan November",
        "penulis": "Rani Kusuma",
        "kategori": "Fiksi",
        "stok": 0,
    },
    {
        "id": 16,
        "judul": "Mengenal Dunia Digital",
        "penulis": "Daffa Ramadhan",
        "kategori": "Teknologi",
        "stok": 8,
    },
    {
        "id": 17,
        "judul": "Catatan Seorang Pemimpi",
        "penulis": "Intan Permata",
        "kategori": "Motivasi",
        "stok": 6,
    },
    {
        "id": 18,
        "judul": "Kisah di Balik Perjalanan",
        "penulis": "Farhan Akbar",
        "kategori": "Petualangan",
        "stok": 1,
    },
    {
        "id": 19,
        "judul": "Dunia Ekonomi Sederhana",
        "penulis": "Gilang Prakoso",
        "kategori": "Ekonomi",
        "stok": 4,
    },
    {
        "id": 20,
        "judul": "Membangun Kebiasaan Baik",
        "penulis": "Citra Anggraini",
        "kategori": "Motivasi",
        "stok": 7,
    },
    {
        "id": 21,
        "judul": "Dasar Pemrograman Web",
        "penulis": "Adam",
        "kategori": "Teknologi",
        "stok": 5,
    },
]


# =========================
# LOAD BOOKS
# =========================

BASE_DIR = Path(__file__).resolve().parent
SEED_FILE = BASE_DIR / "books.json"


def load_books():
    if SEED_FILE.exists():
        try:
            with open(SEED_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list) and len(data) > 0:
                return data

        except (json.JSONDecodeError, OSError):
            pass

    return SEED_DATA.copy()


books = load_books()


# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "message": "Library Dashboard API is running",
        "total_books": len(books),
    }


@app.get("/books", response_model=list[Book])
def get_books():
    return books


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Buku tidak ditemukan",
    )


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate):

    new_id = max(
        (item["id"] for item in books),
        default=0,
    ) + 1

    new_book = {
        "id": new_id,
        "judul": book.judul,
        "penulis": book.penulis,
        "kategori": book.kategori,
        "stok": book.stok,
    }

    books.append(new_book)

    return new_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    for index, book in enumerate(books):

        if book["id"] == book_id:

            deleted_book = books.pop(index)

            return {
                "message": "Buku berhasil dihapus",
                "book": deleted_book,
            }

    raise HTTPException(
        status_code=404,
        detail="Buku tidak ditemukan",
    )