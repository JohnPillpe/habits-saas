type Props = {
  title: string
  company: string
  category?: string | null
  salary?: string | null
  tags?: string[]
  country?: string | null
  city?: string | null
  workType?: string | null
  publishedAt?: string | null
  originalUrl?: string | null
  loading: boolean
  onAnalyze: () => void
}

export default function JobHeader({
  title,
  company,
  category,
  salary,
  tags = [],
  country,
  city,
  workType,
  publishedAt,
  originalUrl,
  loading,
  onAnalyze,
}: Props) {
  const location = [city, country]
    .filter(Boolean)
    .join(", ")

  return (
    <div className="mb-10">

      <h1 className="text-4xl font-bold tracking-tight">
        {title}
      </h1>

      <p className="mt-2 text-lg text-neutral-500">
        {company}
      </p>

      <div className="mt-6 grid gap-4 rounded-2xl border border-neutral-200 p-6 sm:grid-cols-2">

        {category && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Category
            </p>

            <p className="mt-1 text-sm font-medium">
              {category}
            </p>
          </div>
        )}

        {salary && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Salary
            </p>

            <p className="mt-1 text-sm font-medium">
              {salary}
            </p>
          </div>
        )}

        {location && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Location
            </p>

            <p className="mt-1 text-sm font-medium">
              {location}
            </p>
          </div>
        )}

        {workType && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Work type
            </p>

            <p className="mt-1 text-sm font-medium">
              {workType}
            </p>
          </div>
        )}

        {publishedAt && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Published
            </p>

            <p className="mt-1 text-sm font-medium">
              {new Date(publishedAt).toLocaleDateString()}
            </p>
          </div>
        )}

        {tags.length > 0 && (
          <div className="sm:col-span-2">
            <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
              Tags
            </p>

            <div className="mt-2 flex flex-wrap gap-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

      </div>

      <div className="mt-6 flex items-center gap-3">

        {originalUrl ? (
          <a
            href={originalUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg border border-neutral-300 px-5 py-2.5 text-sm font-medium transition hover:bg-neutral-50"
          >
            Open Original Job
          </a>
        ) : (
          <span className="rounded-lg border border-neutral-200 px-5 py-2.5 text-sm text-neutral-400">
            Original job unavailable
          </span>
        )}

        <button
          onClick={onAnalyze}
          disabled={loading}
          className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Analyzing..." : "Analyze with AI"}
        </button>

      </div>

    </div>
  )
}