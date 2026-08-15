import { useState } from "react"

type Props = {
  analysis: any
}

function getMatchInfo(match?: number | null) {
  const score =
    typeof match === "number"
      ? match
      : 0

  if (score >= 70) {
    return {
      color: "#2B4ACC",
      label: "Strong match",
    }
  }

  if (score >= 45) {
    return {
      color: "#C2410C",
      label: "Moderate match",
    }
  }

  return {
    color: "#9A9382",
    label: "Weak match",
  }
}

export default function AnalysisTabs({ analysis }: Props) {
  const [tab, setTab] = useState("why")

  if (!analysis) return null

  const matchScore =
    typeof analysis.match_score === "number"
      ? analysis.match_score
      : 0

  const matchInfo =
    getMatchInfo(matchScore)

  return (
    <div className="mt-10">

      {/* TITLE */}

      <div>

        <h2 className="text-2xl font-bold">
          AI Analysis
        </h2>

        <p className="mt-1 text-neutral-500">
          How well your profile matches this position.
        </p>

      </div>


      {/* SCORE SUMMARY */}

      <div className="mt-6 rounded-xl border-2 border-[#14151A] bg-white p-6 shadow-[4px_4px_0_#14151A]">

        <div className="grid gap-6 md:grid-cols-3">

          {/* MATCH */}

          <div>

            <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
              Match Score
            </p>

            <div className="mt-2 flex items-baseline gap-2">

              <p
                className="text-5xl font-bold"
                style={{ color: matchInfo.color }}
              >
                {matchScore}%
              </p>

              <span className="font-mono text-xs font-medium uppercase tracking-wide text-neutral-500">
                MATCH
              </span>

            </div>

            <div
              className="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-neutral-100"
            >
              <div
                className="h-full rounded-full transition-all"
                style={{
                  width: `${Math.min(
                    Math.max(matchScore, 0),
                    100
                  )}%`,
                  backgroundColor: matchInfo.color,
                }}
              />
            </div>

            <p
              className="mt-3 font-medium"
              style={{
                color: matchInfo.color,
              }}
            >
              {matchInfo.label}
            </p>

          </div>


          {/* SENIORITY */}

          <div>

            <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
              Seniority
            </p>

            <p className="mt-3 text-xl font-semibold">
              {analysis.seniority || "—"}
            </p>

          </div>


          {/* DIFFICULTY */}

          <div>

            <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
              Difficulty
            </p>

            <p className="mt-3 text-xl font-semibold">
              {analysis.difficulty || "—"}
            </p>

          </div>

        </div>

      </div>


      {/* ANALYSIS TABS */}

      <div className="mt-6 overflow-hidden rounded-xl border border-[#E4E4DC] bg-white shadow-[0_1px_3px_rgba(0,0,0,0.06)]">

        <div className="grid grid-cols-4 border-b border-[#E4E4DC] bg-neutral-50">

          <button
            onClick={() => setTab("why")}
            className={`px-4 py-4 text-sm font-medium ${
              tab === "why"
                ? "border-b-2 border-black bg-white text-black"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            Why this score
          </button>

          <button
            onClick={() => setTab("strengths")}
            className={`px-4 py-4 text-sm font-medium ${
              tab === "strengths"
                ? "border-b-2 border-black bg-white text-black"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            Strengths
          </button>

          <button
            onClick={() => setTab("skills")}
            className={`px-4 py-4 text-sm font-medium ${
              tab === "skills"
                ? "border-b-2 border-black bg-white text-black"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            Skills gap
          </button>

          <button
            onClick={() => setTab("improve")}
            className={`px-4 py-4 text-sm font-medium ${
              tab === "improve"
                ? "border-b-2 border-black bg-white text-black"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            How to improve
          </button>

        </div>


        {/* TAB CONTENT */}

        <div className="bg-white p-6">

          {/* WHY */}

          {tab === "why" && (
            <div>

              <h3 className="text-lg font-semibold">
                Why this score
              </h3>

              {analysis.summary && (
                <p className="mt-3 leading-7 text-neutral-600">
                  {analysis.summary}
                </p>
              )}

              {analysis.why?.length > 0 && (
                <ul className="mt-5 space-y-3">

                  {analysis.why.map(
                    (item: string, index: number) => (
                      <li
                        key={index}
                        className="flex gap-3"
                      >

                        <span
                          className="mt-1"
                          style={{
                            color: matchInfo.color,
                          }}
                        >
                          ✕
                        </span>

                        <span className="text-neutral-700">
                          {item}
                        </span>

                      </li>
                    )
                  )}

                </ul>
              )}

            </div>
          )}


          {/* STRENGTHS */}

          {tab === "strengths" && (
            <div>

              <h3 className="text-lg font-semibold">
                Your strengths
              </h3>

              <ul className="mt-5 space-y-3">

                {analysis.strengths?.map(
                  (item: string, index: number) => (
                    <li
                      key={index}
                      className="flex gap-3"
                    >

                      <span className="text-green-600">
                        ✓
                      </span>

                      <span className="text-neutral-700">
                        {item}
                      </span>

                    </li>
                  )
                )}

              </ul>

            </div>
          )}


          {/* SKILLS */}

          {tab === "skills" && (
            <div>

              <h3 className="text-lg font-semibold">
                Skills gap
              </h3>

              {analysis.missing_skills?.length > 0 && (
                <div className="mt-5 space-y-3">

                  {analysis.missing_skills.map(
                    (item: string, index: number) => (
                      <div
                        key={index}
                        className="flex gap-3"
                      >

                        <span
                          style={{
                            color: matchInfo.color,
                          }}
                        >
                          ✕
                        </span>

                        <span className="text-neutral-700">
                          {item}
                        </span>

                      </div>
                    )
                  )}

                </div>
              )}

              {analysis.required_skills?.length > 0 && (
                <div className="mt-6">

                  <p className="text-sm font-medium text-neutral-500">
                    Required skills
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">

                    {analysis.required_skills.map(
                      (item: string, index: number) => (
                        <span
                          key={index}
                          className="
                            rounded-full
                            border
                            border-[#E4E4DC]
                            bg-white
                            px-3
                            py-1
                            text-sm
                          "
                        >
                          {item}
                        </span>
                      )
                    )}

                  </div>

                </div>
              )}

            </div>
          )}


          {/* IMPROVE */}

          {tab === "improve" && (
            <div>

              <h3 className="text-lg font-semibold">
                How to improve your chances
              </h3>

              <ol className="mt-5 space-y-4">

                {analysis.next_steps?.map(
                  (item: string, index: number) => (
                    <li
                      key={index}
                      className="flex gap-3"
                    >

                      <span className="font-semibold text-neutral-400">
                        {index + 1}.
                      </span>

                      <span className="text-neutral-700">
                        {item}
                      </span>

                    </li>
                  )
                )}

              </ol>

            </div>
          )}

        </div>

      </div>

    </div>
  )
}