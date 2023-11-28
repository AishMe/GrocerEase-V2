<template>
  <div>
    <nav class="navbar navbar-expand-xl bg-dark" data-bs-theme="dark" style="min-height: 6rem">
      <div class="container-fluid">
        <a
          class="navbar-brand"
          href="/"
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
          style="font-size: x-large; font-weight: 500"
        >
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" href="/dashboard">Dashboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="/register">Register</a>
            </li>
          </ul>

          <a href="/cart" class="text-white mt-2 position-relative">
            <i class="bi bi-cart4" style="font-size: 35px">
              <span
                v-if="$store.state.cart.length > 0"
                class="position-absolute top-0 start-80 mt-2 translate-middle badge rounded-pill bg-warning text-black"
                style="font-size: 13px; transform: scale(0.8)"
              >
                {{ $store.state.cart.length }}
                <span class="visually-hidden">cart items</span>
              </span>
            </i>
          </a>

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
                    style="height: 3.5rem; width: 3.5rem; border-radius: 50%"
                  />
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                  <li><a class="dropdown-item" href="/profile">Profile</a></li>
                  <li><a class="dropdown-item" href="/cart">Cart</a></li>
                  <li><a class="dropdown-item" href="/orders">Orders</a></li>
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
      this.$router.push({ path: '/' })
      alert('Successfully Logged Out!')
    }
  }
}
</script>
