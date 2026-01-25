'use client';

import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer
} from 'recharts';

interface SkillGapChartProps {
    matchedSkills: string[];
    missingSkills: string[];
}

export default function SkillGapChart({ matchedSkills, missingSkills }: SkillGapChartProps) {
    // Transform data for chart: assign a value (e.g. 100 for matched, 50 for missing)
    const data = [
        ...matchedSkills.map(skill => ({ subject: skill, A: 100, fullMark: 100 })),
        ...missingSkills.map(skill => ({ subject: skill, A: 40, fullMark: 100 }))
    ];

    if (data.length === 0) return <div className="text-center text-gray-500">No data available</div>;

    return (
        <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#6B7280', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                        name="Skill Match"
                        dataKey="A"
                        stroke="#4F46E5"
                        strokeWidth={2}
                        fill="#6366F1"
                        fillOpacity={0.6}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}
