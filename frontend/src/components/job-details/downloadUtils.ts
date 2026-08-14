export function copyToClipboard(text: string) {
  if (!text) return

  navigator.clipboard.writeText(text)
}


/*
 * ============================================================
 * WORD
 * ============================================================
 */

export function downloadAsWord(
  title: string,
  content: string,
) {
  if (!content) return

  const safeTitle = createSafeFileName(title)

  const sections = textToWordHtml(content)

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />

        <title>
          ${escapeHtml(title)}
        </title>

        <style>

          @page {
            size: A4;
            margin: 22mm;
          }

          body {
            font-family:
              Arial,
              Helvetica,
              sans-serif;

            font-size: 11pt;

            line-height: 1.6;

            color: #111827;

            margin: 0;
          }

          h1 {
            font-size: 20pt;

            font-weight: 700;

            margin:
              0 0 28px 0;

            color: #111827;
          }

          h2 {
            font-size: 15pt;

            font-weight: 700;

            margin:
              24px 0 10px 0;

            color: #111827;
          }

          h3 {
            font-size: 12pt;

            font-weight: 700;

            margin:
              20px 0 8px 0;

            color: #111827;
          }

          p {
            margin:
              0 0 12px 0;

            line-height: 1.6;

            text-align: justify;
          }

          ul,
          ol {
            margin:
              8px 0 16px 24px;

            padding: 0;
          }

          li {
            margin-bottom: 7px;

            line-height: 1.55;
          }

          .document {
            width: 100%;
          }

          .section {
            margin-bottom: 18px;
          }

        </style>
      </head>

      <body>

        <div class="document">

          <h1>
            ${escapeHtml(title)}
          </h1>

          ${sections}

        </div>

      </body>
    </html>
  `

  const blob = new Blob(
    [html],
    {
      type: "application/msword",
    },
  )

  const url =
    URL.createObjectURL(blob)

  const link =
    document.createElement("a")

  link.href = url

  link.download =
    `${safeTitle || "document"}.doc`

  document.body.appendChild(link)

  link.click()

  document.body.removeChild(link)

  URL.revokeObjectURL(url)
}


/*
 * ============================================================
 * PDF
 * ============================================================
 */

export function downloadAsPDF(
  title: string,
  content: string,
) {
  if (!content) return

  const printWindow =
    window.open(
      "",
      "_blank",
      "width=900,height=700",
    )

  if (!printWindow) {
    alert(
      "Please allow pop-ups to download the PDF.",
    )

    return
  }

  const sections =
    textToPrintableHtml(content)

  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>

        <meta charset="UTF-8" />

        <title>
          ${escapeHtml(title)}
        </title>

        <style>

          @page {
            size: A4;
            margin: 20mm 20mm 22mm 20mm;
          }

          * {
            box-sizing: border-box;
          }

          body {
            font-family:
              Arial,
              Helvetica,
              sans-serif;

            font-size: 11pt;

            line-height: 1.6;

            color: #111827;

            margin: 0;
          }

          .document {
            width: 100%;
          }

          h1 {
            font-size: 20pt;

            line-height: 1.25;

            font-weight: 700;

            margin:
              0 0 28px 0;

            color: #111827;

            page-break-after: avoid;
          }

          h2 {
            font-size: 15pt;

            line-height: 1.3;

            font-weight: 700;

            margin:
              24px 0 10px 0;

            color: #111827;

            page-break-after: avoid;
          }

          h3 {
            font-size: 12pt;

            line-height: 1.3;

            font-weight: 700;

            margin:
              20px 0 8px 0;

            color: #111827;

            page-break-after: avoid;
          }

          p {
            margin:
              0 0 12px 0;

            line-height: 1.6;

            text-align: justify;

            orphans: 3;

            widows: 3;
          }

          ul,
          ol {
            margin:
              8px 0 16px 24px;

            padding: 0;
          }

          li {
            margin-bottom: 7px;

            line-height: 1.55;

            orphans: 2;

            widows: 2;
          }

          .section {
            margin-bottom: 18px;
          }

          strong {
            font-weight: 700;
          }

        </style>

      </head>

      <body>

        <div class="document">

          <h1>
            ${escapeHtml(title)}
          </h1>

          ${sections}

        </div>

        <script>

          window.onload = function () {
            setTimeout(
              function () {
                window.print()
              },
              250
            )
          }

        </script>

      </body>
    </html>
  `)

  printWindow.document.close()
}


/*
 * ============================================================
 * TEXT → WORD HTML
 * ============================================================
 */

function textToWordHtml(
  content: string,
): string {
  const normalized =
    normalizeContent(content)

  const lines =
    normalized.split("\n")

  const html: string[] = []

  let paragraphLines: string[] = []

  let listType:
    "ul" | "ol" | null = null

  let listItems: string[] = []


  function flushParagraph() {
    if (
      paragraphLines.length === 0
    ) {
      return
    }

    const paragraph =
      paragraphLines
        .join(" ")
        .trim()

    if (paragraph) {
      html.push(
        `<p>${escapeHtml(paragraph)}</p>`,
      )
    }

    paragraphLines = []
  }


  function flushList() {
    if (
      !listType ||
      listItems.length === 0
    ) {
      return
    }

    html.push(
      `<${listType}>${listItems.join("")}</${listType}>`,
    )

    listType = null

    listItems = []
  }


  for (const rawLine of lines) {
    const line =
      rawLine.trim()


    if (!line) {
      flushParagraph()
      flushList()
      continue
    }


    /*
     * BULLET
     */

    const bulletMatch =
      line.match(
        /^[-•*]\s+(.*)$/,
      )

    if (bulletMatch) {
      flushParagraph()

      if (listType !== "ul") {
        flushList()
        listType = "ul"
      }

      listItems.push(
        `<li>${escapeHtml(
          bulletMatch[1],
        )}</li>`,
      )

      continue
    }


    /*
     * NUMBERED LIST
     */

    const numberedMatch =
      line.match(
        /^\d+[.)]\s+(.*)$/,
      )

    if (numberedMatch) {
      flushParagraph()

      if (listType !== "ol") {
        flushList()
        listType = "ol"
      }

      listItems.push(
        `<li>${escapeHtml(
          numberedMatch[1],
        )}</li>`,
      )

      continue
    }


    /*
     * HEADING
     */

    if (
      line.length < 80 &&
      (
        line.endsWith(":") ||
        isLikelyHeading(line)
      )
    ) {
      flushParagraph()
      flushList()

      html.push(
        `<h2>${escapeHtml(
          line.replace(/:$/, ""),
        )}</h2>`,
      )

      continue
    }


    /*
     * NORMAL PARAGRAPH
     */

    flushList()

    paragraphLines.push(line)
  }


  flushParagraph()
  flushList()


  return html.join("\n")
}


/*
 * ============================================================
 * TEXT → PRINTABLE HTML
 * ============================================================
 */

function textToPrintableHtml(
  content: string,
): string {
  return textToWordHtml(content)
}


/*
 * ============================================================
 * NORMALIZATION
 * ============================================================
 */

function normalizeContent(
  content: string,
): string {
  return content
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/\u00a0/g, " ")
    .trim()
}


/*
 * ============================================================
 * HEADING DETECTION
 * ============================================================
 */

function isLikelyHeading(
  line: string,
): boolean {
  if (!line) return false

  if (line.length > 70) {
    return false
  }

  const words =
    line.split(/\s+/)

  if (words.length > 10) {
    return false
  }

  const headingWords = [
    "summary",
    "profile",
    "experience",
    "education",
    "skills",
    "technical skills",
    "professional experience",
    "work experience",
    "qualifications",
    "responsibilities",
    "requirements",
    "key responsibilities",
    "key requirements",
    "about",
    "about the role",
    "why this company",
    "why should we hire you",
    "technical questions",
    "behavioral questions",
    "interview tips",
    "tips",
    "tell me about yourself",
  ]

  const normalized =
    line
      .toLowerCase()
      .replace(/:$/, "")
      .trim()

  if (
    headingWords.includes(
      normalized,
    )
  ) {
    return true
  }

  /*
   * ALL CAPS short lines
   */

  if (
    line === line.toUpperCase() &&
    /[A-Z]/.test(line) &&
    words.length <= 8
  ) {
    return true
  }

  return false
}


/*
 * ============================================================
 * FILE NAME
 * ============================================================
 */

function createSafeFileName(
  title: string,
): string {
  return title
    .replace(/[^a-z0-9]/gi, "_")
    .replace(/_+/g, "_")
    .replace(/^_|_$/g, "")
}


/*
 * ============================================================
 * HTML ESCAPE
 * ============================================================
 */

function escapeHtml(
  value: string,
): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
}