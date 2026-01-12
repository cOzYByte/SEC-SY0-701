import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ArrowLeft, ArrowsClockwise, CaretLeft, CaretRight, Eye, EyeSlash } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const Flashcards = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [domain, setDomain] = useState('all');
  const [cardCount, setCardCount] = useState('20');
  const [started, setStarted] = useState(false);
  const [knownCards, setKnownCards] = useState(new Set());

  const fetchFlashcards = async () => {
    setLoading(true);
    try {
      const params = { count: parseInt(cardCount) };
      if (domain !== 'all') params.domain = parseInt(domain);
      const response = await axios.get(`${API}/questions/flashcards`, { params });
      setQuestions(response.data);
      setCurrentIndex(0);
      setFlipped(false);
      setKnownCards(new Set());
      setStarted(true);
    } catch (error) {
      console.error('Failed to fetch flashcards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFlip = () => {
    setFlipped(!flipped);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setFlipped(false);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      setFlipped(false);
    }
  };

  const markKnown = () => {
    setKnownCards(prev => new Set([...prev, questions[currentIndex].id]));
    handleNext();
  };

  const finishFlashcards = async () => {
    try {
      const submission = {
        answers: questions.map(q => ({
          question_id: q.id,
          selected_answer: knownCards.has(q.id) ? q.correct_answer : '',
          time_taken: 0
        })),
        mode: 'flashcard',
        total_time: 0
      };
      await axios.post(`${API}/progress/submit`, submission);
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to submit:', error);
      navigate('/dashboard');
    }
  };

  const currentCard = questions[currentIndex];
  const progressPercent = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;

  if (!started) {
    return (
      <div className="min-h-screen bg-background">
        <header className="sticky top-0 z-50 glass border-b border-border">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="back-btn">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div className="flex items-center gap-3">
              <Shield weight="duotone" className="w-6 h-6 text-chart-3" />
              <span className="font-mono font-bold text-lg tracking-tight">FLASHCARD MODE</span>
            </div>
          </div>
        </header>

        <main className="max-w-2xl mx-auto px-6 py-12">
          <Card className="corner-accent">
            <CardHeader>
              <CardTitle className="font-mono text-xl tracking-tight">Configure Flashcards</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label className="font-mono text-sm tracking-wider text-muted-foreground">DOMAIN</label>
                <Select value={domain} onValueChange={setDomain} data-testid="fc-domain-select">
                  <SelectTrigger>
                    <SelectValue placeholder="Select domain" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Domains</SelectItem>
                    <SelectItem value="1">Domain 1: General Security Concepts</SelectItem>
                    <SelectItem value="2">Domain 2: Threats & Vulnerabilities</SelectItem>
                    <SelectItem value="3">Domain 3: Security Architecture</SelectItem>
                    <SelectItem value="4">Domain 4: Security Operations</SelectItem>
                    <SelectItem value="5">Domain 5: Program Management</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="font-mono text-sm tracking-wider text-muted-foreground">NUMBER OF CARDS</label>
                <Select value={cardCount} onValueChange={setCardCount} data-testid="fc-count-select">
                  <SelectTrigger>
                    <SelectValue placeholder="Select count" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="10">10 Cards</SelectItem>
                    <SelectItem value="20">20 Cards</SelectItem>
                    <SelectItem value="30">30 Cards</SelectItem>
                    <SelectItem value="50">50 Cards</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                className="w-full font-mono tracking-wider"
                onClick={fetchFlashcards}
                data-testid="start-flashcards-btn"
              >
                START FLASHCARDS
              </Button>
            </CardContent>
          </Card>
        </main>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Shield weight="duotone" className="w-16 h-16 text-chart-3 animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading flashcards...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="exit-flashcards-btn">
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <span className="font-mono font-bold tracking-tight">FLASHCARDS</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="font-mono text-sm text-muted-foreground" data-testid="fc-counter">
                {currentIndex + 1} / {questions.length}
              </span>
              <span className="font-mono text-sm text-primary" data-testid="known-counter">
                {knownCards.size} known
              </span>
            </div>
          </div>
          <Progress value={progressPercent} className="h-2" />
        </div>
      </header>

      {/* Flashcard */}
      <main className="max-w-2xl mx-auto px-6 py-12">
        <AnimatePresence mode="wait">
          <motion.div
            key={`${currentIndex}-${flipped}`}
            initial={{ opacity: 0, rotateY: flipped ? -90 : 90 }}
            animate={{ opacity: 1, rotateY: 0 }}
            exit={{ opacity: 0, rotateY: flipped ? 90 : -90 }}
            transition={{ duration: 0.3 }}
            className="perspective-1000"
          >
            <Card 
              className="min-h-[400px] cursor-pointer corner-accent hover:shadow-lg transition-shadow"
              onClick={handleFlip}
              data-testid="flashcard"
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs tracking-widest text-primary bg-primary/10 px-2 py-1 rounded">
                    DOMAIN {currentCard?.domain}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => { e.stopPropagation(); handleFlip(); }}
                    data-testid="flip-btn"
                  >
                    {flipped ? <EyeSlash className="w-4 h-4 mr-1" /> : <Eye className="w-4 h-4 mr-1" />}
                    {flipped ? 'Hide' : 'Show'} Answer
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center min-h-[300px] text-center">
                {!flipped ? (
                  <div className="space-y-4" data-testid="fc-question">
                    <p className="text-xl font-medium leading-relaxed">{currentCard?.question}</p>
                    <p className="text-muted-foreground text-sm">Click to reveal answer</p>
                  </div>
                ) : (
                  <div className="space-y-6" data-testid="fc-answer">
                    <div className="p-4 bg-primary/10 rounded-lg border border-primary/30">
                      <p className="font-mono text-sm text-primary mb-2">CORRECT ANSWER</p>
                      <p className="text-lg font-medium">
                        {currentCard?.options.find(o => o.id === currentCard.correct_answer)?.text}
                      </p>
                    </div>
                    <div className="text-left">
                      <p className="font-mono text-xs text-muted-foreground mb-2">EXPLANATION</p>
                      <p className="text-muted-foreground">{currentCard?.explanation}</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>

        {/* Controls */}
        <div className="mt-8 flex flex-col gap-4">
          <div className="flex justify-between gap-4">
            <Button
              variant="outline"
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="flex-1"
              data-testid="fc-prev-btn"
            >
              <CaretLeft className="w-5 h-5 mr-1" />
              Previous
            </Button>
            {currentIndex < questions.length - 1 ? (
              <Button
                variant="outline"
                onClick={handleNext}
                className="flex-1"
                data-testid="fc-next-btn"
              >
                Next
                <CaretRight className="w-5 h-5 ml-1" />
              </Button>
            ) : (
              <Button
                onClick={finishFlashcards}
                className="flex-1 font-mono glow-primary"
                data-testid="fc-finish-btn"
              >
                Finish
              </Button>
            )}
          </div>

          {flipped && (
            <div className="flex gap-4">
              <Button
                variant="outline"
                onClick={handleNext}
                className="flex-1 border-destructive/50 text-destructive hover:bg-destructive/10"
                data-testid="fc-repeat-btn"
              >
                <ArrowsClockwise className="w-5 h-5 mr-2" />
                Need Practice
              </Button>
              <Button
                variant="outline"
                onClick={markKnown}
                className="flex-1 border-primary/50 text-primary hover:bg-primary/10"
                data-testid="fc-known-btn"
              >
                Got It!
              </Button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Flashcards;
