type Props = {
    coverLetter: any
  }
  
  export default function CoverLetterTab({
    coverLetter,
  }: Props) {
  
    if (!coverLetter) return null
  
    return (
      <div className="rounded-xl border p-6">
  
        <h2 className="text-2xl font-bold">
          Cover Letter
        </h2>
  
        <pre className="mt-6 whitespace-pre-wrap text-sm">
          {coverLetter.content}
        </pre>
  
      </div>
    )
  }