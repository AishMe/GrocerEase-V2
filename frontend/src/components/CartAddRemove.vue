<template>
  <div v-if="product" class="input-group plus-minus">
    <button
      class="btn btn-outline-secondary"
      :class="loading ? 'disabled' : ''"
      @click="addOrRemove(-1)"
      type="button"
      id="button-addon1"
    >
      -
    </button>
    <input
      type="number"
      v-model="qty"
      disabled
      class="form-control form-control-sm"
      placeholder=""
      aria-label="Example text with button addon"
      aria-describedby="button-addon1"
    />
    <button
      class="btn btn-outline-secondary"
      :class="loading ? 'disabled' : ''"
      @click="addOrRemove(1)"
      type="button"
      id="button-addon1"
    >
      +
    </button>
  </div>
</template>
<script>
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
export default {
  name: 'CartAddRemove',
  props: ['product'],
  data() {
    return {
      loading: false,
      qty: this.product.qty || 1, // Set the initial quantity to the product's quantity or 1
    }
  },
  methods: {
    async addOrRemove(number){
            this.loading = true
            if(number == 1){ //add
                if(this.qty < this.product.stock){
                    this.qty++
                    this.product.qty = this.qty
                    await this.$store.commit('updateCart',{product:this.product})
                    toast.success('cart updated')
                }else{
                    toast.warning('You reached the limit')
                }
            }
            if( number == -1){ //remove
                if(this.qty > 1){
                    this.qty--
                    this.product.qty = this.qty
                    await this.$store.commit('updateCart',{product:this.product})
                    toast.success('cart updated');
                }else{
                    toast.warning('You reached the limit');  
                }
            }

            this.loading = false
        }
  },
  mounted() {
    this.qty = this.product.qty || 1;
  }
}
</script>
<style>
.plus-minus input {
  max-width: 50px;
}
</style>
