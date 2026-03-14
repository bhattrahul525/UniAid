import { Box, Button, Container, Paper, TextField, Typography } from "@mui/material";
import { Form, Formik } from "formik";
import * as Yup from "yup";
import { useRegister } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const validationSchema = Yup.object({
  email: Yup.string().email("Enter a valid email").required("Email is required"),

  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),

  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Confirm your password")
});

const initialValues = {
  email: "",
  password: "",
  confirmPassword: ""
};

export default function RegistrationPagep() {
  const { mutate: register, isPending, error } = useRegister();
  const navigate = useNavigate();
  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        minHeight: "100vh",
        pt: 8,
        pb: 10
      }}
    >
      <Container maxWidth="sm">
        {/* HEADER */}
        <Box textAlign="center" mb={5}>
          <Typography variant="h2" sx={{ fontFamily: "Playfair Display" }}>
            Create Account
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Sign up to start connecting with the academic community.
          </Typography>
        </Box>

        {/* CARD */}
        <Paper
          elevation={0}
          sx={{
            p: 6,
            border: "1px solid",
            borderColor: "divider",
            borderRadius: 4
          }}
        >
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={(values) => {
              register(values, {
                onSuccess: () => {
                  alert("Account created successfully");
                  navigate("/login");
                }
                
              });
            }}
          >
            {({ values, handleChange, errors, touched }) => (
              <Form>
                <TextField
                  label="Email Address"
                  name="email"
                  type="email"
                  value={values.email}
                  onChange={handleChange}
                  error={touched.email && Boolean(errors.email)}
                  helperText={touched.email && errors.email}
                  fullWidth
                  sx={{ mb: 3 }}
                />

                <TextField
                  label="Password"
                  name="password"
                  type="password"
                  value={values.password}
                  onChange={handleChange}
                  error={touched.password && Boolean(errors.password)}
                  helperText={touched.password && errors.password}
                  fullWidth
                  sx={{ mb: 3 }}
                />

                <TextField
                  label="Confirm Password"
                  name="confirmPassword"
                  type="password"
                  value={values.confirmPassword}
                  onChange={handleChange}
                  error={touched.confirmPassword && Boolean(errors.confirmPassword)}
                  helperText={touched.confirmPassword && errors.confirmPassword}
                  fullWidth
                  sx={{ mb: 4 }}
                />

                <Box textAlign="center">
                  <Button type="submit" size="large" variant="contained" disabled={isPending}>
                    {isPending ? "Creating..." : "Sign Up"}
                  </Button>
                </Box>
                {error && (
                  <Typography color="error" textAlign="center">
                    {error.message}
                  </Typography>
                )}
              </Form>
            )}
          </Formik>
        </Paper>
      </Container>
    </Box>
  );
}
