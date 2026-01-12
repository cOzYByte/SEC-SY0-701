import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Target, Lightning, Brain, ArrowRight, Moon, Sun } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { useTheme } from '../context/ThemeContext';
import AuthModal from '../components/AuthModal';

const Landing = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login');

  const features = [
    {
      icon: <Target weight="duotone" className="w-8 h-8" />,
      title: 'PRACTICE MODE',
      description: 'Immediate feedback with detailed explanations for every question.'
    },
    {
      icon: <Lightning weight="duotone" className="w-8 h-8" />,
      title: 'EXAM SIMULATION',
      description: 'Timed 90-question exams mimicking the real SY0-701 experience.'
    },
    {
      icon: <Brain weight="duotone" className="w-8 h-8" />,
      title: 'FLASHCARD MODE',
      description: 'Quick review of concepts with flip-card style learning.'
    },
    {
      icon: <Shield weight="duotone" className="w-8 h-8" />,
      title: 'PROGRESS TRACKING',
      description: 'Per-domain analytics, weak area identification, and study streaks.'
    }
  ];

  const handleGetStarted = (mode) => {
    setAuthMode(mode);
    setShowAuth(true);
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2 shrink-0">
            <Shield weight="duotone" className="w-6 h-6 sm:w-8 sm:h-8 text-primary" />
            <span className="font-mono font-bold text-base sm:text-xl tracking-tight whitespace-nowrap">SEC <span className="text-primary">SY0-701</span></span>
          </div>
          <div className="flex items-center gap-2 sm:gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              data-testid="theme-toggle"
              className="h-8 w-8 sm:h-10 sm:w-10"
            >
              {theme === 'dark' ? <Sun weight="duotone" className="w-4 h-4 sm:w-5 sm:h-5" /> : <Moon weight="duotone" className="w-4 h-4 sm:w-5 sm:h-5" />}
            </Button>
            <Button
              variant="ghost"
              onClick={() => handleGetStarted('login')}
              data-testid="login-btn"
              className="font-mono text-xs sm:text-sm tracking-wider px-2 sm:px-4"
            >
              LOGIN
            </Button>
            <Button
              onClick={() => handleGetStarted('register')}
              data-testid="register-btn"
              className="font-mono text-xs sm:text-sm tracking-wider glow-primary px-2 sm:px-4"
            >
              GET STARTED
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <p className="font-mono text-primary text-sm tracking-widest">COMPTIA SECURITY+ SY0-701</p>
                <h1 className="font-mono text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tighter leading-tight">
                  MASTER YOUR<br />
                  <span className="text-primary">SECURITY+</span><br />
                  CERTIFICATION
                </h1>
                <p className="text-muted-foreground text-lg max-w-lg">
                  A tactical study platform designed for focused preparation. Practice questions, exam simulations, and progress tracking—all in one place.
                </p>
              </div>
              <div className="flex flex-wrap gap-4">
                <Button
                  size="lg"
                  onClick={() => handleGetStarted('register')}
                  data-testid="hero-cta"
                  className="font-mono tracking-wider glow-primary"
                >
                  START STUDYING
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => handleGetStarted('login')}
                  data-testid="hero-login"
                  className="font-mono tracking-wider"
                >
                  CONTINUE PROGRESS
                </Button>
              </div>
              <div className="flex gap-8 pt-4">
                <div>
                  <p className="font-mono text-3xl font-bold tracking-tighter text-primary">880+</p>
                  <p className="text-muted-foreground text-sm">Practice Questions</p>
                </div>
                <div>
                  <p className="font-mono text-3xl font-bold tracking-tighter text-primary">5</p>
                  <p className="text-muted-foreground text-sm">Exam Domains</p>
                </div>
                <div>
                  <p className="font-mono text-3xl font-bold tracking-tighter text-primary">100%</p>
                  <p className="text-muted-foreground text-sm">Coverage</p>
                </div>
              </div>
            </div>
            <div className="relative hidden lg:block">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-transparent rounded-3xl" />
              <img
                src="https://images.unsplash.com/photo-1669052700037-db884b37b2d9?crop=entropy&cs=srgb&fm=jpg&q=85&w=800"
                alt="Cybersecurity"
                className="rounded-3xl opacity-80"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-card/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="font-mono text-primary text-sm tracking-widest mb-4">FEATURES</p>
            <h2 className="font-mono text-3xl sm:text-4xl font-bold tracking-tight">
              EVERYTHING YOU NEED TO PASS
            </h2>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="relative p-6 bg-card border border-border rounded-lg card-hover corner-accent"
              >
                <div className="text-primary mb-4">{feature.icon}</div>
                <h3 className="font-mono font-bold text-sm tracking-wider mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Domains Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="font-mono text-primary text-sm tracking-widest mb-4">SY0-701 EXAM DOMAINS</p>
            <h2 className="font-mono text-3xl sm:text-4xl font-bold tracking-tight">
              COMPREHENSIVE COVERAGE
            </h2>
          </div>
          <div className="space-y-4">
            {[
              { name: 'General Security Concepts', weight: 12 },
              { name: 'Threats, Vulnerabilities & Mitigations', weight: 22 },
              { name: 'Security Architecture', weight: 18 },
              { name: 'Security Operations', weight: 28 },
              { name: 'Security Program Management', weight: 20 }
            ].map((domain, index) => (
              <div key={index} className="flex items-center gap-4 p-4 bg-card border border-border rounded-lg">
                <span className="font-mono text-primary font-bold w-8">{index + 1}.</span>
                <span className="flex-1 font-medium">{domain.name}</span>
                <div className="w-32 h-3 bg-secondary rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary rounded-full"
                    style={{ width: `${domain.weight * 3}%` }}
                  />
                </div>
                <span className="font-mono text-muted-foreground w-12 text-right">{domain.weight}%</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-card/50">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="font-mono text-3xl sm:text-4xl font-bold tracking-tight mb-6">
            READY TO GET <span className="text-primary">CERTIFIED</span>?
          </h2>
          <p className="text-muted-foreground text-lg mb-8">
            Join thousands of IT professionals who passed their Security+ exam using our tactical study approach.
          </p>
          <Button
            size="lg"
            onClick={() => handleGetStarted('register')}
            data-testid="cta-btn"
            className="font-mono tracking-wider glow-primary"
          >
            CREATE FREE ACCOUNT
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-border">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Shield weight="duotone" className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold">SEC SY0-701</span>
          </div>
          <p className="text-muted-foreground text-sm">
            CompTIA Security+ SY0-701 Study Platform
          </p>
        </div>
      </footer>

      {/* Auth Modal */}
      <AuthModal
        open={showAuth}
        onClose={() => setShowAuth(false)}
        initialMode={authMode}
      />
    </div>
  );
};

export default Landing;
