import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Shield, Target, Lightning, Brain, TrendingUp, Fire, Trophy, ChartBar, SignOut, Moon, Sun, CaretRight, Atom } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Progress } from '../components/ui/progress';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [progress, setProgress] = useState(null);
  const [weakAreas, setWeakAreas] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [progressRes, weakRes, historyRes] = await Promise.all([
        axios.get(`${API}/progress`),
        axios.get(`${API}/progress/weak-areas`),
        axios.get(`${API}/progress/history`)
      ]);
      setProgress(progressRes.data);
      setWeakAreas(weakRes.data);
      setHistory(historyRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const domains = [
    { id: 1, name: 'General Security Concepts', weight: 12 },
    { id: 2, name: 'Threats & Vulnerabilities', weight: 22 },
    { id: 3, name: 'Security Architecture', weight: 18 },
    { id: 4, name: 'Security Operations', weight: 28 },
    { id: 5, name: 'Program Management', weight: 20 }
  ];

  const getDomainAccuracy = (domainId) => {
    const area = weakAreas.find(a => a.domain === domainId);
    return area ? area.accuracy : 0;
  };

  const getReadinessScore = () => {
    if (!progress || progress.total_questions_answered === 0) return 0;
    return Math.round(progress.accuracy);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Shield weight="duotone" className="w-16 h-16 text-primary animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield weight="duotone" className="w-8 h-8 text-primary" />
            <span className="font-mono font-bold text-xl tracking-tight">SEC <span className="text-primary">SY0-701</span></span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground hidden sm:block">Welcome, {user?.name}</span>
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              data-testid="dashboard-theme-toggle"
            >
              {theme === 'dark' ? <Sun weight="duotone" className="w-5 h-5" /> : <Moon weight="duotone" className="w-5 h-5" />}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
              data-testid="logout-btn"
            >
              <SignOut weight="duotone" className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Readiness Score */}
          <Card className="col-span-2 row-span-2 relative overflow-hidden corner-accent" data-testid="readiness-card">
            <CardHeader>
              <CardTitle className="font-mono text-sm tracking-wider text-muted-foreground">EXAM READINESS</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center justify-center pb-8">
              <div className="relative w-48 h-48 mb-4">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="96"
                    cy="96"
                    r="88"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="8"
                    className="text-secondary"
                  />
                  <circle
                    cx="96"
                    cy="96"
                    r="88"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="8"
                    strokeDasharray={`${getReadinessScore() * 5.53} 553`}
                    className="text-primary transition-all duration-1000"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center flex-col">
                  <span className="font-mono text-5xl font-bold tracking-tighter" data-testid="readiness-score">
                    {getReadinessScore()}%
                  </span>
                  <span className="text-muted-foreground text-sm">Ready</span>
                </div>
              </div>
              <p className="text-muted-foreground text-center text-sm">
                Based on {progress?.total_questions_answered || 0} questions answered
              </p>
            </CardContent>
          </Card>

          {/* Stats Cards */}
          <Card className="corner-accent" data-testid="questions-card">
            <CardHeader className="pb-2">
              <CardTitle className="font-mono text-xs tracking-wider text-muted-foreground">QUESTIONS</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-mono text-3xl font-bold tracking-tighter" data-testid="total-questions">
                {progress?.total_questions_answered || 0}
              </p>
              <p className="text-muted-foreground text-sm">Answered</p>
            </CardContent>
          </Card>

          <Card className="corner-accent" data-testid="accuracy-card">
            <CardHeader className="pb-2">
              <CardTitle className="font-mono text-xs tracking-wider text-muted-foreground">ACCURACY</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-mono text-3xl font-bold tracking-tighter text-primary" data-testid="accuracy-value">
                {progress?.accuracy || 0}%
              </p>
              <p className="text-muted-foreground text-sm">Correct Rate</p>
            </CardContent>
          </Card>

          <Card className="corner-accent" data-testid="streak-card">
            <CardHeader className="pb-2">
              <CardTitle className="font-mono text-xs tracking-wider text-muted-foreground">STREAK</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Fire weight="duotone" className="w-6 h-6 text-accent" />
                <p className="font-mono text-3xl font-bold tracking-tighter" data-testid="streak-value">
                  {progress?.current_streak || 0}
                </p>
              </div>
              <p className="text-muted-foreground text-sm">Days</p>
            </CardContent>
          </Card>

          <Card className="corner-accent" data-testid="best-streak-card">
            <CardHeader className="pb-2">
              <CardTitle className="font-mono text-xs tracking-wider text-muted-foreground">BEST STREAK</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Trophy weight="duotone" className="w-6 h-6 text-accent" />
                <p className="font-mono text-3xl font-bold tracking-tighter" data-testid="best-streak-value">
                  {progress?.longest_streak || 0}
                </p>
              </div>
              <p className="text-muted-foreground text-sm">Days</p>
            </CardContent>
          </Card>
        </div>

        {/* Study Modes */}
        <div className="mb-8">
          <h2 className="font-mono text-lg font-bold tracking-tight mb-4">STUDY MODES</h2>
          <div className="grid sm:grid-cols-3 gap-4">
            <Button
              variant="outline"
              className="h-auto p-6 flex flex-col items-start gap-3 justify-start card-hover"
              onClick={() => navigate('/practice')}
              data-testid="practice-mode-btn"
            >
              <Target weight="duotone" className="w-8 h-8 text-primary" />
              <div className="text-left">
                <p className="font-mono font-bold tracking-wider">PRACTICE</p>
                <p className="text-muted-foreground text-sm font-sans">Immediate feedback</p>
              </div>
              <CaretRight className="w-5 h-5 ml-auto" />
            </Button>

            <Button
              variant="outline"
              className="h-auto p-6 flex flex-col items-start gap-3 justify-start card-hover"
              onClick={() => navigate('/exam')}
              data-testid="exam-mode-btn"
            >
              <Lightning weight="duotone" className="w-8 h-8 text-accent" />
              <div className="text-left">
                <p className="font-mono font-bold tracking-wider">EXAM SIM</p>
                <p className="text-muted-foreground text-sm font-sans">Timed simulation</p>
              </div>
              <CaretRight className="w-5 h-5 ml-auto" />
            </Button>

            <Button
              variant="outline"
              className="h-auto p-6 flex flex-col items-start gap-3 justify-start card-hover"
              onClick={() => navigate('/flashcards')}
              data-testid="flashcard-mode-btn"
            >
              <Brain weight="duotone" className="w-8 h-8 text-chart-3" />
              <div className="text-left">
                <p className="font-mono font-bold tracking-wider">FLASHCARDS</p>
                <p className="text-muted-foreground text-sm font-sans">Quick review</p>
              </div>
              <CaretRight className="w-5 h-5 ml-auto" />
            </Button>
          </div>
        </div>

        {/* Domain Progress */}
        <div className="grid lg:grid-cols-2 gap-8">
          <Card className="corner-accent" data-testid="domain-progress-card">
            <CardHeader>
              <CardTitle className="font-mono text-sm tracking-wider flex items-center gap-2">
                <ChartBar weight="duotone" className="w-5 h-5 text-primary" />
                DOMAIN PROGRESS
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {domains.map((domain) => {
                const accuracy = getDomainAccuracy(domain.id);
                const area = weakAreas.find(a => a.domain === domain.id);
                return (
                  <div key={domain.id} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-mono text-xs tracking-wider text-muted-foreground">
                        DOMAIN {domain.id}
                      </span>
                      <span className="font-mono text-xs">
                        {area?.answered || 0} Q • {accuracy}%
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <Progress value={accuracy} className="h-3 flex-1" />
                    </div>
                    <p className="text-sm truncate">{domain.name}</p>
                  </div>
                );
              })}
            </CardContent>
          </Card>

          {/* Weak Areas */}
          <Card className="corner-accent" data-testid="weak-areas-card">
            <CardHeader>
              <CardTitle className="font-mono text-sm tracking-wider flex items-center gap-2">
                <TrendUp weight="duotone" className="w-5 h-5 text-destructive" />
                WEAK AREAS
              </CardTitle>
            </CardHeader>
            <CardContent>
              {weakAreas.length > 0 ? (
                <div className="space-y-4">
                  {weakAreas.filter(area => area.accuracy < 70).slice(0, 3).map((area, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                      <div>
                        <p className="font-medium text-sm">{area.domain_name}</p>
                        <p className="text-muted-foreground text-xs">
                          {area.correct}/{area.answered} correct
                        </p>
                      </div>
                      <span className={`font-mono text-sm font-bold ${area.accuracy < 50 ? 'text-destructive' : 'text-accent'}`}>
                        {area.accuracy}%
                      </span>
                    </div>
                  ))}
                  {weakAreas.filter(area => area.accuracy < 70).length === 0 && (
                    <p className="text-muted-foreground text-center py-8">
                      Great job! No weak areas detected.
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-muted-foreground text-center py-8">
                  Complete some practice questions to see your weak areas.
                </p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        {history.length > 0 && (
          <Card className="mt-8 corner-accent" data-testid="history-card">
            <CardHeader>
              <CardTitle className="font-mono text-sm tracking-wider">RECENT SESSIONS</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {history.slice(0, 5).map((session, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                    <div className="flex items-center gap-3">
                      {session.mode === 'practice' && <Target weight="duotone" className="w-5 h-5 text-primary" />}
                      {session.mode === 'exam' && <Lightning weight="duotone" className="w-5 h-5 text-accent" />}
                      {session.mode === 'flashcard' && <Brain weight="duotone" className="w-5 h-5 text-chart-3" />}
                      <div>
                        <p className="font-mono text-sm uppercase">{session.mode}</p>
                        <p className="text-muted-foreground text-xs">
                          {new Date(session.date).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-mono text-sm">
                        {session.correct_answers}/{session.total_questions}
                      </p>
                      <p className={`text-xs ${Math.round((session.correct_answers / session.total_questions) * 100) >= 70 ? 'text-primary' : 'text-destructive'}`}>
                        {Math.round((session.correct_answers / session.total_questions) * 100)}%
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
