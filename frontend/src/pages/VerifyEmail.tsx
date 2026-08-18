import { useEffect, useState } from "react"
import {
  useNavigate,
  useSearchParams,
} from "react-router-dom"

import { verifyEmail } from "@/services/auth"

export default function VerifyEmail() {
  const navigate = useNavigate()
  const [searchParams] =
    useSearchParams()

  const [status, setStatus] =
    useState<
      "loading" | "success" | "error"
    >("loading")

  const [message, setMessage] =
    useState("")

  useEffect(() => {
    const token =
      searchParams.get("token")

    if (!token) {
      setStatus("error")
      setMessage(
        "Invalid verification link.",
      )
      return
    }

    verifyEmail(token)
      .then(() => {
        localStorage.setItem(
          "email_verified",
          "true",
        )

        setStatus("success")
      })
      .catch((error) => {
        setStatus("error")

        setMessage(
          error instanceof Error
            ? error.message
            : "Verification failed.",
        )
      })
  }, [searchParams])

  return (
    <div className="mx-auto max-w-md px-6 py-20 text-center">

      {status === "loading" && (
        <>
          <h1 className="text-2xl font-bold">
            Verifying your email...
          </h1>

          <p className="mt-3 text-sm text-neutral-500">
            Please wait a moment.
          </p>
        </>
      )}

      {status === "success" && (
        <>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
            ✓
          </div>

          <h1 className="mt-6 text-2xl font-bold">
            Email verified
          </h1>

          <p className="mt-3 text-sm text-neutral-500">
            Your email has been successfully
            verified.
          </p>

          <button
            onClick={() => navigate("/")}
            className="mt-8 rounded-lg bg-black px-6 py-3 text-sm text-white"
          >
            Continue to MatchAI
          </button>
        </>
      )}

      {status === "error" && (
        <>
          <h1 className="text-2xl font-bold">
            Verification failed
          </h1>

          <p className="mt-3 text-sm text-neutral-500">
            {message}
          </p>

          <button
            onClick={() => navigate("/")}
            className="mt-8 text-sm font-medium underline"
          >
            Back to MatchAI
          </button>
        </>
      )}

    </div>
  )
}