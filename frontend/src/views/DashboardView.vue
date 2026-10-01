```vue
<script setup>
import { computed, onMounted, ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000/books'

const books = ref([])
const loading = ref(false)
const error = ref('')

const searchQuery = ref('')
const sortOrder = ref('az')

const showForm = ref(false)
const submitting = ref(false)
const deletingId = ref(null)

const form = ref({
  judul: '',
  penulis: '',
  kategori: '',
  stok: 0
})

// ====================
// STATISTICS
// ====================

const totalBooks = computed(() => {
  return books.value.length
})

const lowStockBooks = computed(() => {
  return books.value.filter((book) => book.stok >= 1 && book.stok <= 3).length
})

const totalCategories = computed(() => {
  const categories = books.value.map((book) => book.kategori)

  return new Set(categories).size
})

const totalCopies = computed(() => {
  return books.value.reduce((total, book) => {
    return total + book.stok
  }, 0)
})

// ====================
// SEARCH
// ====================

const filteredBooks = computed(() => {
  const keyword = searchQuery.value.toLowerCase().trim()

  if (!keyword) {
    return books.value
  }

  return books.value.filter((book) => {
    return (
      book.judul.toLowerCase().includes(keyword) ||
      book.penulis.toLowerCase().includes(keyword)
    )
  })
})

// ====================
// SORT
// ====================

const sortedBooks = computed(() => {
  return [...filteredBooks.value].sort((a, b) => {
    const titleA = a.judul.toLowerCase()
    const titleB = b.judul.toLowerCase()

    if (sortOrder.value === 'az') {
      return titleA.localeCompare(titleB)
    }

    return titleB.localeCompare(titleA)
  })
})

// ====================
// STOCK STATUS
// ====================

const getStockStatus = (stok) => {
  if (stok === 0) {
    return 'Stok Habis'
  }

  if (stok <= 3) {
    return 'Menipis'
  }

  return 'Tersedia'
}

const getStockClass = (stok) => {
  if (stok === 0) {
    return 'stock-empty'
  }

  if (stok <= 3) {
    return 'stock-low'
  }

  return 'stock-available'
}

// ====================
// GET BOOKS
// ====================

const fetchBooks = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(API_URL)

    if (!response.ok) {
      throw new Error('Gagal mengambil data buku dari server.')
    }

    books.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// ====================
// FORM
// ====================

const resetForm = () => {
  form.value = {
    judul: '',
    penulis: '',
    kategori: '',
    stok: 0
  }
}

const openForm = () => {
  resetForm()
  error.value = ''
  showForm.value = true
}

const closeForm = () => {
  if (submitting.value) {
    return
  }

  showForm.value = false
  resetForm()
}

// ====================
// POST BOOK
// ====================

const addBook = async () => {
  error.value = ''

  if (
    !form.value.judul.trim() ||
    !form.value.penulis.trim() ||
    !form.value.kategori.trim()
  ) {
    error.value = 'Judul, penulis, dan kategori wajib diisi.'
    return
  }

  if (form.value.stok < 0) {
    error.value = 'Stok tidak boleh kurang dari 0.'
    return
  }

  submitting.value = true

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        judul: form.value.judul.trim(),
        penulis: form.value.penulis.trim(),
        kategori: form.value.kategori.trim(),
        stok: Number(form.value.stok)
      })
    })

    if (!response.ok) {
      const data = await response.json().catch(() => null)

      throw new Error(
        data?.detail
          ? JSON.stringify(data.detail)
          : 'Gagal menambahkan buku.'
      )
    }

    showForm.value = false
    resetForm()

    await fetchBooks()
  } catch (err) {
    error.value = err.message
  } finally {
    submitting.value = false
  }
}

// ====================
// DELETE BOOK
// ====================

const deleteBook = async (bookId) => {
  const confirmed = window.confirm(
    'Apakah kamu yakin ingin menghapus buku ini?'
  )

  if (!confirmed) {
    return
  }

  error.value = ''
  deletingId.value = bookId

  try {
    const response = await fetch(`${API_URL}/${bookId}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Gagal menghapus buku.')
    }

    await fetchBooks()
  } catch (err) {
    error.value = err.message
  } finally {
    deletingId.value = null
  }
}

// ====================
// INITIAL LOAD
// ====================

onMounted(() => {
  fetchBooks()
})
</script>

<template>
  <main class="dashboard">

    <!-- HEADER -->
    <header class="header">
      <div>
        <p class="eyebrow">LIBRARY MANAGEMENT</p>
        <h1>Library Dashboard</h1>
        <p class="subtitle">
          Kelola koleksi buku perpustakaan dengan mudah.
        </p>
      </div>

      <button class="add-button" @click="openForm">
        + Tambah Buku
      </button>
    </header>

    <!-- ERROR -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="state-message">
      Loading data buku...
    </div>

    <!-- DASHBOARD -->
    <template v-else>

      <!-- STATISTICS -->
      <section class="stats">
        <div class="stat-card">
          <span class="stat-label">Total Buku</span>
          <strong class="stat-value">{{ totalBooks }}</strong>
        </div>

        <div class="stat-card">
          <span class="stat-label">Menipis + Habis</span>
          <strong class="stat-value">{{ lowStockBooks }}</strong>
        </div>

        <div class="stat-card">
          <span class="stat-label">Jumlah Kategori</span>
          <strong class="stat-value">{{ totalCategories }}</strong>
        </div>

        <div class="stat-card">
          <span class="stat-label">Total Eksemplar</span>
          <strong class="stat-value">{{ totalCopies }}</strong>
        </div>
      </section>

      <!-- TOOLBAR -->
      <section class="toolbar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari judul atau penulis..."
          class="search-input"
        />

        <div class="sort-buttons">
          <button
            :class="{ active: sortOrder === 'az' }"
            @click="sortOrder = 'az'"
          >
            A-Z
          </button>

          <button
            :class="{ active: sortOrder === 'za' }"
            @click="sortOrder = 'za'"
          >
            Z-A
          </button>
        </div>
      </section>

      <!-- EMPTY DATA -->
      <div v-if="books.length === 0" class="empty-state">
        <h2>Belum ada buku</h2>
        <p>Tambahkan buku pertama ke perpustakaan.</p>

        <button class="add-button" @click="openForm">
          + Tambah Buku
        </button>
      </div>

      <!-- SEARCH EMPTY -->
      <div
        v-else-if="sortedBooks.length === 0"
        class="empty-state"
      >
        <h2>Buku tidak ditemukan</h2>
        <p>Coba gunakan kata kunci pencarian yang berbeda.</p>
      </div>

      <!-- BOOK TABLE -->
      <section v-else class="book-section">

        <div class="section-header">
          <div>
            <h2>Daftar Buku</h2>
            <p>{{ sortedBooks.length }} buku ditampilkan</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Judul</th>
                <th>Penulis</th>
                <th>Kategori</th>
                <th>Stok</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="book in sortedBooks"
                :key="book.id"
              >
                <td>#{{ book.id }}</td>

                <td class="book-title">
                  {{ book.judul }}
                </td>

                <td>
                  {{ book.penulis }}
                </td>

                <td>
                  <span class="category">
                    {{ book.kategori }}
                  </span>
                </td>

                <td>
                  {{ book.stok }}
                </td>

                <td>
                  <span
                    class="stock-badge"
                    :class="getStockClass(book.stok)"
                  >
                    {{ getStockStatus(book.stok) }}
                  </span>
                </td>

                <td>
                  <button
                    class="delete-button"
                    :disabled="deletingId === book.id"
                    @click="deleteBook(book.id)"
                  >
                    {{
                      deletingId === book.id
                        ? 'Menghapus...'
                        : 'Hapus'
                    }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </section>
    </template>

    <!-- ADD BOOK MODAL -->
    <div
      v-if="showForm"
      class="modal-overlay"
      @click.self="closeForm"
    >
      <div class="modal">

        <div class="modal-header">
          <div>
            <p class="eyebrow">NEW BOOK</p>
            <h2>Tambah Buku</h2>
          </div>

          <button
            class="close-button"
            :disabled="submitting"
            @click="closeForm"
          >
            ×
          </button>
        </div>

        <form @submit.prevent="addBook">

          <label>
            Judul
            <input
              v-model="form.judul"
              type="text"
              placeholder="Masukkan judul buku"
              required
            />
          </label>

          <label>
            Penulis
            <input
              v-model="form.penulis"
              type="text"
              placeholder="Masukkan nama penulis"
              required
            />
          </label>

          <label>
            Kategori
            <input
              v-model="form.kategori"
              type="text"
              placeholder="Contoh: Fiksi"
              required
            />
          </label>

          <label>
            Stok
            <input
              v-model.number="form.stok"
              type="number"
              min="0"
              placeholder="0"
              required
            />
          </label>

          <div class="form-actions">
            <button
              type="button"
              class="cancel-button"
              :disabled="submitting"
              @click="closeForm"
            >
              Batal
            </button>

            <button
              type="submit"
              class="add-button"
              :disabled="submitting"
            >
              {{
                submitting
                  ? 'Menyimpan...'
                  : 'Simpan Buku'
              }}
            </button>
          </div>

        </form>
      </div>
    </div>

  </main>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard {
  min-height: 100vh;
  padding: 40px;
  background: #f5f7fb;
  color: #172033;
  font-family:
    Inter,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}

/* HEADER */

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 32px;
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #667085;
}

h1 {
  margin: 0;
  font-size: 34px;
  line-height: 1.2;
}

.subtitle {
  margin: 8px 0 0;
  color: #667085;
}

/* BUTTON */

button {
  border: 0;
  cursor: pointer;
  font: inherit;
}

.add-button {
  padding: 12px 18px;
  border-radius: 10px;
  background: #172033;
  color: white;
  font-weight: 700;
}

.add-button:hover {
  opacity: 0.9;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* ERROR */

.error-message {
  margin-bottom: 20px;
  padding: 14px 16px;
  border: 1px solid #fecaca;
  border-radius: 10px;
  background: #fef2f2;
  color: #b42318;
}

.state-message {
  padding: 60px 20px;
  text-align: center;
  color: #667085;
}

/* STATISTICS */

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.stat-card {
  padding: 22px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: white;
  box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
}

.stat-label {
  display: block;
  margin-bottom: 12px;
  color: #667085;
  font-size: 14px;
}

.stat-value {
  font-size: 30px;
}

/* TOOLBAR */

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  min-width: 0;
  padding: 13px 15px;
  border: 1px solid #d0d5dd;
  border-radius: 10px;
  outline: none;
  background: white;
  font: inherit;
}

.search-input:focus {
  border-color: #667085;
}

.sort-buttons {
  display: flex;
  gap: 8px;
}

.sort-buttons button {
  padding: 12px 16px;
  border: 1px solid #d0d5dd;
  border-radius: 10px;
  background: white;
  color: #344054;
}

.sort-buttons button.active {
  background: #172033;
  color: white;
}

/* TABLE */

.book-section {
  overflow: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: white;
  box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
}

.section-header {
  padding: 22px;
  border-bottom: 1px solid #eaecf0;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
}

.section-header p {
  margin: 5px 0 0;
  color: #667085;
  font-size: 14px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 15px 18px;
  border-bottom: 1px solid #eaecf0;
  text-align: left;
  white-space: nowrap;
}

th {
  background: #f9fafb;
  color: #667085;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

td {
  font-size: 14px;
}

tbody tr:last-child td {
  border-bottom: 0;
}

.book-title {
  min-width: 220px;
  font-weight: 700;
}

.category {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 999px;
  background: #f2f4f7;
  color: #344054;
  font-size: 12px;
  font-weight: 600;
}

/* STOCK */

.stock-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.stock-available {
  background: #ecfdf3;
  color: #027a48;
}

.stock-low {
  background: #fffaeb;
  color: #b54708;
}

.stock-empty {
  background: #fef3f2;
  color: #b42318;
}

/* DELETE */

.delete-button {
  padding: 7px 11px;
  border-radius: 8px;
  background: #fef2f2;
  color: #b42318;
  font-size: 13px;
  font-weight: 700;
}

.delete-button:hover {
  background: #fee4e2;
}

/* EMPTY */

.empty-state {
  padding: 70px 20px;
  border: 1px dashed #d0d5dd;
  border-radius: 14px;
  background: white;
  text-align: center;
}

.empty-state h2 {
  margin: 0 0 8px;
}

.empty-state p {
  margin: 0 0 20px;
  color: #667085;
}

/* MODAL */

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(16, 24, 40, 0.55);
}

.modal {
  width: min(520px, 100%);
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 20px 50px rgba(16, 24, 40, 0.2);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
}

.close-button {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #f2f4f7;
  color: #344054;
  font-size: 24px;
  line-height: 1;
}

form {
  display: grid;
  gap: 16px;
}

label {
  display: grid;
  gap: 7px;
  color: #344054;
  font-size: 14px;
  font-weight: 600;
}

label input {
  width: 100%;
  padding: 12px 13px;
  border: 1px solid #d0d5dd;
  border-radius: 9px;
  outline: none;
  font: inherit;
  font-weight: 400;
}

label input:focus {
  border-color: #667085;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.cancel-button {
  padding: 12px 18px;
  border-radius: 10px;
  background: #f2f4f7;
  color: #344054;
  font-weight: 700;
}

/* RESPONSIVE */

@media (max-width: 1023px) {
  .dashboard {
    padding: 28px;
  }

  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .dashboard {
    padding: 20px 14px;
  }

  .header {
    align-items: flex-start;
    flex-direction: column;
  }

  h1 {
    font-size: 28px;
  }

  .add-button {
    width: 100%;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .toolbar {
    align-items: stretch;
    flex-direction: column;
  }

  .sort-buttons {
    width: 100%;
  }

  .sort-buttons button {
    flex: 1;
  }

  .modal {
    padding: 20px;
  }
}
</style>
```
