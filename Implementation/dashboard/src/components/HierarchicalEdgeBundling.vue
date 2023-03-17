<script lang="js">
import * as d3 from "d3";
import { isEmpty, debounce } from 'lodash';
import { hierarchicalEdgeBundling } from '../scripts/HierachicalEdgeBunding.js';
import { useStore } from '../stores/store';
import { mapState, storeToRefs } from 'pinia';

export default {
  name: "HierarchicalEdgeBundling",
  props: {

  },
  data() {
    return {
      data: [
        {"name":"flare.analytics.cluster.AgglomerativeCluster","size":3938,"imports":["flare.animate.Transitioner","flare.vis.data.DataList","flare.util.math.IMatrix","flare.analytics.cluster.MergeEdge","flare.analytics.cluster.HierarchicalCluster","flare.vis.data.Data"]},
        {"name":"flare.analytics.cluster.CommunityStructure","size":3812,"imports":["flare.analytics.cluster.HierarchicalCluster","flare.animate.Transitioner","flare.vis.data.DataList","flare.analytics.cluster.MergeEdge","flare.util.math.IMatrix"]},
        {"name":"flare.analytics.cluster.HierarchicalCluster","size":6714,"imports":["flare.vis.data.EdgeSprite","flare.vis.data.NodeSprite","flare.vis.data.DataList","flare.vis.data.Tree","flare.util.Arrays","flare.analytics.cluster.MergeEdge","flare.util.Sort","flare.vis.operator.Operator","flare.util.Property","flare.vis.data.Data"]},
        {"name":"flare.analytics.cluster.MergeEdge","size":743,"imports":[]},
        {"name":"flare.analytics.graph.BetweennessCentrality","size":3534,"imports":["flare.animate.Transitioner","flare.vis.data.NodeSprite","flare.vis.data.DataList","flare.util.Arrays","flare.vis.data.Data","flare.util.Property","flare.vis.operator.Operator"]},
        {"name":"flare.analytics.graph.LinkDistance","size":5731,"imports":["flare.animate.Transitioner","flare.vis.data.NodeSprite","flare.vis.data.EdgeSprite","flare.analytics.graph.ShortestPaths","flare.vis.data.Data","flare.util.Property","flare.vis.operator.Operator"]},
        {"name":"flare.analytics.graph.MaxFlowMinCut","size":7840,"imports":["flare.animate.Transitioner","flare.vis.data.NodeSprite","flare.vis.data.EdgeSprite","flare.vis.data.Data","flare.util.Property","flare.vis.operator.Operator"]},
        {"name":"flare.analytics.graph.ShortestPaths","size":5914,"imports":["flare.vis.data.EdgeSprite","flare.vis.data.NodeSprite","flare.animate.Transitioner","flare.vis.operator.Operator","flare.util.heap.HeapNode","flare.util.heap.FibonacciHeap","flare.util.Property","flare.vis.data.Data"]},
        {"name":"flare.analytics.graph.SpanningTree","size":3416,"imports":["flare.animate.Transitioner","flare.vis.data.NodeSprite","flare.vis.operator.IOperator","flare.vis.Visualization","flare.vis.data.TreeBuilder","flare.vis.operator.Operator"]},
        {"name":"flare.analytics.optimization.AspectRatioBanker","size":7074,"imports":["flare.animate.Transitioner","flare.util.Arrays","flare.vis.data.DataSprite","flare.scale.Scale","flare.vis.axis.CartesianAxes","flare.vis.Visualization","flare.util.Property","flare.vis.operator.Operator"]},
        {"name":"flare.animate.Easing","size":17010,"imports":["flare.animate.Transition"]}
      ]
    }
  },
  computed: {

  },
  created() {

  },
  methods: {
    initChart() {
      const chart = hierarchicalEdgeBundling(this.data);
      d3.select('body').append(() => chart);
      console.log(chart)
    }
  },
  watch: {},
  mounted() {

  },
  beforeDestroy() {

  }
}
</script>

<template>
  <div className="chart-container d-flex" ref="hirerarchicalEdgeBunding">
    <svg id="heb-svg" width="100%" height="100%">
      <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
    </svg>
  </div>
</template>

<style scoped>
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