import React from "react";
import { Paper, Typography, Box, TextField, Button } from "@mui/material";
import { Formik, Form } from "formik";
import * as Yup from "yup";

const validationSchema = Yup.object({
  title: Yup.string().required("Title is required"),
  category: Yup.string().required("Category (e.g. Lecture) is required"),
  description: Yup.string().required("Description is required")
});

export default function CreatePostView({ onCancel, onSubmit }) {
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
        Create New Discussion
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Start a conversation with your peers and faculty.
      </Typography>

      <Formik
        initialValues={{ title: "", category: "", description: "", author: "You (Student)" }}
        validationSchema={validationSchema}
        onSubmit={onSubmit}
      >
        {({ values, handleChange, errors, touched }) => (
          <Form>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <TextField
                fullWidth
                label="Thread Title"
                name="title"
                value={values.title}
                onChange={handleChange}
                error={touched.title && Boolean(errors.title)}
                helperText={touched.title && errors.title}
              />

              <TextField
                fullWidth
                label="Category (e.g., Assignment, Lecture, General)"
                name="category"
                value={values.category}
                onChange={handleChange}
                error={touched.category && Boolean(errors.category)}
                helperText={touched.category && errors.category}
              />

              <TextField
                fullWidth
                multiline
                rows={6}
                label="What's on your mind?"
                name="description"
                value={values.description}
                onChange={handleChange}
                error={touched.description && Boolean(errors.description)}
                helperText={touched.description && errors.description}
              />

              <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 2 }}>
                <Button onClick={onCancel} sx={{ border: 'none', color: 'text.secondary' }}>
                  Cancel
                </Button>
                <Button type="submit" variant="contained">
                  Publish Post
                </Button>
              </Box>
            </Box>
          </Form>
        )}
      </Formik>
    </Paper>
  );
}