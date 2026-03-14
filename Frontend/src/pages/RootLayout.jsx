import { Box } from "@mui/material";
import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "../common-components/Sidebar";
import Header from "../common-components/Header";

export default function RootLayout() {
  const [open, setOpen] = useState(false);

  const toggleSidebar = () => {
    setOpen((prev) => !prev);
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar open={open} onClose={() => setOpen(false)} />

      <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <Header onMenuClick={toggleSidebar} />

        <Box
          sx={{
            flex: 1,
            backgroundColor: "background.default"
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}
