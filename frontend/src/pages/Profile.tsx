import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

import { uploadCV } from "@/services/documents"
import { getCVStatus } from "@/services/upload"
import { changePassword } from "@/services/auth"

export default function Profile() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [hasCv, setHasCv] = useState(false)
  const [cvFilename, setCvFilename] = useState("")

  const [loadingCv, setLoadingCv] = useState(true)
  const [uploading, setUploading] = useState(false)

  const [cvSuccess, setCvSuccess] = useState("")
  const [cvError, setCvError] = useState("")

  const [currentPassword, setCurrentPassword] =
    useState("")
  const [newPassword, setNewPassword] =
    useState("")
  const [confirmPassword, setConfirmPassword] =
    useState("")

  const [changingPassword, setChangingPassword] =
    useState(false)
  const [passwordSuccess, setPasswordSuccess] =
    useState("")
  const [passwordError, setPasswordError] =
    useState("")

  const [showCurrentPassword, setShowCurrentPassword] =
    useState(false)

  const [showNewPassword, setShowNewPassword] =
    useState(false)

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false)

  useEffect(() => {
    async function loadProfile() {
      const token = localStorage.getItem("token")

      if (!token) {
        navigate("/login")
        return
      }

      try {
        const data = await getCVStatus(token)

        setEmail(data.email)
        setHasCv(data.has_cv)
        setCvFilename(data.filename || "")
      } catch {
        setCvError("Could not load your profile.")
      } finally {
        setLoadingCv(false)
      }
    }

    loadProfile()
  }, [navigate])

  async function handleReplaceCV(
    e: React.ChangeEvent<HTMLInputElement>,
  ) {
    const file = e.target.files?.[0]

    if (!file) {
      return
    }

    const token = localStorage.getItem("token")

    if (!token) {
      navigate("/login")
      return
    }

    setCvSuccess("")
    setCvError("")

    if (file.type !== "application/pdf") {
      setCvError("Only PDF files are supported.")
      e.target.value = ""
      return
    }

    try {
      setUploading(true)

      const data = await uploadCV(file, token)

      setHasCv(true)
      setCvFilename(data.filename || file.name)
      setCvSuccess("CV uploaded successfully")
    } catch (error) {
      setCvError(
        error instanceof Error
          ? error.message
          : "Could not upload CV.",
      )
    } finally {
      setUploading(false)
      e.target.value = ""
    }
  }

  async function handleChangePassword(
    e: React.FormEvent,
  ) {
    e.preventDefault()

    setPasswordSuccess("")
    setPasswordError("")

    if (newPassword.length < 8) {
      setPasswordError(
        "New password must contain at least 8 characters.",
      )
      return
    }

    if (newPassword !== confirmPassword) {
      setPasswordError(
        "New passwords do not match.",
      )
      return
    }

    try {
      setChangingPassword(true)

      const data = await changePassword(
        currentPassword,
        newPassword,
      )

      setPasswordSuccess(data.message)

      setCurrentPassword("")
      setNewPassword("")
      setConfirmPassword("")
    } catch (error) {
      setPasswordError(
        error instanceof Error
          ? error.message
          : "Could not change password.",
      )
    } finally {
      setChangingPassword(false)
    }
  }

  if (loadingCv) {
    return (
      <section className="mx-auto max-w-3xl px-6 py-12">
        <p className="text-sm text-neutral-500">
          Loading profile...
        </p>
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-12">

      <button
        type="button"
        onClick={() => navigate("/")}
        className="mb-8 text-sm font-medium text-neutral-500 hover:text-black"
      >
        ← Back to jobs
      </button>

      <h1 className="text-3xl font-bold">
        Profile
      </h1>

      {/* =====================================================
          ACCOUNT
          ===================================================== */}

      <div className="mt-8 rounded-2xl border border-neutral-200 p-6">

        <h2 className="text-xl font-semibold">
          Account
        </h2>

        <p className="mt-2 text-sm text-neutral-500">
          Email
        </p>

        <p className="mt-1 text-sm font-medium">
          {email}
        </p>

      </div>


      {/* =====================================================
          CV
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-neutral-200 p-6">

        <h2 className="text-xl font-semibold">
          Your CV
        </h2>

        {hasCv ? (
          <>
            <p className="mt-2 text-sm text-neutral-500">
              Current CV
            </p>

            <p className="mt-1 text-sm font-medium">
              {cvFilename || "CV uploaded"}
            </p>
          </>
        ) : (
          <p className="mt-2 text-sm text-neutral-500">
            You don't have a CV uploaded yet.
            Upload a CV to unlock Match Score and AI analysis.
          </p>
        )}

        {cvSuccess && (
          <div className="mt-5 rounded-lg bg-green-50 p-3 text-sm text-green-700">
            ✓ {cvSuccess}
          </div>
        )}

        {cvError && (
          <div className="mt-5 rounded-lg bg-red-50 p-3 text-sm text-red-600">
            {cvError}
          </div>
        )}

        <label className="mt-6 inline-block cursor-pointer rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white">
          {uploading
            ? "Uploading..."
            : hasCv
              ? "Replace CV"
              : "Upload CV"}

          <input
            type="file"
            accept=".pdf,application/pdf"
            className="hidden"
            disabled={uploading}
            onChange={handleReplaceCV}
          />
        </label>

      </div>


      {/* =====================================================
          CHANGE PASSWORD
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-neutral-200 p-6">

        <h2 className="text-xl font-semibold">
          Change password
        </h2>

        <form
          onSubmit={handleChangePassword}
          className="mt-6 space-y-5"
        >

          <div className="relative">
            <input
              type={
                showCurrentPassword
                  ? "text"
                  : "password"
              }
              required
              autoComplete="current-password"
              value={currentPassword}
              onChange={(e) =>
                setCurrentPassword(e.target.value)
              }
              className="w-full rounded-lg border p-3 pr-12 outline-none focus:ring-2 focus:ring-neutral-200"
              />

              <button
                type="button"
                onClick={() =>
                  setShowCurrentPassword(
                    (current) => !current,
                  )
                }
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-black"
                aria-label={
                  showCurrentPassword
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
                  {showCurrentPassword ? (
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




          <div className="relative">
            <input
              type={
                showNewPassword
                  ? "text"
                  : "password"
              }
              required
              minLength={8}
              autoComplete="new-password"
              placeholder="At least 8 characters"
              value={newPassword}
              onChange={(e) =>
                  setNewPassword(e.target.value)
              }
              className="w-full rounded-lg border p-3 pr-12 outline-none focus:ring-2 focus:ring-neutral-200"
              />

              <button
                type="button"
                onClick={() =>
                  setShowNewPassword(
                    (current) => !current,
                  )
                }
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-black"
                aria-label={
                  showNewPassword
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
                  {showNewPassword ? (
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




          <div className="relative">
            <input
              type={
                showConfirmPassword
                  ? "text"
                  : "password"
                }
                required
                minLength={8}
                autoComplete="new-password"
                placeholder="Repeat your new password"
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(e.target.value)
                }
                className="w-full rounded-lg border p-3 pr-12 outline-none focus:ring-2 focus:ring-neutral-200"
              />

              <button
                type="button"
                onClick={() =>
                  setShowConfirmPassword(
                    (current) => !current,
                  )
                }
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-black"
                aria-label={
                  showConfirmPassword
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
                  {showConfirmPassword ? (
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

          {passwordError && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
              {passwordError}
            </div>
          )}

          {passwordSuccess && (
            <div className="rounded-lg bg-green-50 p-3 text-sm text-green-700">
              ✓ {passwordSuccess}
            </div>
          )}

          <button
            type="submit"
            disabled={changingPassword}
            className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white disabled:opacity-50"
          >
            {changingPassword
              ? "Updating..."
              : "Change password"}
          </button>

        </form>

      </div>

    </section>
  )
}