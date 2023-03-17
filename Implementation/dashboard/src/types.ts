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
    readonly id: number;
    readonly outgoing: number;
    readonly incoming: number;
    readonly rating: number;
}

export interface Link {
    readonly source: number;
    readonly target: number;
    readonly rating: number;
}