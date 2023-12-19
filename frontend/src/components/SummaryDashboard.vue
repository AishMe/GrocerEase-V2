<template>
  <div class="min-vh-100" style="padding-top: 100px">
    <h1 class="my-5 text-center" style="font-size: 5rem; color: #c1e1c1">
      <strong>Sales Summary Dashboard</strong>
    </h1>
    <div class="card-container flex justify-content-center">
      <!-- Cards -->
      <div v-for="(value, key) in cardData" :key="key" class="card">
        <div class="card-header">{{ key }}</div>
        <div class="card-body fw-bold fs-1">{{ value }}</div>
      </div>
    </div>

    <!-- Bar Chart -->
    <div class="chart-container">
      <canvas ref="salesChart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      productSalesData: {},
      cardData: {},
      categoryColors: {},
      usedColors: new Set() // Set to store used colors
    }
  },
  mounted() {
    this.fetchProductSalesData(), this.fetchCardData()
  },
  created() {
    // Fetch categories when the component is created
    this.fetchCategories()
  },
  methods: {
    async logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('role')
      this.$router.push({ path: '/' }).then(() => {
        this.$router.go()
      })
      alert('User Session Expired. Please Login Again.')
    },
    async fetchCardData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/card_data', {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.cardData = responseData.cardData
        } else if (response.status === 401) {
          this.logout()
        } else {
          console.log('ERROR!!!')
        }
      } catch (error) {
        console.error('Error fetching card data:', error)
      }
    },
    async fetchProductSalesData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/product_sales_data', {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.productSalesData = responseData.productSalesData
          this.renderChart()
        } else if (response.status === 401) {
          this.logout()
        } else {
          console.log('ERROR!!!')
        }
      } catch (error) {
        console.error('Error fetching product sales data:', error)
      }
    },
    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories')
        const data = await response.json()

        // Assign distinct bright colors to each category
        this.categoryColors = data.categories.reduce((colors, category) => {
          colors[category.name] = this.getRandomDistinctBrightColor()
          return colors
        }, {})
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    getColorForCategory(category) {
      // Return the color code for the given category
      return this.categoryColors[category] || this.getRandomDistinctBrightColor()
    },
    getRandomDistinctBrightColor() {
      // Generate a random distinct bright color in rgba format
      const randomHue = () => Math.floor(Math.random() * 80)
      const brightness = 50 // Adjust this value to control brightness
      let newColor

      // Keep generating new colors until a distinct one is found
      do {
        newColor = `hsla(${randomHue()}, 100%, ${brightness}%, 0.5)`
      } while (this.usedColors.has(newColor))

      // Add the new color to the used colors set
      this.usedColors.add(newColor)

      return newColor
    },
    renderChart() {
      const ctx = this.$refs.salesChart.getContext('2d')

      // Extract categories and sales for each product
      const categories = Object.values(this.productSalesData).map((value) => value[0])
      const salesValues = Object.values(this.productSalesData).map((value) => value[1])

      // Extract unique categories
      const uniqueCategories = [...new Set(categories)]

      // Create datasets for each category
      const datasets = uniqueCategories.map((category) => ({
        label: category,
        data: salesValues.map((value, index) => (categories[index] === category ? value : 0)),
        backgroundColor: this.getColorForCategory(category),
        borderWidth: 0
        // barThickness: 40,
      }))

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(this.productSalesData),
          datasets: datasets
        },
        options: {
          scales: {
            x: {
              display: false, // Hide the x-axis labels
              beginAtZero: true,
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                color: 'white'
              }
            }
          },
          indexAxis: 'x',
          barPercentage: 35, // Inc this
          categoryPercentage: 0.1 // And dec this
        }
      })
    }
  }
}
</script>

<style scoped>
/* Dark theme styling */
.card-container {
  display: flex;
}

.card {
  width: 215px;
  height: 150px;
  margin: 10px;
  padding: 10px;
  text-align: center;
  background-color: #333;
  color: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.card-body {
  font-size: 24px;
}

.chart-container {
  width: 80%;
  margin: auto;
}

/* Override Chart.js default styles */
canvas {
  background-color: #333;
}
</style>

