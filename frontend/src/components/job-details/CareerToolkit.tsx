import {
  useState,
} from "react"

import OptimizedCVTab from "./OptimizedCVTab"
import CoverLetterTab from "./CoverLetterTab"
import ApplicationAnswersTab from "./ApplicationAnswersTab"
import InterviewPreparationTab from "./InterviewPreparationTab"

type Props = {
  optimizedCV: any
  coverLetter: any
  applicationAnswers: any
  interviewPreparation: any
}

export default function CareerToolkit({
  optimizedCV,
  coverLetter,
  applicationAnswers,
  interviewPreparation,
}: Props) {
  const [
    tab,
    setTab,
  ] = useState("cv")

  if (
    !optimizedCV &&
    !coverLetter &&
    !applicationAnswers &&
    !interviewPreparation
  ) {
    return null
  }

  return (
    <div className="mt-12">

      {/* HEADER */}

      <div>

        <h2 className="text-2xl font-semibold text-neutral-900">
          Generate application materials
        </h2>

        <p className="mt-1 max-w-2xl text-sm leading-6 text-neutral-500">
          Choose a document to review and use for this application.
        </p>

      </div>

      {/* TABS */}

      <div className="mt-6 grid grid-cols-2 overflow-hidden rounded-xl border sm:grid-cols-4">

        <button
          type="button"
          onClick={() => setTab("cv")}
          className={`px-4 py-4 text-sm font-medium transition ${
            tab === "cv"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Optimized CV
        </button>

        <button
          type="button"
          onClick={() => setTab("letter")}
          className={`border-l px-4 py-4 text-sm font-medium transition ${
            tab === "letter"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Cover Letter
        </button>

        <button
          type="button"
          onClick={() => setTab("answers")}
          className={`border-t px-4 py-4 text-sm font-medium transition sm:border-l sm:border-t-0 ${
            tab === "answers"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Answers
        </button>

        <button
          type="button"
          onClick={() => setTab("interview")}
          className={`border-l border-t px-4 py-4 text-sm font-medium transition sm:border-t-0 ${
            tab === "interview"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Interview Prep
        </button>

      </div>

      {/* CONTENT */}

      <div className="mt-6">

        {tab === "cv" && (
          <OptimizedCVTab
            optimizedCV={optimizedCV}
          />
        )}

        {tab === "letter" && (
          <CoverLetterTab
            coverLetter={coverLetter}
          />
        )}

        {tab === "answers" && (
          <ApplicationAnswersTab
            applicationAnswers={
              applicationAnswers
            }
          />
        )}

        {tab === "interview" && (
          <InterviewPreparationTab
            interviewPreparation={
              interviewPreparation
            }
          />
        )}

      </div>

    </div>
  )
}