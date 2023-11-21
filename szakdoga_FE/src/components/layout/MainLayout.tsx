import { Box, Toolbar } from "@mui/material";
import sizeConfig from "../../configs/sizeConfig";
import colorConfigs from "../../configs/colorConfig";
import { Outlet } from "react-router-dom";
import Topbar from "../common/topbar/Topbar";

const MainLayout = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <Topbar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: `${sizeConfig.sidebar.width}`,
          minHeight: "100vh",
          backgroundColor: colorConfigs.mainBg,
        }}
      >
        <Toolbar/>
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout;
