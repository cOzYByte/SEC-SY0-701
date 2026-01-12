import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ArrowLeft, Check, X, CaretRight, Info } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '../components/ui/collapsible';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const Practice = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [domain, setDomain] = useState('all');
  const [questionCount, setQuestionCount] = useState('10');
  const [started, setStarted] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const params = { count: parseInt(questionCount) };
      if (domain !== 'all') params.domain = parseInt(domain);
      const response = await axios.get(`${API}/questions/practice`, { params });
      setQuestions(response.data);
      setAnswers([]);
      setCurrentIndex(0);
      setSelectedAnswer(null);
      setShowResult(false);
      setStarted(true);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (optionId) => {
    if (showResult) return;
    setSelectedAnswer(optionId);
  };

  const handleSubmitAnswer = () => {
    if (!selectedAnswer) return;
    
    const currentQuestion = questions[currentIndex];
    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    
    setAnswers(prev => [...prev, {
      question_id: currentQuestion.id,
      selected_answer: selectedAnswer,
      is_correct: isCorrect
    }]);
    
    setShowResult(true);
    setShowExplanation(true);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
      setShowExplanation(false);
    } else {
      finishPractice();
    }
  };

  const finishPractice = async () => {
    try {
      const submission = {
        answers: answers.map(a => ({
          question_id: a.question_id,
          selected_answer: a.selected_answer,
          time_taken: 0
        })),
        mode: 'practice',
        total_time: 0
      };
      await axios.post(`${API}/progress/submit`, submission);
      navigate('/results', { state: { answers, questions, mode: 'practice' } });
    } catch (error) {
      console.error('Failed to submit:', error);
      navigate('/results', { state: { answers, questions, mode: 'practice' } });
    }
  };

  const currentQuestion = questions[currentIndex];
  const progressPercent = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;

  if (!started) {
    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="sticky top-0 z-50 glass border-b border-border">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="back-btn">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div className="flex items-center gap-3">
              <Shield weight="duotone" className="w-6 h-6 text-primary" />
              <span className="font-mono font-bold text-lg tracking-tight">PRACTICE MODE</span>
            </div>
          </div>
        </header>

        <main className="max-w-2xl mx-auto px-6 py-12">
          <Card className="corner-accent">
            <CardHeader>
              <CardTitle className="font-mono text-xl tracking-tight">Configure Practice Session</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label className="font-mono text-sm tracking-wider text-muted-foreground">DOMAIN</label>
                <Select value={domain} onValueChange={setDomain} data-testid="domain-select">
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
                <label className="font-mono text-sm tracking-wider text-muted-foreground">NUMBER OF QUESTIONS</label>
                <Select value={questionCount} onValueChange={setQuestionCount} data-testid="count-select">
                  <SelectTrigger>
                    <SelectValue placeholder="Select count" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">5 Questions</SelectItem>
                    <SelectItem value="10">10 Questions</SelectItem>
                    <SelectItem value="20">20 Questions</SelectItem>
                    <SelectItem value="30">30 Questions</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                className="w-full font-mono tracking-wider glow-primary"
                onClick={fetchQuestions}
                data-testid="start-practice-btn"
              >
                START PRACTICE
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
          <Shield weight="duotone" className="w-16 h-16 text-primary animate-pulse mx-auto mb-4" />
          <p className="font-mono text-muted-foreground">Loading questions...</p>
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
              <span className="font-mono font-bold tracking-tight">PRACTICE</span>
            </div>
            <span className="font-mono text-sm text-muted-foreground" data-testid="question-counter">
              {currentIndex + 1} / {questions.length}
            </span>
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
            <Card className={`corner-accent ${showResult ? (selectedAnswer === currentQuestion?.correct_answer ? 'flash-success border-primary' : 'shake border-destructive') : ''}`} data-testid="question-card">
              <CardHeader>
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-mono text-xs tracking-widest text-primary bg-primary/10 px-2 py-1 rounded">
                    DOMAIN {currentQuestion?.domain}
                  </span>
                </div>
                <CardTitle className="font-sans text-lg leading-relaxed" data-testid="question-text">
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
                      data-testid={`option-${option.id}`}
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

            {/* Explanation */}
            {showResult && (
              <Collapsible open={showExplanation} onOpenChange={setShowExplanation} className="mt-4">
                <Card className="border-primary/30">
                  <CollapsibleTrigger asChild>
                    <CardHeader className="cursor-pointer hover:bg-secondary/50 transition-colors">
                      <div className="flex items-center gap-2">
                        <Info weight="duotone" className="w-5 h-5 text-primary" />
                        <CardTitle className="font-mono text-sm tracking-wider">EXPLANATION</CardTitle>
                      </div>
                    </CardHeader>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <CardContent className="pt-0" data-testid="explanation">
                      <p className="text-muted-foreground">{currentQuestion?.explanation}</p>
                    </CardContent>
                  </CollapsibleContent>
                </Card>
              </Collapsible>
            )}

            {/* Actions */}
            <div className="mt-6 flex justify-end gap-3">
              {!showResult ? (
                <Button
                  onClick={handleSubmitAnswer}
                  disabled={!selectedAnswer}
                  className="font-mono tracking-wider glow-primary"
                  data-testid="submit-answer-btn"
                >
                  SUBMIT ANSWER
                </Button>
              ) : (
                <Button
                  onClick={handleNext}
                  className="font-mono tracking-wider glow-primary"
                  data-testid="next-btn"
                >
                  {currentIndex < questions.length - 1 ? 'NEXT QUESTION' : 'FINISH'}
                  <CaretRight className="w-5 h-5 ml-1" />
                </Button>
              )}
            </div>
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
};

export default Practice;
