import { Box, Card, Typography } from "@mui/material";
import Divider from "@mui/material/Divider";
type Props = {
  title: string;
  children?: React.ReactNode;
};

const Page: React.FC<Props> = ({ title, children }) => {
  return (
    <Card
      variant="outlined"
      style={{
        height: "90%",
      }}
    >
      <Box sx={{ paddingLeft: "2rem" }}>
        <Typography variant="h4" component="h2">
          {title}
        </Typography>
      </Box>
      <Box sx={{ paddingBottom: "2rem" }}>
        <Divider />
      </Box>
      {children}
    </Card>
  );
};

export default Page;
