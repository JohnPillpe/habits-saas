import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

type Props = {
  keyword: string
  setKeyword: (value: string) => void

  country: string
  setCountry: (value: string) => void

  city: string
  setCity: (value: string) => void

  published: string
  setPublished: (value: string) => void

  workType: string
  setWorkType: (value: string) => void

  onSearch: () => void
}

export default function JobSearchSection({
  keyword,
  setKeyword,
  country,
  setCountry,
  city,
  setCity,
  published,
  setPublished,
  workType,
  setWorkType,
  onSearch,
}: Props) {
  return (
    <div className="space-y-6">
      <div>
        <label className="mb-2 block text-sm font-medium">
          Role / Keywords
        </label>

        <Input
          placeholder="Backend Python"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Input
          placeholder="Country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />

        <Input
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <select
          value={published}
          onChange={(e) => setPublished(e.target.value)}
          className="h-10 w-full rounded-md border bg-background px-3 text-sm"
        >
          <option value="">Published</option>
          <option value="1">Last 24 hours</option>
          <option value="3">Last 3 days</option>
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
        </select>

        <select
          value={workType}
          onChange={(e) => setWorkType(e.target.value)}
          className="h-10 w-full rounded-md border bg-background px-3 text-sm"
        >
          <option value="">Work Type</option>
          <option value="Remote">Remote</option>
          <option value="Hybrid">Hybrid</option>
          <option value="On-site">On-site</option>
        </select>
      </div>

      <Button onClick={onSearch}>
        Search Jobs
      </Button>
    </div>
  )
}