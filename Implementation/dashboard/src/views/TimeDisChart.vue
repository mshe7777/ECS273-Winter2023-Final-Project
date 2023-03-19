<template>
  <div class="time-dis-chart">
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
  innerHeight = ref();

const xAxis = ref(),
  yAxis = ref();

const initChart = () => {
  const div = document.querySelector(".time-dis-chart").getBoundingClientRect();
  width.value = div.width;
  height.value = div.height;
  const svg = d3
    .select(svgRef.value)
    .attr("width", width.value)
    .attr("height", height.value);

  const innerWidth = width.value - margin.value.left - margin.value.right;
  innerHeight.value = height.value - margin.value.bottom - margin.value.top;

  content.value = svg
    .append("g")
    .attr("transform", `translate(${margin.value.left},${margin.value.top})`);

  svg
    .append("text")
    .text("Temporal Distribution")
    .attr("transform", `translate(${width.value / 2},30)`)
    .attr("text-anchor", "middle");

  svg
    .append("text")
    .text("Time")
    .attr("transform", `translate(${width.value / 2},${height.value})`)
    .attr("font-size", "0.8em")
    .attr("text-anchor", "middle");

  svg
    .append("text")
    .text("Growth rate[edges/year]")
    .attr("font-size", "0.8em")
    .attr("text-anchor", "middle")
    .attr("transform", `translate(20,${height.value / 2}) rotate(-90)`);

  xScale.value = d3.scaleBand().range([0, innerWidth]);

  yScale.value = d3.scaleLinear().range([innerHeight.value, 0]);

  xAxis.value = d3.axisBottom().scale(xScale.value);

  yAxis.value = d3.axisLeft().scale(yScale.value);

  content.value
    .append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${innerHeight.value})`);

  content.value.append("g").attr("class", "y-axis");

  updateChart();
};

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
  let step = Math.ceil(chartData.value.length / 7);

  xScale.value.domain(chartData.value.map((d) => d.time));

  yScale.value.domain([0, d3.max(chartData.value, (d) => d.edgeNumber)]).nice();

  xAxis.value.tickFormat(function (d, i) {
    if (i % step) {
      return "";
    } else {
      return d;
    }
  });

  content.value
    .selectAll("rect")
    .data(chartData.value)
    .join("rect")
    .transition()
    .attr("width", xScale.value.bandwidth())
    .attr("height", (d) => {
      return innerHeight.value - yScale.value(d.edgeNumber);
    })
    .attr("x", (d) => xScale.value(d.time))
    .attr("y", (d) => yScale.value(d.edgeNumber))
    .attr("fill", "#409eff");

  content.value
    .selectAll("rect")
    .on("mouseover", function (event, d) {
      d3.select(".tooltip")
        .style("top", event.y + 10 + "px")
        .style("left", event.x + 10 + "px")
        .style("display", "block")
        .html(() => {
          return `<p> <span>Time</span>:${d.time} </p>
        <p> <span>EdgeNumber</span>:${d.edgeNumber} </p>
        `;
        });
    })
    .on("mouseout", function () {
      d3.select(".tooltip").style("display", "none");
    });

  content.value.select(".x-axis").transition().call(xAxis.value);
  content.value.select(".y-axis").transition().call(yAxis.value);
};

onMounted(() => {
  initChart();
});
</script>
<style lang="scss" scoped>
.time-dis-chart {
  width: 100%;
  height: 100%;
}
</style>