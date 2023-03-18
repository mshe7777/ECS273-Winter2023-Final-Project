import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import {
    Node,
    Link,
    ComponentSize,
    Margin,
    EdgeNumberData,
    EdgeWeightData,
    NodeHistoryData,
} from '../types';

export const useStore = defineStore('scatterPlot', {
    state: () => ({
        nodes: [] as Node[],
        links: [] as Link[],
        monthList: [] as string[],
        edgeNumberList: [] as EdgeNumberData[],
        edgeWeightList: [] as EdgeWeightData[],
        nodeHistoricalDataList: [] as NodeHistoryData[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.monthList) && state.size)
        }
    },
    actions: {
        async fetchNetworkData(method: string) {
            axios.post(`${server}/xxx`, {method: method})
                .then(resp => {
                    this.nodes = resp.data.nodes;
                    this.links = resp.data.links;
                    return true;
                })
                .catch(error => console.log(error));
        },
        fetchMonthList() {
             axios.get(`${server}/basic/monthList`)
                .then(resp => {
                    this.monthList = resp.data.monthList
                    return true;
                })
                .catch(error => console.log(error));
        },
        fetchTemporalUserRatingStatistics(month: string) {
             axios.get(`${server}/temporal/userRatingStatistics/${month}`)
                .then(resp => {
                    this.nodes = resp.data.nodes
                    this.links = resp.data.links
                    return true;
                })
                .catch(error => console.log(error));
        },
        fetchTemporalDegreeDistribution(month: string) {
             axios.get(`${server}/temporal/degreeDistribution/${month}`)
                .then(resp => {
                    this.edgeNumberList = resp.data.data
                    return true;
                })
                .catch(error => console.log(error));
        },
        fetchTemporalRatingDistribution(month: string) {
             axios.get(`${server}/temporal/ratingDistribution/${month}`)
                .then(resp => {
                    this.edgeWeightList = resp.data.data
                    return true;
                })
                .catch(error => console.log(error));
        },
        fetchUserMonthlyDegree(userid: string, month: string) {
             axios.get(`${server}/temporal/user/monthlyDegree/${userid}/${month}"`)
                .then(resp => {
                    this.nodeHistoricalDataList = resp.data.data
                    return true;
                })
                .catch(error => console.log(error));
        }
    }
})