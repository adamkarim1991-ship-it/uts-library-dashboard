```vue
<template>
  <main class="about">
    <p class="eyebrow">LIBRARY MANAGEMENT</p>

    <h1>About Library Dashboard</h1>

    <p>
      Library Dashboard adalah mini dashboard untuk
      mengelola data buku perpustakaan menggunakan Vue 3
      sebagai frontend dan FastAPI sebagai backend.
    </p>

    <RouterLink to="/">
      ← Kembali ke Dashboard
    </RouterLink>
  </main>
</template>

<style scoped>
.about {
  min-height: 100vh;
  padding: 50px 40px;
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

.eyebrow {
  margin: 0 0 8px;
  color: #667085;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

h1 {
  margin: 0 0 16px;
  font-size: 32px;
}

p:not(.eyebrow) {
  max-width: 650px;
  margin-bottom: 24px;
  color: #667085;
  line-height: 1.7;
}

a {
  color: #172033;
  font-weight: 700;
  text-decoration: none;
}
</style>
```
