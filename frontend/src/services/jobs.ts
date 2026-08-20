const API_URL = "http://127.0.0.1:8000"


// ============================================================
// TYPES
// ============================================================

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


// ============================================================
// RESPONSE HANDLER
// ============================================================

async function handleResponse(
  response: Response,
) {
  if (!response.ok) {
    const error = await response.text()

    throw new Error(
      error || `Request failed: ${response.status}`,
    )
  }

  return response.json()
}


// ============================================================
// SEARCH PARAMS
// ============================================================

function buildJobSearchParams(
  filters: JobFilters,
) {
  const params = new URLSearchParams()

  const keyword =
    filters.keyword?.trim()

  const country =
    filters.country?.trim()

  const city =
    filters.city?.trim()

  const published =
    filters.published?.trim()

  const workType =
    filters.workType?.trim()

  if (keyword) {
    params.set(
      "keyword",
      keyword,
    )
  }

  if (country) {
    params.set(
      "country",
      country,
    )
  }

  if (city) {
    params.set(
      "city",
      city,
    )
  }

  if (published) {
    params.set(
      "published",
      published,
    )
  }

  if (workType) {
    params.set(
      "workType",
      workType,
    )
  }

  return params
}


// ============================================================
// PUBLIC JOB SEARCH
// ============================================================
//
// IMPORTANT:
//
// This function ALWAYS performs public search.
//
// It is intentionally kept because SearchTabs.tsx imports
// searchPublicJobs directly.
//
// Public users:
//   /job-offers/public
//
// Match Score:
//   null
//
// ============================================================

export async function searchPublicJobs(
  filters: JobFilters,
) {
  const params =
    buildJobSearchParams(filters)

  const response = await fetch(
    `${API_URL}/job-offers/public?${params.toString()}`,
  )

  const jobs =
    await handleResponse(response)

  /*
   * Never expose Match Score through
   * the public endpoint.
   */

  return jobs.map((job: any) => ({
    ...job,
    match_score: null,
  }))
}


// ============================================================
// AUTHENTICATED JOB SEARCH
// ============================================================
//
// Logged-in users:
//
//   /job-offers/search
//
// This endpoint returns Match Score.
//
// ============================================================

export async function searchAuthenticatedJobs(
  filters: JobFilters,
  token: string,
) {
  const params =
    buildJobSearchParams(filters)

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


// ============================================================
// SMART JOB SEARCH
// ============================================================
//
// This is the function that should be used by the main
// Job Search UI.
//
// Guest:
//   → searchPublicJobs()
//   → no Match Score
//
// Logged user:
//   → searchAuthenticatedJobs()
//   → Match Score
//
// ============================================================

export async function searchJobs(
  filters: JobFilters,
) {
  const token =
    localStorage.getItem("token")

  /*
   * ----------------------------------------------------------
   * GUEST
   * ----------------------------------------------------------
   */

  if (!token) {
    return searchPublicJobs(
      filters,
    )
  }


  /*
   * ----------------------------------------------------------
   * LOGGED USER
   * ----------------------------------------------------------
   */

  try {
    return await searchAuthenticatedJobs(
      filters,
      token,
    )
  } catch (error) {

    /*
     * If the token is invalid/expired,
     * do not break Job Search.
     *
     * Fall back to public search.
     */

    if (
      error instanceof Error &&
      (
        error.message.includes("401") ||
        error.message
          .toLowerCase()
          .includes("token") ||
        error.message
          .toLowerCase()
          .includes("auth")
      )
    ) {
      localStorage.removeItem(
        "token",
      )

      return searchPublicJobs(
        filters,
      )
    }

    throw error
  }
}


// ============================================================
// PUBLIC JOBS
// ============================================================
//
// Kept for compatibility with existing components.
//
// IMPORTANT:
//
// Despite the historical name "getPublicJobs",
// this function now performs SMART SEARCH.
//
// Guest:
//   public
//
// Logged user:
//   authenticated + Match Score
//
// ============================================================

export async function getPublicJobs(
  filters: JobFilters,
) {
  return searchJobs(
    filters,
  )
}


// ============================================================
// AUTHENTICATED / PUBLIC SEARCH
// ============================================================
//
// Kept for compatibility with existing components.
//
// Guest:
//   public
//
// Logged user:
//   authenticated
//
// ============================================================

export async function searchJobsForUser(
  filters: JobFilters,
) {
  return searchJobs(
    filters,
  )
}


// ============================================================
// LOCATIONS
// ============================================================

export async function getJobLocations(): Promise<
  JobLocation[]
> {
  const response = await fetch(
    `${API_URL}/job-offers/locations`,
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// JOB DETAIL
// ============================================================

export async function getJobById(
  id: string,
) {
  const cleanId =
    String(id).trim()

  if (!/^\d+$/.test(cleanId)) {
    throw new Error(
      "Invalid job ID",
    )
  }

  const response = await fetch(
    `${API_URL}/job-offers/public/${cleanId}`,
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// AI ANALYSIS
// ============================================================

export async function analyzeJob(
  id: string,
) {
  const token =
    localStorage.getItem("token")

  if (!token) {
    throw new Error(
      "Authentication required",
    )
  }

  const cleanId =
    String(id).trim()

  if (!/^\d+$/.test(cleanId)) {
    throw new Error(
      "Invalid job ID",
    )
  }

  const response = await fetch(
    `${API_URL}/api/career/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",

        Authorization:
          `Bearer ${token}`,
      },

      body: JSON.stringify({
        job_offer_id:
          Number(cleanId),
      }),
    },
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// OPTIMIZED CV
// ============================================================

export async function getOptimizedCV(
  jobId: string,
  token: string,
) {
  const cleanJobId =
    String(jobId).trim()

  const response = await fetch(
    `${API_URL}/api/career/optimized-cv/${cleanJobId}`,
    {
      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    },
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// COVER LETTER
// ============================================================

export async function getCoverLetter(
  jobId: string,
  token: string,
) {
  const cleanJobId =
    String(jobId).trim()

  const response = await fetch(
    `${API_URL}/api/career/cover-letter/${cleanJobId}`,
    {
      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    },
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// APPLICATION ANSWERS
// ============================================================

export async function getApplicationAnswers(
  jobId: string,
  token: string,
) {
  const cleanJobId =
    String(jobId).trim()

  const response = await fetch(
    `${API_URL}/api/career/application-answers/${cleanJobId}`,
    {
      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    },
  )

  return handleResponse(
    response,
  )
}


// ============================================================
// INTERVIEW PREPARATION
// ============================================================

export async function getInterviewPreparation(
  jobId: string,
  token: string,
) {
  const cleanJobId =
    String(jobId).trim()

  const response = await fetch(
    `${API_URL}/api/career/interview-preparation/${cleanJobId}`,
    {
      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    },
  )

  return handleResponse(
    response,
  )
}
