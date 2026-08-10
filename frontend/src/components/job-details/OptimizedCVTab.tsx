type Props = {
    optimizedCV: any
  }
  
  export default function OptimizedCVTab({
    optimizedCV,
  }: Props) {
  
    if (!optimizedCV) return null
  
    return (
      <div className="rounded-xl border p-6">
  
        <h2 className="text-2xl font-bold">
          Optimized CV
        </h2>
  
        <pre className="mt-6 whitespace-pre-wrap text-sm">
          {optimizedCV.content}
        </pre>
  
      </div>
    )
  }