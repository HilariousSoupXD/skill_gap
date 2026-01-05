import { useState } from 'react';
import LandingPage from './components/LandingPage';
import RoleSelector from './components/RoleSelector';
import SkillInput from './components/SkillInput';
import Dashboard from './components/Dashboard';

export default function App() {
  // Simple state to manage which "page" we are showing
  // Options: 'landing', 'roles', 'input', 'results'
  const [view, setView] = useState('landing');
  const [selectedRole, setSelectedRole] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [studentProfile, setStudentProfile] = useState(null);

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setView('input');
  };

  const handleSkillSubmit = ({ result, studentProfile }) => {
    setEvaluationResult(result);
    setStudentProfile(studentProfile);
    setView('results');
  };

  const handleRestart = () => {
    setView('landing');
    setSelectedRole(null);
    setEvaluationResult(null);
    setStudentProfile(null);
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

      {/* PAGE 4: RESULTS (Dashboard) */}
      {view === 'results' && evaluationResult && studentProfile && selectedRole && (
        <Dashboard
          evaluationResult={evaluationResult}
          studentProfile={studentProfile}
          selectedRole={selectedRole}
          onRestart={handleRestart}
        />
      )}

    </div>
  );
}