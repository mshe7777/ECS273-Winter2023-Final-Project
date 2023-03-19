<template>
  <div class="scatter-chart">
    <svg ref="svgRef"></svg>
  </div>
</template>
<script setup>
import { ref, onMounted, defineProps, watch, computed } from "vue";
import * as d3 from "d3";
const props = defineProps({
  data: {
    required: true,
  },
});

const svgRef = ref();
const margin = ref({
  top: 60,
  left: 60,
  right: 30,
  bottom: 30,
});
const width = ref();
const height = ref();

const content = ref();
const xScale = ref(),
  yScale = ref(),
  innerHeight = ref(),
  innerWidth = ref();

const xAxis = ref(),
  yAxis = ref();
const zoom = ref();

const initChart = () => {
  const div = document.querySelector(".scatter-chart").getBoundingClientRect();
  width.value = div.width;
  height.value = div.height;
  const svg = d3
    .select(svgRef.value)
    .attr("width", width.value)
    .attr("height", height.value);

  innerWidth.value = width.value - margin.value.left - margin.value.right;
  innerHeight.value = height.value - margin.value.bottom - margin.value.top;

  content.value = svg
    .append("g")
    .attr("transform", `translate(${margin.value.left},${margin.value.top})`);

  svg
    .append("text")
    .text("In/Out degree Scatter Plot")
    .attr("transform", `translate(${width.value / 2},30)`)
    .attr("text-anchor", "middle");

  xScale.value = d3.scaleLinear().range([0, innerWidth.value]);

  yScale.value = d3.scaleLinear().range([innerHeight.value, 0]);

  xAxis.value = d3
    .axisBottom()
    .scale(xScale.value)
    .tickSize(-innerHeight.value);

  yAxis.value = d3.axisLeft().scale(yScale.value).tickSize(-innerWidth.value);
  zoom.value = d3.zoom().scaleExtent([1, 8]).on("zoom", zoomed);
  content.value
    .append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${innerHeight.value})`);

  content.value.append("g").attr("class", "y-axis");

  updateChart();
};
function zoomed(event) {
  const transform = event.transform;

  // 更新横坐标比例尺和范围
  const newXScale = transform.rescaleX(xScale.value);

  const newXTickFormat = newXScale.tickFormat();

  const xAxis = d3
    .axisBottom(newXScale)
    .tickFormat(newXTickFormat)
    .tickSize(-innerHeight.value);

  content.value.select(".x-axis").call(xAxis);

  // 更新纵坐标比例尺和范围
  const newYScale = transform.rescaleY(yScale.value);

  const newYTickFormat = newYScale.tickFormat();

  const yAxis = d3
    .axisLeft(newYScale)
    .tickFormat(newYTickFormat)
    .tickSize(-innerWidth.value);

  content.value.select(".y-axis").call(yAxis);

  // 更新散点图的位置和大小
  content.value
    .selectAll("circle")
    .attr("cx", (d) => newXScale(d.incoming))
    .attr("cy", (d) => newYScale(d.outgoing))
    .attr("opacity", (d) => {
      let x1 = xScale.value(xScale.value.domain()[0]);
      let x2 = xScale.value(xScale.value.domain()[1]);
      let y1 = yScale.value(yScale.value.domain()[0]);
      let y2 = yScale.value(yScale.value.domain()[1]);

      let nowX = newXScale(d.incoming),
        nowY = newYScale(d.outgoing);
      if (nowX < x1 || nowX > x2 || nowY > y1 || nowY < y2) {
        return 0;
      } else {
        return 1;
      }
    })
    .attr("r", 4);
}
const chartData = computed(() => {
  return props.data;
});

watch(
  () => props.data,
  () => {
    updateChart();
  }
);
const updateChart = () => {
  xScale.value.domain([0, d3.max(chartData.value, (d) => d.incoming)]).nice();
  yScale.value.domain([0, d3.max(chartData.value, (d) => d.outgoing)]).nice();

  content.value
    .selectAll("circle")
    .data(chartData.value)
    .join("circle")
    .transition()
    .attr("cx", (d) => xScale.value(d.incoming))
    .attr("cy", (d) => yScale.value(d.outgoing))
    .attr("r", 4)
    .attr("fill", "#409eff");
  content.value.select(".x-axis").transition().call(xAxis.value);
  content.value.select(".y-axis").transition().call(yAxis.value);

  d3.select(svgRef.value).call(zoom.value);
};

onMounted(() => {
  initChart();
});
</script>
<style lang='scss' scoped>
.scatter-chart {
  width: 100%;
  height: 100%;
}
</style>