import {
  Autocomplete,
  Button,
  Card,
  CardActions,
  CardContent,
  TextField,
} from "@mui/material";
import systems from "../../configs/systemConfig";
import { RefObject, createRef, useEffect, useState } from "react";

type Props = {
  setSelectedSystem: (system: string) => void;
  onPredict: (params: number[]) => void;
  selectedSystem: string;
};
const PredictPage = (props: Props) => {
  const { setSelectedSystem, onPredict, selectedSystem } = props;

  const [inputFields, setInputFields] = useState<string[]>([]);
  const [inputRefs, setInputRefs] = useState<RefObject<any>[]>([]);

  useEffect(() => {
    const system = systems.filter((a) => a.name === selectedSystem)[0];
    if (system) {
      setInputFields(system.paramLabels);
    } else {
      setInputFields([]);
    }

    setInputRefs((elRefs: any) =>
      Array(inputFields.length)
        .fill(0)
        .map((_, i) => elRefs[i] || createRef())
    );
  }, [inputFields.length, selectedSystem]);
  return (
    <Card
      variant="outlined"
      style={{
        height: "70%",
        gap: 1,
        display: "flex",
        flexDirection: "column",
        padding: "5rem",
      }}
    >
      <CardContent>
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          onChange={(_, systemName) => {setSelectedSystem(systemName ?? "")}}
          options={systems.map((system) => system.name)}
          sx={{ width: 300 }}
          renderInput={(params) => <TextField {...params} label="System" />}
        />
        {inputFields.map((label, index) => {
          return (
            <TextField
              key={index}
              type="number"
              label={label}
              inputRef={inputRefs[index]}
            ></TextField>
          );
        })}
      </CardContent>
      {selectedSystem && (
        <CardActions>
          <Button variant="outlined" onClick={()=>onPredict(inputRefs.map(ref => ref.current.value))}>
            Predict
          </Button>
        </CardActions>
      )}
    </Card>
  );
};

export default PredictPage;
