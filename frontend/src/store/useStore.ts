import { create } from 'zustand';
import axios from 'axios';

interface User {
    id: number;
    email: string;
}

interface MatchResult {
    job_role: string;
    score: number;
}

interface AppState {
    user: User | null;
    token: string | null;
    isLoading: boolean;

    // Actions
    setAuth: (token: string, user: User) => void;
    logout: () => void;
    setLoading: (loading: boolean) => void;

    // Async
    checkAuth: () => Promise<void>;
}

export const useStore = create<AppState>((set) => ({
    user: null,
    token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
    isLoading: false,

    setAuth: (token, user) => {
        localStorage.setItem('token', token);
        set({ token, user });
    },

    logout: () => {
        localStorage.removeItem('token');
        set({ token: null, user: null });
    },

    setLoading: (loading) => set({ isLoading: loading }),

    checkAuth: async () => {
        // A placeholder for verifying token validity if backend supports it
        // For now, if token exists, we simulate persistence
        const token = localStorage.getItem('token');
        if (token) {
            set({ token });
        }
    }
}));
