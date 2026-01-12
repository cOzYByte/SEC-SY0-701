import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ArrowLeft, Clock, Flag, CaretLeft, CaretRight, Warning } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../components/ui/dialog';
import { Badge } from '../components/ui/badge';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const Exam = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [flagged, setFlagged] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [started, setStarted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(90 * 60); // 90 minutes
  const [showConfirmEnd, setShowConfirmEnd] = useState(false);
  const [showConfirmExit, setShowConfirmExit] = useState(false);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const startExam = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/questions/exam`);
      setQuestions(response.data);
      setStarted(true);
      startTimer();
    } catch (error) {
      console.error('Failed to fetch questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const startTimer = () => {
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          finishExam();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAnswer = (optionId) => {
    setAnswers(prev => ({
      ...prev,
      [questions[currentIndex].id]: optionId
    }));
  };

  const toggleFlag = () => {
    const questionId = questions[currentIndex].id;
    setFlagged(prev => {
      const newSet = new Set(prev);
      if (newSet.has(questionId)) {
        newSet.delete(questionId);
      } else {
        newSet.add(questionId);
      }
      return newSet;
    });
  };

  const goToQuestion = (index) => {
    setCurrentIndex(index);
  };

  const finishExam = async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    
    try {
      const submission = {
        answers: questions.map(q => ({
          question_id: q.id,
          selected_answer: answers[q.id] || '',
          time_taken: 0
        })),
        mode: 'exam',
        total_time: (90 * 60) - timeLeft
      };
      await axios.post(`${API}/progress/submit`, submission);
      navigate('/results', { state: { answers: Object.entries(answers).map(([qId, ans]) => ({ question_id: qId, selected_answer: ans })), questions, mode: 'exam' } });
    } catch (error) {
      console.error('Failed to submit:', error);
      navigate('/results', { state: { answers: Object.entries(answers).map(([qId, ans]) => ({ question_id: qId, selected_answer: ans })), questions, mode: 'exam' } });
    }
  };

  const currentQuestion = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;
  const progressPercent = questions.length > 0 ? (answeredCount / questions.length) * 100 : 0;

  if (!started) {
    return (
      <div className="min-h-screen bg-background">
        <header className="sticky top-0 z-50 glass border-b border-border">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="back-btn">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div className="flex items-center gap-3">
              <Shield weight="duotone" className="w-6 h-6 text-accent" />
              <span className="font-mono font-bold text-lg tracking-tight">EXAM SIMULATION</span>
            </div>
          </div>
        </header>

        <main className="max-w-2xl mx-auto px-6 py-12">
          <Card className="corner-accent">
            <CardHeader>
              <CardTitle className="font-mono text-xl tracking-tight">CompTIA Security+ SY0-701</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="bg-secondary/50 p-4 rounded-lg space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Questions</span>
                  <span className="font-mono font-bold">90</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Time Limit</span>
                  <span className="font-mono font-bold">90 minutes</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Passing Score</span>
                  <span className="font-mono font-bold">750/900</span>
                </div>
              </div>

              <div className="bg-accent/10 border border-accent/30 p-4 rounded-lg">
                <div className="flex items-start gap-3">
                  <Warning weight="duotone" className="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
                  <div className="text-sm">
                    <p className="font-medium text-accent mb-1">Exam Rules</p>
                    <ul className="text-muted-foreground space-y-1">
                      <li>• No feedback during the exam</li>
                      <li>• You can flag questions for review</li>
                      <li>• Navigate freely between questions</li>
                      <li>• Timer cannot be paused</li>
                    </ul>
                  </div>
                </div>
              </div>

              <Button
                className="w-full font-mono tracking-wider"
                onClick={startExam}
                data-testid="start-exam-btn"
              >
                START EXAM
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
          <Shield weight="duotone" className="w-16 h-16 text-accent animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading exam...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-3">
          <div className="flex items-center justify-between">
            <Button variant="ghost" size="sm" onClick={() => setShowConfirmExit(true)} data-testid="exit-exam-btn">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Exit
            </Button>
            <div className={`flex items-center gap-2 font-mono text-lg ${timeLeft < 300 ? 'text-destructive animate-pulse' : ''}`} data-testid="timer">
              <Clock weight="duotone" className="w-5 h-5" />
              {formatTime(timeLeft)}
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowConfirmEnd(true)}
              data-testid="end-exam-btn"
              className="font-mono text-xs"
            >
              END EXAM
            </Button>
          </div>
          <div className="mt-3 flex items-center gap-3">
            <Progress value={progressPercent} className="h-2 flex-1" />
            <span className="font-mono text-xs text-muted-foreground">
              {answeredCount}/{questions.length}
            </span>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-6 flex gap-6">
        {/* Question Navigator - Desktop */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <Card className="sticky top-32">
            <CardHeader className="py-3">
              <CardTitle className="font-mono text-xs tracking-wider">QUESTION NAVIGATOR</CardTitle>
            </CardHeader>
            <CardContent className="p-3">
              <div className="grid grid-cols-5 gap-1">
                {questions.map((q, idx) => (
                  <button
                    key={q.id}
                    onClick={() => goToQuestion(idx)}
                    data-testid={`nav-q-${idx + 1}`}
                    className={`w-8 h-8 text-xs font-mono rounded transition-colors ${
                      idx === currentIndex
                        ? 'bg-primary text-primary-foreground'
                        : flagged.has(q.id)
                        ? 'bg-accent text-accent-foreground'
                        : answers[q.id]
                        ? 'bg-secondary text-foreground'
                        : 'bg-muted text-muted-foreground hover:bg-secondary'
                    }`}
                  >
                    {idx + 1}
                  </button>
                ))}
              </div>
              <div className="mt-4 space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-secondary rounded" />
                  <span className="text-muted-foreground">Answered</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-accent rounded" />
                  <span className="text-muted-foreground">Flagged</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-muted rounded" />
                  <span className="text-muted-foreground">Unanswered</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </aside>

        {/* Main Question Area */}
        <main className="flex-1 max-w-3xl">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.15 }}
            >
              <Card className="corner-accent" data-testid="exam-question-card">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="font-mono text-xs">
                        Q{currentIndex + 1}
                      </Badge>
                      <Badge variant="outline" className="font-mono text-xs text-primary border-primary/30">
                        DOMAIN {currentQuestion?.domain}
                      </Badge>
                    </div>
                    <Button
                      variant={flagged.has(currentQuestion?.id) ? 'default' : 'outline'}
                      size="sm"
                      onClick={toggleFlag}
                      data-testid="flag-btn"
                      className={flagged.has(currentQuestion?.id) ? 'bg-accent hover:bg-accent/90' : ''}
                    >
                      <Flag weight={flagged.has(currentQuestion?.id) ? 'fill' : 'regular'} className="w-4 h-4 mr-1" />
                      {flagged.has(currentQuestion?.id) ? 'Flagged' : 'Flag'}
                    </Button>
                  </div>
                  <CardTitle className="font-sans text-lg leading-relaxed mt-4" data-testid="exam-question-text">
                    {currentQuestion?.question}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {currentQuestion?.options.map((option) => {
                    const isSelected = answers[currentQuestion.id] === option.id;
                    return (
                      <button
                        key={option.id}
                        onClick={() => handleAnswer(option.id)}
                        data-testid={`exam-option-${option.id}`}
                        className={`w-full p-4 rounded-lg border text-left transition-all flex items-center gap-3 ${
                          isSelected
                            ? 'border-primary bg-primary/10'
                            : 'border-border hover:border-primary/50 hover:bg-secondary/50'
                        }`}
                      >
                        <span className={`font-mono text-sm font-bold w-6 h-6 flex items-center justify-center rounded ${isSelected ? 'bg-primary text-primary-foreground' : 'bg-secondary'}`}>
                          {option.id.toUpperCase()}
                        </span>
                        <span className="flex-1">{option.text}</span>
                      </button>
                    );
                  })}
                </CardContent>
              </Card>

              {/* Navigation */}
              <div className="mt-6 flex justify-between">
                <Button
                  variant="outline"
                  onClick={() => setCurrentIndex(prev => Math.max(0, prev - 1))}
                  disabled={currentIndex === 0}
                  data-testid="prev-question-btn"
                >
                  <CaretLeft className="w-5 h-5 mr-1" />
                  Previous
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setCurrentIndex(prev => Math.min(questions.length - 1, prev + 1))}
                  disabled={currentIndex === questions.length - 1}
                  data-testid="next-question-btn"
                >
                  Next
                  <CaretRight className="w-5 h-5 ml-1" />
                </Button>
              </div>
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* Confirm End Dialog */}
      <Dialog open={showConfirmEnd} onOpenChange={setShowConfirmEnd}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="font-mono">End Exam?</DialogTitle>
            <DialogDescription>
              You have answered {answeredCount} of {questions.length} questions.
              {questions.length - answeredCount > 0 && (
                <span className="text-destructive"> {questions.length - answeredCount} questions are unanswered.</span>
              )}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowConfirmEnd(false)}>
              Continue Exam
            </Button>
            <Button onClick={finishExam} data-testid="confirm-end-btn">
              End Exam
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Confirm Exit Dialog */}
      <Dialog open={showConfirmExit} onOpenChange={setShowConfirmExit}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="font-mono">Exit Exam?</DialogTitle>
            <DialogDescription>
              Your progress will be lost. Are you sure you want to exit?
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowConfirmExit(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={() => navigate('/dashboard')} data-testid="confirm-exit-btn">
              Exit
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Exam;
