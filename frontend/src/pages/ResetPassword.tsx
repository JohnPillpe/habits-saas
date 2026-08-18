import { useState } from "react"
import {
  useNavigate,
  useSearchParams,
} from "react-router-dom"

import { resetPassword } from "@/services/auth"


export default function ResetPassword() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const token = searchParams.get("token")

  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] =
    useState("")

  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState("")
  const [error, setError] = useState("")


  async function handleSubmit(
    e: React.FormEvent,
  ) {
    e.preventDefault()

    setError("")
    setSuccess("")

    if (!token) {
      setError(
        "This password reset link is invalid.",
      )
      return
    }

    if (password.length < 8) {
      setError(
        "Password must contain at least 8 characters.",
      )
      return
    }

    if (password !== confirmPassword) {
      setError(
        "Passwords do not match.",
      )
      return
    }

    try {
      setLoading(true)

      const data = await resetPassword(
        token,
        password,
      )

      setSuccess(data.message)

      setPassword("")
      setConfirmPassword("")
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Could not reset password.",
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
        Create a new password
      </h1>

      <p className="mt-2 text-sm text-neutral-500">
        Choose a new password for your MatchAI
        account.
      </p>


      <form
        onSubmit={handleSubmit}
        className="mt-8 space-y-5"
      >

        <div>

          <label className="mb-2 block text-sm font-medium">
            New password
          </label>

          <input
            type="password"
            required
            minLength={8}
            autoComplete="new-password"
            placeholder="At least 8 characters"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="w-full rounded-lg border p-3 outline-none focus:ring-2 focus:ring-neutral-200"
          />

        </div>


        <div>

          <label className="mb-2 block text-sm font-medium">
            Confirm password
          </label>

          <input
            type="password"
            required
            minLength={8}
            autoComplete="new-password"
            placeholder="Repeat your password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(e.target.value)
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
            <p>{success}</p>

            <button
              type="button"
              onClick={() => navigate("/login")}
              className="mt-3 font-medium text-black underline"
            >
              Go to login
            </button>
          </div>
        )}


        <button
          type="submit"
          disabled={loading || !!success}
          className="w-full rounded-lg bg-black p-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading
            ? "Updating..."
            : "Reset password"}
        </button>

      </form>

    </div>
  )
}