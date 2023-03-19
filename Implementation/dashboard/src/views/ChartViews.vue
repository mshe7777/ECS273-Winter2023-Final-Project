<template>
  <div class="chart-views-wrapper">
    <div class="nav">
      <div class="slider">
        <span>time</span>
        <el-slider
          v-model="time"
          :min="1"
          :max="maxTime"
          @change="changeTime"
          :format-tooltip="formatTooltip"
        />
      </div>

      <div class="slider">
        <span>group by</span>
        <el-select
          v-model="groupSelected"
          class="m-2"
          placeholder="Select"
          @change="changeSelected"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div class="slider">
        <span>gradient </span>
        <el-slider v-model="gradient" :min="1" :max="10" />
      </div>
    </div>
    <div class="center">
      <div class="left">
        <NetworkChart
          :data="NetworkData"
          @emit-node="hdlNode"
          :groupBy="groupBy"
          :gradient="gradient"
        ></NetworkChart>
      </div>
      <div class="right">
        <StackBarChart :data="StackData" :nodeId="selectNode"></StackBarChart>
      </div>
    </div>
    <div class="footer">
      <div class="foot-item">
        <ScatterChart :data="ScatterData"></ScatterChart>
      </div>
      <div class="foot-item">
        <EdgeDisChart :data="EdgeWightData"></EdgeDisChart>
      </div>
      <div class="foot-item">
        <TimeDisChart :data="TemporalData"></TimeDisChart>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import ScatterChart from "./ScatterChart.vue";
import EdgeDisChart from "./EdgeDisChart.vue";
import TimeDisChart from "./TimeDisChart.vue";
import NetworkChart from "./NetworkChart.vue";
import StackBarChart from "./StackBarChart.vue";
import axios from "axios";
import { server } from "../helper.ts";

const time = ref(1);
const maxTime = ref(100);
const monthList = ref([]);

const selectNode = ref("1");

const groupBy = ref("none");
const gradient = ref(1);

const formatTooltip = () => {
  return nowDate.value;
};

const nowDate = computed(() => {
  return monthList.value[time.value - 1];
});

const changeTime = (val) => {
  getNetworkData(nowDate.value);
  getEdgeWightData(nowDate.value);
  getTemporalData(nowDate.value);
};

function hdlNode(id) {
  selectNode.value = id;
  getStackData(selectNode.value, nowDate.value);
}

const groupSelected = ref();

const options = [
  {
    value: "none",
    label: "none",
  },
  {
    value: "rating",
    label: "rating",
  },
  {
    value: "outgoing",
    label: "outgoing",
  },
  {
    value: "incoming",
    label: "incoming",
  },
];

const changeSelected = (val) => {
  groupBy.value = val;
};

const TemporalData = ref([]);

const EdgeWightData = ref([]);

const ScatterData = ref([]);

const StackData = ref([]);

const NetworkData = ref({
  nodes: [],
  links: [],
});

onMounted(() => {
  fetchMonthList();
});

async function fetchMonthList() {
  await axios
    .get(`${server}/basic/monthList`)
    .then((resp) => {
      monthList.value = resp.data.monthList;
      maxTime.value = monthList.value.length;
      changeTime();
      return true;
    })
    .catch((error) => console.log(error));
}

function getNetworkData(month) {
  axios
    .get(`${server}/temporal/userRatingStatistics/${month}`)
    .then((resp) => {
      ScatterData.value = getCalNetworkData(resp.data.links)().nodes;
      selectNode.value = ScatterData.value[0].id;
      NetworkData.value = getCalNetworkData(resp.data.links)();
      getStackData(selectNode.value, nowDate.value);
      return true;
    })
    .catch((error) => console.log(error));
}

function getTemporalData(month) {
  axios
    .get(`${server}/temporal/degreeDistribution/${month}`)
    .then((resp) => {
      TemporalData.value = resp.data.data;
      return true;
    })
    .catch((error) => console.log(error));
}

function getEdgeWightData(month) {
  axios
    .get(`${server}/temporal/ratingDistribution/${month}`)
    .then((resp) => {
      EdgeWightData.value = resp.data.data;
      return true;
    })
    .catch((error) => console.log(error));
}

function getStackData(userid, month) {
  axios
    .get(`${server}/temporal/user/monthlyDegree/${userid}/${month}`)
    .then((resp) => {
      StackData.value = resp.data.data;
      return true;
    })
    .catch((error) => console.log(error));
}

const getCalNetworkData = (links) => {
  return () => {
    const nodes = new Map();
    links.forEach((link) => {
      if (nodes.has(link.source)) {
        let n = nodes.get(link.source);
        n.outgoing = n.outgoing + 1;
        nodes.set(link.source, n);
      } else {
        nodes.set(link.source, {
          id: link.source,
          outgoing: 1,
          incoming: 0,
          in_rating_sum: 0,
        });
      }

      if (nodes.has(link.target)) {
        let n = nodes.get(link.target);
        n.incoming = n.incoming + 1;
        n.in_rating_sum = n.in_rating_sum + link.rating;
        nodes.set(link.target, n); // nodes[link.target+'sour'].incoming++;
      } else {
        nodes.set(link.target, {
          id: link.target,
          outgoing: 0,
          incoming: 1,
          in_rating_sum: link.rating,
        });
      }
    });
    let arr = []; // debugger
    for (let key of nodes.keys()) {
      arr.push(nodes.get(key)); // arr = arr.concat(nodes[i]);
    }
    return {
      nodes: arr,
      links,
    };
  };
};
</script>

<style lang="scss" scoped>
.chart-views-wrapper {
  width: 1200px;
  height: 100vh;
  margin: 0 auto;
  //   background: blanchedalmond;
  .nav {
    width: 100%;
    height: 4rem;

    padding: 0 20px;
    display: flex;
    .slider {
      width: 300px;
      height: 100%;
      display: flex;
      align-items: center;
      margin-right: 100px;
      span {
        width: 100px;
        margin-right: 10px;
      }
    }
  }
  .center {
    width: 100%;
    height: 55vh;

    display: flex;
    .left {
      width: 60%;
      height: 100%;
    }
    .right {
      width: 40%;
      height: 100%;
    }
  }
  .footer {
    width: 100%;
    height: 35vh;
    // background: rebeccapurple;
    display: flex;
    .foot-item {
      width: 33.3%;
      height: 100%;
      // background: red;
    }
  }
}
</style>
