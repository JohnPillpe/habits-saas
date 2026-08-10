import JobCard from "./JobCard"

type Props = {
  jobs: any[]
}

export default function JobResults({ jobs }: Props) {
  const normalizedJobs = jobs.map((job: any) => ({
    id: job.id,
    company: job.company || "Unknown company",
    title: job.title || "Untitled position",
    location: job.country || job.city || "Remote",
    employmentType: job.work_type || "Not specified",
    match: job.match_score ?? 0,
    tags: job.tags || [],
  }))

  return (
    <section className="mt-12">

      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-3xl font-semibold">
          Search Results
        </h2>

        <p className="text-sm text-neutral-500">
          {jobs.length} jobs found
        </p>
      </div>

      <div className="space-y-6">
        {normalizedJobs.map((job) => (
          <JobCard
            key={job.id}
            id={job.id}
            company={job.company}
            title={job.title}
            location={job.city || job.country}
            employmentType={job.work_type}
            match={job.match_score}
            tags={job.tags}
          />
        ))}
      </div>

    </section>
  )
}
