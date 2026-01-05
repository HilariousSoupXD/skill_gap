import React from 'react';

export default function LandingPage({ onStart }) {
  return (
    // Container keeps min-h-screen for centering, lets global grid show through
    <div className="min-h-screen flex items-center justify-center px-4 py-16">
      
      {/* Hero Container */}
      <div className="relative z-10 w-full max-w-2xl">
        
        {/* Notebook Paper Card */}
        <div 
          className="relative bg-white border-2 border-slate-700 shadow-[6px_6px_0px_rgba(0,0,0,0.2)] w-full p-8 md:p-12 transform rotate-1 transition hover:rotate-0 duration-300 overflow-hidden"
          style={{
             backgroundImage: 'linear-gradient(transparent 27px, #BAE6FD 28px)',
             backgroundSize: '100% 28px'
          }}
        >
          
          {/* Red margin line (Flashcard style) */}
          <div className="absolute left-8 md:left-16 top-0 bottom-0 w-0.5 bg-red-500/80 z-20" />

          {/* Content with padding to sit right of the margin line */}
          <div className="pl-6 md:pl-12 relative z-20">
            
            {/* Title with yellow highlighter effect */}
            <div className="relative inline-block mb-8 mt-4">
              {/* Highlighter stroke */}
              <div className="absolute inset-0 bg-[#FEF08A] -rotate-1 -z-10 transform scale-105 skew-x-3 rounded-sm" />
              <h1 className="font-hand text-5xl md:text-7xl text-slate-800 relative z-10 leading-tight">
                Skill Sketch
              </h1>
            </div>

            {/* UPDATED: Background removed to be transparent */}
            <p className="font-sans text-lg md:text-xl text-slate-700 mb-12 leading-relaxed max-w-md">
              Transform your skills into visual insights. Start sketching your potential today!
            </p>

            {/* Button Container */}
            <div className="relative inline-block">
              
              {/* Start Analysis Button */}
              <button 
                onClick={onStart}
                className="group relative px-8 py-4 font-hand text-xl md:text-2xl text-slate-800 bg-[#FDFBF7] border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.2)] rotate-1 hover:bg-[#BAE6FD] hover:rotate-0 hover:shadow-[6px_6px_0px_rgba(0,0,0,0.3)] transition-all duration-200 active:shadow-[2px_2px_0px_rgba(0,0,0,0.2)] active:translate-x-1 active:translate-y-1 overflow-hidden"
              >
                {/* Scribble animation overlay (Yellow) */}
                <span className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-0">
                  <svg
                    className="absolute inset-0 w-full h-full"
                    viewBox="0 0 200 80"
                    fill="none"
                    stroke="#FEF08A" 
                    strokeWidth="4"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M 10 20 C 30 10, 50 30, 70 20 C 90 10, 110 30, 130 20 C 150 10, 170 30, 190 20 M 10 40 C 30 30, 50 50, 70 40 C 90 30, 110 50, 130 40 C 150 30, 170 50, 190 40 M 10 60 C 30 50, 50 70, 70 60 C 90 50, 110 70, 130 60 C 150 50, 170 70, 190 60" />
                  </svg>
                </span>

                {/* Button Text */}
                <span className="relative z-10 flex items-center gap-2">
                   Start Analysis <span>→</span>
                </span>
              </button>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}