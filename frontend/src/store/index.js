import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: [],
    cartTotal: 0,
    notificationCount: 0,
  },
  mutations: {
    async initialiseStore(state) {
      if(localStorage.getItem('cart')){
       state.cart = JSON.parse(localStorage.getItem('cart'))
       console.log(localStorage.getItem('cart'))
      }
      if(localStorage.getItem('cartTotal')){
      state.cartTotal = parseFloat(localStorage.getItem('cartTotal')) 
      }
      return true;
    },
    addRemoveCart(state, payload){
      payload.toAdd?
      state.cart.push(payload.product) :
      state.cart = state.cart.filter(function(obj){
        return obj.id !== payload.product.id
      });
      state.cartTotal = state.cart.reduce((accumulator, object)=>{
        console.log("OBJECT PRICE: ", object.price)
        return parseFloat(accumulator) + parseFloat(object.price * object.qty);
      },0);
      localStorage.setItem('cartTotal',JSON.stringify(state.cartTotal));
      localStorage.setItem('cart',JSON.stringify(state.cart));

      console.log(state.cartTotal)
      console.log(state.cart)
    },
    updateCart(state,payload){
      state.cart.find(o => o.id === payload.product.id).qty = payload.product.qty;
      state.cartTotal = state.cart.reduce((accumulator, object)=>{
        return parseFloat(accumulator) + parseFloat(object.price * object.qty);
      },0);
      localStorage.setItem('cartTotal',JSON.stringify(state.cartTotal));
      localStorage.setItem('cart',JSON.stringify(state.cart));
    },
    setCart(state, cartData) {
      state.cart = cartData;
    },
    setCartTotal(state, total) {
      state.cartTotal = total;
    },
    setNotificationCount(state, count) {
      state.notificationCount = count;
    },
    incrementNotificationCount(state) {
      state.notificationCount++;
    },
    decrementNotificationCount(state) {
      state.notificationCount--;
    },
  },
  actions: {
    clearCart({ commit }) {
      commit('setCart', []); // Clear the cart
      commit('setCartTotal', 0); // Reset the total
      localStorage.removeItem('cart'); // Remove cart from localStorage
      localStorage.removeItem('cartTotal'); // Remove cartTotal from localStorage
    },
    async updateCartInStore({ commit, state }, payload) {
      // Find the index of the product in the cart
      const productIndex = state.cart.findIndex(item => item.id === payload.product.id);
  
      // Update the cart based on the action (add or remove)
      if (payload.product.qty > 0) {
        if (productIndex !== -1) {
          // Update quantity if the product is already in the cart
          state.cart[productIndex].qty = payload.product.qty;
        } else {
          // Add the product to the cart if not already present
          state.cart.push(payload.product);
        }
      } else {
        // Remove the product from the cart if quantity is zero
        state.cart.splice(productIndex, 1);
      }
  
      // Recalculate cart total
      const cartTotal = state.cart.reduce((total, item) => total + item.price * item.qty, 0);
      commit('setCart', state.cart); // Commit mutation to update the cart state
      commit('setCartTotal', cartTotal); // If you have a mutation for total, use it
  
      // Save the updated cart to localStorage if needed
      localStorage.setItem('cart', JSON.stringify(state.cart));
      localStorage.setItem('cartTotal', JSON.stringify(cartTotal));
    },
  },
  modules: {},
})