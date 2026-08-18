import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { forgotPassword } from "@/services/auth"


export default function ForgotPassword() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState("")
  const [error, setError] = useState("")


  async function handleSubmit(
    e: React.FormEvent,
  ) {
    e.preventDefault()

    setError("")
    setSuccess("")
    setLoading(true)

    try {
      const data = await forgotPassword(
        email,
      )

      setSuccess(data.message)
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong.",
      )
    } finally {
      setLoading(false)
    }
  }


  return (
    <div className="mx-auto max-w-md px-6 py-12">

      <button
        type="button"
        onClick={() => navigate("/login")}
        className="mb-10 text-sm font-medium text-neutral-500 hover:text-black"
      >
        ← Back to login
      </button>


      <h1 className="text-3xl font-bold">
        Forgot your password?
      </h1>

      <p className="mt-2 text-sm text-neutral-500">
        Enter your email and we'll send you a
        password reset link.
      </p>


      <form
        onSubmit={handleSubmit}
        className="mt-8 space-y-5"
      >

        <div>

          <label className="mb-2 block text-sm font-medium">
            Email
          </label>

          <input
            type="email"
            required
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="w-full rounded-lg border p-3 outline-none focus:ring-2 focus:ring-neutral-200"
          />

        </div>


        {error && (
          <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}


        {success && (
          <div className="rounded-lg bg-green-50 p-3 text-sm text-green-700">
            {success}
          </div>
        )}


        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-black p-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading
            ? "Sending..."
            : "Send reset link"}
        </button>

      </form>

    </div>
  )
}