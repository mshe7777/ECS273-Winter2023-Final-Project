<script lang="ts">
import HierarchicalEdgeBundling from "./components/HierarchicalEdgeBundling.vue";
import TemporalForceDirectedGraph from "./components/TemporalForceDirectedGraph.vue";
import StatisticsPlotsView from "./components/StatisticsPlotsView.vue";

export default {
  components: {
    HierarchicalEdgeBundling,
    TemporalForceDirectedGraph,
    StatisticsPlotsView
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="5">
        <TemporalForceDirectedGraph/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
