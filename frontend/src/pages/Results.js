import { useLocation, useNavigate } from 'react-router-dom';
import { Shield, ArrowLeft, Check, X, Trophy, Target, ChartPie } from '@phosphor-icons/react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '../components/ui/collapsible';
import { useState } from 'react';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { answers = [], questions = [], mode = 'practice' } = location.state || {};
  const [expandedQuestion, setExpandedQuestion] = useState(null);

  const calculateResults = () => {
    let correct = 0;
    const domainStats = {};

    questions.forEach(q => {
      const answer = answers.find(a => a.question_id === q.id);
      const isCorrect = answer?.selected_answer === q.correct_answer;
      if (isCorrect) correct++;

      if (!domainStats[q.domain]) {
        domainStats[q.domain] = { name: q.domain_name, total: 0, correct: 0 };
      }
      domainStats[q.domain].total++;
      if (isCorrect) domainStats[q.domain].correct++;
    });

    return {
      total: questions.length,
      correct,
      incorrect: questions.length - correct,
      accuracy: questions.length > 0 ? Math.round((correct / questions.length) * 100) : 0,
      domainStats
    };
  };

  const results = calculateResults();
  const passed = results.accuracy >= 75;

  if (!questions.length) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">No results to display</p>
          <Button onClick={() => navigate('/dashboard')}>Return to Dashboard</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} data-testid="back-to-dashboard">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="flex items-center gap-3">
            <Shield weight="duotone" className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold text-lg tracking-tight">
              {mode.toUpperCase()} RESULTS
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {/* Score Card */}
        <Card className={`corner-accent mb-8 ${passed ? 'border-primary/50' : 'border-destructive/50'}`} data-testid="score-card">
          <CardContent className="py-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="text-center md:text-left">
                <div className="flex items-center gap-3 justify-center md:justify-start mb-2">
                  {passed ? (
                    <Trophy weight="duotone" className="w-10 h-10 text-primary" />
                  ) : (
                    <Target weight="duotone" className="w-10 h-10 text-accent" />
                  )}
                  <span className={`font-mono text-xl font-bold ${passed ? 'text-primary' : 'text-accent'}`}>
                    {passed ? 'GREAT JOB!' : 'KEEP PRACTICING'}
                  </span>
                </div>
                <p className="text-muted-foreground">
                  {passed 
                    ? 'You\'re making excellent progress!'
                    : 'Review the incorrect answers and try again.'}
                </p>
              </div>
              
              <div className="flex items-center gap-8">
                <div className="text-center">
                  <p className="font-mono text-5xl font-bold tracking-tighter" data-testid="accuracy-score">
                    {results.accuracy}%
                  </p>
                  <p className="text-muted-foreground text-sm">Accuracy</p>
                </div>
                <div className="h-16 w-px bg-border" />
                <div className="text-center">
                  <p className="font-mono text-3xl font-bold tracking-tighter text-primary" data-testid="correct-count">
                    {results.correct}
                  </p>
                  <p className="text-muted-foreground text-sm">Correct</p>
                </div>
                <div className="text-center">
                  <p className="font-mono text-3xl font-bold tracking-tighter text-destructive" data-testid="incorrect-count">
                    {results.incorrect}
                  </p>
                  <p className="text-muted-foreground text-sm">Incorrect</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Domain Breakdown */}
        <Card className="corner-accent mb-8" data-testid="domain-breakdown">
          <CardHeader>
            <CardTitle className="font-mono text-sm tracking-wider flex items-center gap-2">
              <ChartPie weight="duotone" className="w-5 h-5 text-primary" />
              DOMAIN BREAKDOWN
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {Object.entries(results.domainStats).map(([domain, stats]) => {
              const accuracy = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
              return (
                <div key={domain} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-mono text-xs tracking-wider text-muted-foreground">
                      DOMAIN {domain}: {stats.name}
                    </span>
                    <span className="font-mono text-xs">
                      {stats.correct}/{stats.total} • {accuracy}%
                    </span>
                  </div>
                  <Progress 
                    value={accuracy} 
                    className={`h-3 ${accuracy < 50 ? '[&>div]:bg-destructive' : accuracy < 70 ? '[&>div]:bg-accent' : ''}`}
                  />
                </div>
              );
            })}
          </CardContent>
        </Card>

        {/* Question Review */}
        <Card className="corner-accent" data-testid="question-review">
          <CardHeader>
            <CardTitle className="font-mono text-sm tracking-wider">QUESTION REVIEW</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {questions.map((question, index) => {
              const answer = answers.find(a => a.question_id === question.id);
              const isCorrect = answer?.selected_answer === question.correct_answer;
              const isExpanded = expandedQuestion === question.id;

              return (
                <Collapsible
                  key={question.id}
                  open={isExpanded}
                  onOpenChange={() => setExpandedQuestion(isExpanded ? null : question.id)}
                >
                  <CollapsibleTrigger asChild>
                    <button
                      className={`w-full p-4 rounded-lg border text-left transition-all flex items-start gap-3 hover:bg-secondary/50 ${
                        isCorrect ? 'border-primary/30' : 'border-destructive/30'
                      }`}
                      data-testid={`review-q-${index + 1}`}
                    >
                      <span className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center ${
                        isCorrect ? 'bg-primary/20 text-primary' : 'bg-destructive/20 text-destructive'
                      }`}>
                        {isCorrect ? <Check weight="bold" className="w-4 h-4" /> : <X weight="bold" className="w-4 h-4" />}
                      </span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-mono text-xs text-muted-foreground">Q{index + 1}</span>
                          <span className="font-mono text-xs text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                            D{question.domain}
                          </span>
                        </div>
                        <p className="text-sm line-clamp-2">{question.question}</p>
                      </div>
                    </button>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <div className="mt-2 ml-9 p-4 bg-secondary/30 rounded-lg space-y-4">
                      <div className="space-y-2">
                        {question.options.map(option => {
                          const isSelected = answer?.selected_answer === option.id;
                          const isCorrectOption = option.id === question.correct_answer;
                          return (
                            <div
                              key={option.id}
                              className={`p-3 rounded-lg border text-sm flex items-center gap-2 ${
                                isCorrectOption
                                  ? 'border-primary bg-primary/10'
                                  : isSelected
                                  ? 'border-destructive bg-destructive/10'
                                  : 'border-transparent bg-background'
                              }`}
                            >
                              <span className="font-mono font-bold">{option.id.toUpperCase()}.</span>
                              <span className="flex-1">{option.text}</span>
                              {isCorrectOption && <Check weight="bold" className="w-4 h-4 text-primary" />}
                              {isSelected && !isCorrectOption && <X weight="bold" className="w-4 h-4 text-destructive" />}
                            </div>
                          );
                        })}
                      </div>
                      <div className="p-3 bg-background rounded-lg">
                        <p className="font-mono text-xs text-muted-foreground mb-1">EXPLANATION</p>
                        <p className="text-sm text-muted-foreground">{question.explanation}</p>
                      </div>
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              );
            })}
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            variant="outline"
            onClick={() => navigate('/dashboard')}
            className="font-mono"
            data-testid="back-dashboard-btn"
          >
            Back to Dashboard
          </Button>
          <Button
            onClick={() => navigate(`/${mode === 'exam' ? 'exam' : 'practice'}`)}
            className="font-mono glow-primary"
            data-testid="try-again-btn"
          >
            Try Again
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Results;
