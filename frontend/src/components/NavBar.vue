<template>
  <div>
    <nav class="navbar navbar-expand-xl fixed-top" data-bs-theme="dark" style="min-height: 7rem">
      <div class="container-fluid">
        <a
          class="navbar-brand"
          href="/home"
          style="padding: 0 15px; font-size: x-large; font-weight: 600"
          >GrocerEase</a
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          class="collapse navbar-collapse"
          id="navbarSupportedContent"
          style="font-size: larger; font-weight: 500"
        >
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" href="/dashboard">Dashboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="/register">Register</a>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input
              class="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button class="btn btn-dark btn-outline-success" type="submit">
              <fa-icon class="fas fa-search" color="#ffffff" size="1.2rem"></fa-icon>
            </button>
          </form>
          <ul class="navbar-nav" style="margin-left: 5rem; margin-right: 3rem">
            <li class="nav-item">
              <div class="dropdown">
                <button
                  class="btn dropdown-toggle"
                  type="button"
                  id="dropdownMenuButton1"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <img
                    src="https://creazilla-store.fra1.digitaloceanspaces.com/icons/7914927/man-icon-md.png"
                    alt="avatar"
                    style="height: 2.5rem; width: 2.5rem; border-radius: 50%"
                  />
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                  <li><a class="dropdown-item" href="/profile">Profile</a></li>
                  <li><a class="dropdown-item" href="#">Cart</a></li>
                  <li><a class="dropdown-item" href="#">Orders</a></li>
                  <li><a class="dropdown-item" href="/login">Login</a></li>
                  <li>
                    <a class="dropdown-item" style="cursor: pointer" @click="logout">Logout</a>
                  </li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  methods: {
    logout: function () {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('role')
      this.$router.push({ path: '/home' })
      alert('Successfully Logged Out!')
    }
  }
}
</script>
