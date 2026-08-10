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
      const data = await searchJobs({
        keyword,
        country: "",
        city: "",
        published: "",
        workType: "",
      })

      console.log(data[0])
      setJobs(data)
      
    }

    loadJobs()
  }, [keyword])

  console.log("JOBS:", jobs)
  console.log("ES ARRAY:", Array.isArray(jobs))
  console.log("LENGTH:", jobs.length)

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
  
      <h1 className="mb-8 text-3xl font-semibold">
        Search Results
      </h1>
  
      <p>Total jobs: {jobs.length}</p>
  
      <div className="space-y-6">
  
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            id={job.id}
            company={job.empresa}
            title={job.titulo}
            location={job.pais}
            employmentType={job.tipo}
            match={job.match_score}
            tags={job.tags}
          />
        ))}
  
      </div>
  
    </section>
  )
}