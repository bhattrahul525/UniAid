import { Card, Avatar, Typography, Box, Tooltip, Chip, Stack } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import SmartToyIcon from "@mui/icons-material/SmartToy";

export default function MentorCard({
  firstName,
  lastName,
  mentor_type,
  university,
  bio,
  profileImage,
  mentor_rating,
  aiRecommendation = "-", // default value
  onClick
}) {
  return (
    <Tooltip title={`View ${firstName}'s profile`} arrow>
      <Card
        onClick={onClick}
        sx={{
          height: 340,
          p: 3,
          borderRadius: 4,
          textAlign: "center",
          cursor: "pointer",
          width: "240px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          background: "#ffffff",
          boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
          transition: "all 0.25s ease",

          "&:hover": {
            transform: "translateY(-6px)",
            boxShadow: "0 20px 45px rgba(0,0,0,0.18)"
          }
        }}
      >
        {/* Avatar */}

        <Box display="flex" justifyContent="center" mb={2}>
          <Avatar
            src={profileImage}
            sx={{
              width: 70,
              height: 70,
              border: "3px solid #f2f2f2"
            }}
          />
        </Box>

        {/* Name */}

        <Typography variant="h6" sx={{ fontWeight: 600, fontSize: 18 }}>
          {firstName} {lastName}
        </Typography>

        {/* Role */}

        <Typography sx={{ fontSize: 14, color: "text.secondary" }}>
          {mentor_type?.charAt(0).toUpperCase() + mentor_type?.slice(1)}
        </Typography>

        {/* University */}

        <Typography sx={{ fontSize: 13, color: "text.secondary", mb: 1 }}>{university}</Typography>

        {/* Rating */}

        <Box display="flex" alignItems="center" justifyContent="center" gap={0.5} mb={1}>
          <StarIcon sx={{ fontSize: 18, color: "#ffb400" }} />
          <Typography sx={{ fontWeight: 600, fontSize: 14 }}>{mentor_rating}</Typography>
        </Box>

        {/* AI Recommendation */}

        <Stack direction="row" justifyContent="center" mb={1}>
          <Chip
            icon={<SmartToyIcon />}
            label={`AI Match: ${aiRecommendation}`}
            size="small"
            color="primary"
            variant="outlined"
          />
        </Stack>

        {/* Bio */}

        <Typography
          sx={{
            fontSize: 13,
            color: "#555",
            mt: 1,
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
            overflow: "hidden"
          }}
        >
          {bio}
        </Typography>
      </Card>
    </Tooltip>
  );
}
