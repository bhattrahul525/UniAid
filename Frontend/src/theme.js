import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#5F735C",   // sage green
      light: "#8FA78C",
      dark: "#3F4F3E",
      contrastText: "#ffffff",
    },

    secondary: {
      main: "#A8B7A6",
    },

    background: {
      default: "#F5F5F3",  // off white page background
      paper: "#FFFFFF",
    },

    text: {
      primary: "#1A1A1A",  // dark heading text
      secondary: "#5A5A5A",
    },

    divider: "#E6E6E6",

    grey: {
      100: "#F7F7F7",
      200: "#EEEEEE",
      300: "#E0E0E0",
      500: "#9E9E9E",
      700: "#616161",
    },
  },

  typography: {
    fontFamily: `"Playfair Display", "Inter", serif`,

    h1: {
      fontWeight: 700,
      fontSize: "4rem",
      letterSpacing: "-1px",
    },

    h2: {
      fontWeight: 700,
      fontSize: "3rem",
    },

    h3: {
      fontWeight: 600,
      fontSize: "2rem",
    },

    body1: {
      fontSize: "1rem",
      lineHeight: 1.7,
      color: "#5A5A5A",
    },

    button: {
      textTransform: "none",
      fontWeight: 500,
    },
  },

  shape: {
    borderRadius: 6,
  },

  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "4px",
          padding: "10px 22px",
          border: "1px solid #1A1A1A",
          backgroundColor: "transparent",
          color: "#1A1A1A",

          "&:hover": {
            backgroundColor: "#1A1A1A",
            color: "#ffffff",
          },
        },
      },
    },

    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#FFFFFF",
          color: "#1A1A1A",
          boxShadow: "none",
          borderBottom: "1px solid #E6E6E6",
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
  },
});

export default theme;