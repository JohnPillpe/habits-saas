import { useState } from "react"
import { useNavigate } from "react-router-dom"

const API = "http://127.0.0.1:8000"

export default function Signup() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [showPassword, setShowPassword] =
    useState(false)

  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  function isValidEmail(
    value: string,
  ) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
      value,
    )
  }

  async function handleSignup(
    e: React.FormEvent,
  ) {
    e.preventDefault()

    setError("")

    const normalizedEmail =
      email.trim()

    if (!isValidEmail(normalizedEmail)) {
      setError(
        "Please enter a valid email address.",
      )
      return
    }

    if (!password) {
      setError(
        "Please enter a password.",
      )
      return
    }

    if (loading) {
      return
    }

    try {
      setLoading(true)

      const response = await fetch(
        `${API}/register`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            email: normalizedEmail,
            password,
          }),
        },
      )

      const data =
        await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Registration failed",
        )
      }

      navigate("/login")
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Registration failed",
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-6 py-12">

      <button
        type="button"
        onClick={() => navigate("/")}
        className="mb-10 text-sm font-medium text-neutral-500 hover:text-black"
      >
        ← Back
      </button>

      <h1 className="mb-8 text-3xl font-bold">
        Create Account
      </h1>

      <form
        onSubmit={handleSignup}
        className="space-y-5"
      >

        <div>
          <label className="mb-2 block text-sm font-medium">
            Email
          </label>

          <input
            className="w-full rounded-lg border p-3 outline-none focus:ring-2 focus:ring-neutral-200"
            placeholder="you@example.com"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium">
            Password
          </label>

          <div className="relative">

            <input
              className="w-full rounded-lg border p-3 pr-12 outline-none focus:ring-2 focus:ring-neutral-200"
              placeholder="Password"
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              autoComplete="new-password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
            />

            <button
              type="button"
              onClick={() =>
                setShowPassword(
                  (current) => !current,
                )
              }
              className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-neutral-500 hover:text-black"
              aria-label={
                showPassword
                  ? "Hide password"
                  : "Show password"
              }
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                {showPassword ? (
                  <>
                    <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
                    <circle cx="12" cy="12" r="3" />
                  </>
                ) : (
                  <>
                    <path d="M3 3l18 18" />
                    <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
                    <path d="M9.9 4.2A10.7 10.7 0 0 1 12 4c6.5 0 10 8 10 8a18.3 18.3 0 0 1-3.1 4.3" />
                    <path d="M6.6 6.6C3.8 8.6 2 12 2 12s3.5 8 10 8a10.9 10.9 0 0 0 4.1-.8" />
                  </>
                )}
              </svg>
            </button>

          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-black p-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading
            ? "Creating account..."
            : "Create Account"}
        </button>

      </form>

      <div className="mt-6 text-center text-sm text-neutral-500">
        Already have an account?{" "}
        <button
          type="button"
          onClick={() =>
            navigate("/login")
          }
          className="font-medium text-black hover:underline"
        >
          Login
        </button>
      </div>

    </div>
  )
}