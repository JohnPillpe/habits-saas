import { useState } from "react"
import {
  useNavigate,
  useLocation,
} from "react-router-dom"

import { login } from "@/services/auth"

export default function Login() {
  const navigate = useNavigate()
  const location = useLocation()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [showPassword, setShowPassword] =
    useState(false)

  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleLogin(
    e: React.FormEvent,
  ) {
    e.preventDefault()

    setError("")

    if (loading) {
      return
    }

    try {
      setLoading(true)

      const data = await login(
        email.trim(),
        password,
      )

      localStorage.setItem(
        "token",
        data.access_token,
      )

      navigate(
        location.state?.from || "/",
      )
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to log in.",
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
        Login
      </h1>

      <form
        onSubmit={handleLogin}
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
              autoComplete="current-password"
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

        <div className="flex justify-end">
          <button
            type="button"
            onClick={() =>
              navigate("/forgot-password")
            }
            className="text-sm text-neutral-600 hover:text-black hover:underline"
          >
            Forgot password?
          </button>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-black p-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading
            ? "Logging in..."
            : "Login"}
        </button>

      </form>

      <div className="mt-6 text-center text-sm text-neutral-500">
        Don't have an account?{" "}
        <button
          type="button"
          onClick={() =>
            navigate("/signup")
          }
          className="font-medium text-black hover:underline"
        >
          Create one
        </button>
      </div>

    </div>
  )
}