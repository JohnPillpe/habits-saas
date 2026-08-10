type Props = {
  title: string
  company: string
  category: string
  originalUrl: string
  loading: boolean
  onAnalyze: () => void
}

export default function JobHeader({
  title,
  company,
  category,
  originalUrl,
  loading,
  onAnalyze,
}: Props) {
  return (
    <div className="mb-10">

      <h1 className="text-4xl font-bold tracking-tight">
        {title}
      </h1>

      <p className="mt-2 text-lg text-neutral-500">
        {company} · {category}
      </p>

      <div className="mt-6 flex items-center gap-3">

        <a
          href={originalUrl}
          target="_blank"
          rel="noreferrer"
          className="rounded-lg border border-neutral-300 px-5 py-2.5 text-sm font-medium transition hover:bg-neutral-50"
        >
          Open Original Job
        </a>

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