import {
  useState,
} from "react"

import {
  copyToClipboard,
  downloadAsWord,
  downloadAsPDF,
} from "./downloadUtils"

type Props = {
  interviewPreparation: any
}

export default function InterviewPreparationTab({
  interviewPreparation,
}: Props) {
  const [
    downloadOpen,
    setDownloadOpen,
  ] = useState(false)

  const [
    copied,
    setCopied,
  ] = useState(false)

  if (!interviewPreparation) return null

  const technicalQuestions =
    interviewPreparation.technical_questions || []

  const behavioralQuestions =
    interviewPreparation.behavioral_questions || []

  const tips =
    interviewPreparation.tips || []

  const content = [
    technicalQuestions.length > 0
      ? `Technical Questions\n\n${technicalQuestions
          .map(
            (item: string) =>
              `• ${item}`,
          )
          .join("\n")}`
      : "",

    behavioralQuestions.length > 0
      ? `Behavioral Questions\n\n${behavioralQuestions
          .map(
            (item: string) =>
              `• ${item}`,
          )
          .join("\n")}`
      : "",

    tips.length > 0
      ? `Interview Tips\n\n${tips
          .map(
            (item: string) =>
              `• ${item}`,
          )
          .join("\n")}`
      : "",
  ]
    .filter(Boolean)
    .join("\n\n\n")

  const handleCopy = async () => {
    await copyToClipboard(content)

    setCopied(true)

    setTimeout(() => {
      setCopied(false)
    }, 1500)
  }

  return (
    <div className="rounded-xl border bg-white p-6">

      {/* HEADER */}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <h2 className="text-xl font-semibold text-neutral-900">
          Interview Preparation
        </h2>

        <div className="flex flex-wrap items-center gap-2">

          <button
            type="button"
            onClick={handleCopy}
            className="rounded-lg border px-3 py-2 text-xs font-medium text-neutral-700 transition hover:bg-neutral-50"
          >
            {copied ? "Copied" : "Copy"}
          </button>

          <div className="relative">

            <button
              type="button"
              onClick={() =>
                setDownloadOpen(
                  !downloadOpen,
                )
              }
              className="rounded-lg bg-black px-3 py-2 text-xs font-medium text-white transition hover:bg-neutral-800"
            >
              Download
            </button>

            {downloadOpen && (
              <div className="absolute right-0 z-20 mt-2 w-40 overflow-hidden rounded-lg border bg-white shadow-lg">

                <button
                  type="button"
                  onClick={() => {
                    downloadAsWord(
                      "Interview Preparation",
                      content,
                    )

                    setDownloadOpen(false)
                  }}
                  className="block w-full px-4 py-3 text-left text-xs font-medium text-neutral-700 hover:bg-neutral-50"
                >
                  Word
                </button>

                <button
                  type="button"
                  onClick={() => {
                    downloadAsPDF(
                      "Interview Preparation",
                      content,
                    )

                    setDownloadOpen(false)
                  }}
                  className="block w-full px-4 py-3 text-left text-xs font-medium text-neutral-700 hover:bg-neutral-50"
                >
                  PDF
                </button>

              </div>
            )}

          </div>

        </div>

      </div>

      {/* CONTENT */}

      <div className="mt-6 border-t pt-6">

        <div className="space-y-8">

          {technicalQuestions.length > 0 && (
            <div>

              <h3 className="text-sm font-semibold text-neutral-900">
                Technical Questions
              </h3>

              <ul className="mt-3 space-y-3">

                {technicalQuestions.map(
                  (
                    item: string,
                    index: number,
                  ) => (
                    <li
                      key={`${item}-${index}`}
                      className="flex gap-3 text-sm leading-7 text-neutral-700"
                    >
                      <span className="text-neutral-400">
                        •
                      </span>

                      <span>
                        {item}
                      </span>
                    </li>
                  ),
                )}

              </ul>

            </div>
          )}

          {behavioralQuestions.length > 0 && (
            <div>

              <h3 className="text-sm font-semibold text-neutral-900">
                Behavioral Questions
              </h3>

              <ul className="mt-3 space-y-3">

                {behavioralQuestions.map(
                  (
                    item: string,
                    index: number,
                  ) => (
                    <li
                      key={`${item}-${index}`}
                      className="flex gap-3 text-sm leading-7 text-neutral-700"
                    >
                      <span className="text-neutral-400">
                        •
                      </span>

                      <span>
                        {item}
                      </span>
                    </li>
                  ),
                )}

              </ul>

            </div>
          )}

          {tips.length > 0 && (
            <div>

              <h3 className="text-sm font-semibold text-neutral-900">
                Interview Tips
              </h3>

              <ul className="mt-3 space-y-3">

                {tips.map(
                  (
                    item: string,
                    index: number,
                  ) => (
                    <li
                      key={`${item}-${index}`}
                      className="flex gap-3 text-sm leading-7 text-neutral-700"
                    >
                      <span className="text-neutral-400">
                        •
                      </span>

                      <span>
                        {item}
                      </span>
                    </li>
                  ),
                )}

              </ul>

            </div>
          )}

        </div>

      </div>

    </div>
  )
}