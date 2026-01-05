import { useState } from 'react';
import LandingPage from './components/LandingPage';
import RoleSelector from './components/RoleSelector';

export default function App() {
  // Simple state to manage which "page" we are showing
  // Options: 'landing', 'roles', 'input', 'results'
  const [view, setView] = useState('landing');

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
          onSelect={(role) => {
            console.log('Selected role:', role);
            // TODO: Navigate to next step (e.g., setView('input'))
          }}
          onBack={() => setView('landing')}
        />
      )}

    </div>
  );
}