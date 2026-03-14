import React from "react";
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  Avatar,
  Chip,
  Stack,
  Divider,
  Grid,
  Tooltip
} from "@mui/material";

import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import SchoolIcon from "@mui/icons-material/School";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import TravelExploreIcon from "@mui/icons-material/TravelExplore";
import { useSessions } from "../hooks/useSessions";
const mockSessions = [
  {
    id: 1,
    type: "private",
    mentor: "Dr. Sarah Chen",
    field: "Data Science",
    university: "Stanford University",
    topic: "Machine Learning Project Review",
    description:
      "1-on-1 session to review your machine learning project architecture, datasets, and model evaluation techniques.",
    date: "Oct 14, 2026",
    time: "10:00 AM",
    duration: "45 mins",
    users: []
  },
  {
    id: 2,
    type: "private",
    mentor: "Marcus Thorne",
    field: "Product Management",
    university: "Harvard Business School",
    topic: "Breaking into Product Management",
    description:
      "Career consultation focused on transitioning from engineering into product management roles.",
    date: "Oct 16, 2026",
    time: "2:30 PM",
    duration: "30 mins",
    users: []
  },
  {
    id: 3,
    type: "registered",
    mentor: "Leo Vance",
    field: "Artificial Intelligence",
    university: "MIT",
    topic: "Introduction to Neural Networks",
    description:
      "Workshop covering neural network fundamentals, training techniques, and practical use cases.",
    date: "Oct 12, 2026",
    time: "9:00 AM",
    duration: "1.5 hours",
    users: []
  },
  {
    id: 4,
    type: "registered",
    mentor: "Aisha Rahman",
    field: "Cybersecurity",
    university: "University of Oxford",
    topic: "Cybersecurity Career Roadmap",
    description:
      "Learn how to break into cybersecurity roles and understand the key certifications and skills required.",
    date: "Oct 18, 2026",
    time: "6:00 PM",
    duration: "1 hour",
    users: []
  },
  {
    id: 5,
    type: "public",
    mentor: "Elena Rodriguez",
    field: "Operations & Strategy",
    university: "Harvard Business School",
    topic: "Startup Strategy & Market Expansion",
    description:
      "Open workshop discussing startup scaling strategies and international market expansion.",
    date: "Oct 13, 2026",
    time: "11:30 AM",
    duration: "1 hour",
    users: []
  },
  {
    id: 6,
    type: "public",
    mentor: "Jordan Smith",
    field: "UX Design",
    university: "Rhode Island School of Design",
    topic: "Design Thinking Fundamentals",
    description:
      "Interactive design thinking workshop focused on empathy, ideation, prototyping, and testing.",
    date: "Oct 15, 2026",
    time: "4:00 PM",
    duration: "2 hours",
    users: []
  },
  {
    id: 7,
    type: "public",
    mentor: "Daniel Park",
    field: "Software Engineering",
    university: "University of Melbourne",
    topic: "System Design for Engineers",
    description:
      "Learn how to approach system design interviews and build scalable distributed systems.",
    date: "Oct 20, 2026",
    time: "5:30 PM",
    duration: "1.5 hours",
    users: []
  },
  {
    id: 8,
    type: "private",
    mentor: "Priya Kapoor",
    field: "Data Analytics",
    university: "Monash University",
    topic: "Resume & Portfolio Review",
    description:
      "Detailed feedback on your resume, GitHub projects, and portfolio before applying for internships.",
    date: "Oct 19, 2026",
    time: "1:00 PM",
    duration: "45 mins",
    users: []
  },
  {
    id: 9,
    type: "registered",
    mentor: "Thomas Nguyen",
    field: "Cloud Engineering",
    university: "University of Sydney",
    topic: "Getting Started with AWS",
    description:
      "Hands-on workshop introducing AWS services and how to build your first cloud architecture.",
    date: "Oct 22, 2026",
    time: "3:00 PM",
    duration: "2 hours",
    users: []
  },
  {
    id: 10,
    type: "public",
    mentor: "Maria Gonzalez",
    field: "Entrepreneurship",
    university: "INSEAD",
    topic: "Building Your First Startup",
    description:
      "Learn the basics of building and launching a startup, from idea validation to funding.",
    date: "Oct 25, 2026",
    time: "7:00 PM",
    duration: "1 hour",
    users: []
  }
];
export default function SessionsGridPage() {
  const { data: sessions = [], isLoading, isError } = useSessions();

  const displaySessions = sessions.length === 0 && !isLoading ? mockSessions : sessions;
  if (isLoading) return <Typography>Loading sessions...</Typography>;
  if (isError) return <Typography>Error loading sessions</Typography>;
  const mappedSessions = displaySessions.map((s) => {
    const dateObj = new Date(s.scheduled_at);

    return {
      id: s.id,
      type: s.session_type,
      mentor: `${s.mentor_first_name} ${s.mentor_last_name}`,
      field: s.users?.[0]?.mentee?.field_of_study || "General",
      university: s.users?.[0]?.mentee?.preferred_destination_country || null,

      topic: s.title,
      description: s.description,

      date: dateObj.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric"
      }),

      time: dateObj.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit"
      }),

      duration: "45 mins", // backend doesn't provide yet
      users: s.users
    };
  });

  const privateSessions = mappedSessions.filter((s) => s.type === "private");
  const registeredSessions = mappedSessions.filter((s) => s.type === "registered");
  const publicSessions = mappedSessions.filter((s) => s.type === "public");

  const SessionCard = ({ session }) => (
    <Paper
      elevation={0}
      sx={{
        p: 4,
        border: "1px solid",
        borderColor: "divider",
        borderRadius: 4,
        height: 500,
        width: 500,
        display: "flex",
        flexDirection: "column",
        transition: "box-shadow 0.2s, border-color 0.2s",
        "&:hover": { boxShadow: 2, borderColor: "primary.main" },
        overflow: "hidden"
      }}
    >
      <Box display="flex" gap={2.5} mb={3} sx={{ minWidth: 0, height: 64 }}>
        <Avatar
          sx={{
            bgcolor: "primary.main",
            width: 64,
            height: 64,
            fontSize: "1.5rem",
            flexShrink: 0
          }}
        >
          {session.mentor[0]}
        </Avatar>

        <Box
          sx={{
            minWidth: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center"
          }}
        >
          {session.topic && (
            <Tooltip title={session.topic} arrow enterDelay={300}>
              <Typography
                variant="h5"
                noWrap
                sx={{
                  fontWeight: 700,
                  lineHeight: 1.2,
                  mb: 0.5,
                  fontSize: "1.4rem"
                }}
              >
                {session.topic}
              </Typography>
            </Tooltip>
          )}

          <Tooltip title={session.mentor} arrow enterDelay={300}>
            <Typography
              variant="subtitle1"
              fontWeight="600"
              color={session.topic ? "text.secondary" : "text.primary"}
              noWrap
              sx={{ fontSize: "1.15rem" }}
            >
              {session.topic ? `by ${session.mentor}` : session.mentor}
            </Typography>
          </Tooltip>
        </Box>
      </Box>

      <Box sx={{ height: 40, mb: 2, overflow: "hidden" }}>
        <Stack direction="row" flexWrap="nowrap" gap={1.5}>
          <Chip
            label={session.field}
            sx={{
              bgcolor: "action.hover",
              fontWeight: "bold",
              fontSize: "0.95rem",
              py: 2
            }}
          />

          {session.university && (
            <Chip
              icon={<SchoolIcon />}
              label={session.university}
              variant="outlined"
              sx={{ fontSize: "0.95rem", py: 2 }}
            />
          )}
        </Stack>
      </Box>

      <Tooltip title={session.description} arrow placement="top" enterDelay={300}>
        <Typography
          variant="body1"
          color="text.secondary"
          sx={{
            mb: 3,
            flexGrow: 1,
            wordBreak: "break-word",
            overflow: "hidden",
            textOverflow: "ellipsis",
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            fontSize: "1.1rem",
            lineHeight: 1.6,
            cursor: "pointer"
          }}
        >
          {session.description}
        </Typography>
      </Tooltip>

      <Box
        sx={{
          bgcolor: "background.default",
          p: 2,
          borderRadius: 2,
          mb: 3,
          flexShrink: 0
        }}
      >
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Stack direction="row" alignItems="center" spacing={1.5}>
              <CalendarTodayIcon sx={{ fontSize: 22, color: "text.secondary" }} />
              <Typography variant="body1" fontWeight="600" noWrap>
                {session.date}
              </Typography>
            </Stack>
          </Grid>

          <Grid item xs={6}>
            <Stack direction="row" alignItems="center" spacing={1.5}>
              <AccessTimeIcon sx={{ fontSize: 22, color: "text.secondary" }} />
              <Typography variant="body1" fontWeight="600" noWrap>
                {session.time} AEST
              </Typography>
            </Stack>
          </Grid>

          <Grid item xs={12}>
            <Stack direction="row" alignItems="center" spacing={1.5}>
              <HourglassEmptyIcon sx={{ fontSize: 22, color: "text.secondary" }} />
              <Typography variant="body1" fontWeight="600" noWrap>
                {session.duration}
              </Typography>
            </Stack>
          </Grid>
        </Grid>
      </Box>

      <Box mt="auto">
        {session.type === "private" || session.type === "registered" ? (
          <Button
            size="large"
            variant="contained"
            fullWidth
            disableElevation
            sx={{
              borderRadius: 2,
              py: 1.5,
              fontSize: "1.1rem",
              fontWeight: "bold"
            }}
          >
            Enter Room
          </Button>
        ) : (
          <Button
            size="large"
            variant="outlined"
            fullWidth
            sx={{
              borderRadius: 2,
              py: 1.5,
              fontSize: "1.1rem",
              fontWeight: "bold",
              borderWidth: 2,
              "&:hover": { borderWidth: 2 }
            }}
          >
            Register
          </Button>
        )}
      </Box>
    </Paper>
  );

  return (
    <Box sx={{ backgroundColor: "background.default", minHeight: "100vh", pt: 8, pb: 10 }}>
      <Container maxWidth="lg">
        {privateSessions.length > 0 && (
          <Box mb={6}>
            <Stack direction="row" alignItems="center" spacing={1.5} mb={3}>
              <PersonOutlineIcon color="primary" sx={{ fontSize: 36 }} />
              <Typography variant="h4" sx={{ fontFamily: "Playfair Display", fontWeight: 600 }}>
                Private Sessions
              </Typography>
            </Stack>

            <Grid container spacing={4}>
              {privateSessions.map((session) => (
                <Grid item xs={12} md={6} key={session.id}>
                  <SessionCard session={session} />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {privateSessions.length > 0 && <Divider sx={{ my: 6 }} />}

        {registeredSessions.length > 0 && (
          <Box mb={6}>
            <Stack direction="row" alignItems="center" spacing={1.5} mb={3}>
              <EventAvailableIcon color="success" sx={{ fontSize: 36 }} />
              <Typography variant="h4" sx={{ fontFamily: "Playfair Display", fontWeight: 600 }}>
                My Registered Workshops
              </Typography>
            </Stack>

            <Grid container spacing={4}>
              {registeredSessions.map((session) => (
                <Grid item xs={12} md={6} key={session.id}>
                  <SessionCard session={session} />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {registeredSessions.length > 0 && <Divider sx={{ my: 6 }} />}

        {publicSessions.length > 0 && (
          <Box>
            <Stack direction="row" alignItems="center" spacing={1.5} mb={3}>
              <TravelExploreIcon color="secondary" sx={{ fontSize: 36 }} />
              <Typography variant="h4" sx={{ fontFamily: "Playfair Display", fontWeight: 600 }}>
                Available Public Sessions
              </Typography>
            </Stack>

            <Grid container spacing={4}>
              {publicSessions.map((session) => (
                <Grid item xs={12} md={6} key={session.id}>
                  <SessionCard session={session} />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Container>
    </Box>
  );
}
