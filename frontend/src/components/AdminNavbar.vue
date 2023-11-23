<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark" style="min-height: 3rem">
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
            <li class="nav-item">
              <a class="nav-link active" href="/login">Login</a>
            </li>
            <a class="mx-5" href="http://127.0.0.1:5000/download_csv" target="_blank">
              <button class="btn btn-primary" type="button">Download CSV</button>
            </a>
          </ul>

          <!-- <form class="d-flex" role="search">
            <input
              class="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button class="btn btn-dark btn-outline-success" type="submit">
              <fa-icon class="fas fa-search" color="#ffffff" size="1.2rem"></fa-icon>
            </button>
          </form> -->
          <a href="/manager_pending" class="text-white mx-5 position-relative">
            <i class="bi bi-bell-fill" style="font-size: 22px">
              <span
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                style="font-size: 12px; transform: scale(0.8)"
              >
                1
                <span class="visually-hidden">pending requests</span>
              </span>
            </i>
          </a>

          <ul class="navbar-nav" style="margin-right: 3rem">
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
                  <li><a class="dropdown-item" href="/manager_pending">Pending</a></li>
                  <li><a class="dropdown-item" href="/manager_accepted">Accepted</a></li>
                  <li><a class="dropdown-item" href="/manager_rejected">Rejected</a></li>
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
