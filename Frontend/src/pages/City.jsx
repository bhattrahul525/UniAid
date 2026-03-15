import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import {
  Box,
  Container,
  Grid,
  Stack,
  Typography
} from "@mui/material";
import { useParams } from "react-router-dom";
import cityData from "../assets/city-data";

const Label = ({ children }) => (
  <Typography
    sx={{
      fontSize: 13,
      fontWeight: 700,
      letterSpacing: 2,
      textTransform: "uppercase",
      color: "#90caf9",
      mb: 1
    }}
  >
    {children}
  </Typography>
);

export default function CityPage() {
  const { city } = useParams();
  const data = cityData[city];

  if (!data) return <Typography>City not found</Typography>;

  const formattedCity = city.charAt(0).toUpperCase() + city.slice(1);

  return (
    <Box
      sx={{
        minHeight: "calc(100vh - 160px)",
        pt: 8,
        pb: 10,
        background: "linear-gradient(180deg,#0f172a 0%,#020617 100%)"
      }}
    >
      <Container
        maxWidth="lg"
        sx={{
          maxWidth: "1100px"
        }}
      >
        {/* UNIVERSITIES */}

        {data.universities && (
          <Box mb={6}>
            <Label>Universities</Label>

            <Stack spacing={1}>
              {data.universities.map((uni, idx) => (
                <Typography
                  key={idx}
                  sx={{
                    fontSize: 15,
                    color: "rgba(255,255,255,0.9)"
                  }}
                >
                  {uni}
                </Typography>
              ))}
            </Stack>
          </Box>
        )}

        {data.description && (
          <Box mb={6}>
            <Typography
              variant="h4"
              sx={{
                mb: 2,
                fontWeight: 700,
                color: "#fff"
              }}
            >
              Overview
            </Typography>

            <Typography
              sx={{
                fontSize: 16,
                lineHeight: 1.7,
                color: "rgba(255,255,255,0.9)"
              }}
            >
              {data.description}
            </Typography>
          </Box>
        )}

        {/* FOOD */}

        {data.cheapFood && (
          <Box mb={6}>
            <Label>Affordable Food</Label>

            <ul style={{ paddingLeft: 20 }}>
              {data.cheapFood.map((food, i) => (
                <li key={i}>
                  <Typography
                    sx={{
                      fontSize: 15,
                      color: "rgba(255,255,255,0.9)"
                    }}
                  >
                    {food}
                  </Typography>
                </li>
              ))}
            </ul>
          </Box>
        )}

        {/* RENT */}

        {data.rent && (
          <Box mb={6}>
            <Label>Student Rent</Label>

            <Typography
              sx={{
                fontSize: 15,
                color: "rgba(255,255,255,0.9)"
              }}
            >
              {data.rent}
            </Typography>
          </Box>
        )}

        {/* TRANSPORT */}

        {data.transport && (
          <Box mb={6}>
            <Label>Transport</Label>

            <Typography
              sx={{
                fontSize: 15,
                color: "rgba(255,255,255,0.9)"
              }}
            >
              {data.transport}
            </Typography>
          </Box>
        )}

        {/* SAFETY */}

        {data.scams && (
          <Box
            sx={{
              mt: 8,
              p: 4,
              borderRadius: 3,
              border: "1px solid rgba(255,183,77,0.25)",
              background: "rgba(255,183,77,0.06)"
            }}
          >
            <Stack direction="row" alignItems="center" spacing={1} mb={3}>
              <WarningAmberIcon sx={{ color: "#ffb74d" }} />

              <Typography
                sx={{
                  fontWeight: 700,
                  color: "#ffb74d",
                  fontSize: 18
                }}
              >
                Student Safety
              </Typography>
            </Stack>

            <Grid container spacing={2}>
              {data.scams.map((scam, idx) => (
                <Grid item xs={12} sm={6} key={idx}>
                  <Typography
                    sx={{
                      fontSize: 15,
                      color: "rgba(255,255,255,0.9)"
                    }}
                  >
                    • {scam}
                  </Typography>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* EXTRA */}

        {data.additional && (
          <Box mt={6}>
            <Label>Extra Info</Label>

            <Typography
              sx={{
                fontSize: 15,
                color: "rgba(255,255,255,0.9)"
              }}
            >
              {data.additional}
            </Typography>
          </Box>
        )}
      </Container>
    </Box>
  );
}
