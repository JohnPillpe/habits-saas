const API_URL = "http://127.0.0.1:8000"

export type JobFilters = {
  keyword: string
  country: string
  city: string
  published: string
  workType: string
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.text()
    throw new Error(error || `Request failed: ${response.status}`)
  }

  return response.json()
}

export async function searchJobs(filters: JobFilters) {
  const params = new URLSearchParams()

  if (filters.keyword.trim()) {
    params.set("keyword", filters.keyword.trim())
  }

  if (filters.country.trim()) {
    params.set("country", filters.country.trim())
  }

  if (filters.city.trim()) {
    params.set("city", filters.city.trim())
  }

  if (filters.published) {
    params.set("published", filters.published)
  }

  if (filters.workType.trim()) {
    params.set("workType", filters.workType.trim())
  }

  const response = await fetch(
    `${API_URL}/job-offers/public?${params.toString()}`
  )

  return handleResponse(response)
}

export async function getPublicJobs(filters: JobFilters) {
  return searchJobs(filters)
}

export async function getJobById(id: string) {
  const response = await fetch(
    `${API_URL}/job-offers/public/${id}`
  )

  return handleResponse(response)
}

export async function analyzeJob(id: string) {
  const token = localStorage.getItem("token")

  if (!token) {
    throw new Error("Authentication required")
  }

  const response = await fetch(
    `${API_URL}/api/career/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        job_offer_id: Number(id),
      }),
    }
  )

  return handleResponse(response)
}

export async function getOptimizedCV(
  jobId: string,
  token: string,
) {
  const response = await fetch(
    `${API_URL}/api/career/optimized-cv/${jobId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  return handleResponse(response)
}

export async function getCoverLetter(
  jobId: string,
  token: string,
) {
  const response = await fetch(
    `${API_URL}/api/career/cover-letter/${jobId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  return handleResponse(response)
}

export async function getApplicationAnswers(
  jobId: string,
  token: string,
) {
  const response = await fetch(
    `${API_URL}/api/career/application-answers/${jobId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  return handleResponse(response)
}

export async function getInterviewPreparation(
  jobId: string,
  token: string,
) {
  const response = await fetch(
    `${API_URL}/api/career/interview-preparation/${jobId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  return handleResponse(response)
}

export async function searchJobsForUser(
  filters: JobFilters,
) {
  const token = localStorage.getItem("token")

  if (!token) {
    throw new Error("Authentication required")
  }

  const params = new URLSearchParams()

  if (filters.keyword.trim()) {
    params.set("keyword", filters.keyword.trim())
  }

  if (filters.country.trim()) {
    params.set("country", filters.country.trim())
  }

  if (filters.city.trim()) {
    params.set("city", filters.city.trim())
  }

  if (filters.published) {
    params.set("published", filters.published)
  }

  if (filters.workType.trim()) {
    params.set("workType", filters.workType.trim())
  }

  const response = await fetch(
    `${API_URL}/job-offers/search?${params.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return handleResponse(response)
}