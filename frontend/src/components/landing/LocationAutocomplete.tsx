import { useEffect, useRef, useState } from "react"

type Props = {
  value: string
  onChange: (value: string) => void
  placeholder: string
  endpoint: string
  disabled?: boolean
}

type CountryResponse = {
  regions?: string[]
  countries?: string[]
}

export default function LocationAutocomplete({
  value,
  onChange,
  placeholder,
  endpoint,
  disabled = false,
}: Props) {
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const query = value.trim()

    if (!query) {
      setSuggestions([])
      setOpen(false)
      return
    }

    const controller = new AbortController()

    const timer = setTimeout(async () => {
      try {
        setLoading(true)

        const url = new URL(endpoint, window.location.origin)

        url.searchParams.set("q", query)

        const response = await fetch(
          url.toString(),
          {
            method: "GET",
            signal: controller.signal,
          }
        )

        if (!response.ok) {
          throw new Error(
            `Location request failed: ${response.status}`
          )
        }

        const data = await response.json()

        let results: string[] = []

        // --------------------------------------------------
        // COUNTRIES ENDPOINT
        // --------------------------------------------------

        if (
          data &&
          typeof data === "object" &&
          !Array.isArray(data)
        ) {
          const regions = Array.isArray(data.regions)
            ? data.regions
            : []

          const countries = Array.isArray(data.countries)
            ? data.countries
            : []

          results = [
            ...regions.map(
              (item: unknown) => String(item)
            ),
            ...countries.map(
              (item: unknown) => String(item)
            ),
          ]
        }

        // --------------------------------------------------
        // CITIES ENDPOINT
        // --------------------------------------------------

        else if (Array.isArray(data)) {
          results = data.map(
            (item: unknown) => String(item)
          )
        }

        // --------------------------------------------------
        // CLEAN RESULTS
        // --------------------------------------------------

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
          error
        )

        setSuggestions([])
        setOpen(false)
      } finally {
        setLoading(false)
      }
    }, 200)

    return () => {
      clearTimeout(timer)
      controller.abort()
    }
  }, [value, endpoint])

  // --------------------------------------------------
  // CLOSE WHEN CLICKING OUTSIDE
  // --------------------------------------------------

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(
          event.target as Node
        )
      ) {
        setOpen(false)
      }
    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    )

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      )
    }
  }, [])

  // --------------------------------------------------
  // SELECT
  // --------------------------------------------------

  function handleSelect(item: string) {
    onChange(item)
    setOpen(false)
  }

  return (
    <div
      ref={containerRef}
      className="relative w-full"
    >
      <input
        type="text"
        value={value}
        disabled={disabled}
        placeholder={placeholder}
        autoComplete="off"
        onFocus={() => {
          if (suggestions.length > 0) {
            setOpen(true)
          }
        }}
        onChange={(event) => {
          onChange(event.target.value)
          setOpen(true)
        }}
        className="w-full"
      />

      {open && (
        <div
          className="
            absolute
            left-0
            right-0
            top-full
            z-50
            mt-1
            max-h-64
            overflow-y-auto
            rounded-md
            border
            bg-white
            shadow-lg
          "
        >
          {loading && (
            <div className="px-3 py-2 text-sm text-gray-500">
              Searching...
            </div>
          )}

          {!loading &&
            suggestions.map((item) => (
              <button
                key={item}
                type="button"
                className="
                  block
                  w-full
                  cursor-pointer
                  px-3
                  py-2
                  text-left
                  text-sm
                  hover:bg-gray-100
                "
                onMouseDown={(event) => {
                  event.preventDefault()
                }}
                onClick={() => {
                  handleSelect(item)
                }}
              >
                {item}
              </button>
            ))}
        </div>
      )}
    </div>
  )
}