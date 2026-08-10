const API = "http://127.0.0.1:8000"

export async function uploadCV(
  file: File,
  token: string,
) {
  const formData = new FormData()

  formData.append("file", file)

  const response = await fetch(`${API}/upload/cv`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Upload failed")
  }

  return response.json()
}