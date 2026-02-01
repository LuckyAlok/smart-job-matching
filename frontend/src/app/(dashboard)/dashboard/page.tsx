'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import { useStore } from '@/store/useStore';
import JobCard from '@/components/dashboard/JobCard';
import { useRouter } from 'next/navigation';
import { config } from '@/config';


export default function Dashboard() {
    const [matches, setMatches] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const { token, user } = useStore();
    const router = useRouter();

    // Redirect if not logged in
    useEffect(() => {
        if (!token && typeof window !== 'undefined') {
            router.push('/login');
        }
    }, [token, router]);

    useEffect(() => {
        async function fetchMatches() {
            if (!token) return;
            try {
                setLoading(true);
                // 1. Get Job Roles
                const rolesResp = await axios.get(`${config.API_URL}/job-roles/`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                // 2. Fetch match and recommendations for each role
                // Ideally backend should provide a batch endpoint, but we loop for now (Proof of Concept)
                // Taking top 5 roles for demo
                const roles = rolesResp.data.slice(0, 5);

                const results = await Promise.all(roles.map(async (role: any) => {
                    try {
                        // Get Match Score
                        const matchResp = await axios.post(`${config.API_URL}/matches/${role.id}`, {}, {
                            headers: { Authorization: `Bearer ${token}` }
                        });

                        // Get Recommendations based on missing skills
                        const missing = matchResp.data.missing_skills || [];
                        let courses: any[] = [];

                        if (missing.length > 0) {
                            const recResp = await axios.get(`${config.API_URL}/courses/recommendations?skills=${missing.join(',')}`, {
                                headers: { Authorization: `Bearer ${token}` }
                            });
                            // Flatten the grouped structure for simplicity
                            courses = recResp.data.flatMap((g: any) => g.courses).slice(0, 3);
                        }

                        return {
                            role: role.title,
                            score: matchResp.data.score,
                            matchedSkills: matchResp.data.matched_skills,
                            missingSkills: missing,
                            courses: courses
                        };
                    } catch (error) {
                        console.error(`Error matching role ${role.id}:`, error);
                        return null;
                    }
                }));

                const finalMatches = results.filter(r => r !== null);
                setMatches(finalMatches);

                if (finalMatches.length === 0) {
                    console.warn("No matches found. Check if backend has job roles or if matching failed.");
                }
            } catch (err) {
                console.error("Failed to load dashboard", err);
            } finally {
                setLoading(false);
            }
        }

        fetchMatches();
    }, [token]);

    if (loading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
                <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <p className="mt-4 text-gray-500 font-medium">Analyzing Profile...</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8 flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Your Dashboard</h1>
                        <p className="text-gray-500">Welcome back, {user?.email || 'Candidate'}</p>
                    </div>
                    <button
                        onClick={() => { useStore.getState().logout(); router.push('/login'); }}
                        className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg"
                    >
                        Sign Out
                    </button>
                </header>

                <section className="space-y-6">
                    <h2 className="text-xl font-semibold text-gray-800">Job Matches</h2>
                    <div className="space-y-4">
                        {matches.map((match, idx) => (
                            <JobCard key={idx} {...match} />
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
}
