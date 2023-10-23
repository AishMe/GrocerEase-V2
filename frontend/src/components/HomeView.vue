<template>
  <div style="background-color: #3a915d; height: 100vh">
    <div class="flex justify-content-center align-items-center">
      <div class="text-center pt-2">
        <transition name="fade" mode="out-in">
          <div :key="currentImage">
            <img class="mx-auto" :src="currentImage" style="height: 70%; width: 70%" />
          </div>
        </transition>
      </div>

      <transition name="fade" mode="out-in" v-if="showButton">
        <div key="button" class="text-center mb-4 font">
          <a class="btn btn-dark btn-lg px-4 py-2" type="button" href="/login">Shop Now</a>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import FrontPageDesign from '../assets/FrontPageDesign.png'
import FrontPageDesign2 from '../assets/FrontPageDesign2.png'

export default {
  data() {
    return {
      currentImage: FrontPageDesign,
      showButton: false
    }
  },
  mounted() {
    // Timer to change the image after 3 seconds
    setTimeout(() => {
      this.currentImage = FrontPageDesign2

      // Timer to show the button after image replacement
      setTimeout(() => {
        this.showButton = true
      }, 1000) // Adjust the delay as needed
    }, 1500) // Adjust the delay as needed
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
