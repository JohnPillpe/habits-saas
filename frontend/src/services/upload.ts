const API = "http://127.0.0.1:8000"

export async function hasCV(token: string) {
  const response = await fetch(
    `${API}/upload/has-cv`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Could not load CV status.",
    )
  }

  return data
}


export async function getCVStatus(
  token: string,
) {
  return hasCV(token)
}