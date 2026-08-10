type Props = {
    applicationAnswers: any
  }
  
  export default function ApplicationAnswersTab({
    applicationAnswers,
  }: Props) {
  
    if (!applicationAnswers) return null
  
    return (
      <div className="rounded-xl border p-6">
  
        <h2 className="text-2xl font-bold">
          Application Answers
        </h2>
  
        <div className="space-y-8 mt-6">
  
          <div>
            <h3 className="font-semibold">
              Tell me about yourself
            </h3>
  
            <p className="mt-2 whitespace-pre-wrap">
              {applicationAnswers.tell_me_about_yourself}
            </p>
          </div>
  
          <div>
            <h3 className="font-semibold">
              Why this company?
            </h3>
  
            <p className="mt-2 whitespace-pre-wrap">
              {applicationAnswers.why_this_company}
            </p>
          </div>
  
          <div>
            <h3 className="font-semibold">
              Why should we hire you?
            </h3>
  
            <p className="mt-2 whitespace-pre-wrap">
              {applicationAnswers.why_should_we_hire_you}
            </p>
          </div>
  
          <div>
            <h3 className="font-semibold">
              Greatest strength
            </h3>
  
            <p className="mt-2 whitespace-pre-wrap">
              {applicationAnswers.greatest_strength}
            </p>
          </div>
  
          <div>
            <h3 className="font-semibold">
              Greatest weakness
            </h3>
  
            <p className="mt-2 whitespace-pre-wrap">
              {applicationAnswers.greatest_weakness}
            </p>
          </div>
  
        </div>
  
      </div>
    )
  }