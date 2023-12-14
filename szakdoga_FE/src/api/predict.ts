import axios from "axios"

export type PredictRequest = {
    name: string,
    modelParams: number[]
}
export type Response = {
    expected: number[][],
    predicted: number[][],
    r2Score: number,
}

export const DefaultResponse: Response = {
    expected: [],
    predicted: [],
    r2Score: NaN,
}

export const predict = (request: PredictRequest) => axios.post<Response>('https://szakdogabe-gizqhebctq-ew.a.run.app/predict/',request).then(res => res.data);