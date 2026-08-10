import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"

import JobCard from "@/components/jobs/JobCard"
import { searchJobs } from "@/services/jobs"

export default function Results() {
  const [jobs, setJobs] = useState<any[]>([])
  const [searchParams] = useSearchParams()

  const keyword = searchParams.get("keyword") ?? ""

  useEffect(() => {
    async function loadJobs() {
      try {
        const data = await searchJobs({
          keyword,
          country: "",
          city: "",
          published: "",
          workType: "",
        })

        setJobs(data)
      } catch (error) {
        console.error("Error loading jobs:", error)
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
            company={job.empresa}
            title={job.titulo}
            location={
              job.ciudad ||
              job.city ||
              job.pais ||
              job.country ||
              "Remote"
            }
            employmentType={
              job.tipo_trabajo ||
              job.work_type ||
              "Remote"
            }
            match={job.match_score}
            tags={job.tags}
            category={job.categoria}
            salary={job.salario}
          />
        ))}
      </div>

    </section>
  )
}