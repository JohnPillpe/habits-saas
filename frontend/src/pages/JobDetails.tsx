import { useEffect, useState } from "react"
import {
  getJobById,
  analyzeJob,
  getOptimizedCV,
  getCoverLetter,
  getApplicationAnswers,
  getInterviewPreparation,
} from "@/services/jobs"

import { hasCV } from "@/services/upload"
import {
  useLocation,
  useNavigate,
  useParams,
} from "react-router-dom"

import JobHeader from "@/components/job-details/JobHeader"
import AnalysisTabs from "@/components/job-details/AnalysisTabs"
import CareerToolkit from "@/components/job-details/CareerToolkit"
import UploadCVModal from "@/components/jobs/UploadCVModal"

export default function JobDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()

  const [job, setJob] = useState<any>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [showUpload, setShowUpload] = useState(false)

  const [optimizedCV, setOptimizedCV] =
    useState<any>(null)

  const [coverLetter, setCoverLetter] =
    useState<any>(null)

  const [applicationAnswers, setApplicationAnswers] =
    useState<any>(null)

  const [interviewPreparation, setInterviewPreparation] =
    useState<any>(null)

  useEffect(() => {
    async function loadJob() {
      if (!id) return

      const data = await getJobById(id)
      setJob(data)
    }

    loadJob()
  }, [id])

  async function runAnalysis() {
    if (!id) return

    const token = localStorage.getItem("token")

    if (!token) {
      navigate("/login", {
        state: {
          from: `/jobs/${id}`,
        },
      })
      return
    }

    try {
      setLoading(true)

      const data = await analyzeJob(id)

      setAnalysis(data)

      const cv = await getOptimizedCV(
        id,
        token,
      )

      setOptimizedCV(cv)

      const letter = await getCoverLetter(
        id,
        token,
      )

      setCoverLetter(letter)

      const answers =
        await getApplicationAnswers(
          id,
          token,
        )

      setApplicationAnswers(answers)

      const interview =
        await getInterviewPreparation(
          id,
          token,
        )

      setInterviewPreparation(interview)

    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    if (!id) return

    const token = localStorage.getItem("token")

    if (!token) {
      navigate("/login", {
        state: {
          from: `/jobs/${id}`,
        },
      })

      return
    }

    const result = await hasCV(token)

    if (!result.has_cv) {
      setShowUpload(true)
      return
    }

    await runAnalysis()
  }

  async function handleCVUploaded() {
    setShowUpload(false)
    await runAnalysis()
  }

  if (!job) {
    return (
      <p className="p-10">
        Loading...
      </p>
    )
  }

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">

      <button
        onClick={() => {
          if (location.state?.from) {
            navigate(location.state.from)
          } else {
            navigate("/")
          }
        }}
        className="mb-6 text-sm font-medium text-neutral-500 hover:text-black"
      >
        ← Back to search results
      </button>

      <JobHeader
        title={job.titulo}
        company={job.empresa}
        category={job.categoria}
        originalUrl={job.enlace}
        loading={loading}
        onAnalyze={handleAnalyze}
      />

      <AnalysisTabs
        analysis={analysis}
      />

      <CareerToolkit
        optimizedCV={optimizedCV}
        coverLetter={coverLetter}
        applicationAnswers={applicationAnswers}
        interviewPreparation={interviewPreparation}
      />

      <UploadCVModal
        open={showUpload}
        onClose={() => setShowUpload(false)}
        onUploaded={handleCVUploaded}
      />

    </section>
  )
}