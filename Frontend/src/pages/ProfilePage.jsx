import {
  Autocomplete,
  Avatar,
  Box,
  Button,
  Container,
  Divider,
  FormControlLabel,
  Grid,
  MenuItem,
  Paper,
  Switch,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
  Typography
} from "@mui/material";
import { Form, Formik } from "formik";
import { useState } from "react";
import * as Yup from "yup";
import { useProfile, useUpdateProfile } from "../hooks/useProfile";
import { useSelector } from "react-redux";
import toast from "react-hot-toast";

const countries = [
  "Afghanistan",
  "Albania",
  "Algeria",
  "Argentina",
  "Australia",
  "Austria",
  "Bangladesh",
  "Brazil",
  "Canada",
  "China",
  "Colombia",
  "Denmark",
  "Egypt",
  "Finland",
  "France",
  "Germany",
  "Greece",
  "India",
  "Indonesia",
  "Ireland",
  "Israel",
  "Italy",
  "Japan",
  "Kenya",
  "Malaysia",
  "Mexico",
  "Netherlands",
  "New Zealand",
  "Nigeria",
  "Norway",
  "Pakistan",
  "Peru",
  "Philippines",
  "Poland",
  "Portugal",
  "Russia",
  "Saudi Arabia",
  "Singapore",
  "South Africa",
  "South Korea",
  "Spain",
  "Sri Lanka",
  "Sweden",
  "Switzerland",
  "Thailand",
  "Turkey",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "United States",
  "Vietnam"
];

const degreeLevels = ["Bachelor", "Master", "PhD"];
const accommodationTypes = ["Dorm", "Shared", "Private"];
const mentorTypes = ["Student", "Parent", "Professor"];
const menteeTypes = ["Student", "Parent"];

// Custom menu properties to increase dropdown length
const longerDropdownProps = {
  PaperProps: {
    style: {
      maxHeight: 400 // Increases the visible dropdown box height
    }
  }
};

const mentorExperienceLabels = {
  visa_experience: "Visa & Immigration",
  housing_experience: "Finding Housing",
  cultural_adaptation_experience: "Cultural Adjustment",
  career_guidance_experience: "Career & Internships"
};

const menteeConcernLabels = {
  scholarship_interest: "Looking for Scholarships",
  work_while_studying_interest: "Working While Studying",
  concern_visa: "Visa & Immigration",
  concern_accommodation: "Finding Accommodation",
  concern_safety: "Campus & City Safety",
  concern_academics: "Academic Expectations",
  concern_career: "Career Opportunities",
  concern_culture: "Cultural Adjustment"
};

const validationSchema = Yup.object({
  role: Yup.string().required("Please select a role"),

  firstName: Yup.string().trim().required("First name required"),

  lastName: Yup.string().trim().required("Last name required"),

  field_of_study: Yup.string().when("role", {
    is: "Mentor",
    then: (s) => s.required("Field of study required")
  }),

  degree_level: Yup.string().required("Degree level required"),

  /* -------------------- MENTOR VALIDATION -------------------- */

  mentor_type: Yup.string().when("role", {
    is: "Mentor",
    then: (s) => s.required("Mentor type required")
  }),

  university: Yup.string().when("role", {
    is: "Mentor",
    then: (s) => s.required("University required")
  }),

  years_in_country: Yup.number()
    .typeError("Must be a number")
    .when("role", {
      is: "Mentor",
      then: (s) =>
        s.min(0, "Must be 0 or more").required("Years in country required")
    }),

  languages_spoken: Yup.string().when("role", {
    is: "Mentor",
    then: (s) => s.required("Languages required")
  }),

  availability_hours_per_week: Yup.number()
    .typeError("Must be a number")
    .when("role", {
      is: "Mentor",
      then: (s) => s.min(1, "Minimum 1 hour").required("Availability required")
    }),

  graduation_year: Yup.number()
    .typeError("Must be a number")
    .when("role", {
      is: "Mentor",
      then: (s) =>
        s
          .min(1990, "Invalid year")
          .max(2100, "Invalid year")
          .required("Graduation year required")
    }),

  /* -------------------- EXPERIENCE SWITCHES -------------------- */

  visa_experience: Yup.boolean(),

  housing_experience: Yup.boolean(),

  cultural_adaptation_experience: Yup.boolean(),

  career_guidance_experience: Yup.boolean(),

  /* -------------------- SYSTEM FIELDS -------------------- */

  sessions_completed: Yup.number().min(0).default(0),

  response_time_hours: Yup.number().min(1).default(24),

  mentor_rating: Yup.number().min(0).max(5).default(0),

  /* -------------------- MENTEE VALIDATION -------------------- */

  home_country: Yup.string().when("role", {
    is: "Mentee",
    then: (s) => s.required("Home country required")
  }),

  intended_start_year: Yup.number()
    .typeError("Must be a number")
    .when("role", {
      is: "Mentee",
      then: (s) => s.required("Start year required")
    }),

  preferred_language: Yup.string().when("role", {
    is: "Mentee",
    then: (s) => s.required("Preferred language required")
  })
});

const initialValues = {
  profileImage: null,
  role: "Mentee",
  firstName: "",
  lastName: "",
  field_of_study: "",
  degree_level: "",

  mentor_type: "",
  university: "",
  years_in_country: "",
  languages_spoken: "",
  availability_hours_per_week: "",
  graduation_year: "",
  visa_experience: false,
  housing_experience: false,
  cultural_adaptation_experience: false,
  career_guidance_experience: false,
  mentee_type: "",
  home_country: "",
  target_university: "",
  intended_start_year: "",
  preferred_language: "",
  accommodation_type: "",
  scholarship_interest: false,
  work_while_studying_interest: false,
  concern_visa: false,
  concern_accommodation: false,
  concern_safety: false,
  concern_academics: false,
  concern_career: false,
  concern_culture: false
};

const SectionTitle = ({ children }) => (
  <Typography
    variant="h6"
    sx={{
      mt: 5,
      mb: 3,
      fontWeight: 700,
      fontFamily: "Playfair Display",
      color: "primary.main"
    }}
  >
    {children}
  </Typography>
);
export const mapApiToFormik = (data) => {
  if (!data) {
    return initialValues;
  }
  const mentor = data?.mentor || {};
  const mentee = data?.mentee || {};

  return {
    ...initialValues,
    profileImage: null,

    role: mentor ? "Mentor" : "Mentee",

    firstName: data?.first_name || mentor?.first_name || "",
    lastName: data?.last_name || mentor?.last_name || "",

    field_of_study: mentor?.field_of_study || mentee?.field_of_study || "",
    degree_level: mentor?.degree_level || mentee?.degree_level || "",

    /* Mentor fields */
    mentor_type: mentor?.mentor_type || "",
    university: mentor?.university || "",
    years_in_country: mentor?.years_in_country || "",
    languages_spoken: mentor?.languages_spoken || "",
    availability_hours_per_week: mentor?.availability_hours_per_week || "",
    graduation_year: mentor?.graduation_year || "",

    visa_experience: Boolean(mentor?.visa_experience),
    housing_experience: Boolean(mentor?.housing_experience),
    cultural_adaptation_experience: Boolean(
      mentor?.cultural_adaptation_experience
    ),
    career_guidance_experience: Boolean(mentor?.career_guidance_experience),

    /* Mentee fields */
    mentee_type: mentee?.user_type || "",
    home_country: mentee?.home_country || "",
    target_university: mentee?.preferred_destination_country || "",
    intended_start_year: "",
    preferred_language: mentee?.preferred_language || "",

    accommodation_type: "",
    scholarship_interest: false,
    work_while_studying_interest: false,

    concern_visa: false,
    concern_accommodation: false,
    concern_safety: false,
    concern_academics: false,
    concern_career: false,
    concern_culture: false
  };
};

export default function RegisterPage() {
  const [imagePreview, setImagePreview] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  const userId = useSelector((state) => state.auth.user?.user_id);
  const { data: profileData, isLoading, isError } = useProfile();
  console.log("Mapped Form Values:", mapApiToFormik(profileData));
  const updateProfile = useUpdateProfile();

  if (isLoading) {
    return <Typography>Loading profile...</Typography>;
  }

  if (isError) {
    console.warn("Profile API failed, using default values");
  }
  const handleSubmit = (values) => {
    const payload = {
      user_id: userId,
      first_name: values.first_name,
      last_name: values.last_name,
      user_type: values.role === "Mentor" ? "mentor" : "mentee",
      email: values.email,
      mentor: null,
      mentee: null
    };

    if (values.role === "Mentor") {
      payload.mentor = {
        first_name: values.firstName,
        last_name: values.lastName,
        mentor_type: values.mentor_type,
        university: values.university,
        field_of_study: values.field_of_study,
        degree_level: values.degree_level,
        languages_spoken: values.languages_spoken,

        years_in_country: Number(values.years_in_country),
        availability_hours_per_week: Number(values.availability_hours_per_week),
        graduation_year: Number(values.graduation_year),

        visa_experience: values.visa_experience ? 1 : 0,
        housing_experience: values.housing_experience ? 1 : 0,
        cultural_adaptation_experience: values.cultural_adaptation_experience
          ? 1
          : 0,
        career_guidance_experience: values.career_guidance_experience ? 1 : 0,

        sessions_completed: 0,
        response_time_hours: 24,
        mentor_rating: 0
      };
    } else {
      payload.mentee = {
        user_type: values.mentee_type,
        home_country: values.home_country,
        preferred_destination_country: values.target_university,
        field_of_study: values.field_of_study,
        degree_level: values.degree_level,
        preferred_language: values.preferred_language
      };
    }

    updateProfile.mutate(payload, {
      onSuccess: () => {
        toast.success(
          "🎉 Profile updated successfully! Your information is now saved.", { duration: 5000 }
        );
      },
      onError: () => {
        toast.error(
          "⚠️ We couldn't update your profile right now. Please check your information and try again.", { duration: 5000 }
        );
      }
    });

    console.log("Formatted DB Payload:", payload);
  };

  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        minHeight: "100vh",
        pt: 8,
        pb: 10
      }}
    >
      <Container maxWidth="md">
        <Paper
          elevation={0}
          sx={{
            p: { xs: 3, sm: 6 },
            border: "1px solid",
            borderColor: "divider",
            borderRadius: 4
          }}
        >
          <Formik
            initialValues={
              profileData ? mapApiToFormik(profileData) : initialValues
            }
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
            enableReinitialize
          >
            {({ values, handleChange, errors, touched, setFieldValue }) => (
              <Form>
                {/* ROLE SELECTION */}
                <Box
                  display="flex"
                  flexDirection="column"
                  alignItems="center"
                  mb={4}
                >
                  <Typography
                    variant="overline"
                    color="text.secondary"
                    sx={{ letterSpacing: 2, mb: 2 }}
                  >
                    I am registering as a:
                  </Typography>
                  <ToggleButtonGroup
                    color="primary"
                    value={values.role}
                    exclusive
                    onChange={(e, newRole) => {
                      if (newRole !== null) setFieldValue("role", newRole);
                    }}
                    sx={{ mb: 4 }}
                  >
                    <ToggleButton
                      value="Mentee"
                      sx={{ px: { xs: 2, sm: 4 }, py: 1.5, fontWeight: 600 }}
                    >
                      Student / Mentee
                    </ToggleButton>
                    <ToggleButton
                      value="Mentor"
                      sx={{ px: { xs: 2, sm: 4 }, py: 1.5, fontWeight: 600 }}
                    >
                      Guide / Mentor
                    </ToggleButton>
                  </ToggleButtonGroup>

                  {/* PROFILE IMAGE */}
                  <Box position="relative">
                    <Avatar
                      src={imagePreview}
                      onClick={() => setModalOpen(true)}
                      sx={{
                        width: 100,
                        height: 100,
                        cursor: "pointer",
                        bgcolor: "primary.dark",
                        border: "2px solid",
                        borderColor: "primary.main",
                        "&:hover": { opacity: 0.8 },
                        transition: "0.2s"
                      }}
                    />
                  </Box>
                </Box>

                <Divider sx={{ my: 4 }} />

                {/* BASIC INFO */}
                <SectionTitle>Basic Information</SectionTitle>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="First Name"
                      name="firstName"
                      value={values.firstName}
                      onChange={handleChange}
                      error={touched.firstName && Boolean(errors.firstName)}
                      helperText={touched.firstName && errors.firstName}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Last Name"
                      name="lastName"
                      value={values.lastName}
                      onChange={handleChange}
                      error={touched.lastName && Boolean(errors.lastName)}
                      helperText={touched.lastName && errors.lastName}
                      fullWidth
                    />
                  </Grid>

                  {/* Field of Study: Full width to give ample room for long major names */}
                  <Grid item xs={12}>
                    <TextField
                      label="Field of Study (e.g., Computer Science)"
                      name="field_of_study"
                      value={values.field_of_study}
                      onChange={handleChange}
                      fullWidth
                    />
                  </Grid>

                  {/* Degree Level: Full width to ensure label never cuts off */}
                  <Grid item xs={12}>
                    <TextField
                      select
                      label="Degree Level"
                      name="degree_level"
                      value={values.degree_level}
                      onChange={handleChange}
                      sx={{ width: 200 }}
                      error={
                        touched.degree_level && Boolean(errors.degree_level)
                      }
                      helperText={touched.degree_level && errors.degree_level}
                      SelectProps={{ MenuProps: longerDropdownProps }}
                    >
                      {degreeLevels.map((lvl) => (
                        <MenuItem key={lvl} value={lvl}>
                          {lvl}
                        </MenuItem>
                      ))}
                    </TextField>
                  </Grid>
                </Grid>

                {/* MENTOR SPECIFIC */}
                {values.role === "Mentor" && (
                  <>
                    <SectionTitle>Mentorship Details</SectionTitle>
                    <Grid container spacing={3}>
                      <Grid item xs={12}>
                        <TextField
                          label="Current University"
                          name="university"
                          value={values.university}
                          onChange={handleChange}
                          fullWidth
                          error={
                            touched.university && Boolean(errors.university)
                          }
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          select
                          label="Mentor Type"
                          name="mentor_type"
                          value={values.mentor_type}
                          onChange={handleChange}
                          error={
                            touched.mentor_type && Boolean(errors.mentor_type)
                          }
                          helperText={touched.mentor_type && errors.mentor_type}
                          sx={{ width: 150 }}
                        >
                          {mentorTypes.map((type) => (
                            <MenuItem key={type} value={type}>
                              {type}
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          label="Languages Spoken"
                          name="languages_spoken"
                          placeholder="e.g. English, Hindi"
                          value={values.languages_spoken}
                          onChange={handleChange}
                          fullWidth
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <TextField
                          label="Years in Country"
                          name="years_in_country"
                          type="number"
                          value={values.years_in_country}
                          onChange={handleChange}
                          fullWidth
                          error={
                            touched.years_in_country &&
                            Boolean(errors.years_in_country)
                          }
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <TextField
                          label="Graduation Year"
                          name="graduation_year"
                          type="number"
                          value={values.graduation_year}
                          onChange={handleChange}
                          fullWidth
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <TextField
                          label="Hours/Week Free"
                          name="availability_hours_per_week"
                          type="number"
                          value={values.availability_hours_per_week}
                          onChange={handleChange}
                          fullWidth
                          error={
                            touched.availability_hours_per_week &&
                            Boolean(errors.availability_hours_per_week)
                          }
                        />
                      </Grid>
                    </Grid>

                    <SectionTitle>Areas of Expertise</SectionTitle>
                    <Typography variant="body2" color="text.secondary" mb={3}>
                      Toggle the topics you can help students with:
                    </Typography>
                    <Grid container spacing={2}>
                      {Object.entries(mentorExperienceLabels).map(
                        ([key, label]) => (
                          <Grid item xs={12} sm={6} key={key}>
                            <FormControlLabel
                              control={
                                <Switch
                                  checked={values[key]}
                                  onChange={(e) =>
                                    setFieldValue(key, e.target.checked)
                                  }
                                  color="primary"
                                />
                              }
                              label={
                                <Typography variant="body1">{label}</Typography>
                              }
                              sx={{ wordBreak: "break-word" }}
                            />
                          </Grid>
                        )
                      )}
                    </Grid>
                  </>
                )}

                {/* MENTEE SPECIFIC */}
                {values.role === "Mentee" && (
                  <>
                    <SectionTitle>Study Plans</SectionTitle>
                    <Grid container spacing={3}>
                      {/* Home Country: Full width */}
                      <Grid item xs={12}>
                        <Autocomplete
                          options={countries}
                          value={values.home_country || null}
                          onChange={(e, value) =>
                            setFieldValue("home_country", value || "")
                          }
                          sx={{ width: 300 }}
                          ListboxProps={{ style: { maxHeight: 400 } }}
                          renderInput={(params) => (
                            <TextField
                              {...params}
                              label="Home Country"
                              error={
                                touched.home_country &&
                                Boolean(errors.home_country)
                              }
                            />
                          )}
                        />
                      </Grid>

                      {/* Target University: Full width */}
                      <Grid item xs={12}>
                        <TextField
                          label="Target University"
                          name="target_university"
                          value={values.target_university}
                          onChange={handleChange}
                          fullWidth
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          select
                          label="Mentee Type"
                          name="mentee_type"
                          value={values.mentee_type}
                          onChange={handleChange}
                          sx={{ width: 150 }}
                        >
                          {menteeTypes.map((type) => (
                            <MenuItem key={type} value={type}>
                              {type}
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>
                      {/* Housing Type: 50% width */}
                      <Grid item xs={12} sm={6}>
                        <TextField
                          select
                          label="Housing Type"
                          name="accommodation_type"
                          value={values.accommodation_type}
                          sx={{ width: 200 }}
                          onChange={handleChange}
                          fullWidth
                          SelectProps={{ MenuProps: longerDropdownProps }}
                        >
                          {accommodationTypes.map((type) => (
                            <MenuItem key={type} value={type}>
                              {type}
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>

                      {/* Start Year: 50% width */}
                      <Grid item xs={12} sm={6}>
                        <TextField
                          label="Intended Start Year"
                          name="intended_start_year"
                          type="number"
                          value={values.intended_start_year}
                          onChange={handleChange}
                          sx={{ width: 200 }}
                          error={
                            touched.intended_start_year &&
                            Boolean(errors.intended_start_year)
                          }
                        />
                      </Grid>

                      {/* Preferred Language: Full width */}
                      <Grid item xs={12} sm={14}>
                        <TextField
                          label="Preferred Language for Guidance"
                          name="preferred_language"
                          value={values.preferred_language}
                          sx={{ width: 250 }}
                          onChange={handleChange}
                        />
                      </Grid>
                    </Grid>

                    <SectionTitle>Primary Concerns</SectionTitle>
                    <Typography variant="body2" color="text.secondary" mb={3}>
                      Toggle the areas where you need guidance:
                    </Typography>
                    <Grid container spacing={2}>
                      {Object.entries(menteeConcernLabels).map(
                        ([key, label]) => (
                          <Grid item xs={12} sm={6} key={key}>
                            <FormControlLabel
                              control={
                                <Switch
                                  checked={values[key]}
                                  onChange={(e) =>
                                    setFieldValue(key, e.target.checked)
                                  }
                                  color="primary"
                                />
                              }
                              label={
                                <Typography variant="body1">{label}</Typography>
                              }
                              sx={{ wordBreak: "break-word" }}
                            />
                          </Grid>
                        )
                      )}
                    </Grid>
                  </>
                )}

                {/* SUBMIT */}
                <Box textAlign="center" mt={6}>
                  <Button
                    type="submit"
                    size="large"
                    variant="contained"
                    disabled={updateProfile.isPending}
                  >
                    {updateProfile.isPending ? "Saving..." : "Update Profile"}
                  </Button>
                </Box>
              </Form>
            )}
          </Formik>
        </Paper>
      </Container>
    </Box>
  );
}
