import { writable } from 'svelte/store';

interface RatingFormDetails {
	name: string;
	product_id: number;
}

export const ratingDetails = writable<RatingFormDetails>({
	name: "Overall",
	product_id: 0
});
