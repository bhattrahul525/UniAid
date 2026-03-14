import { Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import CityPage from "./pages/City";
import DashboardPage from "./pages/DashboardPage";
import ForumPage from "./pages/ForumPage";
import GlobePage from "./pages/Globe";
import Landing from "./pages/Landing";
import LoginPage from "./pages/LoginPage";
import MentorDetails from "./pages/MentorDetails";
import MentorshipPage from "./pages/MentoringPage";
import Profile from "./pages/ProfilePage";
import RegistrationPage from "./pages/RegistrationPage";
import RootLayout from "./pages/RootLayout";
import SessionsGridPage from "./pages/SessionPage";
import ProtectedRoute from "./routes/ProtectedRouter";
import PublicRoute from "./routes/PublicRoute";

function App() {
 
  return (
    <Routes>
      {/* PUBLIC ROUTES */}

      <Route
        path="/"
        element={
          <PublicRoute>
            <Landing />
          </PublicRoute>
        }
      />

      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        }
      />

      <Route
        path="/register"
        element={
          <PublicRoute>
            <RegistrationPage />
          </PublicRoute>
        }
      />

      {/* PROTECTED ROUTES */}

      <Route
        element={
          <ProtectedRoute>
            <RootLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/forum" element={<ForumPage />} />
        <Route path="/mentorship" element={<MentorshipPage />} />
        <Route path="/mentor/:slug" element={<MentorDetails />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/city-info" element={<GlobePage />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/city/:city" element={<CityPage />} />
        <Route path="/sessions" element={<SessionsGridPage />} />
      </Route>
    </Routes>
  );
}

export default App;
