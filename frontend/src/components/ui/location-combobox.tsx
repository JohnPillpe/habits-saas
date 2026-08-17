import { useEffect, useRef, useState } from "react"

type LocationComboboxProps = {
  type: "country" | "city"
  value: string
  onChange: (value: string) => void
  country?: string
  placeholder?: string
  disabled?: boolean
}

const API_URL = "http://127.0.0.1:8000"

export default function LocationCombobox({
  type,
  value,
  onChange,
  country,
  placeholder,
  disabled = false,
}: LocationComboboxProps) {
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (disabled) {
      setSuggestions([])
      setOpen(false)
      return
    }

    const query = value.trim()

    if (!query) {
      setSuggestions([])
      setOpen(false)
      return
    }

    if (type === "city" && !country?.trim()) {
      setSuggestions([])
      setOpen(false)
      return
    }

    const controller = new AbortController()

    const timer = window.setTimeout(async () => {
      try {
        setLoading(true)

        const params = new URLSearchParams()

        params.set("q", query)

        if (type === "city" && country?.trim()) {
          params.set("country", country.trim())
        }

        const endpoint =
          type === "country"
            ? `${API_URL}/job-offers/locations/countries`
            : `${API_URL}/job-offers/locations/cities`

        const response = await fetch(
          `${endpoint}?${params.toString()}`,
          {
            signal: controller.signal,
          },
        )

        if (!response.ok) {
          throw new Error(
            `Location request failed: ${response.status}`,
          )
        }

        const data = await response.json()

        let results: string[] = []

        if (Array.isArray(data)) {
          // Cities endpoint
          results = data.map(String)
        } else if (
          data &&
          typeof data === "object"
        ) {
          // Countries / regions endpoint
          const regions = Array.isArray(data.regions)
            ? data.regions.map(String)
            : []

          const countries = Array.isArray(data.countries)
            ? data.countries.map(String)
            : []

          results = [
            ...regions,
            ...countries,
          ]
        }

        results = Array.from(
          new Set(
            results
              .map((item) => item.trim())
              .filter(Boolean)
          )
        )

        setSuggestions(results.slice(0, 50))
        setOpen(results.length > 0)


      } catch (error) {
        if (
          error instanceof DOMException &&
          error.name === "AbortError"
        ) {
          return
        }

        console.error(
          "Location autocomplete error:",
          error,
        )

        setSuggestions([])
        setOpen(false)
      } finally {
        setLoading(false)
      }
    }, 250)

    return () => {
      window.clearTimeout(timer)
      controller.abort()
    }
  }, [value, type, country, disabled])

  useEffect(() => {
    function handleOutsideClick(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(
          event.target as Node,
        )
      ) {
        setOpen(false)
      }
    }

    document.addEventListener(
      "mousedown",
      handleOutsideClick,
    )

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick,
      )
    }
  }, [])

  function handleSelect(option: string) {
    onChange(option)
    setOpen(false)
  }

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    onChange(event.target.value)
    setOpen(true)
  }

  return (
    <div
      ref={containerRef}
      className="relative"
    >
      <input
        type="text"
        value={value}
        onChange={handleChange}
        onFocus={() => {
          if (suggestions.length > 0) {
            setOpen(true)
          }
        }}
        placeholder={placeholder}
        disabled={disabled}
        autoComplete="off"
        className="
          h-10
          w-full
          rounded-md
          border
          bg-background
          px-3
          text-sm
          outline-none
          transition
          focus:ring-2
          focus:ring-neutral-200
          disabled:cursor-not-allowed
          disabled:opacity-50
        "
      />

      {loading && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-neutral-400">
          ...
        </div>
      )}

      {open && suggestions.length > 0 && (
        <div
          className="
            absolute
            z-50
            mt-1
            max-h-60
            w-full
            overflow-auto
            rounded-md
            border
            bg-white
            py-1
            shadow-lg
          "
        >
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onMouseDown={(event) => {
                event.preventDefault()
              }}
              onClick={() => handleSelect(suggestion)}
              className="
                block
                w-full
                px-3
                py-2
                text-left
                text-sm
                hover:bg-neutral-100
              "
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}