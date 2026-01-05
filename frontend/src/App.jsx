import { useState } from 'react';
import LandingPage from './components/LandingPage';
import RoleSelector from './components/RoleSelector';
import SkillInput from './components/SkillInput';

export default function App() {
  // Simple state to manage which "page" we are showing
  // Options: 'landing', 'roles', 'input', 'results'
  const [view, setView] = useState('landing');
  const [selectedRole, setSelectedRole] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setView('input');
  };

  const handleSkillSubmit = (result) => {
    setEvaluationResult(result);
    setView('results');
    // TODO: Create Results component to display the evaluation
    console.log('Evaluation result:', result);
  };

  return (
    // We apply the background class here if your body tag doesn't have it.
    // If you set the grid on the <body> in index.css, you can remove 'bg-paper'.
    <div className="min-h-screen bg-paper text-slate-800 font-sans">
      
      {/* PAGE 1: LANDING */}
      {view === 'landing' && (
        <LandingPage onStart={() => setView('roles')} />
      )}

      {/* PAGE 2: ROLE SELECTION */}
      {view === 'roles' && (
        <RoleSelector 
          onSelect={handleRoleSelect}
          onBack={() => setView('landing')}
        />
      )}

      {/* PAGE 3: SKILL INPUT */}
      {view === 'input' && selectedRole && (
        <SkillInput
          selectedRole={selectedRole}
          onSubmit={handleSkillSubmit}
          onBack={() => setView('roles')}
        />
      )}

      {/* PAGE 4: RESULTS (placeholder) */}
      {view === 'results' && (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-4xl font-hand text-slate-800 mb-4">Evaluation Complete!</h1>
            <p className="text-lg font-sans text-slate-600 mb-8">
              Results view coming soon...
            </p>
            <button
              onClick={() => setView('landing')}
              className="px-6 py-3 border-2 border-slate-700 bg-white font-hand text-xl shadow-[4px_4px_0px_rgba(0,0,0,0.15)] hover:shadow-[6px_6px_0px_rgba(0,0,0,0.2)] transition-all"
            >
              Start Over
            </button>
          </div>
        </div>
      )}

    </div>
  );
}