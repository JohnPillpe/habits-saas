const API_URL = "http://127.0.0.1:8000"

export type JobFilters = {
  keyword: string
  country: string
  city: string
  published: string
  workType: string
}

export type JobLocation = {
  country: string
  city: string
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.text()

    throw new Error(
      error || `Request failed: ${response.status}`
    )
  }

  return response.json()
}

/*
 * --------------------------------------------------
 * BUILD SEARCH PARAMS
 * --------------------------------------------------
 *
 * Single source of truth for all job searches.
 */

function buildJobSearchParams(
  filters: JobFilters,
) {
  const params = new URLSearchParams()

  const keyword = filters.keyword?.trim()
  const country = filters.country?.trim()
  const city = filters.city?.trim()
  const published = filters.published?.trim()
  const workType = filters.workType?.trim()

  if (keyword) {
    params.set("keyword", keyword)
  }

  if (country) {
    params.set("country", country)
  }

  if (city) {
    params.set("city", city)
  }

  if (published) {
    params.set("published", published)
  }

  if (workType) {
    params.set("workType", workType)
  }

  return params
}

/*
 * --------------------------------------------------
 * PUBLIC JOBS
 * --------------------------------------------------
 */

export async function searchJobs(
  filters: JobFilters,
) {
  const params =
    buildJobSearchParams(filters)

  const response = await fetch(
    `${API_URL}/job-offers/public?${params.toString()}`
  )

  return handleResponse(response)
}

export async function getPublicJobs(
  filters: JobFilters,
) {
  return searchJobs(filters)
}

/*
 * --------------------------------------------------
 * JOB LOCATIONS
 * --------------------------------------------------
 */

export async function getJobLocations(): Promise<
  JobLocation[]
> {
  const response = await fetch(
    `${API_URL}/job-offers/locations`
  )

  return handleResponse(response)
}

/*
 * --------------------------------------------------
 * JOB DETAIL
 * --------------------------------------------------
 */

export async function getJobById(
  id: string,
) {
  const response = await fetch(
    `${API_URL}/job-offers/public/${id}`
  )

  return handleResponse(response)
}

/*
 * --------------------------------------------------
 * AI ANALYSIS
 * --------------------------------------------------
 */

export async function analyzeJob(
  id: string,
) {
  const token =
    localStorage.getItem("token")

  if (!token) {
    throw new Error(
      "Authentication required"
    )
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

/*
 * --------------------------------------------------
 * OPTIMIZED CV
 * --------------------------------------------------
 */

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

/*
 * --------------------------------------------------
 * COVER LETTER
 * --------------------------------------------------
 */

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

/*
 * --------------------------------------------------
 * APPLICATION ANSWERS
 * --------------------------------------------------
 */

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

/*
 * --------------------------------------------------
 * INTERVIEW PREPARATION
 * --------------------------------------------------
 */

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

/*
 * --------------------------------------------------
 * AUTHENTICATED SEARCH
 * --------------------------------------------------
 */

export async function searchJobsForUser(
  filters: JobFilters,
) {
  const token =
    localStorage.getItem("token")

  if (!token) {
    throw new Error(
      "Authentication required"
    )
  }

  const params =
    buildJobSearchParams(filters)

  const response = await fetch(
    `${API_URL}/job-offers/search?${params.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  return handleResponse(response)
}