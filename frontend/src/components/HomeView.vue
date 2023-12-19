 <template>
  <div class="position-relative" style="height: 100vh">
    <Transition name="fade" appear>
      <img
        class="mx-auto"
        v-if="showImage"
        :src="image"
        alt="Your Image"
        style="height: 100%; width: 100%"
      />
    </Transition>
    <div class="button-container">
      <Transition name="bounce" appear>
        <button v-if="showButton" @click="redirectToLogin" class="shop-button">SHOP NOW</button>
      </Transition>
    </div>
  </div>
</template>

<script>
import entryPage from '../assets/entryPage.png'
export default {
  data() {
    return {
      image: entryPage,
      showImage: false,
      showText: false,
      showButton: false
    }
  },
  mounted() {
    setTimeout(() => {
      this.showImage = true
      setTimeout(() => {
        this.showText = true
        setTimeout(() => {
          this.showButton = true
        }, 1000)
      }, 1000)
    }, 200)
  },
  methods: {
    redirectToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style>
/* Add your existing CSS styles here */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.8s;
}

.bounce-leave-active {
  animation: bounce-in 0.8s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

.button-container {
  position: absolute;
  top: 35%;
  left: 51%;
  transform: translate(-50%, -50%);
}

.shop-button {
  background-color: #c1e1c1;
  color: #1f1f1f;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 30px;
  font-weight: bolder;
}

.shop-button:hover {
  background-color: #9ecf9e;
}
</style>
