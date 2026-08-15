export type MatchLevel = "strong" | "moderate" | "weak"

export type MatchTone = {
  level: MatchLevel
  color: string
  label: string
}

export function getMatchLevel(score: number): MatchLevel {
  if (score >= 70) {
    return "strong"
  }

  if (score >= 45) {
    return "moderate"
  }

  return "weak"
}

export function getMatchTone(score: number): MatchTone {
  const level = getMatchLevel(score)

  if (level === "strong") {
    return {
      level,
      color: "var(--match-strong)",
      label: "Strong match",
    }
  }

  if (level === "moderate") {
    return {
      level,
      color: "var(--match-mid)",
      label: "Moderate match",
    }
  }

  return {
    level,
    color: "var(--match-weak)",
    label: "Weak match",
  }
}