import {
  Drawer,
  Box,
  Typography,
  List,
  ListItemButton,
  ListItemText,
  IconButton,
  Divider,
  Button
} from "@mui/material";

import CloseIcon from "@mui/icons-material/Close";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { logout } from "../slices/authSlice";
import logo from "../assets/uniaid-logo.png";

const drawerWidth = 240;
const itemStyle = {
  width: "80%",
  borderRadius: 2,
  justifyContent: "center",
  "&:hover": {
    background: "rgba(46,204,113,0.12)"
  }
};
function Sidebar({ open, onClose, variant = "temporary" }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  const go = (path) => {
    navigate(path);
    onClose();
  };

  return (
    <Drawer
      anchor="left"
      variant={variant}
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column"
        }
      }}
    >
      {/* Header */}

      <Box
        sx={{
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          px: 3,
          py: 3
        }}
      >
        {/* Logo */}
        <Box
          component="img"
          src={logo}
          alt="UniAid Logo"
          sx={{
            position: "absolute",
            left: "-52px",
            width: "190px",
            height: "180px",
            objectFit: "contain",
            bottom: "-37px",
          }}
        />

        {/* Brand text */}
        <Typography
          sx={{
            fontSize: 24,
            fontWeight: 800,
            letterSpacing: 1.2,
            background: "linear-gradient(90deg,#2ecc71,#27ae60)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            textShadow: "0 0 12px rgba(46,204,113,0.45)"
          }}
        >
          UniAid
        </Typography>

        {/* Close button */}
        <IconButton
          onClick={onClose}
          sx={{
            position: "absolute",
            right: 8
          }}
        >
          <CloseIcon />
        </IconButton>
      </Box>

      <Divider />

      {/* Navigation */}

      <List
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 1,
          pt: 2
        }}
      >
        <ListItemButton onClick={() => go("/mentorship")} sx={itemStyle}>
          <ListItemText
            primary="Mentors"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>

        <ListItemButton onClick={() => go("/city-info")} sx={itemStyle}>
          <ListItemText
            primary="City Guide"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>

        <ListItemButton onClick={() => go("/sessions")} sx={itemStyle}>
          <ListItemText
            primary="Sessions"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>

        <ListItemButton onClick={() => go("/forum")} sx={itemStyle}>
          <ListItemText
            primary="Forum"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>

        <ListItemButton onClick={() => go("/chat")} sx={itemStyle}>
          <ListItemText
            primary="Chat"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>

        <ListItemButton onClick={() => go("/profile")} sx={itemStyle}>
          <ListItemText
            primary="Profile"
            primaryTypographyProps={{ align: "center", fontWeight: 500 }}
          />
        </ListItemButton>
      </List>

      <Box sx={{ flexGrow: 1 }} />

      {/* Logout */}

      <Box sx={{ p: 2 }}>
        <Button
          fullWidth
          variant="outlined"
          color="error"
          onClick={handleLogout}
          sx={{
            borderRadius: 2
          }}
        >
          Logout
        </Button>
      </Box>
    </Drawer>
  );
}

export default Sidebar;
