  const API = "http://127.0.0.1:8000"

  export async function hasCV(token: string) {
    const response = await fetch(`${API}/upload/has-cv`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return response.json()
  }