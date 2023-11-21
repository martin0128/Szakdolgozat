import { AppBar, Toolbar, Typography } from "@mui/material";
import sizeConfig from "../../../configs/sizeConfig";
import colorConfigs from "../../../configs/colorConfig";

const Topbar = () => {
  const colorConfig = colorConfigs.topbar;
  const title = "Rendszeridentifikáció mélytanulásos hálók segítségével"
  return (
    <AppBar
      position="fixed"
      sx={{
        width: `100%`,
        ml: sizeConfig.sidebar.width,
        boxShadow: "unset",
        backgroundColor: colorConfig.bg,
        color: colorConfig.color,
      }}
    >
      <Toolbar>
        <Typography variant="h6">
            {title}
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Topbar;
