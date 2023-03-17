import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Node, Link, ComponentSize, Margin } from '../types';

export const useStore = defineStore('scatterPlot', {
    state: () => ({
        starTime: '' as string,
        endTime: '' as string,
        nodes: [] as Node[],
        links: [] as Link[],

        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.nodes) && state.size)
        }
    },
    actions: {
        async fetchNetworkData(method: string) {
            axios.post(`${server}/xxx`, {method: method})
                .then(resp => {
                    this.starTime = resp.data.starTime;
                    this.endTime = resp.data.endTime;
                    this.nodes = resp.data.nodes;
                    this.links = resp.data.links;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})