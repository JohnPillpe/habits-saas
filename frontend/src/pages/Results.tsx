import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"

import JobCard from "@/components/jobs/JobCard"
import { searchJobsForUser } from "@/services/jobs"

export default function Results() {
  const [jobs, setJobs] = useState<any[]>([])
  const [searchParams] = useSearchParams()

  const keyword = searchParams.get("keyword") ?? ""

  useEffect(() => {
    async function loadJobs() {
      try {
        const data = await searchJobsForUser({
          keyword,
          country: "",
          city: "",
          published: "",
          workType: "",
        })

        console.log("FIRST JOB:", data[0])
        console.log("JOBS:", data)

        setJobs(data)
      } catch (error) {
        console.error("Error loading jobs:", error)
        setJobs([])
      }
    }

    loadJobs()
  }, [keyword])

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">

      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-semibold">
          Search Results
        </h1>

        <p className="text-sm text-neutral-500">
          {jobs.length} jobs found
        </p>
      </div>

      <div className="space-y-6">

        {jobs.map((job) => (
          <JobCard
            key={job.id}
            id={job.id}
            company={job.company}
            title={job.title}
            location={job.city || job.country || "Remote"}
            category={job.category}
            salary={job.salary}
            employmentType={job.work_type}
            match={job.match_score}
            tags={job.tags}
          />
        ))}

      </div>

    </section>
  )
}