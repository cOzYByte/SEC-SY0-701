import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ArrowLeft, Brain, Lightning, Check, X, Repeat, CaretRight, Trophy, Fire, ChartLineUp } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Badge } from '../components/ui/badge';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const SmartReview = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(true);
  const [started, setStarted] = useState(false);
  const [sessionStats, setSessionStats] = useState({ reviewed: 0, correct: 0 });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/spaced-repetition/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch SR stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const startReview = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/spaced-repetition/due?limit=20`);
      if (response.data.length === 0) {
        alert('No cards due for review! Great job staying on top of your studies.');
        return;
      }
      setQuestions(response.data);
      setStarted(true);
    } catch (error) {
      console.error('Failed to fetch due cards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (optionId) => {
    if (showResult) return;
    setSelectedAnswer(optionId);
  };

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer) return;
    
    const currentQuestion = questions[currentIndex];
    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    
    // Quality rating: 0-2 = fail, 3-5 = pass
    // We'll use: wrong = 1, correct = 4, easy = 5
    const quality = isCorrect ? 4 : 1;
    
    try {
      await axios.post(`${API}/spaced-repetition/review`, {
        question_id: currentQuestion.id,
        quality
      });
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
    
    setSessionStats(prev => ({
      reviewed: prev.reviewed + 1,
      correct: prev.correct + (isCorrect ? 1 : 0)
    }));
    
    setShowResult(true);
  };

  const handleRateAndNext = async (quality) => {
    const currentQuestion = questions[currentIndex];
    
    try {
      await axios.post(`${API}/spaced-repetition/review`, {
        question_id: currentQuestion.id,
        quality
      });
    } catch (error) {
      console.error('Failed to submit rating:', error);
    }
    
    handleNext();
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      // Session complete
      navigate('/dashboard');
    }
  };

  const currentQuestion = questions[currentIndex];
  const progressPercent = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;

  if (loading && !started) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Brain weight="duotone" className="w-16 h-16 text-primary animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading Smart Review...</p>
        </div>
      </div>
    );
  }

  if (!started) {
    return (
      <div className="min-h-screen bg-background">
        <header className="sticky top-0 z-50 glass border-b border-border">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="back-btn">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div className="flex items-center gap-3">
              <Brain weight="duotone" className="w-6 h-6 text-primary" />
              <span className="font-mono font-bold text-lg tracking-tight">SMART REVIEW</span>
            </div>
          </div>
        </header>

        <main className="max-w-2xl mx-auto px-6 py-12">
          <Card className="corner-accent mb-6">
            <CardHeader>
              <CardTitle className="font-mono text-xl tracking-tight flex items-center gap-2">
                <Lightning weight="duotone" className="w-6 h-6 text-accent" />
                Spaced Repetition
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-muted-foreground">
                Smart Review uses the <span className="text-primary font-medium">SM-2 algorithm</span> to optimize your study sessions. 
                Questions you struggle with appear more frequently, while mastered topics are spaced out over time.
              </p>
              
              {stats && (
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-secondary/50 p-4 rounded-lg text-center">
                    <Fire weight="duotone" className="w-8 h-8 text-accent mx-auto mb-2" />
                    <p className="font-mono text-2xl font-bold" data-testid="due-count">{stats.due_today}</p>
                    <p className="text-muted-foreground text-sm">Due Today</p>
                  </div>
                  <div className="bg-secondary/50 p-4 rounded-lg text-center">
                    <Trophy weight="duotone" className="w-8 h-8 text-primary mx-auto mb-2" />
                    <p className="font-mono text-2xl font-bold" data-testid="mastered-count">{stats.mastered}</p>
                    <p className="text-muted-foreground text-sm">Mastered</p>
                  </div>
                  <div className="bg-secondary/50 p-4 rounded-lg text-center">
                    <ChartLineUp weight="duotone" className="w-8 h-8 text-chart-3 mx-auto mb-2" />
                    <p className="font-mono text-2xl font-bold" data-testid="learning-count">{stats.learning}</p>
                    <p className="text-muted-foreground text-sm">Learning</p>
                  </div>
                  <div className="bg-secondary/50 p-4 rounded-lg text-center">
                    <Brain weight="duotone" className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                    <p className="font-mono text-2xl font-bold" data-testid="new-count">{stats.new_cards}</p>
                    <p className="text-muted-foreground text-sm">New Cards</p>
                  </div>
                </div>
              )}

              <div className="bg-primary/10 border border-primary/30 p-4 rounded-lg">
                <p className="text-sm text-primary font-medium mb-2">How it works:</p>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Answer correctly → See it again in longer intervals</li>
                  <li>• Answer incorrectly → See it again soon</li>
                  <li>• Rate difficulty to fine-tune your schedule</li>
                </ul>
              </div>

              <Button
                className="w-full font-mono tracking-wider glow-primary"
                onClick={startReview}
                disabled={stats?.due_today === 0}
                data-testid="start-review-btn"
              >
                {stats?.due_today === 0 ? 'NO CARDS DUE' : `START REVIEW (${stats?.due_today} cards)`}
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
          <Brain weight="duotone" className="w-16 h-16 text-primary animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading cards...</p>
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
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="exit-btn">
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <span className="font-mono font-bold tracking-tight">SMART REVIEW</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="font-mono text-sm text-muted-foreground" data-testid="review-counter">
                {currentIndex + 1} / {questions.length}
              </span>
              <Badge variant="outline" className="font-mono">
                {sessionStats.correct}/{sessionStats.reviewed} correct
              </Badge>
            </div>
          </div>
          <Progress value={progressPercent} className="h-2" />
        </div>
      </header>

      {/* Question */}
      <main className="max-w-3xl mx-auto px-6 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            <Card className={`corner-accent ${showResult ? (selectedAnswer === currentQuestion?.correct_answer ? 'flash-success border-primary' : 'shake border-destructive') : ''}`} data-testid="sr-question-card">
              <CardHeader>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="outline" className="font-mono text-xs text-primary border-primary/30">
                    DOMAIN {currentQuestion?.domain}
                  </Badge>
                  {currentQuestion?.sr_data?.is_new && (
                    <Badge className="font-mono text-xs bg-accent">NEW</Badge>
                  )}
                  {!currentQuestion?.sr_data?.is_new && currentQuestion?.sr_data?.interval > 0 && (
                    <Badge variant="outline" className="font-mono text-xs">
                      Interval: {currentQuestion?.sr_data?.interval}d
                    </Badge>
                  )}
                </div>
                <CardTitle className="font-sans text-lg leading-relaxed" data-testid="sr-question-text">
                  {currentQuestion?.question}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {currentQuestion?.options.map((option) => {
                  const isSelected = selectedAnswer === option.id;
                  const isCorrect = option.id === currentQuestion.correct_answer;
                  const showCorrect = showResult && isCorrect;
                  const showIncorrect = showResult && isSelected && !isCorrect;

                  return (
                    <button
                      key={option.id}
                      onClick={() => handleAnswer(option.id)}
                      disabled={showResult}
                      data-testid={`sr-option-${option.id}`}
                      className={`w-full p-4 rounded-lg border text-left transition-all flex items-center gap-3 ${
                        showCorrect
                          ? 'border-primary bg-primary/10 text-foreground'
                          : showIncorrect
                          ? 'border-destructive bg-destructive/10 text-foreground'
                          : isSelected
                          ? 'border-primary bg-primary/5'
                          : 'border-border hover:border-primary/50 hover:bg-secondary/50'
                      }`}
                    >
                      <span className="font-mono text-sm font-bold w-6 h-6 flex items-center justify-center rounded bg-secondary">
                        {option.id.toUpperCase()}
                      </span>
                      <span className="flex-1">{option.text}</span>
                      {showCorrect && <Check weight="bold" className="w-5 h-5 text-primary" />}
                      {showIncorrect && <X weight="bold" className="w-5 h-5 text-destructive" />}
                    </button>
                  );
                })}
              </CardContent>
            </Card>

            {/* Explanation & Rating */}
            {showResult && (
              <Card className="mt-4 border-primary/30">
                <CardContent className="pt-6">
                  <p className="font-mono text-xs text-muted-foreground mb-2">EXPLANATION</p>
                  <p className="text-muted-foreground mb-6" data-testid="sr-explanation">
                    {currentQuestion?.explanation}
                  </p>
                  
                  <p className="font-mono text-xs text-muted-foreground mb-3">HOW WELL DID YOU KNOW THIS?</p>
                  <div className="grid grid-cols-3 gap-3">
                    <Button
                      variant="outline"
                      onClick={() => handleRateAndNext(1)}
                      className="border-destructive/50 text-destructive hover:bg-destructive/10"
                      data-testid="rate-again-btn"
                    >
                      <Repeat className="w-4 h-4 mr-2" />
                      Again
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleRateAndNext(3)}
                      className="border-accent/50 text-accent hover:bg-accent/10"
                      data-testid="rate-hard-btn"
                    >
                      Hard
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleRateAndNext(5)}
                      className="border-primary/50 text-primary hover:bg-primary/10"
                      data-testid="rate-easy-btn"
                    >
                      <Check className="w-4 h-4 mr-2" />
                      Easy
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Submit Button */}
            {!showResult && (
              <div className="mt-6 flex justify-end">
                <Button
                  onClick={handleSubmitAnswer}
                  disabled={!selectedAnswer}
                  className="font-mono tracking-wider glow-primary"
                  data-testid="sr-submit-btn"
                >
                  REVEAL ANSWER
                </Button>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
};

export default SmartReview;
