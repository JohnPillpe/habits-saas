import { useState } from "react"

import { Button } from "@/components/ui/button"

import AnalysisTabs from "@/components/job-details/AnalysisTabs"
import CareerToolkit from "@/components/job-details/CareerToolkit"

import {
  getOptimizedCV,
  getCoverLetter,
  getApplicationAnswers,
  getInterviewPreparation,
} from "@/services/jobs"

export default function AnalyzeJobSection() {
  const [jobId, setJobId] = useState<number | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)

  const [optimizedCV, setOptimizedCV] = useState<any>(null)
  const [coverLetter, setCoverLetter] = useState<any>(null)
  const [applicationAnswers, setApplicationAnswers] =
    useState<any>(null)
  const [interviewPreparation, setInterviewPreparation] =
    useState<any>(null)

  const [jobText, setJobText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleAnalyze() {
    if (!jobText.trim()) {
      setError("Please paste a job posting first.")
      return
    }

    setLoading(true)
    setError("")

    // Clear previous results
    setAnalysis(null)
    setOptimizedCV(null)
    setCoverLetter(null)
    setApplicationAnswers(null)
    setInterviewPreparation(null)

    try {
      const token = localStorage.getItem("token")

      if (!token) {
        throw new Error("Please log in first.")
      }

      // --------------------------------------------------
      // 1. Analyze pasted job
      // --------------------------------------------------

      const response = await fetch(
        "http://127.0.0.1:8000/analysis/paste",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            content: jobText,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || "Analysis failed"
        )
      }

      setJobId(data.job_id)

      // --------------------------------------------------
      // 2. Generate career materials
      // --------------------------------------------------

      const careerResponse = await fetch(
        "http://127.0.0.1:8000/api/career/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            job_offer_id: data.job_id,
          }),
        }
      )

      const careerData = await careerResponse.json()

      if (!careerResponse.ok) {
        throw new Error(
          careerData.detail ||
            "Career analysis failed"
        )
      }

      setAnalysis(careerData)

      // --------------------------------------------------
      // 3. Get Optimized CV
      // --------------------------------------------------

      const cv = await getOptimizedCV(
        data.job_id,
        token
      )

      setOptimizedCV(cv)

      // --------------------------------------------------
      // 4. Get Cover Letter
      // --------------------------------------------------

      const letter = await getCoverLetter(
        data.job_id,
        token
      )

      setCoverLetter(letter)

      // --------------------------------------------------
      // 5. Get Application Answers
      // --------------------------------------------------

      const answers =
        await getApplicationAnswers(
          data.job_id,
          token
        )

      setApplicationAnswers(answers)

      // --------------------------------------------------
      // 6. Get Interview Preparation
      // --------------------------------------------------

      const interview =
        await getInterviewPreparation(
          data.job_id,
          token
        )

      setInterviewPreparation(interview)

    } catch (err: any) {
      console.error(err)

      setError(
        err.message ||
          "Something went wrong"
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">

      {/* PASTE JOB */}
      <div>
        <label className="mb-2 block text-sm font-medium">
          Paste a Job
        </label>

        <textarea
          value={jobText}
          onChange={(e) =>
            setJobText(e.target.value)
          }
          placeholder="Paste the full job posting here..."
          className="min-h-[300px] w-full rounded-md border border-input bg-background px-3 py-3 text-sm shadow-sm outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      <p className="text-sm text-neutral-500">
        Paste the job description and we’ll analyze it
        against your CV.
      </p>

      {/* ERROR */}
      {error && (
        <p className="text-sm text-red-500">
          {error}
        </p>
      )}

      {/* BUTTON */}
      <Button
        onClick={handleAnalyze}
        disabled={
          loading ||
          !jobText.trim()
        }
      >
        {loading
          ? "Analyzing..."
          : "Analyze with AI"}
      </Button>

      {/* RESULTS */}
      {analysis && (
        <>
          {/* AI ANALYSIS */}
          <AnalysisTabs
            analysis={analysis}
          />

          {/* CAREER TOOLKIT */}
          <CareerToolkit
            optimizedCV={optimizedCV}
            coverLetter={coverLetter}
            applicationAnswers={
              applicationAnswers
            }
            interviewPreparation={
              interviewPreparation
            }
          />
        </>
      )}

    </div>
  )
}