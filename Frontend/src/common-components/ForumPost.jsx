import { Card, CardContent, Typography, Stack, Avatar, Button } from "@mui/material";

export default function ForumPost({ title, author, description }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6">{title}</Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {description}
        </Typography>

        <Stack direction="row" spacing={2} alignItems="center">
          <Avatar>{author[0]}</Avatar>
          <Typography variant="body2">{author}</Typography>
        </Stack>

        <Button variant="contained" sx={{ mt: 2 }}>
          View Details
        </Button>
      </CardContent>
    </Card>
  );
}
