const API_URL = "http://127.0.0.1:8000"

export async function getPublicJobs() {
  const response = await fetch(`${API_URL}/job-offers/public`)

  if (!response.ok) {
    throw new Error("Failed to fetch jobs")
  }

  return response.json()
}