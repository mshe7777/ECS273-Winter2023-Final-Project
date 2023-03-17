<script lang="ts">
import * as d3 from "d3";
import { isEmpty, debounce } from 'lodash';
import { useStore } from '../stores/store';
import { mapState, storeToRefs } from 'pinia';
import { forceGraph } from '../scripts/TemporalForceDirectedGraph.js';
import { horizontalBarChart } from '../scripts/SingleNodeDegreeBarchart.js';

export default {
  name: "TemporalForceDirectedGraph",
  props: {

  },
  data() {
    return {
      network: {

      }
    }
  },
  setup() {
    // const store = useStore()
    // const { resize } = storeToRefs(store);
    // return {
    //   store, // Return store as the local state, but when you update the property value, the store is also updated.
    //   resize,
    // }
  },
  computed: {
    // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
    // ...mapState(useStore, ['endTime']) // Traditional way to map the store state to the local state
  },
  created() {
   // this.store.fetchNetworkData(this.endTime);
  },
  methods: {
    onResize() {  // record the updated size of the target element
      let target = this.$refs.forceDirectedGraphContainer as HTMLElement
      if (target === undefined || target === null) return;
      this.store.size = { width: target.clientWidth, height: target.clientHeight };
    },
    initNetworkGraph() {

      const chart = forceGraph(this.network, {
        nodeId: d => d.id,
        nodeGroup: d => d.group,
        nodeTitle: d => `${d.id}\n${d.group}`,
        linkStrokeWidth: l => Math.sqrt(l.value),
        width: 1000,
        height: 600
      });
      d3.select('body').append(() => chart);
    },
    initSingleNodeDegreeBarchart() {
      const chart = horizontalBarChart(this.nodeData, {
        x: d => d.frequency,
        y: d => d.letter,
        yDomain: d3.groupSort(data, ([d]) => -d.frequency, d => d.letter), // sort by descending frequency
        xFormat: '%',
        xLabel: 'Frequency',
        color: 'steelblue'
      });
      d3.select('body').append(() => chart);
    }

  },
  watch: {
    rerender(newSize) {
      if (!isEmpty(newSize)) {
        d3.select('#fdg-svg').selectAll('*').remove() // Clean all the elements in the chart
        this.initNetworkGraph()
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
  <div class="chart-container d-flex" ref="forceDirectedGraphContainer">
    <svg id="fdg-svg" width="100%" height="100%">
      <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
    </svg>
  </div>
</template>

<style scoped>
.chart-container{
    height: 100%;
}
html, body {
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  width: 100%;
  height: 100%;
  color: #444444;
  overflow: scroll;
}

h1 {
  font-size: 24px;
}

a {
  color: #0083B7;
}
</style>