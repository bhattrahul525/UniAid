import React, { useState } from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Stack,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Chip,
  Divider,
  Button
} from "@mui/material";

import { alpha } from "@mui/material/styles";

import StarIcon from "@mui/icons-material/Star";
import ForumIcon from "@mui/icons-material/Forum";
import SchoolIcon from "@mui/icons-material/School";
import AccessTimeIcon from "@mui/icons-material/AccessTime";

import dayjs from "dayjs";

/* ---------- DATA ---------- */

const today = dayjs();
const nextTwoWeeks = Array.from({ length: 14 }, (_, i) => today.add(i, "day"));

const sampleTopics = [
  "Portfolio Review",
  "Intro to Machine Learning",
  "Design Thinking Workshop",
  "Product Strategy Clinic",
  "Data Science AMA",
  "Career Roadmapping",
  "Mock Interview Session"
];

const sampleMentors = [
  { name: "Dr. Sarah Chen", field: "Data Science", rating: 4.9, avatar: "SC" },
  { name: "Marcus Thorne", field: "Product Management", rating: 4.8, avatar: "MT" },
  { name: "Jordan Smith", field: "UX Design", rating: 4.7, avatar: "JS" },
  { name: "Elena Rodriguez", field: "Operations", rating: 4.9, avatar: "ER" }
];

const universities = ["MIT", "Stanford", "Harvard", "CMU", "RISD", "UCLA"];

const generateSessionsForNextTwoWeeks = () => {
  const sessionsByDate = {};

  nextTwoWeeks.forEach((date, index) => {
    const count = (index % 3) + 1;
    const key = date.format("YYYY-MM-DD");

    sessionsByDate[key] = Array.from({ length: count }, (_, i) => {
      const topic = sampleTopics[(index + i) % sampleTopics.length];
      const mentor = sampleMentors[(index + i) % sampleMentors.length];
      const university = universities[(index + i) % universities.length];

      return {
        id: `${key}-${i}`,
        topic,
        mentor: mentor.name,
        field: mentor.field,
        university,
        time: `${9 + i}:00 AM`
      };
    });
  });

  return sessionsByDate;
};

const sessionsByDate = generateSessionsForNextTwoWeeks();
const mentors = sampleMentors.slice(0, 3);

const discussions = [
  { title: "Best resources to break into ML research?", replies: 42, category: "career" },
  { title: "Can someone review my UX case study?", replies: 31, category: "design" },
  { title: "How to prepare for product interviews at FAANG?", replies: 27, category: "product" },
  { title: "Tips for balancing school and internships", replies: 19, category: "student-life" }
];

/* ---------- COMPONENT ---------- */

export default function DashboardPage() {

  const [selectedDate, setSelectedDate] = useState(today.format("YYYY-MM-DD"));
  const sessionsForDay = sessionsByDate[selectedDate] || [];

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#f3f6fb",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        py: 6,
        px: 2
      }}
    >
      <Container
        maxWidth="lg"
        sx={{
          width: "100%"
        }}
      >
        <Paper
          elevation={0}
          sx={{
            borderRadius: 5,
            p: 4,
            border: "1px solid #dbe3f0",
            boxShadow: "0 22px 55px rgba(15,23,42,0.08)",
            bgcolor: "#ffffff"
          }}
        >
          {/* HEADER */}

          <Box mb={4}>
            <Typography variant="h5" fontWeight={800} sx={{ color: "#0f172a", letterSpacing: "-0.02em" }}>
              Student Dashboard
            </Typography>

            <Typography sx={{ color: "#64748b" }}>
              Overview of your mentorship sessions and community activity
            </Typography>
          </Box>

          {/* MAIN GRID */}

          <Grid container spacing={4}>
            {/* LEFT COLUMN */}

            <Grid item xs={12} md={8}>
              {/* CALENDAR */}

              <Paper
                sx={{
                  p: 3,
                  borderRadius: 4,
                  border: "1px solid #dde5f2",
                  mb: 3,
                }}
              >
                <Typography fontWeight={700} mb={2}>
                  Upcoming Sessions
                </Typography>

                <Box
                  sx={{
                    display: "grid",
                    gridTemplateColumns: "repeat(7,1fr)",
                    gap: 1,
                  }}
                >
                  {nextTwoWeeks.map((date) => {
                    const key = date.format("YYYY-MM-DD");
                    const selected = key === selectedDate;

                    return (
                      <Button
                        key={key}
                        onClick={() => setSelectedDate(key)}
                        sx={{
                          borderRadius: 3,
                          py: 1,
                          flexDirection: "column",
                          bgcolor: selected ? "#e0edff" : "#ffffff",
                          border: "1px solid",
                          borderColor: selected ? "#2563eb" : "#e5edf7",
                          color: selected ? "#1d4ed8" : "#475569"
                        }}
                      >
                        <Typography variant="caption">
                          {date.format("ddd")}
                        </Typography>

                        <Typography fontWeight={700}>
                          {date.format("D")}
                        </Typography>
                      </Button>
                    );
                  })}
                </Box>
              </Paper>

              {/* SESSION LIST */}

              <Paper
                sx={{ p: 3, borderRadius: 4, border: "1px solid #e4ebf5" }}
              >
                <Typography fontWeight={700} mb={2}>
                  Sessions on {dayjs(selectedDate).format("D MMM")}
                </Typography>

                {sessionsForDay.map((session, index) => (
                  <React.Fragment key={session.id}>
                    {index > 0 && <Divider sx={{ my: 2 }} />}

                    <Grid container alignItems="center">
                      <Grid item xs={8}>
                        <Typography fontWeight={700} sx={{ color: "#0f172a" }}>
                          {session.topic}
                        </Typography>

                        <Typography variant="body2" sx={{ color: "#64748b" }}>
                          {session.mentor} • {session.field}
                        </Typography>

                        <Stack direction="row" spacing={1} mt={1}>
                          <Chip
                            size="small"
                            icon={<SchoolIcon sx={{ fontSize: 16 }} />}
                            label={session.university}
                            sx={{ bgcolor: "#eef2ff", color: "#3730a3" }}
                          />

                          <Chip
                            size="small"
                            icon={<AccessTimeIcon sx={{ fontSize: 16 }} />}
                            label={session.time}
                            sx={{ bgcolor: "#ecfeff", color: "#0f766e" }}
                          />
                        </Stack>
                      </Grid>

                      <Grid item xs={4} textAlign="right">
                        <Button
                          variant="contained"
                          sx={{
                            textTransform: "none",
                            borderRadius: 999,
                            px: 3,
                            bgcolor: "#2563eb"
                          }}
                        >
                          View details
                        </Button>
                      </Grid>
                    </Grid>
                  </React.Fragment>
                ))}
              </Paper>
            </Grid>

            {/* RIGHT COLUMN */}

            <Grid item xs={12} md={4}>
              <Stack spacing={3}>
                {/* TOP MENTORS */}

                <Paper
                  sx={{ p: 3, borderRadius: 4, border: "1px solid #dde5f2" }}
                >
                  <Stack direction="row" spacing={1} mb={2}>
                    <StarIcon sx={{ color: "#fbbf24" }} />

                    <Typography fontWeight={700}>Top Mentors</Typography>
                  </Stack>

                  <List disablePadding>
                    {mentors.map((m) => (
                      <ListItem key={m.name} sx={{ px: 0, py: 1.25 }}>
                        <ListItemAvatar>
                          <Avatar
                            sx={{
                              bgcolor: alpha("#3182ce", 0.12),
                              color: "#2b6cb0",
                            }}
                          >
                            {m.avatar}
                          </Avatar>
                        </ListItemAvatar>

                        <ListItemText
                          primary={
                            <Typography sx={{ fontWeight: 600, color: "#0f172a" }}>
                              {m.name}
                            </Typography>
                          }
                          secondary={
                            <Typography variant="body2" sx={{ color: "#64748b" }}>
                              {m.field}
                            </Typography>
                          }
                        />

                        <Chip
                          label={m.rating}
                          size="small"
                          sx={{
                            bgcolor: "#fff7e6",
                            color: "#b45309",
                            fontWeight: 700,
                            borderRadius: 999
                          }}
                        />
                      </ListItem>
                    ))}
                  </List>
                </Paper>

                {/* FORUM POSTS */}

                <Paper
                  sx={{ p: 3, borderRadius: 4, border: "1px solid #dde5f2" }}
                >
                  <Stack direction="row" spacing={1} mb={2}>
                    <ForumIcon color="primary" />

                    <Typography fontWeight={700}>Top Forum Posts</Typography>
                  </Stack>

                  {discussions.map((d) => (
                    <Box
                      key={d.title}
                      sx={{
                        p: 2,
                        borderRadius: 3,
                        mb: 1.5,
                        bgcolor: "#f8fafc",
                        cursor: "pointer",
                        border: "1px solid transparent",
                        transition: "0.15s",
                        "&:hover": {
                          bgcolor: "#e0edff",
                          borderColor: alpha("#2563eb", 0.4)
                        }
                      }}
                    >
                      <Typography fontWeight={600} sx={{ color: "#0f172a" }}>
                        {d.title}
                      </Typography>

                      <Typography variant="caption" sx={{ color: "#2563eb", fontWeight: 600 }}>
                        {d.replies} replies
                      </Typography>
                    </Box>
                  ))}
                </Paper>
              </Stack>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </Box>
  );
}