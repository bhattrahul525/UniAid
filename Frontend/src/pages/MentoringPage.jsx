import { useMemo, useState } from "react";
import {
  Container,
  Grid,
  Typography,
  TextField,
  InputAdornment,
  Box
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import MentorCard from "../common-components/MentorCard";
import { useNavigate } from "react-router-dom";
import { CircularProgress } from "@mui/material";
import { useMentors, useMentorRecommendations } from "../hooks/useMentors";
import { useSelector } from "react-redux";

const randomImages = [
  "https://i.pravatar.cc/300?img=1",
  "https://i.pravatar.cc/300?img=2",
  "https://i.pravatar.cc/300?img=3",
  "https://i.pravatar.cc/300?img=4",
  "https://i.pravatar.cc/300?img=5",
  "https://i.pravatar.cc/300?img=6",
  "https://i.pravatar.cc/300?img=7",
  "https://i.pravatar.cc/300?img=8",
  "https://i.pravatar.cc/300?img=9",
  "https://i.pravatar.cc/300?img=10",
  "https://i.pravatar.cc/300?img=11",
  "https://i.pravatar.cc/300?img=12",
  "https://i.pravatar.cc/300?img=13",
  "https://i.pravatar.cc/300?img=14",
  "https://i.pravatar.cc/300?img=15",
  "https://i.pravatar.cc/300?img=16",
  "https://i.pravatar.cc/300?img=17",
  "https://i.pravatar.cc/300?img=18",
  "https://i.pravatar.cc/300?img=19",
  "https://i.pravatar.cc/300?img=20",
  "https://i.pravatar.cc/300?img=21",
  "https://i.pravatar.cc/300?img=22",
  "https://i.pravatar.cc/300?img=23",
  "https://i.pravatar.cc/300?img=24",
  "https://i.pravatar.cc/300?img=25",
  "https://i.pravatar.cc/300?img=26",
  "https://i.pravatar.cc/300?img=27",
  "https://i.pravatar.cc/300?img=28",
  "https://i.pravatar.cc/300?img=29",
  "https://i.pravatar.cc/300?img=30",
  "https://i.pravatar.cc/300?img=31",
  "https://i.pravatar.cc/300?img=32",
  "https://i.pravatar.cc/300?img=33",
  "https://i.pravatar.cc/300?img=34",
  "https://i.pravatar.cc/300?img=35",
  "https://i.pravatar.cc/300?img=36",
  "https://i.pravatar.cc/300?img=37",
  "https://i.pravatar.cc/300?img=38",
  "https://i.pravatar.cc/300?img=39",
  "https://i.pravatar.cc/300?img=40",
  "https://i.pravatar.cc/300?img=41",
  "https://i.pravatar.cc/300?img=42",
  "https://i.pravatar.cc/300?img=43",
  "https://i.pravatar.cc/300?img=44",
  "https://i.pravatar.cc/300?img=45",
  "https://i.pravatar.cc/300?img=46",
  "https://i.pravatar.cc/300?img=47",
  "https://i.pravatar.cc/300?img=48",
  "https://i.pravatar.cc/300?img=49",
  "https://i.pravatar.cc/300?img=50"
];

const randomBios = [
  "Helping international students settle smoothly into Australian universities.",
  "Guiding students through accommodation, visas, and early career planning.",
  "Supporting new arrivals with practical tips for living and studying abroad.",
  "Helping students navigate academics, internships, and networking.",
  "Mentoring students interested in data science and technology careers.",
  "Helping international students adjust to Australian culture and lifestyle.",
  "Guiding students through part-time job searches and career preparation.",
  "Helping students transition from university into professional roles.",
  "Providing support for academic challenges and research opportunities.",
  "Mentoring students pursuing careers in AI and machine learning.",
  "Helping international students build confidence in a new country.",
  "Sharing experience on visas, housing, and student life in Australia.",
  "Supporting students interested in research and postgraduate studies.",
  "Helping students balance academics, internships and social life.",
  "Guiding students through networking and career growth strategies.",
  "Helping students understand Australian workplace culture.",
  "Providing advice on career paths in tech and analytics.",
  "Mentoring students interested in software engineering roles.",
  "Supporting international students through their first semester.",
  "Helping students prepare for technical interviews and internships.",
  "Guiding students in building strong academic foundations.",
  "Helping new students understand university systems and resources.",
  "Providing insights on research careers and PhD pathways.",
  "Mentoring students interested in entrepreneurship and startups.",
  "Helping international students build professional networks.",
  "Supporting students exploring data analytics and business intelligence.",
  "Helping students improve productivity and study techniques.",
  "Guiding students through the Australian internship landscape.",
  "Helping students build strong resumes and portfolios.",
  "Supporting international students in adapting to university life.",
  "Helping students discover career opportunities in tech.",
  "Providing insights into the Australian job market.",
  "Helping students explore career opportunities in research.",
  "Mentoring students interested in cloud computing and infrastructure.",
  "Helping students learn how to manage academic pressure.",
  "Guiding students toward industry-relevant skills.",
  "Supporting students with career decision making.",
  "Helping international students find opportunities for growth.",
  "Providing support for transitioning into industry roles.",
  "Helping students prepare for graduate programs.",
  "Mentoring students interested in cybersecurity careers.",
  "Helping students understand academic research processes.",
  "Supporting international students in adapting socially.",
  "Helping students explore different technology career paths.",
  "Guiding students through professional networking.",
  "Helping students navigate university resources effectively.",
  "Supporting students aiming for leadership roles in tech.",
  "Helping students build technical confidence.",
  "Mentoring students interested in innovation and technology.",
  "Helping students succeed academically and professionally."
];

export default function MentorshipPage() {
  const [prompt, setPrompt] = useState("");
  const navigate = useNavigate();
  const userId = useSelector((state) => state.auth.user?.user_id);
  const { data: mentors = [], isLoading, isError } = useMentors();
  const [mode, setMode] = useState("all");
  const recommendationParams =
    mode === "profile"
      ? { userId, topK: 8 }
      : mode === "prompt"
        ? {
            userId,
            numberOfQuery: 10,
            prompt
          }
        : null;

  const {
    data: recommendedMentors,
    isLoading: isRecommendationsLoading,
    isError: isRecommendationsError
  } = useMentorRecommendations(recommendationParams);

  const enrichedMentors = useMemo(() => {
    return mentors.slice(0, 50).map((mentor, index) => ({
      ...mentor,
      firstName: mentor.first_name,
      lastName: mentor.last_name,
      profileImage: randomImages[index % randomImages.length],
      bio: randomBios[index % randomBios.length]
    }));
  }, [mentors]);

  const enrichedRecommendedMentors = useMemo(() => {
    if (!recommendedMentors || recommendedMentors.length === 0) return [];

    return recommendedMentors.map((item) => {
      const mentor = item.mentor || item;
      return {
        ...mentor,
        id: mentor.mentor_id ?? mentor.id,
        firstName: mentor.first_name || mentor.firstName,
        lastName: mentor.last_name || mentor.lastName,
        profileImage:
          mentor.profileImage ||
          randomImages[Math.floor(Math.random() * randomImages.length)],
        bio:
          mentor.bio || randomBios[Math.floor(Math.random() * randomBios.length)]
      };
    });
  }, [recommendedMentors]);

  const displayMentors =
    mode === "all" ? enrichedMentors : enrichedRecommendedMentors;

  if (isLoading || isRecommendationsLoading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 10 }}>
        <CircularProgress />
      </Box>
    );
  }
  if (isError || isRecommendationsError) {
    return (
      <Typography sx={{ textAlign: "center", mt: 10 }}>
        Something went wrong while loading mentors.
      </Typography>
    );
  }

  return (
    <Box
      sx={{
        height: "calc(100vh - 160px)", // subtract header height
        display: "flex",
        flexDirection: "column",
        overflow: "hidden"
      }}
    >
      <Container
        maxWidth="lg"
        sx={{
          pt: 5,
          pb: 2
        }}
      >
        {/* SEARCH + CUSTOMIZE */}

        <Box mb={4} display="flex" gap={2} alignItems="center">
          {/* SEARCH INPUT */}

          <TextField
            fullWidth
            placeholder="Describe the mentor you need (example: Professor in Computer Science at Monash)"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            variant="outlined"
            sx={{
              "& .MuiOutlinedInput-root": {
                background: "#fff",
                border: "1px solid rgba(0,0,0,0.06)",
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
                },

                "&.Mui-focused": {
                  boxShadow: "0 6px 20px rgba(25,118,210,0.25)"
                }
              },

              "& input": {
                padding: "14px 10px",
                fontSize: "15px"
              }
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: "text.secondary" }} />
                </InputAdornment>
              )
            }}
          />

          {/* CUSTOMIZE BUTTON */}

          <Box
            onClick={() => {
              if (prompt.trim().length > 0) setMode("prompt");
            }}
            sx={{
              px: 3,
              height: "56px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "40px",
              fontWeight: 600,
              color: "white",
              cursor: "pointer",
              background: "linear-gradient(135deg,#2e7d32,#4caf50)",
              boxShadow: "0 4px 14px rgba(0,0,0,0.15)",
              transition: "all 0.2s ease",
              whiteSpace: "nowrap",

              "&:hover": {
                transform: "translateY(-2px)",
                boxShadow: "0 6px 18px rgba(0,0,0,0.2)"
              }
            }}
          >
            Customize
          </Box>

          {/* AI MATCH BUTTON */}

          <Box
            onClick={() => setMode("profile")}
            sx={{
              px: 3,
              height: "56px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "40px",
              fontWeight: 600,
              fontSize: "14px",
              color: "white",
              cursor: "pointer",
              background: "linear-gradient(135deg,#1b5e20,#43a047)",
              boxShadow: "0 4px 14px rgba(0,0,0,0.15)",
              transition: "all 0.2s ease",
              whiteSpace: "nowrap",

              "&:hover": {
                transform: "translateY(-2px)",
                boxShadow: "0 6px 18px rgba(0,0,0,0.2)"
              }
            }}
          >
            🤖 Find My Best Mentor Match
          </Box>
        </Box>
        {mode === "prompt" && (
          <Typography sx={{ mb: 2, fontWeight: 600 }}>
            🤖 AI matched mentors for: "{prompt}"
          </Typography>
        )}

        {mode === "profile" && (
          <Typography sx={{ mb: 2, fontWeight: 600 }}>
            🤖 Best mentors based on your profile
          </Typography>
        )}
      </Container>

      {/* SCROLL AREA */}

      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          px: 3,
          pb: 4
        }}
      >
        <Container
          maxWidth="lg"
          sx={{
            height: "100%",
            display: "flex",
            flexDirection: "column"
          }}
        >
          {displayMentors.length > 0 ? (
            <Grid container spacing={3}>
              {displayMentors.map((mentor) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={mentor.id}>
                  <MentorCard
                    firstName={mentor.firstName}
                    lastName={mentor.lastName}
                    mentor_type={mentor.mentor_type}
                    university={mentor.university}
                    mentor_rating={mentor.mentor_rating}
                    profileImage={mentor.profileImage}
                    bio={mentor.bio}
                    aiRecommendation={
                      mentor.final_score ? mentor.final_score.toFixed(2) : "-"
                    }
                    onClick={() =>
                      navigate(`/mentor/${mentor.id}`, { state: mentor })
                    }
                  />
                </Grid>
              ))}
            </Grid>
          ) : (
            <Typography color="text.secondary" sx={{ mt: 4 }}>
              No mentors found.
            </Typography>
          )}
        </Container>
      </Box>
    </Box>
  );
}
