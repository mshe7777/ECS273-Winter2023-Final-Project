<template>
  <div className="network-chart">
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
  groupBy: String,
  gradient: {
    type: Number,
    default: 1,
  },
});

const emitInfo = defineEmits(["emitNode"]);

const GROUP = {
  none: "",
  incoming: "incoming",
  rating: "in_rating_sum",
  outgoing: "outgoing",
};

const svgRef = ref();
const margin = ref({
  top: 60,
  left: 60,
  right: 30,
  bottom: 30,
});
const width = ref();
const height = ref();
const svg = ref();
const tooltip = ref();
const colorScale = ref();

const zoom = ref();

const initChart = () => {
  const div = document.querySelector(".network-chart").getBoundingClientRect();
  width.value = div.width;
  height.value = div.height;

  svg.value = d3
    .select(svgRef.value)
    .attr("width", width.value)
    .attr("height", height.value)
    .append("g");

  tooltip.value = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("display", "none");

  d3.select(svgRef.value)
    .append("defs")
    .append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 20)
    .attr("refY", 0)
    .attr("markerWidth", 3)
    .attr("markerHeight", 3)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr("fill", "#999");

  colorScale.value = d3.scaleOrdinal().range(d3.schemeCategory10);
  zoom.value = d3.zoom().scaleExtent([1, 8]).on("zoom", zoomed);
  updateChart(chartData.value);
};

function zoomed(event) {
  svg.value.attr("transform", event.transform);
}

const chartData = computed(() => {
  return props.data;
});
watch(
  () => props.data,
  (newVal) => {
    updateChart(newVal);
  }
);
const updateChart = ({ nodes, links, statistic }) => {
  let link = svg.value
    .selectAll("line")
    .data(links)
    .join("line")
    .style("stroke", "#aaa")
    .attr("marker-end", "url(#arrow)");

  let text = svg.value
    .selectAll(".weight")
    .data(links)
    .join("text")
    .attr("class", "weight")
    .attr("font-size", "0.3em")
    .style("user-select", "none")
    .text((d) => {
      return d.rating;
    });

  // Initialize the nodes
  let node = svg.value
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 4)
    .on("mouseover", function (event, d) {
      emitInfo("emitNode", d.id);
      d3.select(".tooltip")
        .style("top", event.y + 10 + "px")
        .style("left", event.x + 10 + "px")
        .style("display", "block")
        .html(() => {
          return `<p> <span>Id</span>:${d.id} </p>
        <p> <span>Incoming</span>:${d.incoming} </p>
        <p> <span>Outgoing</span>:${d.outgoing} </p>
        <p> <span>In_rating_sum</span>:${d.in_rating_sum} </p>
        `;
        });
    })
    .on("mouseout", function (event, d) {
      d3.select(".tooltip").style("display", "none");
    });

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink()
        .links(links)
        .id((d) => d.id)
    )
    .force("charge", d3.forceManyBody().strength(-10))
    .force("center", d3.forceCenter(width.value / 2, height.value / 2))
    .on("tick", ticked);
  simulation.alpha(1).restart();

  d3.select(svgRef.value).call(zoom.value);

  function ticked() {
    link
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      });

    text
      .attr("x", function (d) {
        return (d.source.x + d.target.x) / 2;
      })
      .attr("y", function (d) {
        return (d.source.y + d.target.y) / 2 - 4;
      })
      .attr("transform", function (d) {
        const bbox = this.getBBox();
        const rx = bbox.width / 2 + 2;
        const ry = bbox.height / 2 + 2;
        const angle = Math.atan2(
          d.target.y - d.source.y,
          d.target.x - d.source.x
        );
        return `rotate(${
          (angle * 180) / Math.PI
        }, ${(d.source.x + d.target.x) / 2}, ${(d.source.y + d.target.y) / 2})`;
      });

    node
      .attr("cx", function (d) {
        return d.x;
      })
      .attr("cy", function (d) {
        return d.y;
      });
  }

  updateColor();
};

watch(
  () => props.groupBy,
  (newVal) => {
    updateColor();
  }
);

watch(
  () => props.gradient,
  (newVal) => {
    updateColor();
  }
);

function updateColor() {
  let { nodes } = chartData.value;
  let temp = GROUP[props.groupBy];
  let max = +d3.max(nodes, (d) => d[temp]);
  let min = +d3.min(nodes, (d) => d[temp]);

  colorScale.value.domain(d3.range(props.gradient));

  let legend_num = !temp ? 0 : props.gradient;

  let step = Math.ceil((max - min) / props.gradient);

  d3.select(svgRef.value)
    .selectAll(".legend-rect")
    .data(d3.range(1, legend_num + 1))
    .join("rect")
    .attr("class", "legend-rect")
    .attr("width", 20)
    .attr("height", 10)
    .attr("x", 50)
    .attr("y", (d, i) => i * 20)
    .attr("fill", (d) => {
      return colorScale.value(d);
    });

  d3.select(svgRef.value)
    .selectAll(".legend-text")
    .data(d3.range(1, legend_num + 1))
    .join("text")
    .attr("class", "legend-text")
    .text((d, i) => {
      return `${min + step * i} - ${min + step * (i + 1)}`;
    })
    .attr("font-size", "0.8em")
    .attr("x", 80)
    .attr("y", (d, i) => i * 20 + 10);

  svg.value.selectAll("circle").attr("fill", (d) => {
    let nowD = Math.ceil((d[temp] - min) / step);
    if (nowD === 0) nowD = 1;
    return !temp ? "" : colorScale.value(nowD);
  });
}

onMounted(() => {
  initChart();
});
</script>
<style lang="scss" scoped>
.network-chart {
  width: 100%;
  height: 100%;
}
</style>