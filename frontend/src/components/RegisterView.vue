<template>
  <div>
    <section>
      <div class="container py-3 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-xl-10">
            <div class="card text-black" style="border-radius: 2rem; background-color: #f4f7f3">
              <div class="card-body p-md-5">
                <div class="row justify-content-center">
                  <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                    <p class="text-center h1 fw-bold mb-4 mx-1 mx-md-4">Sign up</p>

                    <form class="mx-1 mx-md-4" @submit.prevent="register">
                      <div class="d-flex flex-row align-items-center mb-2">
                        <div class="form-outline flex-fill mb-0">
                          <input type="text" id="userName" class="form-control" v-model="name" required/>
                          <label class="form-label" for="userName">Name</label>
                        </div>
                      </div>

                      <div class="d-flex flex-row align-items-center mb-4">
                        <div class="form-outline flex-fill mb-0">
                          <input type="email" id="eMail" class="form-control" v-model="email" required/>
                          <label class="form-label" for="eMail">Email</label>
                        </div>
                      </div>

                      <div class="d-flex flex-row align-items-center mb-4">
                        <div class="form-outline flex-fill mb-0">
                          <input
                            type="password"
                            id="passWord"
                            class="form-control"
                            v-model="password"
                            required
                          />
                          <label class="form-label" for="passWord">Password</label>
                        </div>
                      </div>

                      <div class="d-flex flex-row align-items-center mb-4">
                        <div class="form-outline flex-fill mb-0">
                          <select
                            class="form-select mb-1"
                            aria-label="Default select example"
                            v-model="role"
                            required
                          >
                            <option value="none" disabled selected>Role</option>
                            <option value="user">User</option>
                            <option value="manager">Manager</option>
                            <!-- <option value="admin">Admin</option> -->
                          </select>
                          <label class="form-label">Role</label>
                        </div>
                      </div>

                      <div class="form-check mb-5">
                        <input
                          class="form-check-input me-2"
                          type="checkbox"
                          value=""
                          id="form2Example3c"
                        />
                        <label class="form-check-label" for="form2Example3" required>
                          I agree all statements in <a href="#!">Terms of service</a>
                        </label>
                      </div>

                      <div class="d-flex justify-content-center pt-1">
                        <button class="btn btn-dark btn-lg btn-block" type="submit">
                          Register
                        </button>
                      </div>
                    </form>
                  </div>
                  <div
                    class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2"
                  >
                    <img
                      src="https://www.grocersapp.com/blog/wp-content/uploads/2021/01/people-shopping-groceries-online_23-2148530105.jpg"
                      class="img-fluid"
                      alt="Form Image"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      name: '',
      password: '',
      role: ''
    }
  },

  methods: {
    register: async function () {
      if (this.role === 'manager') {
        this.role = 'pending'
      }
      const req = await fetch('http://127.0.0.1:5000/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: this.email,
          name: this.name,
          password: this.password,
          role: this.role
        })
      })

      const res = await req.json()
      if (req.ok) {
        alert("You've Registered Successfully!")
        this.$router.push({ path: '/login' })
      } else {
        alert(res.msg)
      }
    }
  }
}
</script>
