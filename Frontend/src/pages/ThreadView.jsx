import React, { useState } from "react";
import { Paper, Typography, Box, TextField, Button, Divider, Avatar } from "@mui/material";
import { Formik, Form } from "formik";

export default function ThreadView({ post }) {
  // This state now resets whenever post.id changes because of the key in ForumPage
 const [comments, setComments] = useState(
  post.comments || [
    { id: "initial", author: "System", text: `Welcome to the discussion for ${post.title}.` }
  ]
);

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        p: { md: 6, xs: 3 }, 
        border: "1px solid", 
        borderColor: "divider", 
        borderRadius: 2,
        bgcolor: 'background.paper',
      }}
    >
      <Typography variant="h3" sx={{ mb: 1, fontFamily: 'Playfair Display' }}>
        {post.title}
      </Typography>
      
      <Typography variant="subtitle2" sx={{ color: 'primary.main', mb: 4, fontWeight: 700 }}>
        {post.author} • {post.category}
      </Typography>

      <Typography variant="body1" sx={{ lineHeight: 1.7, mb: 6 }}>
        {post.description}
      </Typography>

      <Divider sx={{ mb: 4 }} />

      <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Discussion</Typography>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mb: 6 }}>
        {comments.map((c) => (
          <Box key={c.id} sx={{ display: 'flex', gap: 2 }}>
            <Avatar sx={{ bgcolor: 'primary.dark', width: 32, height: 32, fontSize: '0.8rem' }}>{c.author[0]}</Avatar>
            <Box>
              <Typography variant="caption" sx={{ color: 'primary.light', fontWeight: 700 }}>{c.author}</Typography>
              <Typography variant="body2" sx={{ mt: 0.5 }}>{c.text}</Typography>
            </Box>
          </Box>
        ))}
      </Box>

      {/* REPLY SECTION */}
      <Formik
        initialValues={{ reply: "" }}
        onSubmit={(values, { resetForm }) => {
          if (!values.reply.trim()) return;
          setComments([...comments, { id: Date.now(), author: "You", text: values.reply }]);
          resetForm();
        }}
      >
        {({ values, handleChange }) => (
          <Form>
            <TextField
              fullWidth
              multiline
              rows={3}
              name="reply"
              placeholder="Post a reply..."
              value={values.reply}
              onChange={handleChange}
              sx={{ bgcolor: 'background.default', mb: 2 }}
            />
            <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button type="submit" variant="contained">Reply</Button>
            </Box>
          </Form>
        )}
      </Formik>
    </Paper>
  );
}