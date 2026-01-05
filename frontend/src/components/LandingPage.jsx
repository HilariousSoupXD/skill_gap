import React from 'react';

export default function LandingPage({ onStart }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
      
      {/* Main Hero Container */}
      <div className="relative z-10 w-full max-w-4xl">
        
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
            <div className="relative inline-block mb-6 mt-4">
              {/* Highlighter stroke */}
              <div className="absolute inset-0 bg-[#FEF08A] -rotate-1 -z-10 transform scale-105 skew-x-3 rounded-sm" />
              <h1 className="font-hand text-5xl md:text-7xl text-slate-800 relative z-10 leading-tight">
                Skill Sketch
              </h1>
            </div>

            {/* Description */}
            <div className="mb-10 space-y-4">
              <p className="font-sans text-base md:text-lg text-slate-700 leading-relaxed max-w-2xl">
                <strong className="font-hand text-xl">What is Skill Sketch?</strong> A skill gap analyzer 
                that visualizes your proficiency, identifies missing skills, and generates a personalized 
                learning plan with prioritized resources for your target role.
              </p>
            </div>

            {/* Feature Highlights - Checkbox Style */}
            <div className="mb-10 space-y-3 max-w-2xl">
              <div className="flex items-start gap-3">
                <div className="mt-1 w-6 h-6 border-2 border-slate-700 rounded-sm flex-shrink-0 relative flex items-center justify-center">
                  {/* Green Check Mark with Marker Font */}
                  <span className="font-hand text-green-600 text-4xl leading-none">✓</span>
                </div>
                <p className="font-sans text-sm md:text-base text-slate-700">
                  <span className="font-hand text-lg">Visual Skill Assessment</span> — See your strengths and gaps on a radar chart
                </p>
              </div>
              
              <div className="flex items-start gap-3">
                <div className="mt-1 w-6 h-6 border-2 border-slate-700 rounded-sm flex-shrink-0 relative flex items-center justify-center">
                  {/* Green Check Mark with Marker Font */}
                  <span className="font-hand text-green-600 text-4xl leading-none">✓</span>
                </div>
                <p className="font-sans text-sm md:text-base text-slate-700">
                  <span className="font-hand text-lg">Smart Learning Plan</span> — Automatic week-by-week schedule with priorities
                </p>
              </div>
              
              <div className="flex items-start gap-3">
                <div className="mt-1 w-6 h-6 border-2 border-slate-700 rounded-sm flex-shrink-0 relative flex items-center justify-center">
                  {/* Green Check Mark with Marker Font */}
                  <span className="font-hand text-green-600 text-4xl leading-none">✓</span>
                </div>
                <p className="font-sans text-sm md:text-base text-slate-700">
                  <span className="font-hand text-lg">Curated Resources</span> — Hand-picked courses and tutorials for each skill
                </p>
              </div>
            </div>

            {/* Button Container - Centered */}
            <div className="flex justify-center">
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
    </div>
  );
}