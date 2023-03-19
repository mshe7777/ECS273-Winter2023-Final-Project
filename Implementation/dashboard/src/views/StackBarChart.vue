<template>
  <div className="stack-bar-chart">
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
  nodeId: {
    required: true,
  },
});

const svgRef = ref();
const margin = ref({
  top: 100,
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

const stack = ref();
const color = ref();

const initChart = () => {
  const div = document
    .querySelector(".stack-bar-chart")
    .getBoundingClientRect();
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

    .attr("class", "title")
    .attr("transform", `translate(${width.value / 2},30)`)
    .attr("text-anchor", "middle");

  const naiveKey = ["outgoing", "incoming"];

  stack.value = d3
    .stack()
    .keys(naiveKey)
    .order(d3.stackOrderNone)
    .offset(d3.stackOffsetNone);

  color.value = d3.scaleOrdinal().domain(naiveKey).range(d3.schemeCategory10);

  let legend = svg
    .selectAll(".legend")
    .data(naiveKey)
    .join("g")
    .attr("transform", (d, i) => `translate(${150 + 100 * i},50)`);

  legend
    .append("text")
    .text((d) => d)
    .attr("font-size", "0.8em")
    .attr("x", 30)
    .attr("y", 8);

  legend
    .append("rect")
    .attr("width", 20)
    .attr("height", 10)
    .attr("fill", (d, i) => color.value(d));

  yScale.value = d3.scaleBand().range([0, innerHeight.value]);

  xScale.value = d3.scaleLinear().range([0, innerWidth]);

  xAxis.value = d3.axisTop().scale(xScale.value);

  yAxis.value = d3.axisLeft().scale(yScale.value);

  content.value.append("g").attr("class", "x-axis");

  content.value.append("g").attr("class", "y-axis");
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
watch(
  () => props.nodeId,
  () => {
    d3.select(".title").text(`Node ${props.nodeId} historical degree`);
  }
);
const updateChart = () => {
  d3.select(".title").text(`Node ${props.nodeId} historical degree`);
  const stackData = stack.value(chartData.value);

  yScale.value.domain(chartData.value.map((d) => d.month)).padding(0.2);
  const maxValue = d3.max(stackData, (d) => {
    return d3.max(d, (subD) => d3.max(subD));
  });
  xScale.value.domain([0, maxValue]);

  content.value
    .selectAll(".stackGroup")
    .data(stackData)
    .join("g")
    .attr("class", "stackGroup")
    .attr("fill", (d, i) => {
      return color.value(d.key);
    })
    .selectAll("rect")
    .data((d) => d)
    .join("rect")
    .transition()
    .attr("width", (d) => {
      return xScale.value(d[1]) - xScale.value(d[0]);
    })
    .attr("opacity", "0.8")
    .attr("height", yScale.value.bandwidth())
    .attr("y", (d) => {
      return yScale.value(d.data.month);
    })
    .attr("x", (d) => xScale.value(d[0]));

  content.value
    .selectAll("rect")
    .on("mouseover", (event, d) => {
      d3.select(".tooltip")
        .style("top", event.y + 10 + "px")
        .style("left", event.x + 10 + "px")
        .style("display", "block")
        .html(() => {
          return `<p> <span>month</span>:${d.data.month} </p>
        <p> <span class='maker' style='background:${color.value(
          "incoming"
        )}'> </span><span>Incoming</span>:${d.data.incoming} </p>
        <p> <span class='maker' style='background:${color.value(
          "outgoing"
        )}'> </span><span>Outgoing</span>:${d.data.outgoing} </p>

        `;
        });
    })
    .on("mouseout", function (event, d) {
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
.stack-bar-chart {
  width: 100%;
  height: 100%;
}
</style>