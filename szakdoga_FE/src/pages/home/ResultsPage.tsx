import { Button } from "@mui/material";
import { Response } from "../../api/predict";

type Props = {
  result: Response;
  selectedSystem: string;
  back: () => void;
};

const ResultsPage = (props: Props) => {
  const { result, selectedSystem, back } = props;
  return (
    <>
      <p>{selectedSystem}</p>
      <div>results: {result.expected}</div>
      <Button onClick={back}>Back</Button>
    </>
  );
};

export default ResultsPage;
