import React, { useRef, useState, useEffect } from "react";
import Globe from "react-globe.gl";
import { Box, Container, Typography, Paper, Autocomplete, TextField } from "@mui/material";
import { useNavigate } from "react-router-dom";

const cities = [
  { name: "Melbourne", lat: -37.8136, lng: 144.9631, path: "/city/melbourne" },
  { name: "Sydney", lat: -33.8688, lng: 151.2093, path: "/city/sydney" },
  { name: "Brisbane", lat: -27.4698, lng: 153.0251, path: "/city/brisbane" },
  { name: "Perth", lat: -31.9505, lng: 115.8605, path: "/city/perth" },
  { name: "Adelaide", lat: -34.9285, lng: 138.6007, path: "/city/adelaide" },
  { name: "Canberra", lat: -35.2809, lng: 149.13, path: "/city/canberra" },
  { name: "London", lat: 51.5072, lng: -0.1276, path: "/city/london" },
  { name: "Paris", lat: 48.8566, lng: 2.3522, path: "/city/paris" },
  { name: "Berlin", lat: 52.52, lng: 13.405, path: "/city/berlin" },
  { name: "New York", lat: 40.7128, lng: -74.006, path: "/city/newyork" },
  { name: "Tokyo", lat: 35.6762, lng: 139.6503, path: "/city/tokyo" },
  { name: "Singapore", lat: 1.3521, lng: 103.8198, path: "/city/singapore" },
  { name: "Delhi", lat: 28.6139, lng: 77.209, path: "/city/delhi" },
  { name: "Dubai", lat: 25.2048, lng: 55.2708, path: "/city/dubai" },
  { name: "Cape Town", lat: -33.9249, lng: 18.4241, path: "/city/capetown" },
  { name: "São Paulo", lat: -23.5505, lng: -46.6333, path: "/city/saopaulo" }
];

export default function GlobePage() {
  const globeRef = useRef();
  const navigate = useNavigate();
  const [selectedCity, setSelectedCity] = useState(null);

  const handleCitySelect = (city) => {
    if (!city || !globeRef.current) return;

    setSelectedCity(city);

    globeRef.current.pointOfView({ lat: city.lat, lng: city.lng, altitude: 1.5 }, 1200);

    setTimeout(() => {
      navigate(city.path);
    }, 1200);
  };

  useEffect(() => {
    if (!globeRef.current) return;

    globeRef.current.pointOfView({ lat: 20, lng: 0, altitude: 2 }, 0);

    const controls = globeRef.current.controls();

    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.5;

    const timer = setTimeout(() => {
      controls.autoRotate = false;
    }, 4000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <Box
      sx={{
        height: "calc(100vh - 160px)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        pt: 6,
        pb: 6,
      }}
    >
      <Container maxWidth="lg">
        {/* HEADER */}
        <Box textAlign="center" mb={4}>
          <Typography variant="h2" sx={{ fontFamily: "Playfair Display", color: "black" }}>
            Discover Your New City
          </Typography>

          <Typography sx={{ color: "black" }}>
            Discover top cities around the world to begin your academic journey.
          </Typography>
        </Box>

        {/* SEARCH BAR */}
        <Box mb={3} display="flex" justifyContent="center">
          <Autocomplete
            sx={{ width: 420 }}
            options={cities}
            getOptionLabel={(option) => option.name}
            onChange={(e, value) => handleCitySelect(value)}
            slotProps={{
              popper: { sx: { mt: 1 } },
              paper: {
                sx: {
                  borderRadius: "18px",
                  overflow: "hidden",
                  boxShadow: "0 12px 30px rgba(0,0,0,0.15)"
                }
              }
            }}
            renderOption={(props, option) => (
              <Box
                component="li"
                {...props}
                sx={{
                  px: 3,
                  py: 1.5,
                  fontSize: "15px",
                  "&:hover": {
                    backgroundColor: "rgba(25,118,210,0.08)"
                  }
                }}
              >
                {option.name}
              </Box>
            )}
            renderInput={(params) => (
              <TextField
                {...params}
                placeholder="Search a city"
                sx={{
                  background: "#ffffff",
                  borderRadius: "40px",

                  "& .MuiOutlinedInput-root": {
                    borderRadius: "40px",
                    transition: "all 0.25s ease",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",

                    "& fieldset": {
                      borderColor: "rgba(0,0,0,0.08)"
                    },

                    "&:hover fieldset": {
                      borderColor: "#1976d2"
                    },

                    "&.Mui-focused fieldset": {
                      borderColor: "#1976d2",
                      borderWidth: "2px"
                    }
                  }
                }}
              />
            )}
          />
        </Box>

        {/* GLOBE */}
        <Paper
          elevation={0}
          sx={{
            borderRadius: 4,
            border: "1px solid rgba(255,255,255,0.1)",
            height: 600,
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            overflow: "hidden",
            background: `
              radial-gradient(circle at center, #0f172a 0%, #020617 70%),
              url("https://www.transparenttextures.com/patterns/stardust.png")
            `
          }}
        >
          <Globe
            ref={globeRef}
            width={900}
            height={600}
            backgroundColor="rgba(0,0,0,0)"
            globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
            atmosphereColor="#3a7bd5"
            atmosphereAltitude={0.25}
            pointsData={cities}
            pointLat="lat"
            pointLng="lng"
            pointRadius={0.5}
            pointColor={() => "#ff6b6b"}
            onPointClick={(point) => handleCitySelect(point)}
          />
        </Paper>
      </Container>
    </Box>
  );
}
