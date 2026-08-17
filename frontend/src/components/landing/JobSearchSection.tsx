import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import LocationCombobox from "@/components/ui/location-combobox"

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
  loading?: boolean
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
  loading = false,
}: Props) {
  function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()
    onSearch()
  }

  function handleCountryChange(value: string) {
    setCountry(value)

    // A city selected for another country
    // should never remain active.
    if (!value.trim()) {
      setCity("")
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      <div>
        <label className="mb-2 block text-sm font-medium">
          Role / Keywords
        </label>

        <Input
          placeholder="Backend Python"
          value={keyword}
          onChange={(e) =>
            setKeyword(e.target.value)
          }
        />
      </div>

      <div className="grid gap-4 md:grid-cols-4">

        <LocationCombobox
          type="country"
          value={country}
          onChange={handleCountryChange}
          placeholder="Country"
        />

        <LocationCombobox
          type="city"
          value={city}
          onChange={setCity}
          country={country}
          placeholder={
            country
              ? "City"
              : "Select country first"
          }
          disabled={!country.trim()}
        />

        <select
          value={published}
          onChange={(e) =>
            setPublished(e.target.value)
          }
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
          <option value="">
            Published
          </option>

          <option value="1">
            Last 24 hours
          </option>

          <option value="3">
            Last 3 days
          </option>

          <option value="7">
            Last 7 days
          </option>

          <option value="30">
            Last 30 days
          </option>
        </select>

        <select
          value={workType}
          onChange={(e) =>
            setWorkType(e.target.value)
          }
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
          <option value="">
            Work Type
          </option>

          <option value="Remote">
            Remote
          </option>

          <option value="Hybrid">
            Hybrid
          </option>

          <option value="On-site">
            On-site
          </option>
        </select>
      </div>

      <Button
        type="submit"
        disabled={loading}
      >
        {loading ? "Searching..." : "Search Jobs"}
      </Button>
    </form>
  )
}