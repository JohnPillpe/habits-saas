import { useEffect, useState } from "react"

import JobSearchSection from "./JobSearchSection"
import AnalyzeJobSection from "./AnalyzeJobSection"

import { useJobs } from "@/context/JobContext"

import {
  getJobLocations,
  searchJobs,
} from "@/services/jobs"

import JobResults from "../jobs/JobResults"

type LocationOption = {
  country: string
  city: string
}

export default function SearchTabs() {
  const [activeTab, setActiveTab] =
    useState<"search" | "analyze">("search")

  const {
    jobs,
    setJobs,
    filters,
    setFilters,
  } = useJobs()

  const [showResults, setShowResults] =
    useState(jobs.length > 0)

  const [locations, setLocations] =
    useState<LocationOption[]>([])

  const [loadingLocations, setLoadingLocations] =
    useState(false)

  const [searching, setSearching] =
    useState(false)

  const [searchError, setSearchError] =
    useState<string | null>(null)

  /*
   * --------------------------------------------------
   * LOAD LOCATIONS
   * --------------------------------------------------
   */

  useEffect(() => {
    let cancelled = false

    async function loadLocations() {
      try {
        setLoadingLocations(true)

        const data = await getJobLocations()

        if (!cancelled) {
          setLocations(data)
        }
      } catch (error) {
        console.error(
          "Failed to load job locations:",
          error
        )
      } finally {
        if (!cancelled) {
          setLoadingLocations(false)
        }
      }
    }

    loadLocations()

    return () => {
      cancelled = true
    }
  }, [])

  /*
   * --------------------------------------------------
   * SEARCH
   * --------------------------------------------------
   */

  async function handleSearch() {
    if (searching) {
      return
    }
  
    try {
      setSearching(true)
      setSearchError(null)
  
      const data = await searchJobs(filters)
  
      setJobs(data)
      setShowResults(true)
  
    } catch (error) {
      console.error(
        "Job search failed:",
        error
      )
  
      setSearchError(
        error instanceof Error
          ? error.message
          : "Unable to search jobs."
      )
  
    } finally {
      setSearching(false)
    }
  }

  return (
    <section className="px-6 pb-20">
      <div className="mx-auto max-w-6xl">

        {/* TABS */}

        <div className="flex">

          <button
            type="button"
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
            type="button"
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

        {/* CONTENT */}

        <div className="rounded-b-xl rounded-tr-xl border p-8">

          {activeTab === "search" ? (

            <JobSearchSection

              keyword={filters.keyword}

              setKeyword={(value) =>
                setFilters((current) => ({
                  ...current,
                  keyword: value,
                }))
              }

              country={filters.country}

              setCountry={(value) =>
                setFilters((current) => ({
                  ...current,
                  country: value,
                }))
              }

              city={filters.city}

              setCity={(value) =>
                setFilters((current) => ({
                  ...current,
                  city: value,
                }))
              }

              published={filters.published}

              setPublished={(value) =>
                setFilters((current) => ({
                  ...current,
                  published: value,
                }))
              }

              workType={filters.workType}

              setWorkType={(value) =>
                setFilters((current) => ({
                  ...current,
                  workType: value,
                }))
              }

              locations={locations}
              loading={
                searching ||
                loadingLocations
              }

              onSearch={handleSearch}
            />

          ) : (

            <AnalyzeJobSection />

          )}

          {/* ERROR */}

          {searchError && activeTab === "search" && (
            <div
              className="
                mt-4
                rounded-lg
                border
                border-red-200
                bg-red-50
                px-4
                py-3
                text-sm
                text-red-700
              "
            >
              {searchError}
            </div>
          )}

        </div>

        {/* RESULTS */}

        {activeTab === "search" &&
          showResults && (
            <JobResults jobs={jobs} />
          )}

      </div>
    </section>
  )
}