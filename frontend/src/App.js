import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import { Toaster } from "./components/ui/sonner";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Practice from "./pages/Practice";
import Exam from "./pages/Exam";
import Flashcards from "./pages/Flashcards";
import Results from "./pages/Results";

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }
  
  if (!user) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }
  
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<PublicRoute><Landing /></PublicRoute>} />
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/practice" element={<ProtectedRoute><Practice /></ProtectedRoute>} />
      <Route path="/exam" element={<ProtectedRoute><Exam /></ProtectedRoute>} />
      <Route path="/flashcards" element={<ProtectedRoute><Flashcards /></ProtectedRoute>} />
      <Route path="/results" element={<ProtectedRoute><Results /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="App">
          <div className="noise-overlay" />
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
          <Toaster />
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
