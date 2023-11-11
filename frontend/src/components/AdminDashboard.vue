<template>
  <div>
    <div class="fab">
      <a href="#" @click="addCategory">
        <i class="fa fa-plus"></i>
      </a>
    </div>

    <div class="row">
      <div v-for="(category, index) in categories" :key="index" class="col-md-4 d-flex justify-content-center">
        <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem;">
          <img
            :src="category.cat_image ? category.cat_image : require('@/assets/images/Logo.png')"
            :alt="category.name + ' Image'"
            style="width: 100%; height: 10vw; object-fit: cover;"
            class="card-img-top"
          />
          <div class="card-body">
            <center><h3 style="color: black">{{ category.name }}</h3></center>

            <div class="overflow-auto" style="height: 400px;">
              <div v-for="product in productsByCategory[category.section_id]" :key="product.product_id" class="card mb-2 shadow p-3 mb-5 rounded" style="width: 310px;">
                <img
                  :src="product.image ? product.image : require('@/assets/images/Logo.png')"
                  :alt="product.name + ' Image'"
                  style="width: 100%; height: 7vw; object-fit: cover;"
                  class="card-img-top"
                />
                <div class="card-body">
                  <center><h5 class="card-title" style="color: black">{{ product.name }}</h5></center>
                  <hr style="margin-top: 1rem; border: 1px solid black;" />
                  <p class="card-text">
                    Manufacturing Date: {{ product.manufacture_date }}<br/>
                    Rate per unit: Rs.{{ product.rate_per_unit }}/{{ product.unit }}<br/>
                    Stock: {{ product.stock }}
                  </p>
                  <div class="d-flex justify-content-center align-items-center">
                    <a href="#" @click="updateProduct(product.product_id)"><button class="btn btn-outline-warning"><i class="fa fa-pencil"></i>Edit</button></a>
                    <span style="flex-grow: 0.5;"></span>
                    <a href="#" @click="deleteProduct(product.product_id)"><button class="btn btn-outline-danger"><i class="fa fa-trash"></i>Delete</button></a>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <br/>
              <div class="d-flex justify-content-between">
                <a href="#" @click="addProduct(category.section_id)"><button class="btn btn-outline-primary"><i class="fa fa-plus-circle"></i>Add Items</button></a>
                <span style="flex-grow: 1;"></span>
                <a href="#" @click="updateCategory(category.section_id)"><button class="btn btn-outline-warning"><i class="fa fa-pencil"></i></button></a>
                <span style="flex-grow: 0.3;"></span>
                <a href="#" @click="deleteCategory(category.section_id)"><button class="btn btn-outline-danger"><i class="fa fa-trash"></i></button></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
  return {
    categories: [
      {
        name: "Category 1",
        cat_image: "https://images2.alphacoders.com/128/1284104.jpg",
        section_id: 1,
      },
      {
        name: "Category 2",
        cat_image: "https://images2.alphacoders.com/128/1284104.jpg",
        section_id: 2,
      },
      {
        name: "Category 3",
        cat_image: "https://images2.alphacoders.com/128/1284104.jpg",
        section_id: 3,
      },
      {
        name: "Category 4",
        cat_image: "https://images2.alphacoders.com/128/1284104.jpg",
        section_id: 4,
      },
    ],// Add more categories as needed
    productsByCategory: {
      1: [
        {
          name: "Product 1",
          image: "product1.jpg",
          manufacture_date: "2023-01-01",
          rate_per_unit: 10,
          unit: "unit",
          stock: 100,
          product_id: 1,
        },
        {
          name: "Product 2",
          image: "product2.jpg",
          manufacture_date: "2023-02-01",
          rate_per_unit: 15,
          unit: "unit",
          stock: 150,
          product_id: 2,
        },
      ],// Add more products to category 1
      2: [
        {
          name: "Product 3",
          image: "product3.jpg",
          manufacture_date: "2023-03-01",
          rate_per_unit: 20,
          unit: "unit",
          stock: 200,
          product_id: 3,
        },
        {
          name: "Product 4",
          image: "product4.jpg",
          manufacture_date: "2023-04-01",
          rate_per_unit: 25,
          unit: "unit",
          stock: 250,
          product_id: 4,
        },
      ],// Add more products to category 2

      3: [
        {
          name: "Product 5",
          image: "product5.jpg",
          manufacture_date: "2023-05-01",
          rate_per_unit: 30,
          unit: "unit",
          stock: 300,
          product_id: 5,
        },
        {
          name: "Product 6",
          image: "product6.jpg",
          manufacture_date: "2023-06-01",
          rate_per_unit: 35,
          unit: "unit",
          stock: 350,
          product_id: 6,
        },
      ],// Add more products to category 3
      4: [
        {
          name: "Product 7",
          image: "product7.jpg",
          manufacture_date: "2023-07-01",
          rate_per_unit: 40,
          unit: "unit",
          stock: 400,
          product_id: 7,
        },
        {
          name: "Product 8",
          image: "product8.jpg",
          manufacture_date: "2023-08-01",
          rate_per_unit: 45,
          unit: "unit",
          stock: 450,
          product_id: 8,
        },
      ],// Add more products to category 4]
    }}},
  methods: {
    addCategory() {
      // Logic to add a new category
    },
    deleteCategory(sectionId) {
      // Logic to delete the category based on sectionId
    },
    updateCategory(sectionId) {
      // Logic to update the category based on sectionId
    },
    addProduct(sectionId) {
      // Logic to add a new product to the given sectionId
    },
    deleteProduct(productId) {
      // Logic to delete the product based on productId
    },
    updateProduct(productId) {
      // Logic to update the product based on productId
    },
  }
}
</script>

