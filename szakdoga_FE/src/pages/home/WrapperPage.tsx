import { useState } from "react";
import { DefaultResponse, PredictRequest, predict } from "../../api/predict";
import PredictPage from "./PredictPage";
import ResultsPage from "./ResultsPage";

const WrapperPage = () => {
  const [selectedSystem, setSelectedSystem] = useState("");
  const [isPredictDone, setPredictIsDone] = useState(false);
  const [results, setResults] = useState(DefaultResponse);

  const onPredict = async (params: number[]) => {
    const req: PredictRequest = {
      name: selectedSystem,
      modelParams: params,
    };
    setResults(await predict(req));
    setPredictIsDone(true);
  };
  const updateSelectedSystem = (system: string) => setSelectedSystem(system);

  return isPredictDone ? (
    <ResultsPage result={results} selectedSystem={selectedSystem} back={() => setPredictIsDone(false)} />
  ) : (
    <PredictPage
      setSelectedSystem={updateSelectedSystem}
      onPredict={onPredict}
      selectedSystem={selectedSystem}
    />
  );
};

export default WrapperPage;