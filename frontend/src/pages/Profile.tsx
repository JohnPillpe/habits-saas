import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { uploadCV } from "@/services/documents"

export default function Profile() {
  const navigate = useNavigate()

  const [hasCv, setHasCv] = useState(true)
  const [loading, setLoading] = useState(false)

  async function handleReplaceCV(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0]

    if (!file) return

    const token = localStorage.getItem("token")

    if (!token) {
      navigate("/login")
      return
    }

    try {
      setLoading(true)

      await uploadCV(file, token)

      setHasCv(true)

      alert("CV replaced successfully")

    } catch (error) {
      alert("Could not upload CV")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-12">

      <button
        onClick={() => navigate("/")}
        className="mb-8 text-sm font-medium text-neutral-500 hover:text-black"
      >
        ← Back to jobs
      </button>

      <h1 className="text-3xl font-bold">
        Profile
      </h1>

      <div className="mt-8 rounded-2xl border border-neutral-200 p-6">

        <h2 className="text-xl font-semibold">
          Your CV
        </h2>

        <p className="mt-2 text-sm text-neutral-500">
          {hasCv
            ? "You have a CV uploaded."
            : "You don't have a CV uploaded yet."}
        </p>

        <label className="mt-6 inline-block cursor-pointer rounded-lg bg-black px-5 py-2.5 text-sm text-white">
          {loading ? "Uploading..." : "Replace CV"}

          <input
            type="file"
            accept=".pdf"
            className="hidden"
            disabled={loading}
            onChange={handleReplaceCV}
          />
        </label>

      </div>

    </section>
  )
}