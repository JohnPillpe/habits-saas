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
              {showPassword ? "◉" : "◌"}
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