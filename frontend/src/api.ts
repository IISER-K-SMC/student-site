
export const API_URL = "http://localhost:8000/";

export async function getMenu(): Promise<MenuItem[]>  {
	const res = await fetch(API_URL + 'menu/');
	if (res.status !== 200) {
		throw new Error("Invalid status from API");
	}
	return await res.json()
}

export interface MenuItem {
	product_id: number;
	name: string;
	meal: number;
	special: boolean;
}

export interface FeedbackData {
	product_id: number;
	stars: number;
	feedback: string;
	username: string;
}

export async function sendFeedback(
		feedbackData: FeedbackData
	){
	const res = await fetch(API_URL + 'feedback/', {
		method: "POST",
		headers: {
      		'Accept': 'application/json',
      		'Content-Type': 'application/json'
    	},
		body: JSON.stringify(feedbackData)
	});
	if (res.status !== 200) {
		throw new Error("Invalid status from API");
	}
	return await res.json()
}
