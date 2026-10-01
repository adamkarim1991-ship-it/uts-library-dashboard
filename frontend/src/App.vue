<template>
  <nav class="navbar">
    <RouterLink to="/">
      Dashboard
    </RouterLink>

    <RouterLink to="/about">
      About
    </RouterLink>
  </nav>

  <RouterView />
</template>

<style scoped>
.navbar {
  display: flex;
  gap: 20px;
  padding: 16px 40px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.navbar a {
  color: #344054;
  text-decoration: none;
  font-weight: 600;
}

.navbar a.router-link-active {
  color: #172033;
  font-weight: 800;
}
</style>