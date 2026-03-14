import { Box, Typography, Chip } from "@mui/material";

export default function ForumPost({ title, author, category, timestamp, onClick, isSelected }) {
  return (
    <Box
      onClick={onClick}
      sx={{
        p: 3,
        cursor: "pointer",
        borderBottom: "1px solid",
        borderColor: "divider",
        transition: "all 0.3s ease",
        position: 'relative',
        bgcolor: isSelected ? "rgba(143, 167, 140, 0.05)" : "transparent",
        "&:hover": {
          bgcolor: "rgba(255, 255, 255, 0.02)",
          pl: 4, // Subtle "slide" effect on hover
        },
        // Modern selection indicator
        "&::after": {
            content: '""',
            position: 'absolute',
            left: 0,
            top: '20%',
            height: isSelected ? '60%' : '0%',
            width: '4px',
            bgcolor: 'primary.main',
            borderRadius: '0 4px 4px 0',
            transition: 'all 0.3s ease'
        }
      }}
    >
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={1.5}>
        <Typography variant="caption" sx={{ color: "primary.main", fontWeight: 800, letterSpacing: 0.5 }}>
          {category.toUpperCase()}
        </Typography>
        <Typography variant="caption" sx={{ color: "text.secondary", fontSize: '0.7rem' }}>
          {timestamp}
        </Typography>
      </Box>

      <Typography variant="body1" sx={{ 
        fontFamily: "Playfair Display",
        fontSize: "1.1rem",
        fontWeight: isSelected ? 700 : 500,
        color: isSelected ? "primary.main" : "text.primary",
        mb: 1
      }}>
        {title}
      </Typography>

      <Typography variant="caption" sx={{ color: "text.secondary", fontStyle: 'italic' }}>
        By {author}
      </Typography>
    </Box>
  );
}