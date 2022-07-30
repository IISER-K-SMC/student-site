export async function getMenu(): Promise<MenuItem[]>  {
	const res = await fetch(API_URL + 'menu');
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
	product_name: string;
	stars: number;
	feedback: string;
}

export async function sendFeedback(
		feedbackData: FeedbackData,
		token: string,
	){
	const res = await fetch(API_URL + 'feedback', {
		method: "POST",
		headers: {
      		'Accept': 'application/json',
      		'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token,
    	},
		body: JSON.stringify(feedbackData)
	});
	switch(res.status){
		case 200:
			return await res.json()
		case 401:
			throw new Error("Authentication error please login again");
		default:
			throw new Error("Invalid status from API");
	}
}

export interface FeedbackResponse {
	datetime: string;
	username: string;
	stars: number;
	productName: string;
	feedback: string;
}

export async function getFeedbacks(after: string, before: string): Promise<FeedbackResponse[]> {
	const res = await fetch(API_URL + 'get-feedback?'
							+ new URLSearchParams({before, after})
						   );
	return await res.json()
}


/**
* Returns the authentication token
*/
export async function authenticate(username: string, password: string): Promise<string>{
	const res = await fetch(API_URL + "token", {
		method: 'POST',
		body: 'grant_type=password&username=' + username + '&password=' + password,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		}
	});
	switch(res.status) {
		case 200:
			const data = await res.json();
			return data.access_token;
		case 400:
			throw new Error("Invalid username or password");
		default:
			throw new Error("Unknown error");

	}
}

export async function logout_user(token: string) {
	const res = await fetch(API_URL + 'logout',{
		headers: {
      		'Accept': 'application/json',
      		'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token,
    	},
	});
	switch(res.status){
		case 200:
			console.log("LOGGED OUT")
			return await res.json()
		default:
			throw new Error("Invalid status from API");
	}
}
export async function get_past_orders(token: string) {
	const res = await fetch(API_URL + 'orders',{
		headers: {
      		'Accept': 'application/json',
      		'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token,
    	},
	});
	switch(res.status){
		case 200:
			const data = res.json()
			return data
		default:
			throw new Error("Invalid status from API");
	}
}
