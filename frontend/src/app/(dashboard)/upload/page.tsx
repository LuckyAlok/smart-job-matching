'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { useStore } from '@/store/useStore';
import Dropzone from '@/components/upload/Dropzone';
import { FileText, CheckCircle2 } from 'lucide-react';
import { config } from '@/config';


export default function UploadPage() {
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [uploadSuccess, setUploadSuccess] = useState(false);
    const { token, setAuth } = useStore();
    const router = useRouter();

    const handleFileSelect = async (file: File) => {
        if (!token) {
            router.push('/login');
            return;
        }

        setIsUploading(true);
        setError(null);
        setUploadSuccess(false);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // 1. Upload Resume
            const response = await axios.post(`${config.API_URL}/resume/upload`, formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data',
                },
            });

            // 2. Add fake progress delay for UX
            await new Promise(resolve => setTimeout(resolve, 1500));

            console.log('Upload success:', response.data);
            setUploadSuccess(true);

            // 3. Redirect to dashboard after short delay
            setTimeout(() => {
                router.push('/dashboard');
            }, 1000);

        } catch (err: any) {
            console.error('Upload failed:', err);
            setError(err.response?.data?.detail || 'Failed to upload resume. Please try again.');
        } finally {
            setIsUploading(false);
        }
    };

    if (uploadSuccess) {
        return (
            <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
                <div className="bg-white p-8 rounded-2xl shadow-xl text-center max-w-md w-full animate-in fade-in zoom-in duration-300">
                    <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-6">
                        <CheckCircle2 className="w-8 h-8 text-green-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Resume Analyzed!</h2>
                    <p className="text-gray-500 mb-6">
                        We've extracted your skills and experience. Redirecting to your personalized dashboard...
                    </p>
                    <div className="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                        <div className="h-full bg-green-500 animate-[progress_1s_ease-in-out_infinite]" style={{ width: '100%' }}></div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-4xl mx-auto pt-10">
                <div className="text-center mb-10">
                    <h1 className="text-3xl font-bold text-gray-900 mb-3">Upload Your Resume</h1>
                    <p className="text-gray-500 max-w-lg mx-auto">
                        Drag and drop your PDF resume to let our AI extract your skills and match you with the best job roles.
                    </p>
                </div>

                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                    <Dropzone
                        onFileSelect={handleFileSelect}
                        isUploading={isUploading}
                        error={error}
                    />

                    <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="flex flex-col items-center text-center p-4">
                            <div className="p-3 bg-blue-50 rounded-lg mb-3">
                                <FileText className="w-6 h-6 text-blue-600" />
                            </div>
                            <h3 className="font-semibold text-gray-900">Smart Parsing</h3>
                            <p className="text-sm text-gray-500 mt-1">Automatically extracts skills, experience, and education.</p>
                        </div>
                        <div className="flex flex-col items-center text-center p-4">
                            <div className="p-3 bg-purple-50 rounded-lg mb-3">
                                <CheckCircle2 className="w-6 h-6 text-purple-600" />
                            </div>
                            <h3 className="font-semibold text-gray-900">Instant Matching</h3>
                            <p className="text-sm text-gray-500 mt-1">Compare your profile against top job roles instantly.</p>
                        </div>
                        <div className="flex flex-col items-center text-center p-4">
                            <div className="p-3 bg-orange-50 rounded-lg mb-3">
                                <CheckCircle2 className="w-6 h-6 text-orange-600" />
                            </div>
                            <h3 className="font-semibold text-gray-900">Gap Analysis</h3>
                            <p className="text-sm text-gray-500 mt-1">Identify missing skills and get course recommendations.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
