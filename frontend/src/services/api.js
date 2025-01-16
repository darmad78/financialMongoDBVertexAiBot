const API_URL = "http://localhost:8000"; // FastAPI backend URL

export async function getTransactions(userId) {
  const response = await fetch(`${API_URL}/transactions/${userId}`);
  const data = await response.json();
  return data;
}

export async function getBudget(userId) {
  const response = await fetch(`${API_URL}/budget/${userId}`);
  const data = await response.json();
  return data;
}