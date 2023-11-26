import { Box, Button } from "@mui/material";
import { Response } from "../../api/predict";
import { LineChart } from "@mui/x-charts";
import Page from "../../components/Page";

type Props = {
  result: Response;
  selectedSystem: string;
  back: () => void;
};

const ResultsPage = (props: Props) => {
  const { result, selectedSystem, back } = props;
  return (
    <Page title={selectedSystem}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "spaceBetween",
        }}
      >
        <Box sx={{ display: "flex" }}>
          <LineChart
            title="Expected"
            series={[
              {
                data: result.expected[0],
                showMark: false,
                curve: "natural",
              },
              {
                data: result.expected[1],
                showMark: false,
                curve: "natural",
              },
            ]}
            width={window.innerWidth * 0.4}
            height={window.innerHeight * 0.6}
          />
          <LineChart
            title="Predicted"
            series={[
              {
                data: result.predicted[0],
                showMark: false,
                curve: "natural",
              },
              {
                data: result.predicted[1],
                showMark: false,
                curve: "natural",
              },
            ]}
            width={window.innerWidth * 0.4}
            height={window.innerHeight * 0.6}
          />
        </Box>
        <Box sx={{ paddingLeft: "1.5rem" }}>
          <Button variant="contained" onClick={back}>
            Back
          </Button>
        </Box>
      </Box>
    </Page>
  );
};

export default ResultsPage;
