
<script lang="ts">
import * as d3 from "d3";
import { isEmpty, debounce } from 'lodash';
import { useStore } from '../stores/store';
import { mapState, storeToRefs } from 'pinia';
import { scatterplot } from '../scripts/DegreeScatterPlot.js';
import { edgeWeightHistogram } from '../scripts/EdgeWeightDistribution.js';
import { temporalHistogram } from '../scripts/TemporalDistribution.js';
import { degreeBarChart } from '../scripts/DegreeDistribution.js';

export default {
  name: "StatisticsPlotsView",
  props: [

  ],
  data() {
    return {
      network: {

      },
      nodeData: {

      },
      edgeWeightData: {

      },
      edgeTemporalData: {

      },
      degreeDistributionData: {

      }
    }
  },
  setup() {

  },
  computed: {

  },
  created() {

  },
  methods: {
    onResize() {  // record the updated size of the target element
      let target = this.$refs.statisticsPlotsContainer as HTMLElement
      if (target === undefined || target === null) return;
      this.store.size = { width: target.clientWidth, height: target.clientHeight };
    },
    initDegreeScatterPlot() {
      const chart = scatterplot(this.network, {
        x: d => d.mpg,
        y: d => d.hp,
        title: d => d.name,
        xLabel: 'Miles per gallon →',
        yLabel: '↑ Horsepower',
        stroke: 'steelblue',
        width: 1000,
        height: 600
      });
      d3.select('body').append(() => chart);
    },
    initEdgeWeightDistribution() {
      const chart = edgeWeightHistogram(this.edgeWeightData, {
        value: d => d.rate,
        label: "Unemployment rate (%) →",
        width: 1000,
        height: 500,
        color: "steelblue"
      });
      d3.select('body').append(() => chart);
    },
    initTemporalDistribution() {
      const chart = temporalHistogram(this.edgeTemporalData, {
        value: d => d.rate,
        label: "Unemployment rate (%) →",
        width: 1000,
        height: 500,
        color: "steelblue"
      });
      d3.select('body').append(() => chart);
    },
    initDegreeDistribution() {
      const chart = degreeBarChart(this.degreeDistributionData, {
        x: d => d.letter,
        y: d => d.frequency,
        xDomain: d3.groupSort(data, ([d]) => -d.frequency, d => d.letter), // sort by descending frequency
        yFormat: '%',
        yLabel: 'Frequency',
        color: 'steelblue'
      });
      d3.select('body').append(() => chart);
    }
  },
  watch: {
    rerender(newSize) {
      if (!isEmpty(newSize)) {
        d3.select('#spc-svg').selectAll('*').remove() // Clean all the elements in the chart
        this.initChart()
      }
    }
  },
  // The following are general setup for resize events.
  mounted() {
    window.addEventListener('resize', debounce(this.onResize, 100))
    this.onResize()
  },
  beforeDestroy() {
   window.removeEventListener('resize', this.onResize)
  }

}

</script>

<template>
  <div className="chart-container d-flex" ref="statisticsPlotsContainer">
    <svg id="spc-svg" width="100%" height="100%">
      <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
    </svg>
  </div>
</template>

<style scoped>

</style>