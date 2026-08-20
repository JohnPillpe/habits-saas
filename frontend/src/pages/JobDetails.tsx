import { useEffect, useState } from "react"
import DOMPurify from "dompurify"

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

  const [descriptionExpanded, setDescriptionExpanded] =
    useState(false)
    
    useEffect(() => {
      async function loadJob() {
        if (!id) return
    
        if (!/^\d+$/.test(id)) {
          console.error(
            "Invalid job route ID:",
            id,
          )
          setJob(null)
          return
        }
    
        try {
          const data = await getJobById(id)
    
          console.log(
            "JOB DETAILS:",
            data,
          )
    
          setJob(data)
        } catch (error) {
          console.error(
            "Could not load job:",
            error,
          )
        }
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

    } catch (error) {
      console.error(
        "Analysis failed:",
        error,
      )
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


  const jobDescription =
    job.description ??
    job.descripcion ??
    "Job description unavailable."


  const cleanJobDescription =
    DOMPurify.sanitize(jobDescription)


  /*
   * ============================================================
   * DESCRIPTION EXPANDED
   * ============================================================
   */

  if (descriptionExpanded) {
    return (
      <section className="min-h-screen bg-white">

        <div className="mx-auto max-w-5xl px-6 py-10">

          <button
            onClick={() =>
              setDescriptionExpanded(false)
            }
            className="mb-8 text-sm font-medium text-neutral-500 hover:text-black"
          >
            ← Back to AI Analysis
          </button>

          <div className="rounded-2xl border border-neutral-200 bg-white p-8">

            <h1 className="text-3xl font-bold">
              {job.title ?? job.titulo}
            </h1>

            <p className="mt-2 text-lg text-neutral-500">
              {job.company ?? job.empresa}
            </p>

            <div className="mt-8">

              <h2 className="text-xl font-semibold">
                Job description
              </h2>

              <div
                className="prose prose-neutral mt-5 max-w-none leading-7 text-justify"
                dangerouslySetInnerHTML={{
                  __html: cleanJobDescription,
                }}
              />

            </div>

          </div>

        </div>

      </section>
    )
  }


  /*
   * ============================================================
   * NORMAL JOB VIEW — BEFORE AI ANALYSIS
   * ============================================================
   */

  if (!analysis) {
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
          title={job.title ?? job.titulo}
          company={job.company ?? job.empresa}
          category={
            job.category ??
            job.categoria
          }
          salary={
            job.salary ??
            job.salario
          }
          tags={
            Array.isArray(job.tags)
              ? job.tags
              : []
          }
          country={
            job.country ??
            job.pais
          }
          city={
            job.city ??
            job.ciudad
          }
          workType={
            job.work_type ??
            job.tipo_trabajo
          }
          publishedAt={
            job.published_at ??
            job.publicado_en
          }
          originalUrl={
            job.url ??
            job.enlace
          }
          loading={loading}
          onAnalyze={handleAnalyze}
        />


        <div className="mt-10 rounded-2xl border border-neutral-200 bg-white p-8">

          <h2 className="text-2xl font-semibold">
            Job description
          </h2>

          <div
            className="prose prose-neutral mt-5 max-w-none leading-7 text-justify"
            dangerouslySetInnerHTML={{
              __html: cleanJobDescription,
            }}
          />

        </div>


        <UploadCVModal
          open={showUpload}
          onClose={() => setShowUpload(false)}
          onUploaded={handleCVUploaded}
        />

      </section>
    )
  }


  /*
   * ============================================================
   * AI ANALYSIS VIEW
   * ============================================================
   */

  return (
    <section className="min-h-screen bg-neutral-50">

      <div className="grid min-h-screen lg:grid-cols-[360px_minmax(0,1fr)]">

        {/* =====================================================
            LEFT — JOB DESCRIPTION
        ====================================================== */}

        <aside className="border-r border-neutral-200 bg-white">

          <div className="sticky top-0 flex h-screen flex-col">

            <div className="border-b border-neutral-200 px-6 py-5">

              <p className="text-xs font-semibold uppercase tracking-wide text-neutral-400">
                Job description
              </p>

              <h2 className="mt-2 line-clamp-2 text-lg font-semibold leading-6 text-neutral-900">
                {job.title ?? job.titulo}
              </h2>

              <p className="mt-1 text-sm text-neutral-500">
                {job.company ?? job.empresa}
              </p>

            </div>


            <div className="flex-1 overflow-y-auto px-6 py-6">

              <div
                className="
                  prose
                  prose-neutral
                  prose-sm
                  max-w-none
                  text-neutral-600
                  text-justify
                  leading-6
                  prose-headings:font-semibold
                  prose-headings:text-neutral-900
                  prose-p:my-3
                  prose-ul:my-3
                  prose-ol:my-3
                  prose-li:my-1
                  prose-strong:text-neutral-800
                "
                dangerouslySetInnerHTML={{
                  __html: cleanJobDescription,
                }}
              />

            </div>


            <div className="border-t border-neutral-200 px-6 py-4">

              <button
                onClick={() =>
                  setDescriptionExpanded(true)
                }
                className="
                  w-full
                  rounded-lg
                  border
                  border-neutral-300
                  px-4
                  py-2.5
                  text-sm
                  font-medium
                  text-neutral-700
                  transition
                  hover:bg-neutral-50
                  hover:text-black
                "
              >
                Expand description
              </button>

            </div>

          </div>

        </aside>


        {/* =====================================================
            RIGHT — AI RESULTS
        ====================================================== */}

        <main className="min-w-0">

          <div className="mx-auto max-w-6xl px-6 py-10">

            <button
              onClick={() => {
                if (location.state?.from) {
                  navigate(location.state.from)
                } else {
                  navigate("/")
                }
              }}
              className="mb-8 text-sm font-medium text-neutral-500 hover:text-black"
            >
              ← Back to search results
            </button>


            <AnalysisTabs
              analysis={analysis}
            />


            <CareerToolkit
              optimizedCV={optimizedCV}
              coverLetter={coverLetter}
              applicationAnswers={applicationAnswers}
              interviewPreparation={interviewPreparation}
            />

          </div>

        </main>

      </div>


      <UploadCVModal
        open={showUpload}
        onClose={() => setShowUpload(false)}
        onUploaded={handleCVUploaded}
      />

    </section>
  )
}