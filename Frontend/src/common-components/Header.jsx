import { AppBar, Toolbar, IconButton, Typography, Box } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useLocation } from "react-router-dom";
import { useMemo } from "react";

const routeTitles = {
  "/forum": "Community Forum",
  "/mentorship": "Mentors",
  "/chat": "Student Chat",
  "/city-info": "City Exploration",
  "/profile": "Your Profile Details",
  "/sessions": "Session Directory",
  "/dashboard": "Your Dashboard"
};

const routeSubtitles = {
  "/sessions": "Manage your schedule and discover new workshops. All times are in AEST.",
  "/profile": "Tell us about yourself so mentors can help you better.",
  "/dashboard": "Your personalized space to explore mentors, sessions, and student resources.",
};

const headerBackgrounds = {
  "/dashboard": "https://images.unsplash.com/photo-1523580846011-d3a5bc25702b",
  "/forum": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d",
  "/chat": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
  "/city-info": "https://images.unsplash.com/photo-1505761671935-60b3a7427bad",
  "/profile": "https://images.unsplash.com/photo-1494790108377-be9c29b29330",

  /* NEW sessions background (workshop / meeting) */
  "/sessions": "https://images.unsplash.com/photo-1552664730-d307ca884978"
};

const mentorBackgrounds = [
  "https://images.unsplash.com/photo-1556761175-b413da4baf72",
  "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
  "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
  "https://images.unsplash.com/photo-1521737604893-d14cc237f11d",
  "https://images.unsplash.com/photo-1516321318423-f06f85e504b3"
];

export default function Header({ onMenuClick }) {
  const location = useLocation();

  const randomMentorBg = useMemo(() => {
    return mentorBackgrounds[Math.floor(Math.random() * mentorBackgrounds.length)];
  }, []);

  let title = routeTitles[location.pathname];
  let subtitle = routeSubtitles[location.pathname];
  let bg = headerBackgrounds[location.pathname];

  /* Mentorship page random background */
  if (location.pathname === "/mentorship") {
    bg = randomMentorBg;
  }

  /* Mentor details dynamic route */
  if (location.pathname.startsWith("/mentor/")) {
    title = "Mentor Details";
    bg = randomMentorBg;
  }

  /* City guide dynamic route */
  if (!title && location.pathname.startsWith("/city/")) {
    const city = location.pathname.split("/city/")[1];
    const formattedCity = city.charAt(0).toUpperCase() + city.slice(1);

    title = `City Guide • ${formattedCity}`;
    bg = "https://images.unsplash.com/photo-1505761671935-60b3a7427bad";
  }

  title = title || "UniAid";
  subtitle = subtitle || "UniAid Student Platform";

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        height: 160,
        justifyContent: "center",
        backgroundImage: `
          linear-gradient(
            rgba(0,0,0,0.65),
            rgba(0,0,0,0.65)
          ),
          url(${bg})
        `,
        backgroundSize: "cover",
        backgroundPosition: "center"
      }}
    >
      <Toolbar>
        <IconButton onClick={onMenuClick} sx={{ color: "white" }}>
          <MenuIcon />
        </IconButton>

        <Box ml={2}>
          <Typography
            variant="h4"
            sx={{ color: "white", fontWeight: 600 }}
          >
            {title}
          </Typography>

          <Typography
            variant="body2"
            sx={{ color: "rgba(255,255,255,0.8)" }}
          >
            {subtitle}
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
}