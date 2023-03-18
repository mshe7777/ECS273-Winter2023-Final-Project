// Global types and interfaces are stored here.
export interface Margin {
    readonly left: number;
    readonly right: number;
    readonly top: number;
    readonly bottom: number;
}

export interface ComponentSize {
    width: number;
    height: number;
}

export interface Node {
    readonly id: string;
    readonly outgoing: number;
    readonly incoming: number;
    readonly in_rating_sum: number;
    readonly out_rating_sum: number;
}

export interface Link {
    readonly source: string;
    readonly target: string;
    readonly rating: number;
    readonly time: number;
}

export interface EdgeNumberData {
    readonly time: number;
    readonly edgeNumber: number;
}

export interface EdgeWeightData {
    readonly edgeRating: number;
    readonly frequency: number;
}

export interface NodeHistoryData {
    readonly month: string;
    readonly incoming: number;
    readonly outgoing: number;
}