import {
  Box,
  Button,
  Card,
  Divider,
  FormControlLabel,
  FormGroup,
  Switch,
  Typography,
} from "@mui/material";
import { Response } from "../../api/predict";
import { LineChart } from "@mui/x-charts";
import Page from "../../components/Page";
import { useState } from "react";

type Props = {
  result: Response;
  selectedSystem: string;
  back: () => void;
};

const ResultsPage = (props: Props) => {
  const { result, selectedSystem, back } = props;
  const [isExpectedShown, setIsExpectedShown] = useState(true);
  return (
    <>
    <FormGroup>
      <FormControlLabel
        control={
          <Switch
            defaultChecked
            onChange={(e) => setIsExpectedShown(e.target.checked)}
          />
        }
        label="Show Expected"
      />
      </FormGroup>
      <Page title={selectedSystem} r2Score={result.r2Score}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "spaceBetween",
          }}
        >
          <Box sx={{ display: "flex", gap: 2, justifyContent: "center" }}>
            <Card sx={{ textAlign: "center" }} variant="outlined">
              <Typography variant="h5">Predicted</Typography>
              <Divider />
              <LineChart
                title="Predicted"
                series={result.predicted.map((ser) => {
                  return {
                    data: ser,
                    showMark: false,
                    curve: "natural",
                  };
                })}
                width={window.innerWidth * 0.4}
                height={window.innerHeight * 0.6}
              />
            </Card>
            {isExpectedShown && (
              <Card sx={{ textAlign: "center" }} variant="outlined">
                <Typography variant="h5">Expected</Typography>
                <Divider />
                <LineChart
                  title="Expected"
                  series={result.expected.map((ser) => {
                    return {
                      data: ser,
                      showMark: false,
                      curve: "natural",
                    };
                  })}
                  width={window.innerWidth * 0.4}
                  height={window.innerHeight * 0.6}
                />
              </Card>
            )}
          </Box>
          <Box sx={{ paddingLeft: "1.5rem" }}>
            <Button variant="contained" onClick={back}>
              Back
            </Button>
          </Box>
        </Box>
      </Page>
    </>
  );
};

export default ResultsPage;
