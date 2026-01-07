import React from "react";
import { Code, BarChart, PenTool } from "lucide-react";

export default function RoleSelector({ onSelect, onBack }) {
  // Hardcoded roles to avoid API call delay (roles are static data)
  const roles = [
    {
      id: "SDE",
      label: "SDE",
      description: "Core CS & Systems",
      icon: "code",
      skills: ["DSA", "OS", "DBMS", "CN", "C++", "Git", "Linux", "SQL"]
    },
    {
      id: "DataAnalyst",
      label: "Data Scientist",
      description: "Stats & Analytics",
      icon: "chart",
      skills: ["Statistics", "SQL", "Python", "Pandas", "NumPy", "DSA", "Git"]
    }
  ];

  // 2. Icon Helper
  const getIconComponent = (iconName) => {
    switch (iconName) {
      case "code":
        return <Code className="w-12 h-12 text-slate-800" strokeWidth={1.5} />;
      case "chart":
        return <BarChart className="w-12 h-12 text-slate-800" strokeWidth={1.5} />;
      default:
        return <PenTool className="w-12 h-12 text-slate-800" strokeWidth={1.5} />;
    }
  };

  // 3. Visual Helpers (Sticky Colors & Rotations)
  const getStickyColor = (index) => {
    const colors = ["bg-[#FEF08A]", "bg-[#BAE6FD]", "bg-[#FBCFE8]"]; // Yellow, Blue, Pink
    return colors[index % colors.length];
  };

  const getRotation = (index) => {
    const rotations = ["rotate-1", "-rotate-1", "rotate-2", "-rotate-2", "rotate-0"];
    return rotations[index % rotations.length];
  };

  // Main UI
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 bg-transparent">

      {/* Header */}
      <div className="relative mb-16 text-center">
        {/* Highlighter effect behind text */}
        <div className="absolute inset-0 bg-[#FEF08A] transform -skew-x-6 rounded-sm opacity-60 -z-10" />
        <h1 className="text-5xl md:text-6xl text-slate-800 font-hand relative z-10 px-4">
          Pick Your Path
        </h1>
      </div>

      {/* Role Cards Grid */}
      <div className="flex flex-wrap gap-10 justify-center max-w-6xl mb-12">
        {roles.map((role, index) => (
          <button
            key={role.id}
            onClick={() => onSelect(role)}
            className={`
              relative w-72 h-72 p-6
              ${getStickyColor(index)}
              ${getRotation(index)}
              border-2 border-slate-700
              shadow-[4px_4px_0px_rgba(0,0,0,0.15)]
              transition-all duration-300
              hover:scale-105 hover:rotate-0 hover:shadow-[8px_8px_0px_rgba(0,0,0,0.2)] hover:z-20
              cursor-pointer
              flex flex-col items-center justify-center gap-4
              group
            `}
          >
            {/* Scotch Tape Visual */}
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-20 h-8 bg-white/30 backdrop-blur-[1px] border-l border-r border-white/40 shadow-sm rotate-1" />

            {/* Icon Circle */}
            <div className="p-4 bg-white/20 rounded-full border border-slate-700/10 group-hover:bg-white/40 transition-colors">
              {getIconComponent(role.icon)}
            </div>

            {/* Title */}
            <h2 className="text-3xl text-slate-800 font-hand font-bold">
              {role.label}
            </h2>

            {/* Description */}
            <p className="text-sm text-slate-700 text-center leading-relaxed font-sans px-2">
              {role.description}
            </p>
          </button>
        ))}
      </div>

      {/* Back Button */}
      <button
        onClick={onBack}
        className="text-xl text-slate-500 hover:text-slate-800 transition-colors font-hand flex items-center gap-2 group"
      >
        <span className="group-hover:-translate-x-1 transition-transform">←</span> 
        Back to Cover
      </button>
    </div>
  );
}