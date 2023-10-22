<template>
  <div>
    <section class="vh-100" style="background-image: url('https://muffingroup.com/blog/wp-content/uploads/2021/03/gr.jpg'); padding-top: 3rem;">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-xl-10">
            <div class="card" style="border-radius: 1rem">
              <div class="row g-0" style="background-color: #F4F7F3;">
                <div class="col-md-6 col-lg-7 d-none d-md-block">
                  <img
                    src="https://www.grocersapp.com/blog/wp-content/uploads/2021/01/people-shopping-groceries-online_23-2148530105.jpg"
                    
                    alt="login form"
                    class="img-fluid"
                    style="padding-top: 8rem;"
                  />
                  <!-- https://cdni.iconscout.com/illustration/premium/thumb/girl-doing-online-grocery-shopping-5713142-4771662.png -->
                </div>
                <div class="col-md-6 col-lg-5 d-flex align-items-center">
                  <div class="card-body p-4 p-lg-5 text-black">
                    <form @submit.prevent="login">
                      <div class="d-flex align-items-center mb-3 pb-1">
                        <img src="../assets/logo_2.png" alt="Logo" class="me-3" style="height: 3rem; width: 1.82rem;">
                        <span class="h1 fw-bold mb-0">SIGN IN</span>
                      </div>

                      <h5 class="fw-normal mb-3 pb-3" style="letter-spacing: 1px">
                        Sign into your account
                      </h5>

                      <div class="form-outline mb-4">
                        <input
                          type="email"
                          id="form2Example17"
                          class="form-control form-control-lg"
                          v-model="email"
                        />
                        <label class="form-label" for="form2Example17">Email address</label>
                      </div>

                      <div class="form-outline mb-4">
                        <input
                          type="password"
                          id="form2Example27"
                          class="form-control form-control-lg"
                          v-model="password"
                        />
                        <label class="form-label" for="form2Example27">Password</label>
                      </div>

                      <div class="pt-1 mb-4">
                        <button class="btn btn-dark btn-lg btn-block" type="submit">Login</button>
                      </div>

                      <a class="small text-muted" href="#!">Forgot password?</a>
                      <p class="mb-5 pb-lg-2" style="color: #393f81">
                        Don't have an account? <a href="#!" style="color: #393f81">Register here</a>
                      </p>
                      <a href="#!" class="small text-muted">Terms of use.</a>
                      <a href="#!" class="small text-muted">Privacy policy</a>
                    </form>
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
      password: ''
    }
  },

  methods: {
    login: async function () {
      const req = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      })

      const res = await req.json()
      if (req.ok) {
        if (res.access_token) {
          localStorage.setItem('accessToken', res.access_token)
          localStorage.setItem('role', res.role)
          alert(res.msg)
          this.$router.push({ path: '/prot' })
        } else {
          alert(res.msg)
        }
      } else {
        alert(res.msg)
      }
    }
  }
}
</script>
