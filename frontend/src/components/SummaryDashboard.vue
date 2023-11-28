<template>
    <div>This this the Summary Page</div>
</template>


<!-- <template>
    <div id="wrapper">
      <div class="content-area">
        <div class="container-fluid">
  
          <div class="main">
 
            <div class="row sparkboxes mt-4">

              <div class="col-md-3">
                <div class="box box1">
                  <div class="details">
                    <h3>1213</h3>
                    <h4>CLICKS</h4>
                  </div>
                  <div ref="spark1"></div>
                </div>
              </div>

              <div class="col-md-3">
                <div class="box box2">
                  <div class="details">
                    <h3>422</h3>
                    <h4>VIEWS</h4>
                  </div>
                  <div ref="spark2"></div>
                </div>
              </div>
      
              <div class="col-md-3">
                <div class="box box3">
                  <div class="details">
                    <h3>311</h3>
                    <h4>LEADS</h4>
                  </div>
                  <div ref="spark3"></div>
                </div>
              </div>
 
              <div class="col-md-3">
                <div class="box box4">
                  <div class="details">
                    <h3>22</h3>
                    <h4>SALES</h4>
                  </div>
                  <div ref="spark4"></div>
                </div>
              </div>
            </div>
  
   
            <div class="row mt-4">

              <div class="col-md-5">
                <div class="box shadow mt-4">
                  <div ref="lineChart"></div>
                </div>
              </div>
 
              <div class="col-md-7">
                <div class="box shadow mt-4">
                  <div ref="radialBarChart"></div>
                </div>
              </div>
            </div>
  
            
            <div class="row mt-4">
    
              <div class="col-md-5">
                <div class="box shadow mt-4">
                  <div ref="barChart"></div>
                </div>
              </div>

              <div class="col-md-7">
                <div class="box shadow mt-4">
                  <div ref="areaChart"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import VueApexCharts from "vue-apexcharts";
  import "apexcharts/dist/apexcharts.css";
  
  
  export default {
    components: {
    apexchart: VueApexCharts,
  },
    mounted() {
      // Sparkboxes
      this.renderSparkChart("spark1", spark1);
      this.renderSparkChart("spark2", spark2);
      this.renderSparkChart("spark3", spark3);
      this.renderSparkChart("spark4", spark4);
  
      // Line Chart
      this.renderApexChart("lineChart", optionsLine);
  
      // RadialBar Chart
      this.renderApexChart("radialBarChart", optionsCircle4);
  
      // Bar Chart
      this.renderApexChart("barChart", optionsBar);
  
      // Area Chart
      this.renderApexChart("areaChart", optionsArea);
    },
    methods: {
      renderSparkChart(id, options) {
        new ApexCharts(this.$refs[id], options).render();
      },
      renderApexChart(id, options) {
        new ApexCharts(this.$refs[id], options).render();
      },
    },
  };
  </script>
  
  <style scoped>
.sparkboxes .box {
  padding-top: 10px;
  padding-bottom: 10px;
  text-shadow: 0 1px 1px 1px #666;
  box-shadow: 0px 1px 15px 1px rgba(69, 65, 78, 0.08);
  position: relative;
  border-radius: 5px;
}

.sparkboxes .box .details {
  position: absolute;
  color: #fff;
  transform: scale(0.7) translate(-22px, 20px);
}
.sparkboxes strong {
  position: relative;
  z-index: 3;
  top: -8px;
  color: #fff;
}


.sparkboxes .box1 {
  background-image: linear-gradient( 135deg, #ABDCFF 10%, #0396FF 100%);
}

.sparkboxes .box2 {
  background-image: linear-gradient( 135deg, #2AFADF 10%, #4C83FF 100%);
}

.sparkboxes .box3 {
  background-image: linear-gradient( 135deg, #FFD3A5 10%, #FD6585 100%);
}

.sparkboxes .box4 {
  background-image: linear-gradient( 135deg, #EE9AE5 10%, #5961F9 100%);
}
  </style>
   -->