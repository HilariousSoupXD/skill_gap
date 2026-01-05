import React, { useMemo, useState } from 'react';
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from 'recharts';
import { Paperclip, GraduationCap, Code, BookOpen, Youtube, FileText } from 'lucide-react';

export default function Dashboard({ evaluationResult, studentProfile, selectedRole, onRestart }) {
  // Track completed resources per week (week + resourceId combination) - for display only, doesn't update radar
  const [completedResources, setCompletedResources] = useState(new Set());

  // Create resource lookup map with full resource data
  const resourceMap = useMemo(() => {
    if (!evaluationResult?.plan?.selected_resources) return new Map();
    return new Map(
      evaluationResult.plan.selected_resources.map(r => [r.id, r])
    );
  }, [evaluationResult]);

  // Transform skill levels to radar data format (using original studentProfile, no updates)
  const radarData = useMemo(() => {
    return selectedRole.skills.map(skill => ({
      skill,
      value: (studentProfile[skill] || 0) * 100, // Convert to 0-100 scale
    }));
  }, [studentProfile, selectedRole]);

  // Get plan weeks
  const planWeeks = evaluationResult?.plan?.weeks || {};

  // Helper function to generate explanation for priority/skim labels
  const getResourceExplanation = (resource) => {
    const roleRequirementsFull = evaluationResult?.role_requirements_full || {};
    const gaps = evaluationResult?.gaps || {};
    
    const explanations = [];
    
    // Check priority reason
    if (resource.priority === 'high') {
      const highWeightSkills = [];
      for (const skill of resource.covered_skills || []) {
        if (roleRequirementsFull[skill]) {
          const weight = roleRequirementsFull[skill].weight || 0;
          const gap = gaps[skill] || 0;
          const required = roleRequirementsFull[skill].required || 0;
          const current = studentProfile[skill] || 0;
          
          // High priority: high weight AND significant gap
          if (weight >= 0.15 && gap > 0.2) {
            highWeightSkills.push({ 
              skill, 
              weight: (weight * 100).toFixed(0), 
              gap: (gap * 100).toFixed(0),
              current: (current * 100).toFixed(0),
              required: (required * 100).toFixed(0)
            });
          }
        }
      }
      if (highWeightSkills.length > 0) {
        const skillNames = highWeightSkills.map(s => s.skill).join(', ');
        const maxWeight = Math.max(...highWeightSkills.map(s => parseFloat(s.weight)));
        const maxGap = Math.max(...highWeightSkills.map(s => parseFloat(s.gap)));
        explanations.push(`High priority: Covers critical skills (${skillNames}) with ${maxWeight}% role weight and ${maxGap}% skill gap`);
      }
    } else if (resource.priority === 'medium') {
      const mediumReasons = [];
      for (const skill of resource.covered_skills || []) {
        if (roleRequirementsFull[skill]) {
          const weight = roleRequirementsFull[skill].weight || 0;
          const gap = gaps[skill] || 0;
          const required = roleRequirementsFull[skill].required || 0;
          const current = studentProfile[skill] || 0;
          
          if (weight >= 0.15 && gap > 0.05 && gap <= 0.2) {
            // High weight but small gap
            mediumReasons.push(`high-weight skill (${skill}, ${(weight * 100).toFixed(0)}%) with small gap`);
          } else if (weight >= 0.1 && weight < 0.15 && gap > 0.1) {
            // Medium weight with gap
            mediumReasons.push(`medium-weight skill (${skill}, ${(weight * 100).toFixed(0)}%)`);
          } else if (gap > 0.2) {
            // Any weight with significant gap
            mediumReasons.push(`significant gap in ${skill}`);
          }
        }
      }
      if (mediumReasons.length > 0) {
        explanations.push(`Medium priority: ${mediumReasons.join(', ')}`);
      }
    }
    
    // Check skim reason (mutually exclusive with high priority)
    if (resource.can_skim) {
      const skimReasons = [];
      for (const skill of resource.covered_skills || []) {
        if (roleRequirementsFull[skill]) {
          const weight = roleRequirementsFull[skill].weight || 0;
          const required = roleRequirementsFull[skill].required || 0;
          const current = studentProfile[skill] || 0;
          const gap = gaps[skill] || 0;
          
          if (weight >= 0.15 && current >= required) {
            // High weight but already proficient
            skimReasons.push(`already proficient in high-weight skill ${skill} (${(weight * 100).toFixed(0)}% role weight)`);
          } else if (weight >= 0.15 && gap <= 0.05) {
            // High weight but very small gap (almost proficient)
            skimReasons.push(`nearly proficient in high-weight skill ${skill} (${(weight * 100).toFixed(0)}% role weight, ${(gap * 100).toFixed(0)}% gap)`);
          } else if (weight < 0.1) {
            // Low weight
            skimReasons.push(`low-weight skill (${skill}, ${(weight * 100).toFixed(0)}% role weight)`);
          } else if (current >= required) {
            // Already proficient
            skimReasons.push(`already proficient in ${skill}`);
          }
        }
      }
      if (skimReasons.length > 0) {
        explanations.push(`Can skim: ${skimReasons.join(', ')}`);
      }
    }
    
    return explanations.length > 0 ? explanations.join('. ') : null;
  };

  // Handle checkbox toggle - track by week and resourceId (for display only)
  const handleResourceToggle = (weekNum, resourceId) => {
    const resourceKey = `${weekNum}-${resourceId}`;
    setCompletedResources(prev => {
      const newSet = new Set(prev);
      if (newSet.has(resourceKey)) {
        newSet.delete(resourceKey);
      } else {
        newSet.add(resourceKey);
      }
      return newSet;
    });
  };

  // Check if a resource is completed in a specific week
  const isResourceCompleted = (weekNum, resourceId) => {
    return completedResources.has(`${weekNum}-${resourceId}`);
  };

  return (
    <div className="min-h-screen p-8 bg-transparent">
      {/* Header with Title and Assessment Complete Stamp */}
      <div className="relative mb-8">
        {/* Main Title */}
        <div className="mb-6">
          <h1 className="text-5xl md:text-6xl font-hand text-slate-800">
            Skills Assessment Report
          </h1>
          <p className="text-lg md:text-xl font-sans text-slate-600 mt-2">
            Your personalized learning roadmap
          </p>
        </div>
        
        {/* Assessment Complete Stamp - Red, rotated, stencil-like */}
        <div className="absolute top-0 right-0 z-20">
          <div className="px-6 py-3 border-4 border-red-600 bg-white rotate-[-12deg] shadow-[4px_4px_0px_rgba(0,0,0,0.2)]">
            <span className="text-red-600 font-bold text-xl md:text-2xl tracking-wider uppercase" style={{ fontFamily: 'Arial, sans-serif', letterSpacing: '0.1em' }}>
              ASSESSMENT COMPLETE
            </span>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
        
        {/* Left Column: Stats Panel */}
        <div className="space-y-8">
          
          {/* Skill Levels Section */}
          <div className="bg-white border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.15)] p-6 rotate-1 overflow-visible">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-hand text-slate-800">Skill Levels</h2>
            </div>
            
            {/* Radar Chart */}
            <div className="flex justify-center items-center w-full py-4 overflow-visible">
              <div className="relative" style={{ width: '400px', height: '400px' }}>
                <RadarChart 
                  width={400} 
                  height={400} 
                  data={radarData} 
                  margin={{ top: 40, right: 50, bottom: 40, left: 50 }}
                >
                <defs>
                  {/* Custom striped pattern for fill - scribbled look */}
                  <pattern
                    id="radarPattern"
                    x="0"
                    y="0"
                    width="8"
                    height="8"
                    patternUnits="userSpaceOnUse"
                  >
                    <path
                      d="M 0 8 L 8 0"
                      stroke="#BAE6FD"
                      strokeWidth="1.2"
                      strokeLinecap="round"
                    />
                  </pattern>
                </defs>
                <PolarGrid stroke="#cbd5e1" />
                <PolarAngleAxis
                  dataKey="skill"
                  tick={{ fill: '#1e293b', fontSize: 14, fontFamily: 'Nunito' }}
                />
                <PolarRadiusAxis
                  angle={90}
                  domain={[0, 100]}
                  tick={{ fill: '#64748b', fontSize: 12 }}
                />
                <Radar
                  name="Your current level"
                  dataKey="value"
                  stroke="#1e293b"
                  strokeWidth={2}
                  fill="url(#radarPattern)"
                  fillOpacity={0.7}
                />
              </RadarChart>
              </div>
            </div>

            {/* Legend */}
            <div className="flex items-center justify-center gap-2 mt-4">
              <svg width="24" height="16" className="border border-slate-700">
                <defs>
                  <pattern
                    id="legendPattern"
                    x="0"
                    y="0"
                    width="8"
                    height="8"
                    patternUnits="userSpaceOnUse"
                  >
                    <path
                      d="M 0 8 L 8 0"
                      stroke="#BAE6FD"
                      strokeWidth="1.2"
                      strokeLinecap="round"
                    />
                  </pattern>
                </defs>
                <rect width="24" height="16" fill="url(#legendPattern)" fillOpacity={0.7} />
              </svg>
              <span className="text-sm font-sans text-slate-700">Your current level</span>
            </div>
          </div>

          {/* Skill Importance Section */}
          <div className="bg-white border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.15)] p-6 -rotate-1">
            <h2 className="text-3xl font-hand text-slate-800 mb-4">Skill Importance</h2>
            <p className="text-sm font-sans text-slate-600 mb-4 italic">
              Skills ranked by importance for {selectedRole?.label || 'this role'}
            </p>
            <div className="space-y-3">
              {(() => {
                const roleRequirementsFull = evaluationResult?.role_requirements_full || {};
                const skillsWithWeights = selectedRole?.skills
                  ?.map(skill => ({
                    skill,
                    weight: roleRequirementsFull[skill]?.weight || 0,
                    required: roleRequirementsFull[skill]?.required || 0
                  }))
                  .filter(s => s.weight > 0)
                  .sort((a, b) => b.weight - a.weight) || [];
                
                if (skillsWithWeights.length === 0) {
                  return <p className="text-slate-600 font-sans">No skill data available</p>;
                }
                
                return skillsWithWeights.map(({ skill, weight, required }, index) => {
                  const weightPercent = (weight * 100).toFixed(0);
                  // Different colors for each skill based on index for variety
                  const colorSchemes = [
                    { border: 'border-red-500', bg: 'bg-red-50' },
                    { border: 'border-orange-500', bg: 'bg-orange-50' },
                    { border: 'border-yellow-500', bg: 'bg-yellow-50' },
                    { border: 'border-green-500', bg: 'bg-green-50' },
                    { border: 'border-blue-500', bg: 'bg-blue-50' },
                    { border: 'border-indigo-500', bg: 'bg-indigo-50' },
                    { border: 'border-purple-500', bg: 'bg-purple-50' },
                    { border: 'border-pink-500', bg: 'bg-pink-50' },
                  ];
                  const colorScheme = colorSchemes[index % colorSchemes.length];
                  const borderColor = colorScheme.border;
                  const bgColor = colorScheme.bg;
                  
                  return (
                    <div
                      key={skill}
                      className={`inline-block border-2 ${borderColor} ${bgColor} rounded-full rotate-2 px-5 py-2.5 mx-2 mb-2 relative group min-w-fit`}
                    >
                      <span className="text-lg font-hand text-slate-800 whitespace-nowrap">{skill}</span>
                      <span className="ml-2 text-xs font-hand text-slate-600 whitespace-nowrap">({weightPercent}%)</span>
                      {/* Tooltip on hover */}
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-slate-800 text-white text-xs font-sans rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                        {weightPercent}% role weight • Required: {(required * 100).toFixed(0)}%
                      </div>
                    </div>
                  );
                });
              })()}
            </div>
          </div>
        </div>

        {/* Right Column: Learning Plan Timeline */}
        <div className="space-y-6">
          <div className="bg-white border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.15)] p-6 rotate-1">
            <h2 className="text-3xl font-hand text-slate-800 mb-6">Learning Plan</h2>
            
            {/* Adjustment Note */}
            {evaluationResult?.plan?.adjustment_note && (
              <div className="mb-4 p-3 bg-yellow-50 border-2 border-yellow-300 rounded rotate-1">
                <p className="text-sm font-sans text-yellow-900">
                  📝 {evaluationResult.plan.adjustment_note}
                </p>
              </div>
            )}
            
            {/* Week Items */}
            <div className="pl-8 space-y-8">
                {Object.entries(planWeeks).map(([weekNum, resourceIds]) => {
                  const weekResources = resourceIds
                    .map(id => resourceMap.get(id))
                    .filter(Boolean);

                  return (
                    <div key={weekNum} className="relative">
                      {/* Week Circle */}
                      <div className="absolute -left-12 top-0 w-8 h-8 bg-[#FEF08A] border-2 border-slate-700 rounded-full flex items-center justify-center shadow-sm">
                        <span className="text-sm font-hand font-bold text-slate-800">
                          {weekNum}
                        </span>
                      </div>

                      {/* Week Content */}
                      <div className="ml-2">
                        <h3 className="text-2xl font-hand text-slate-800 mb-3">
                          Week {weekNum}
                        </h3>

                        {/* Tasks */}
                        {weekResources.length > 0 ? (
                          <div className="space-y-3 mb-4">
                            {weekResources.map((resource) => {
                              const priority = resource.priority || 'medium';
                              const canSkim = resource.can_skim || false;
                              const priorityColors = {
                                high: 'bg-red-100 border-red-300 text-red-800',
                                medium: 'bg-yellow-100 border-yellow-300 text-yellow-800',
                                low: 'bg-blue-100 border-blue-300 text-blue-800'
                              };
                              // If can skim, show "Can Skim" label instead of priority
                              const priorityLabels = {
                                high: '🔥 High Priority',
                                medium: '⭐ Medium Priority',
                                low: canSkim ? '💨 Can Skim' : '📚 Low Priority'
                              };
                              
                              return (
                                <div key={resource.id} className="space-y-1">
                                  <div className="flex items-start gap-2">
                                    <input
                                      type="checkbox"
                                      className="mt-1 w-5 h-5 border-2 border-slate-700 rounded-sm cursor-pointer accent-slate-700"
                                      checked={isResourceCompleted(weekNum, resource.id)}
                                      onChange={() => handleResourceToggle(weekNum, resource.id)}
                                    />
                                    <div className="flex-1 min-w-0">
                                      <div className="flex flex-wrap items-center gap-2">
                                        <span className="text-slate-800 font-sans break-words">
                                          {resource.title}
                                          {resource.is_split && resource.part && (
                                            <span className="text-xs text-slate-500 ml-1">({resource.part})</span>
                                          )}
                                        </span>
                                        {/* Priority Badge */}
                                        <span className={`px-2 py-0.5 text-xs font-hand border-2 rounded rotate-1 flex-shrink-0 ${priorityColors[priority]}`}>
                                          {priorityLabels[priority]}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                  {/* Covered Skills */}
                                  {resource.covered_skills && resource.covered_skills.length > 0 && (
                                    <div className="ml-7 text-xs text-slate-600 font-sans">
                                      Covers: {resource.covered_skills.join(', ')}
                                    </div>
                                  )}
                                  {/* Resource Link with Icon */}
                                  {resource.url && (
                                    <div className="ml-7 mt-1 flex items-center gap-2">
                                      {(() => {
                                        const iconType = resource.icon_type || resource.type || 'docs';
                                        const iconProps = { className: "w-4 h-4 text-slate-600 flex-shrink-0" };
                                        
                                        switch(iconType) {
                                          case 'university':
                                            return <GraduationCap {...iconProps} />;
                                          case 'code':
                                            return <Code {...iconProps} />;
                                          case 'youtube':
                                            return <Youtube {...iconProps} />;
                                          case 'docs':
                                          case 'theory':
                                            return <BookOpen {...iconProps} />;
                                          default:
                                            return <FileText {...iconProps} />;
                                        }
                                      })()}
                                      <a
                                        href={resource.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-blue-600 underline decoration-wavy decoration-blue-400 font-sans text-xs hover:text-blue-800"
                                      >
                                        {resource.title}
                                      </a>
                                    </div>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        ) : (
                          <p className="text-slate-500 font-sans text-sm mb-4">
                            No tasks assigned this week
                          </p>
                        )}
                      </div>
                    </div>
                  );
                })}

                {Object.keys(planWeeks).length === 0 && (
                  <p className="text-slate-500 font-sans">No learning plan available</p>
                )}
              </div>
          </div>
        </div>
      </div>

      {/* Footer: Restart Analysis Button */}
      <div className="flex justify-center mt-12 mb-8">
        <button
          onClick={onRestart}
          className="px-8 py-4 bg-[#FBCFE8] border-2 border-slate-700 shadow-[4px_4px_0px_rgba(0,0,0,0.15)] font-hand text-xl text-slate-800 hover:bg-[#F9A8D4] hover:shadow-[6px_6px_0px_rgba(0,0,0,0.2)] transition-all duration-200 rotate-1 hover:rotate-0 active:shadow-[2px_2px_0px_rgba(0,0,0,0.15)] active:translate-x-1 active:translate-y-1"
        >
          Restart Analysis
        </button>
      </div>
    </div>
  );
}

