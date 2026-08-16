import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

type LocationOption = {
  country: string
  city: string
}

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

  locations: LocationOption[]
  loading: boolean

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
  locations,
  loading,
  onSearch,
}: Props) {
  const countries = Array.from(
    new Set(
      locations
        .map((location) => location.country)
        .filter(Boolean)
    )
  ).sort()

  const cities = Array.from(
    new Set(
      locations
        .filter((location) => {
          if (!country.trim()) {
            return true
          }

          return location.country
            ?.toLowerCase()
            .includes(country.trim().toLowerCase())
        })
        .map((location) => location.city)
        .filter(Boolean)
    )
  ).sort()

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!loading) {
      onSearch()
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      {/* ROLE / KEYWORDS */}

      <div>
        <label
          htmlFor="job-keyword"
          className="mb-2 block text-sm font-medium"
        >
          Role / Keywords
        </label>

        <Input
          id="job-keyword"
          placeholder="Backend Python"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          autoComplete="off"
        />
      </div>

      {/* FILTERS */}

      <div className="grid gap-4 md:grid-cols-4">

        {/* COUNTRY */}

        <div>
          <label
            htmlFor="job-country"
            className="sr-only"
          >
            Country
          </label>

          <Input
            id="job-country"
            list="country-options"
            placeholder="Country"
            value={country}
            onChange={(e) => {
              setCountry(e.target.value)

              // Si cambia el país, limpiamos la ciudad
              // para evitar combinaciones inválidas.
              if (city) {
                setCity("")
              }
            }}
            autoComplete="off"
          />

          <datalist id="country-options">
            {countries.map((countryOption) => (
              <option
                key={countryOption}
                value={countryOption}
              />
            ))}
          </datalist>
        </div>

        {/* CITY */}

        <div>
          <label
            htmlFor="job-city"
            className="sr-only"
          >
            City
          </label>

          <Input
            id="job-city"
            list="city-options"
            placeholder="City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            autoComplete="off"
          />

          <datalist id="city-options">
            {cities.map((cityOption) => (
              <option
                key={cityOption}
                value={cityOption}
              />
            ))}
          </datalist>
        </div>

        {/* PUBLISHED */}

        <select
          value={published}
          onChange={(e) => setPublished(e.target.value)}
          className="
            h-10
            w-full
            rounded-md
            border
            bg-background
            px-3
            text-sm
          "
        >
          <option value="">Published</option>
          <option value="1">Last 24 hours</option>
          <option value="3">Last 3 days</option>
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
        </select>

        {/* WORK TYPE */}

        <select
          value={workType}
          onChange={(e) => setWorkType(e.target.value)}
          className="
            h-10
            w-full
            rounded-md
            border
            bg-background
            px-3
            text-sm
          "
        >
          <option value="">Work Type</option>
          <option value="Remote">Remote</option>
          <option value="Hybrid">Hybrid</option>
          <option value="On-site">On-site</option>
        </select>

      </div>

      {/* SEARCH */}

      <Button
        type="submit"
        disabled={loading}
      >
        {loading ? "Searching..." : "Search Jobs"}
      </Button>

    </form>
  )
}