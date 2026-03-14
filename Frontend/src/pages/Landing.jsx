import { Box, Container, Typography, Button, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import { useRef } from "react";
import { motion } from "framer-motion";

const features = [
  {
    title: "Pre-arrival Guidance",
    desc: "Learn about visa preparation, accommodation, banking and budgeting before arriving."
  },
  {
    title: "Mentor Matching",
    desc: "Connect with senior students and alumni mentors who can guide you."
  },
  {
    title: "Scam Alerts",
    desc: "Stay protected by learning about common scams targeting students."
  },
  {
    title: "City Exploration",
    desc: "Discover cheap food places, grocery stores and cultural spots."
  },
  {
    title: "Transport Guide",
    desc: "Understand public transport, taxis and airport pickup options."
  }
];

export default function Landing() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const auth = useSelector((state) => state.auth);

  useEffect(() => {
    if (auth?.token) {
      navigate("/mentorship");
    }
  }, [auth, navigate]);

  useEffect(() => {
    const video = videoRef.current;

    const handleScroll = () => {
      if (!video) return;

      const scrollTop = window.scrollY;
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;

      const scrollFraction = scrollTop / scrollHeight;

      const duration = video.duration || 1;

      video.currentTime = duration * scrollFraction;
    };

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <Box>
      <Box
        sx={{
          position: "sticky",
          top: 0,
          height: "100vh",
          overflow: "hidden",
          background: "black"
        }}
      >
        <video
          ref={videoRef}
          src="/hero-video.mp4"
          muted
          playsInline
          preload="auto"
          onLoadedMetadata={(e) => {
            e.target.currentTime = 0;
          }}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            zIndex: -1
          }}
        />

        <Container
          maxWidth="md"
          sx={{
            textAlign: "center",
            position: "relative",
            zIndex: 2,
            color: "white",
            pt: 20
          }}
        >
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
          >
            <Typography variant="h2" gutterBottom>
              UniAid: Your Ultimate Guide to University Life Abroad
            </Typography>

            <Typography variant="h6" sx={{ mb: 4 }}>
              Helping new international students connect with mentors, avoid scams, and explore
              their new city.
            </Typography>
          </motion.div>
        </Container>
      </Box>

      {/* FEATURES SECTION */}

      {/* FEATURES SECTION */}
      <Box
        sx={{
          py: 14,
          position: "relative",
          background: "transparent"
        }}
      >
        <Container maxWidth="md" sx={{ position: "relative", zIndex: 2 }}>
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 80 }}
              whileInView={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -80 }}
              transition={{
                duration: 0.7,
                delay: index * 0.15
              }}
              viewport={{
                once: false,
                margin: "-100px"
              }}
            >
              <Card
                sx={{
                  mb: 6,
                  p: 3,
                  borderRadius: 4,
                  backdropFilter: "blur(10px)",
                  background: "rgba(255,255,255,0.85)",
                  boxShadow: "0 10px 40px rgba(0,0,0,0.25)"
                }}
              >
                <CardContent>
                  <Typography variant="h4" gutterBottom>
                    {feature.title}
                  </Typography>

                  <Typography color="text.secondary" fontSize={18}>
                    {feature.desc}
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </Container>
      </Box>

      {/* CTA */}

      {/* CTA */}

      <Box
        sx={{
          py: 14,
          display: "flex",
          justifyContent: "center",
          alignItems: "center"
        }}
      >
        <Container
          maxWidth="sm"
          sx={{
            textAlign: "center",
            position: "relative",
            zIndex: 2,
            color: "white",
            background: "rgba(0,0,0,0.55)",
            backdropFilter: "blur(10px)",
            borderRadius: 4,
            px: 6,
            py: 6,
            boxShadow: "0 20px 60px rgba(0,0,0,0.4)"
          }}
        >
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <Typography
              variant="h4"
              gutterBottom
              sx={{
                fontWeight: 700,
                textShadow: "0px 4px 20px rgba(0,0,0,0.7)"
              }}
            >
              Start Your Journey Today
            </Typography>

            <Typography
              sx={{
                mb: 4,
                color: "rgba(255,255,255,0.85)",
                fontSize: 18
              }}
            >
              Join UniAid or login to your existing account to connect with mentors, ask questions,
              and navigate university life with confidence.
            </Typography>

            <Box
              sx={{
                display: "flex",
                justifyContent: "center",
                gap: 3,
                flexWrap: "wrap"
              }}
            >
              {/* REGISTER BUTTON */}

              <Button
                variant="contained"
                size="large"
                onClick={() => navigate("/register")}
                sx={{
                  px: 5,
                  py: 1.5,
                  fontSize: 16,
                  fontWeight: 600,
                  borderRadius: 3,
                  background: "linear-gradient(135deg,#4f46e5,#7c3aed)",
                  boxShadow: "0 10px 30px rgba(79,70,229,0.6)",
                  transition: "all 0.3s ease",
                  "&:hover": {
                    transform: "translateY(-3px)",
                    boxShadow: "0 15px 40px rgba(79,70,229,0.8)"
                  }
                }}
              >
                Join UniAid
              </Button>

              {/* LOGIN BUTTON */}

              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate("/login")}
                sx={{
                  px: 5,
                  py: 1.5,
                  fontSize: 16,
                  fontWeight: 600,
                  borderRadius: 3,
                  color: "white",
                  borderColor: "white",
                  transition: "all 0.3s ease",
                  "&:hover": {
                    background: "white",
                    color: "black",
                    borderColor: "white"
                  }
                }}
              >
                Login
              </Button>
            </Box>
          </motion.div>
        </Container>
      </Box>
    </Box>
  );
}
