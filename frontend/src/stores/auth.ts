import { writable } from 'svelte/store';

interface AuthDetails {
	username: string;
	token: string;
}

// undefined maens not logged in
export const authDetails = writable<AuthDetails>(undefined);
