<template>
  <div class="min-vh-100">
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
      // productSalesData: {
      //   "Product1": ["Dairy Products", 234],
      //   "Product2": ["Fruits", 218.35],
      //   "Product3": ["Stationary", 261.35],
      //   "Product4": ["Vegetables", 66.89],
      //   "Product5": ["Dairy Products", 251.3],
      //   "Product6": ["Fruits", 163.75],
      //   "Product7": ["Stationary", 453.6],
      //   "Product8": ["Vegetables", 351.89],
      // },
      productSalesData: {},
      // cardData: {
      //   "Total Users": 23,
      //   "Out of Stock": 10,
      //   "Limited in Stock": 6,
      //   "Total Products": 39,
      //   "Total Sales": 4563
      // }
      cardData: {}
    }
  },
  mounted() {
    this.fetchProductSalesData(), this.fetchCardData()
  },
  methods: {
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
        } else {
          console.log('ERROR!!!')
        }
      } catch (error) {
        console.error('Error fetching product sales data:', error)
      }
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
    },
    getColorForCategory(category) {
      // Define color codes for each category
      const colorCodes = {
        'Dairy Products': 'rgba(255, 99, 132, 0.5)', // Red
        Fruits: 'rgba(255, 205, 86, 0.5)', // Yellow
        Stationary: 'rgba(75, 192, 192, 0.5)', // Teal
        Vegetables: 'rgba(54, 162, 235, 0.5)' // Blue
      }

      // Return the color code for the given category
      return colorCodes[category]
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

