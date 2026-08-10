type Props = {
    interviewPreparation: any
  }
  
  export default function InterviewPreparationTab({
    interviewPreparation,
  }: Props) {
  
    if (!interviewPreparation) return null
  
    return (
      <div className="rounded-xl border p-6">
  
        <h2 className="text-2xl font-bold">
          Interview Preparation
        </h2>
  
        <div className="mt-6">
  
          <strong>
            Technical Questions
          </strong>
  
          <ul className="mt-3 list-disc pl-6">
            {interviewPreparation.technical_questions?.map(
              (item: string) => (
                <li key={item}>{item}</li>
              )
            )}
          </ul>
  
        </div>
  
        <div className="mt-8">
  
          <strong>
            Behavioral Questions
          </strong>
  
          <ul className="mt-3 list-disc pl-6">
            {interviewPreparation.behavioral_questions?.map(
              (item: string) => (
                <li key={item}>{item}</li>
              )
            )}
          </ul>
  
        </div>
  
        <div className="mt-8">
  
          <strong>
            Interview Tips
          </strong>
  
          <ul className="mt-3 list-disc pl-6">
            {interviewPreparation.tips?.map(
              (item: string) => (
                <li key={item}>{item}</li>
              )
            )}
          </ul>
  
        </div>
  
      </div>
    )
  }