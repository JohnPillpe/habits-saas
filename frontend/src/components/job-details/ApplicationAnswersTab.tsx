import {
  useState,
} from "react"

import {
  copyToClipboard,
  downloadAsWord,
  downloadAsPDF,
} from "./downloadUtils"

type Props = {
  applicationAnswers: any
}

export default function ApplicationAnswersTab({
  applicationAnswers,
}: Props) {
  const [
    downloadOpen,
    setDownloadOpen,
  ] = useState(false)

  const [
    copied,
    setCopied,
  ] = useState(false)

  if (!applicationAnswers) return null

  const sections = [
    {
      title: "Tell me about yourself",
      value:
        applicationAnswers.tell_me_about_yourself,
    },
    {
      title: "Why this company?",
      value:
        applicationAnswers.why_this_company,
    },
    {
      title: "Why should we hire you?",
      value:
        applicationAnswers.why_should_we_hire_you,
    },
    {
      title: "Greatest strength",
      value:
        applicationAnswers.greatest_strength,
    },
    {
      title: "Greatest weakness",
      value:
        applicationAnswers.greatest_weakness,
    },
  ]

  const content = sections
    .filter(
      (section) =>
        section.value,
    )
    .map(
      (section) =>
        `${section.title}\n\n${section.value}`,
    )
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
          Application Answers
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
                      "Application Answers",
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
                      "Application Answers",
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

          {sections.map(
            (section) => {

              if (!section.value) {
                return null
              }

              return (
                <div
                  key={section.title}
                >

                  <h3 className="text-sm font-semibold text-neutral-900">
                    {section.title}
                  </h3>

                  <p className="mt-3 whitespace-pre-wrap break-words font-sans text-sm leading-7 text-neutral-700">
                    {section.value}
                  </p>

                </div>
              )
            },
          )}

        </div>

      </div>

    </div>
  )
}