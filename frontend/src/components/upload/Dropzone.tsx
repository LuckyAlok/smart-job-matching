'use client';

import { useState, useRef } from 'react';
import { UploadCloud, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface DropzoneProps {
    onFileSelect: (file: File) => void;
    isUploading: boolean;
    progress?: number;
    error?: string | null;
}

export default function Dropzone({ onFileSelect, isUploading, progress, error }: DropzoneProps) {
    const [isDragActive, setIsDragActive] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragActive(true);
        } else if (e.type === 'dragleave') {
            setIsDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            // Check file type
            const file = e.dataTransfer.files[0];
            if (file.type === 'application/pdf') {
                onFileSelect(file);
            } else {
                alert('Please upload a PDF file.');
            }
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <div className="w-full max-w-xl mx-auto">
            <div
                className={`relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl transition-colors duration-300 ${isDragActive
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 bg-white hover:bg-gray-50'
                    } ${error ? 'border-red-500 bg-red-50' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => !isUploading && inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    className="hidden"
                    accept="application/pdf"
                    onChange={handleChange}
                    disabled={isUploading}
                />

                <AnimatePresence mode='wait'>
                    {isUploading ? (
                        <motion.div
                            key="uploading"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center"
                        >
                            <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
                            <p className="text-lg font-medium text-gray-700">Analyzing Resume...</p>
                            {progress !== undefined && (
                                <div className="w-48 h-2 bg-gray-200 rounded-full mt-4 overflow-hidden">
                                    <div
                                        className="h-full bg-blue-500 transition-all duration-300"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                            )}
                        </motion.div>
                    ) : error ? (
                        <motion.div
                            key="error"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center text-center p-4"
                        >
                            <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                            <p className="text-lg font-medium text-red-600 mb-2">Upload Failed</p>
                            <p className="text-sm text-gray-500 mb-4">{error}</p>
                            <button
                                className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50"
                                onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
                            >
                                Try Again
                            </button>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="idle"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center text-center p-4 cursor-pointer"
                        >
                            <div className="p-4 bg-blue-50 rounded-full mb-4">
                                <UploadCloud className="w-8 h-8 text-blue-600" />
                            </div>
                            <p className="text-lg font-medium text-gray-900 mb-1">
                                Click or drag resume here
                            </p>
                            <p className="text-sm text-gray-500">
                                PDF format only (Max 10MB)
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
