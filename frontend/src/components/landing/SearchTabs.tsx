import { useState } from "react"

import JobSearchSection from "./JobSearchSection"
import AnalyzeJobSection from "./AnalyzeJobSection"

import { useJobs } from "@/context/JobContext"

import { searchJobs } from "@/services/jobs"

import JobResults from "../jobs/JobResults"

export default function SearchTabs() {
  const [activeTab, setActiveTab] =
    useState<"search" | "analyze">("search")

  const {
    jobs,
    setJobs,
    filters,
    setFilters,
  } = useJobs()

  const [showResults, setShowResults] = useState(jobs.length > 0)

  async function handleSearch() {
    const data = await searchJobs(filters)

    setJobs(data)

    setShowResults(true)

  }

  return (
    <section className="px-6 pb-20">
      <div className="mx-auto max-w-6xl">

        <div className="flex">

          <button
            onClick={() => setActiveTab("search")}
            className={`rounded-t-xl border border-b-0 px-6 py-3 ${
              activeTab === "search"
                ? "bg-white"
                : "bg-neutral-100"
            }`}
          >
            Search Jobs
          </button>

          <button
            onClick={() => setActiveTab("analyze")}
            className={`ml-2 rounded-t-xl border border-b-0 px-6 py-3 ${
              activeTab === "analyze"
                ? "bg-white"
                : "bg-neutral-100"
            }`}
          >
            Paste a Job
          </button>

        </div>

        <div className="rounded-b-xl rounded-tr-xl border p-8">

          {activeTab === "search" ? (

            <JobSearchSection
              keyword={filters.keyword}
              setKeyword={(v) =>
                setFilters((f) => ({
                  ...f,
                  keyword: v,
                }))
              }

              country={filters.country}
              setCountry={(v) =>
                setFilters((f) => ({
                  ...f,
                  country: v,
                }))
              }

              city={filters.city}
              setCity={(v) =>
                setFilters((f) => ({
                  ...f,
                  city: v,
                }))
              }

              published={filters.published}
              setPublished={(v) =>
                setFilters((f) => ({
                  ...f,
                  published: v,
                }))
              }

              workType={filters.workType}
              setWorkType={(v) =>
                setFilters((f) => ({
                  ...f,
                  workType: v,
                }))
              }

              onSearch={handleSearch}
            />

          ) : (

            <AnalyzeJobSection />

          )}

        </div>

        {activeTab === "search" && showResults && (
          <JobResults jobs={jobs} />
        )}

      </div>
    </section>
  )
}