import { Card } from "@/components/ui/card"
import { Link } from "react-router-dom"

type JobCardProps = {
  id: number
  company: string
  title: string
  location: string
  employmentType: string
  match?: number | null
  tags?: string | string[]
}

export default function JobCard({
  id,
  company,
  title,
  location,
  employmentType,
  match,
  tags,
}: JobCardProps) {
  const tagList = Array.isArray(tags)
    ? tags
    : tags
      ? tags.split(",")
      : []

  const hasMatch =
    typeof match === "number"

  return (
    <Card className="rounded-2xl border border-neutral-200 bg-white p-6 transition hover:border-neutral-300 hover:shadow-lg">

      <div className="flex items-start justify-between">

        <div className="flex gap-5">

          {hasMatch && (
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-neutral-100">
              <div className="text-center">
                <p className="text-2xl font-bold">
                  {match}%
                </p>

                <p className="text-[10px] uppercase text-neutral-500">
                  Match
                </p>
              </div>
            </div>
          )}

          <div>
            <h3 className="text-xl font-semibold text-neutral-900">
              {title}
            </h3>

            <p className="mt-1 text-sm text-neutral-500">
              {company}
            </p>
          </div>

        </div>

        <div className="rounded-full border border-neutral-200 px-3 py-1 text-xs">
          {employmentType || "Remote"}
        </div>

      </div>

      <div className="mt-5 flex items-center gap-3 text-sm text-neutral-600">
        <span>{location}</span>
        <span>•</span>
        <span>{employmentType}</span>
      </div>

      {tagList.length > 0 && (
        <div className="mt-5 flex flex-wrap gap-2">
          {tagList.slice(0, 4).map((tag, index) => (
            <span
              key={`${tag}-${index}`}
              className="rounded-full border border-neutral-200 bg-neutral-50 px-3 py-1 text-xs text-neutral-700"
            >
              {tag.trim()}
            </span>
          ))}
        </div>
      )}

      <div className="mt-6 flex justify-end border-t border-neutral-100 pt-4">
        <Link
          to={`/jobs/${id}`}
          state={{
            from:
              window.location.pathname +
              window.location.search,
          }}
          className="text-sm font-medium text-neutral-900 hover:underline"
        >
          View job →
        </Link>
      </div>

    </Card>
  )
}