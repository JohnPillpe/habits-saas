import { useState } from "react"

import { uploadCV } from "@/services/documents"

type Props = {
  open: boolean
  onClose: () => void
  onUploaded?: () => void
}

export default function UploadCVModal({
  open,
  onClose,
  onUploaded,
}: Props) {
  const [loading, setLoading] = useState(false)

  if (!open) return null

  async function handleFile(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0]

    if (!file) return

    const token = localStorage.getItem("token")

    if (!token) return

    try {
      setLoading(true)

      await uploadCV(file, token)

      onUploaded?.()

      onClose()

    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">

      <div className="w-full max-w-lg rounded-2xl bg-white p-8">

        <h2 className="text-2xl font-bold">
          Upload your CV
        </h2>

        <p className="mt-2 text-neutral-500">
          PDF only
        </p>

        <input
          type="file"
          accept=".pdf"
          className="mt-6"
          disabled={loading}
          onChange={handleFile}
        />

        <div className="mt-8 flex justify-end">

          <button
            onClick={onClose}
            className="rounded-lg border px-5 py-2"
          >
            Cancel
          </button>

        </div>

      </div>

    </div>
  )
}