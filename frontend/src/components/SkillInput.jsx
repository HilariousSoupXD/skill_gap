import React, { useState } from 'react';

export default function SkillInput({ selectedRole, onSubmit, onBack }) {
  const [skillValues, setSkillValues] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Initialize skill values to 0 if not set
  React.useEffect(() => {
    if (selectedRole?.skills) {
      const initialValues = {};
      selectedRole.skills.forEach(skill => {
        if (skillValues[skill] === undefined) {
          initialValues[skill] = 0;
        }
      });
      if (Object.keys(initialValues).length > 0) {
        setSkillValues(prev => ({ ...prev, ...initialValues }));
      }
    }
  }, [selectedRole]);

  // Get sticky color for role badge (matching RoleSelector logic)
  const getRoleBadgeColor = () => {
    if (!selectedRole) return "bg-[#FEF08A]";
    // Match the color logic from RoleSelector
    const roleIndex = selectedRole.id === "SDE" ? 0 : 1;
    const colors = ["bg-[#FEF08A]", "bg-[#BAE6FD]", "bg-[#FBCFE8]"];
    return colors[roleIndex % colors.length];
  };

  // Get fill color (hex) matching role badge
  const getRoleFillColor = () => {
    if (!selectedRole) return "#FEF08A";
    const roleIndex = selectedRole.id === "SDE" ? 0 : 1;
    const colors = ["#FEF08A", "#BAE6FD", "#FBCFE8"];
    return colors[roleIndex % colors.length];
  };

  // Get proficiency label colors (gradient from red to green)
  const getProficiencyColor = (level) => {
    const colors = {
      none: "#FCA5A5",      // Light red
      novice: "#FCD34D",   // Yellow/amber
      competent: "#93C5FD", // Light blue
      expert: "#86EFAC"     // Light green
    };
    return colors[level] || "#FEF08A";
  };

  const handleSkillChange = (skill, value) => {
    setSkillValues(prev => ({ ...prev, [skill]: parseInt(value) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      // Convert slider values (0-100) to proficiency (0.0-1.0)
      const studentProfile = {};
      selectedRole.skills.forEach(skill => {
        const value = skillValues[skill] || 0;
        studentProfile[skill] = value / 100.0;
      });

      // Prepare payload
      const payload = {
        role: selectedRole.id,
        student_profile: studentProfile
      };

      // Call API
      const response = await fetch("http://127.0.0.1:5000/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      onSubmit({ result: data, studentProfile });
    } catch (err) {
      console.error("Submit error:", err);
      setError(err.message || "Failed to submit evaluation. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!selectedRole) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-xl text-slate-500 font-hand">No role selected</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-8 bg-transparent">
      
      {/* Error Banner */}
      {error && (
        <div className="mb-8 px-6 py-4 bg-red-100 border-2 border-red-300 text-red-700 rounded rotate-1 font-hand text-xl shadow-sm max-w-2xl">
          ⚠️ {error}
        </div>
      )}

      {/* Header with Yellow Highlighter */}
      <div className="relative mb-4 text-center">
        <div className="absolute inset-0 bg-[#FEF08A] transform -skew-x-6 rounded-sm opacity-60 -z-10" />
        <h1 className="text-5xl md:text-6xl text-slate-800 font-hand relative z-10 px-4">
          Rate Your Skills
        </h1>
      </div>

      {/* Be Honest! Text */}
      <p className="text-xl md:text-2xl text-slate-600 font-hand text-center mb-8 italic">
        Be Honest!
      </p>

      {/* Role Badge (Sticky Note) */}
      <div className={`relative mb-12 ${getRoleBadgeColor()} border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.15)] rotate-1 px-6 py-3`}>
        <h2 className="text-2xl text-slate-800 font-hand font-bold">
          {selectedRole.label}
        </h2>
      </div>

      {/* Form Container */}
      <form onSubmit={handleSubmit} className="w-full max-w-4xl space-y-8 mb-12">
        
        {/* Skills Section */}
        <div className="space-y-10">
          {selectedRole.skills?.map((skill, index) => {
            const value = skillValues[skill] || 0;
            const isExpert = value >= 80;
            
            // Check which proficiency levels have been crossed
            const hasCrossedNone = value > 0;
            const hasCrossedNovice = value >= 33;
            const hasCrossedCompetent = value >= 66;
            const hasCrossedExpert = value >= 100;
            
            return (
              <div key={skill} className="space-y-3">
                {/* Skill Label */}
                <label className="block text-2xl text-slate-800 font-hand font-bold">
                  {skill}
                </label>

                {/* Custom Ruler-mometer Slider */}
                <div className="relative">
                  {/* Scale Labels (Tooltip Bubbles Above Track) */}
                  <div className="relative mb-2 h-12 pointer-events-none">
                    {/* None (0%) */}
                    <div className="absolute left-0">
                      <div 
                        className={`relative border-2 border-slate-700 shadow-[3px_3px_0px_rgba(0,0,0,0.15)] px-3 py-1 rotate-1 transition-all duration-200 ${
                          hasCrossedNone ? 'px-4 py-1.5 scale-110' : 'px-3 py-1'
                        }`}
                        style={{ backgroundColor: getProficiencyColor('none') }}
                      >
                        <span className={`font-hand text-slate-800 font-bold transition-all duration-200 ${
                          hasCrossedNone ? 'text-base' : 'text-sm'
                        }`}>None</span>
                      </div>
                    </div>
                    
                    {/* Novice (33%) */}
                    <div className="absolute left-[33%] -translate-x-1/2">
                      <div 
                        className={`relative border-2 border-slate-700 shadow-[3px_3px_0px_rgba(0,0,0,0.15)] px-3 py-1 -rotate-1 transition-all duration-200 ${
                          hasCrossedNovice ? 'px-4 py-1.5 scale-110' : 'px-3 py-1'
                        }`}
                        style={{ backgroundColor: getProficiencyColor('novice') }}
                      >
                        <span className={`font-hand text-slate-800 font-bold transition-all duration-200 ${
                          hasCrossedNovice ? 'text-base' : 'text-sm'
                        }`}>Novice</span>
                      </div>
                    </div>
                    
                    {/* Competent (66%) */}
                    <div className="absolute left-[66%] -translate-x-1/2">
                      <div 
                        className={`relative border-2 border-slate-700 shadow-[3px_3px_0px_rgba(0,0,0,0.15)] px-3 py-1 rotate-1 transition-all duration-200 ${
                          hasCrossedCompetent ? 'px-4 py-1.5 scale-110' : 'px-3 py-1'
                        }`}
                        style={{ backgroundColor: getProficiencyColor('competent') }}
                      >
                        <span className={`font-hand text-slate-800 font-bold transition-all duration-200 ${
                          hasCrossedCompetent ? 'text-base' : 'text-sm'
                        }`}>Competent</span>
                      </div>
                    </div>
                    
                    {/* Expert (100%) */}
                    <div className="absolute right-0">
                      <div 
                        className={`relative border-2 border-slate-700 shadow-[3px_3px_0px_rgba(0,0,0,0.15)] px-3 py-1 -rotate-1 transition-all duration-200 ${
                          hasCrossedExpert ? 'px-4 py-1.5 scale-110' : 'px-3 py-1'
                        }`}
                        style={{ backgroundColor: getProficiencyColor('expert') }}
                      >
                        <span className={`font-hand text-slate-800 font-bold transition-all duration-200 ${
                          hasCrossedExpert ? 'text-base' : 'text-sm'
                        }`}>Expert</span>
                      </div>
                    </div>
                  </div>

                  {/* Ruler Track Container */}
                  <div className="relative h-12 flex items-center">
                    {/* Ruler Track (thick black line) */}
                    <div className="absolute left-0 right-0 h-1 bg-slate-800" />
                    
                    {/* Fill color matching role badge */}
                    <div 
                      className="absolute left-0 h-1 z-0"
                      style={{ 
                        width: `${value}%`,
                        backgroundColor: getRoleFillColor()
                      }}
                    />

                    {/* Fire Emoji to the right of the scale line when expert */}
                    {isExpert && (
                      <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-16 z-10">
                        <span className="text-3xl animate-bounce">🔥</span>
                      </div>
                    )}

                    {/* Scale Markers (Tick Marks Only) */}
                    <div className="absolute left-0 right-0 h-full flex items-center">
                      {/* None (0%) */}
                      <div className="absolute left-0">
                        <div className="w-0.5 h-4 bg-slate-800" />
                      </div>
                      
                      {/* Novice (33%) */}
                      <div className="absolute left-[33%] -translate-x-1/2">
                        <div className="w-0.5 h-4 bg-slate-800" />
                      </div>
                      
                      {/* Competent (66%) */}
                      <div className="absolute left-[66%] -translate-x-1/2">
                        <div className="w-0.5 h-4 bg-slate-800" />
                      </div>
                      
                      {/* Expert (100%) */}
                      <div className="absolute right-0">
                        <div className="w-0.5 h-4 bg-slate-800" />
                      </div>
                    </div>

                    {/* Slider Input (invisible, positioned for interaction - fully draggable) */}
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={value}
                      onChange={(e) => handleSkillChange(skill, e.target.value)}
                      onInput={(e) => handleSkillChange(skill, e.target.value)}
                      onMouseDown={(e) => e.stopPropagation()}
                      onTouchStart={(e) => e.stopPropagation()}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-grab active:cursor-grabbing z-30"
                      style={{ WebkitAppearance: 'none', appearance: 'none', pointerEvents: 'auto' }}
                    />

                    {/* Handle (white circle with thick black border) - no transition for instant response */}
                    <div
                      className="absolute top-1/2 -translate-y-1/2 w-8 h-8 bg-white border-4 border-slate-800 rounded-full shadow-[2px_2px_0px_rgba(0,0,0,0.2)] z-20 pointer-events-none"
                      style={{ 
                        left: `clamp(0px, calc(${value}% - 16px), calc(100% - 32px))` 
                      }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Submit Button (Stamped Sticker Style) */}
        <div className="flex justify-center pt-8">
          <button
            type="submit"
            disabled={isSubmitting}
            className="relative px-10 py-5 font-hand text-2xl text-slate-800 bg-[#FDFBF7] border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.2)] rotate-1 hover:bg-[#BAE6FD] hover:rotate-0 hover:shadow-[6px_6px_0px_rgba(0,0,0,0.3)] transition-all duration-200 active:shadow-[2px_2px_0px_rgba(0,0,0,0.2)] active:translate-x-1 active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Assignment'}
          </button>
        </div>
      </form>

      {/* Back Button */}
      <button
        onClick={onBack}
        className="text-xl text-slate-500 hover:text-slate-800 transition-colors font-hand flex items-center gap-2 group"
      >
        <span className="group-hover:-translate-x-1 transition-transform">←</span> 
        Back to Roles
      </button>
    </div>
  );
}

