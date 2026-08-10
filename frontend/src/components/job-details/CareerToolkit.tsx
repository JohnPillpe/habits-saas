import { useState } from "react"

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
  const [tab, setTab] = useState("cv")

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

      <h2 className="text-2xl font-semibold">
        Generate application materials
      </h2>

      <p className="mt-1 text-sm text-neutral-500">
        Choose a document to review and use for this application.
      </p>

      {/* TABS */}
      <div className="mt-6 grid grid-cols-4 overflow-hidden rounded-xl border">

        <button
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
          onClick={() => setTab("answers")}
          className={`border-l px-4 py-4 text-sm font-medium transition ${
            tab === "answers"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Answers
        </button>

        <button
          onClick={() => setTab("interview")}
          className={`border-l px-4 py-4 text-sm font-medium transition ${
            tab === "interview"
              ? "bg-black text-white"
              : "bg-white text-neutral-700 hover:bg-neutral-50"
          }`}
        >
          Interview Prep
        </button>

      </div>

      {/* CONTENT */}
      <div className="mt-6 rounded-xl border bg-white p-6">

        {tab === "cv" && (
          <OptimizedCVTab optimizedCV={optimizedCV} />
        )}

        {tab === "letter" && (
          <CoverLetterTab coverLetter={coverLetter} />
        )}

        {tab === "answers" && (
          <ApplicationAnswersTab
            applicationAnswers={applicationAnswers}
          />
        )}

        {tab === "interview" && (
          <InterviewPreparationTab
            interviewPreparation={interviewPreparation}
          />
        )}

      </div>

    </div>
  )
}