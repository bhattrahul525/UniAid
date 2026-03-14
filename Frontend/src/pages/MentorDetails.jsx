import AccessTimeIcon from "@mui/icons-material/AccessTime";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import PublicIcon from "@mui/icons-material/Public";
import SchoolIcon from "@mui/icons-material/School";
import TranslateIcon from "@mui/icons-material/Translate";
import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";
import {
  Avatar,
  Box,
  Button,
  Chip,
  Container,
  Divider,
  Paper,
  Stack,
  Typography
} from "@mui/material";
import { useParams, useLocation } from "react-router-dom";

// Increased Label font size from 0.75rem to 0.85rem
const Label = ({ children }) => (
  <Typography
    variant="caption"
    sx={{
      display: "block",
      color: "text.secondary",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: 1.5,
      fontSize: "0.85rem",
      mb: 1
    }}
  >
    {children}
  </Typography>
);
const mentorGreen = "#8FA386";
const mentorGreenBorder = "#6E8367";

export default function MentorDetails() {
  const { slug } = useParams();
  const location = useLocation();

  const mentor = location.state;
  console.log(mentor, "Mentor details passed via state");
  if (!mentor) {
    return (
      <Container sx={{ mt: 10 }}>
        <Typography variant="h4">Mentor not found</Typography>
      </Container>
    );
  }
  const getExpertiseTags = () => {
    const tags = [];

    if (mentor.visa_experience) tags.push("Visa & Immigration");
    if (mentor.housing_experience) tags.push("Finding Housing");
    if (mentor.cultural_adaptation_experience) tags.push("Cultural Adjustment");
    if (mentor.career_guidance_experience) tags.push("Career & Internships");

    return tags;
  };

  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        minHeight: "100vh",
        pt: { xs: 4, md: 10 },
        pb: 10
      }}
    >
      <Container maxWidth="lg">
        <Paper
          elevation={0}
          sx={{
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            borderRadius: 5,
            bgcolor: "background.paper",
            border: "1px solid",
            borderColor: "divider",
            overflow: "hidden",
            position: "relative",
            minHeight: "600px",
            boxShadow: "0 30px 60px rgba(0,0,0,0.08)"
          }}
        >
          {/* DESKTOP BOOKING BUTTON */}
          <Button
            variant="contained"
            disableElevation
            startIcon={<EventAvailableIcon />}
            sx={{
              position: "absolute",
              top: 32,
              right: 32,
              bgcolor: mentorGreen,
              color: "#000",
              border: "1px solid",
              borderColor: mentorGreenBorder,
              textTransform: "none",
              borderRadius: 4,
              px: 4,
              py: 1,
              fontSize: "1.05rem", // Bumped button font
              fontWeight: 600,
              "&:hover": {
                bgcolor: "primary.dark"
              },
              display: { xs: "none", md: "flex" },
              zIndex: 10
            }}
            onClick={() => console.log("Open Scheduling Modal")}
          >
            Book a Session
          </Button>

          {/* LEFT SIDEBAR - Quick Stats & Contact */}
          <Box
            sx={{
              width: { xs: "100%", md: "340px" },
              bgcolor: "rgba(0,0,0,0.02)",
              p: { xs: 4, md: 6 },
              borderRight: { md: "1px solid" },
              borderBottom: { xs: "1px solid", md: "none" },
              borderColor: "divider",
              textAlign: "center",
              display: "flex",
              flexDirection: "column",
              alignItems: "center"
            }}
          >
            <Avatar
              src={
                mentor.profileImage ||
                `https://ui-avatars.com/api/?name=${mentor.first_name}+${mentor.last_name}&background=1976d2&color=fff&size=256`
              }
              alt={`${mentor.first_name} ${mentor.last_name}`}
              sx={{
                width: 150,
                height: 150,
                mb: 3,
                fontSize: "3.5rem",
                border: "5px solid",
                borderColor: "background.paper",
                boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
                transition: "transform 0.2s ease",
                "&:hover": {
                  transform: "scale(1.05)"
                }
              }}
            />
            <Chip
              icon={<VerifiedUserIcon style={{ color: "black" }} />}
              label={mentor.mentor_type}
              sx={{
                mb: 4,
                bgcolor: mentorGreen,
                color: "#000",
                border: "1px solid",
                borderColor: mentorGreenBorder,
                "&:hover": {
                  bgcolor: "#7C916F"
                }
              }}
            />
            <Chip
              label={`⭐ AI Match Score: ${mentor.final_score?.toFixed(2) || "N/A"}`}
              sx={{ mt: 2 }}
            />

            <Stack spacing={3} sx={{ textAlign: "left", width: "100%" }}>
              <Box display="flex" alignItems="center" gap={2}>
                <TranslateIcon color="action" />
                <Box>
                  <Label>Languages</Label>
                  <Typography
                    variant="body1"
                    fontWeight={500}
                    fontSize="1.05rem"
                  >
                    {mentor.languages_spoken?.split(";").join(", ")}
                  </Typography>
                </Box>
              </Box>

              <Box display="flex" alignItems="center" gap={2}>
                <PublicIcon color="action" />
                <Box>
                  <Label>Local Experience</Label>
                  <Typography
                    variant="body1"
                    fontWeight={500}
                    fontSize="1.05rem"
                  >
                    {mentor.years_in_country} Years in Country
                  </Typography>
                </Box>
              </Box>

              <Box display="flex" alignItems="center" gap={2}>
                <AccessTimeIcon color="action" />
                <Box>
                  <Label>Availability</Label>
                  <Typography
                    variant="body1"
                    fontWeight={500}
                    fontSize="1.05rem"
                  >
                    {mentor.availability_hours_per_week} hrs/week
                  </Typography>
                </Box>
              </Box>
            </Stack>

            {/* UPDATED STATS BOX: Dark background, black text, larger fonts */}
            <Box
              sx={{
                mt: "auto",
                pt: 2,
                pb: 2,
                px: 3,
                width: "100%",
                bgcolor: mentorGreen,
                color: "#000",
                border: "1px solid",
                borderColor: mentorGreenBorder,
                borderRadius: 3,
                textAlign: "center",
                boxShadow: "0 4px 12px rgba(0,0,0,0.05)"
              }}
            >
              <Typography
                sx={{
                  fontSize: "1.15rem",
                  fontWeight: 500,
                  display: "block",
                  mb: 0.5
                }}
              >
                Avg. Response:{" "}
                <strong>{mentor.response_time_hours} hours</strong>
              </Typography>
              <Typography
                sx={{ fontSize: "1.25rem", fontWeight: 700, display: "block" }}
              >
                ★ {mentor.mentor_rating}{" "}
                <span style={{ fontSize: "0.95rem", fontWeight: 400 }}>
                  ({mentor.sessions_completed} sessions)
                </span>
              </Typography>
            </Box>

            {/* DESKTOP BOOKING BUTTON */}
            <Button
              variant="contained"
              disableElevation
              startIcon={<EventAvailableIcon />}
              sx={{
                position: "absolute",
                top: 32,
                right: 32,
                bgcolor: "primary.main", // (Or whatever background color you chose)
                color: "#000", // <--- Changed to black
                textTransform: "none",
                borderRadius: 4,
                px: 4,
                py: 1,
                fontSize: "1.05rem",
                fontWeight: 600,
                "&:hover": {
                  bgcolor: "primary.dark"
                },
                display: { xs: "none", md: "flex" },
                zIndex: 10
              }}
              onClick={() => console.log("Open Scheduling Modal")}
            >
              Book a Session
            </Button>
          </Box>

          {/* RIGHT CONTENT - Academic Info & Guidance Areas */}
          <Box sx={{ flex: 1, p: { xs: 4, md: 8 } }}>
            <Box mb={6}>
              <Typography
                variant="h2"
                sx={{
                  fontFamily: "Playfair Display",
                  fontWeight: 700,
                  mb: 1,
                  fontSize: { xs: "2.5rem", md: "3.5rem" }
                }}
              >
                {mentor.first_name} {mentor.last_name}
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  color: "text.secondary",
                  fontWeight: 400,
                  display: "flex",
                  alignItems: "center",
                  gap: 1,
                  fontSize: "1.3rem"
                }}
              >
                <SchoolIcon />
                {mentor.university}
              </Typography>
            </Box>
            {/* Using Flexbox instead of Grid for exact gap control */}
            <Box
              sx={{
                display: "flex",
                flexDirection: { xs: "column", sm: "row" },
                gap: { xs: 4, sm: 12 }, // <--- '12' is the distance. Adjust this number up or down!
                mb: 6
              }}
            >
              <Box>
                <Label>Field of Study</Label>
                <Typography
                  sx={{
                    fontWeight: 600,
                    fontSize: "1.4rem",
                    color: mentorGreenBorder
                  }}
                >
                  {mentor.field_of_study}
                </Typography>
              </Box>

              <Box>
                <Label>Degree</Label>
                <Typography sx={{ fontWeight: 500, fontSize: "1.4rem" }}>
                  {mentor.degree_level}
                </Typography>
              </Box>
            </Box>

            {/* GUIDANCE AREAS */}
            <Box mb={6}>
              <Label>I can guide you with:</Label>
              <Box
                sx={{ display: "flex", flexWrap: "wrap", gap: 1.5, mt: 1.5 }}
              >
                {getExpertiseTags().map((skill, index) => (
                  <Chip
                    key={index}
                    label={skill}
                    sx={{
                      fontSize: "1rem",
                      fontWeight: 500,
                      px: 1,
                      py: 2.5,
                      borderRadius: 3,
                      bgcolor: mentorGreen,
                      color: "#000",
                      border: "1px solid",
                      borderColor: mentorGreenBorder
                    }}
                  />
                ))}
              </Box>
            </Box>

            <Divider sx={{ mb: 5 }} />

            {/* BIO */}
            <Box>
              <Label>About Me</Label>
              <Typography
                variant="body1"
                sx={{
                  lineHeight: 1.8,
                  color: "text.primary",
                  fontSize: "1.2rem", // Bumped bio font
                  maxWidth: "800px",
                  mt: 2
                }}
              >
                {mentor.bio}
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}
