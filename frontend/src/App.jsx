import { useState } from 'react';
import LandingPage from './components/LandingPage';

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

      {/* PAGE 2: ROLE SELECTION (Placeholder) */}
      {view === 'roles' && (
        <div className="min-h-screen flex flex-col items-center justify-center p-4 animate-in fade-in zoom-in duration-300">
          <div className="max-w-md w-full bg-white border-2 border-slate-700 shadow-[6px_6px_0px_rgba(0,0,0,0.2)] p-8 rotate-1">
            <h1 className="font-hand text-4xl mb-4">Select Your Character</h1>
            <p className="mb-6">
              This is where the Role Selection cards will go next!
            </p>
            <button 
              onClick={() => setView('landing')}
              className="text-sm underline text-slate-500 hover:text-red-500"
            >
              ← Back to Home
            </button>
          </div>
        </div>
      )}

    </div>
  );
}