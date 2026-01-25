'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Briefcase, ChevronDown, ChevronUp } from 'lucide-react';
import ReadinessMeter from './ReadinessMeter';
import SkillGapChart from './SkillGapChart';

interface JobCardProps {
    role: string;
    score: number;
    matchedSkills: string[];
    missingSkills: string[];
    courses: Array<{ title: string; platform: string; link: string; difficulty: string }>;
}

export default function JobCard({ role, score, matchedSkills, missingSkills, courses }: JobCardProps) {
    const [expanded, setExpanded] = useState(false);

    return (
        <motion.div
            layout
            className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-4"
        >
            <div
                className="p-4 flex items-center justify-between cursor-pointer"
                onClick={() => setExpanded(!expanded)}
            >
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-50 rounded-lg">
                        <Briefcase className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900">{role}</h3>
                        <p className="text-sm text-gray-500">
                            {matchedSkills.length} matches • {missingSkills.length} missing
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <div className="text-right">
                        <span className={`text-lg font-bold ${score >= 70 ? 'text-green-600' : 'text-yellow-600'}`}>
                            {score}%
                        </span>
                    </div>
                    {expanded ? <ChevronUp className="w-5 h-5 text-gray-400" /> : <ChevronDown className="w-5 h-5 text-gray-400" />}
                </div>
            </div>

            <AnimatePresence>
                {expanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="border-t border-gray-50 bg-gray-50/50"
                    >
                        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Visuals */}
                            <div className="flex flex-col items-center">
                                <h4 className="text-sm font-semibold text-gray-700 mb-4">Readiness Analysis</h4>
                                <div className="flex gap-8 items-center">
                                    <ReadinessMeter score={score} />
                                </div>
                            </div>

                            <div className="flex flex-col items-center">
                                <h4 className="text-sm font-semibold text-gray-700 mb-2">Skill Gap Radar</h4>
                                <SkillGapChart matchedSkills={matchedSkills} missingSkills={missingSkills} />
                            </div>

                            {/* Recommendations */}
                            <div className="md:col-span-2">
                                <h4 className="text-sm font-semibold text-gray-700 mb-3">Recommended Courses</h4>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                    {courses.length > 0 ? courses.map((course, i) => (
                                        <a
                                            key={i}
                                            href={course.link}
                                            target="_blank"
                                            className="block p-3 bg-white rounded-lg border hover:border-blue-400 transition shadow-sm"
                                        >
                                            <div className="text-xs font-bold text-blue-600 mb-1">{course.platform}</div>
                                            <div className="text-sm font-medium text-gray-900 line-clamp-1">{course.title}</div>
                                            <div className="text-xs text-gray-500 mt-1 capitalize">{course.difficulty}</div>
                                        </a>
                                    )) : <p className="text-sm text-gray-500 italic">No specific recommendations found.</p>}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
