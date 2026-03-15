import {
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Box
} from "@mui/material";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import { useLogin } from "../hooks/useAuth";
import { useDispatch } from "react-redux";
import { setAuth } from "../slices/authSlice";

const validationSchema = Yup.object({
  username: Yup.string().required("Username required"),
  password: Yup.string().required("Password required")
});

const initialValues = {
  username: "",
  password: ""
};

export default function LoginPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  // React Query mutation
  const { mutate: login, isPending, error } = useLogin();

  return (
    <Box
      sx={{ backgroundColor: "background.default", minHeight: "100vh", pt: 12 }}
    >
      <Container maxWidth="sm">
        <Box textAlign="center" mb={7}>
          <Typography variant="h2">Welcome Back to UniAid!</Typography>
          <Typography variant="body1" color="text.secondary">
            Login to your academic community
          </Typography>
        </Box>

        <Paper
          elevation={0}
          sx={{
            p: 6,
            border: "1px solid",
            borderColor: "divider",
            maxWidth: 500,
            margin: "0 auto"
          }}
        >
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={(values) => {
              login(values, {
                onSuccess: (data) => {
                  const authData = {
                    token: data.token,
                    user: data.user,
                    isAuthenticated: true
                  };

                  // Redux
                  dispatch(setAuth(authData));

                  // LocalStorage
                  localStorage.setItem("auth", JSON.stringify(authData));

                  console.log("Login successful:", authData);

                  navigate("/dashboard");
                }
              });
            }}
          >
            {({ values, handleChange, errors, touched }) => (
              <Form>
                <Box display="flex" flexDirection="column" gap={3}>
                  <TextField
                    label="Email"
                    name="username"
                    value={values.username}
                    onChange={handleChange}
                    error={touched.username && Boolean(errors.username)}
                    helperText={touched.username && errors.username}
                    fullWidth
                  />

                  <TextField
                    label="Password"
                    type="password"
                    name="password"
                    value={values.password}
                    onChange={handleChange}
                    error={touched.password && Boolean(errors.password)}
                    helperText={touched.password && errors.password}
                    fullWidth
                  />

                  {/* LOGIN BUTTON */}
                  <Box textAlign="center" mt={2}>
                    <Button
                      type="submit"
                      size="large"
                      variant="contained"
                      disabled={isPending}
                    >
                      {isPending ? "Logging in..." : "Login"}
                    </Button>
                  </Box>

                  {/* API ERROR MESSAGE */}
                  {error && (
                    <Typography color="error" textAlign="center" sx={{ mt: 1 }}>
                      {error.message}
                    </Typography>
                  )}
                </Box>
              </Form>
            )}
          </Formik>
        </Paper>
      </Container>
    </Box>
  );
}
