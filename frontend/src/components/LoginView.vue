<template>
  <div>
    <section>
      <div class="container h-100 mb-5" style="padding-top: 125px">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-xl-10">
            <div class="card" style="border-radius: 2rem; background-color: #f4f7f3">
              <div class="row g-0">
                <div class="col-md-6 col-lg-7 d-none d-md-block">
                  <img
                    src="https://www.grocersapp.com/blog/wp-content/uploads/2021/01/people-shopping-groceries-online_23-2148530105.jpg"
                    alt="login form"
                    class="img-fluid"
                    style="padding-top: 8rem"
                  />
                </div>
                <div class="col-md-6 col-lg-5 d-flex align-items-center">
                  <div class="card-body p-4 p-lg-5 text-black">
                    <form @submit.prevent="login">
                      <div class="d-flex align-items-center mb-3 pb-1">
                        <span class="h1 fw-bold mb-0">Sign in</span>
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
                          required
                        />
                        <label class="form-label" for="form2Example17">Email address</label>
                      </div>

                      <div class="form-outline mb-4">
                        <input
                          type="password"
                          id="form2Example27"
                          class="form-control form-control-lg"
                          v-model="password"
                          required
                        />
                        <label class="form-label" for="form2Example27">Password</label>
                      </div>

                      <div class="pt-1 mb-4">
                        <button class="btn btn-dark btn-lg btn-block" type="submit">Login</button>
                      </div>

                      <a class="small text-muted" @click="showPasswordResetForm"
                        >Forgot password?</a
                      >
                      <p class="mb-5 pb-lg-2" style="color: #393f81">
                        Don't have an account?
                        <a href="/register" style="color: #393f81">Register here</a>
                      </p>
                      <a href="#!" class="small text-muted">Terms of use</a>
                      <span> | </span>
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
    <section>
      <!-- Password Reset Form -->
      <div v-if="showPasswordFormBool" class="form-container">
        <div class="form card">
          <div class="card-header">
            <h5 class="mb-0">Password Reset Form</h5>
          </div>
          <form @submit.prevent="resetPassword">
            <div class="card-body">
              <div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email ID</label>
                  <input
                    type="text"
                    class="form-control"
                    id="email"
                    v-model="email"
                    placeholder="Enter Your Email-ID"
                    required
                  />
                </div>
              </div>
              <div>
                <div class="mb-3">
                  <label for="newPassword" class="form-label">New Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="newPassword"
                    v-model="newPassword"
                    placeholder="Enter Your New Password"
                    required
                  />
                </div>
              </div>
              <div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="confirmPassword"
                    v-model="confirmPassword"
                    placeholder="Confirm Your New Password"
                    required
                  />
                </div>
              </div>
              <br />

              <!-- Submit and Cancel Buttons -->
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-success">Done</button>
                <button @click.prevent="cancelPasswordReset" class="btn btn-secondary">
                  Cancel
                </button>
              </div>
            </div>
          </form>
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
      password: '',
      showPasswordFormBool: false,
      newPassword: '',
      confirmPassword: ''
    }
  },

  methods: {
    login: async function () {
      const req = await fetch('http://127.0.0.1:5000/api/user/login', {
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
          this.$router.push({ path: '/dashboard' }).then(() => {
            this.$router.go()
          })
        } else {
          alert('Login Failed. Please Try Again.')
        }
      } else {
        alert('Login Failed. Please Try Again.')
      }
    },
    async resetPassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert('Password doesnot match. Confirm the new password again.')
      } else {
        await fetch(`http://127.0.0.1:5000/api/user/reset_password_request`, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({ email: this.email, password: this.newPassword })
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Resetting password failed')
            }
            return response.json()
          })
          .then((data) => {
            console.log('password reset successful:', data.message)
            this.cancelPasswordReset()
            alert(data.message)
          })
          .catch((error) => {
            // Handle password reset failure
            console.error('Error resetting the password:', error)
          })
      }
    },
    // Cancel password reset form
    cancelPasswordReset() {
      this.showPasswordFormBool = false
      this.newPassword = ''
      this.confirmPassword = ''
    },
    showPasswordResetForm() {
      this.showPasswordFormBool = true
    }
  }
}
</script>

<style scoped>
.form-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(50px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.form {
  width: 400px;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
}
</style>
