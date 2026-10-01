from pydantic import BaseModel


class BookBase(BaseModel):
    judul: str
    penulis: str
    kategori: str
    stok: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int