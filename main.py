import requests
import json
from datetime import datetime

DATE_PATTERN = "%b/%d/%Y"
URL_LINK = "https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json"

# Data Fetching Module
def FetchData(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

# Data Parsing and Transformation Module
def ParseDate(datestring):
    return datetime.strptime(datestring, DATE_PATTERN)

def JobGaps(lastdate, firstdate):
    Last = ParseDate(lastdate)
    First = ParseDate(firstdate)
    return (First - Last).days

# Data Processing Module
def ProcessCandidate(CandidateProfile):
    NameInformation = CandidateProfile.get("contact_info", {}).get("name", {})
    ResumeNameInformation = CandidateProfile.get("contact_info", {}).get("resume_name", {})
    FullName = ResumeNameInformation.get("formatted_name") or NameInformation.get("formatted_name")
    if not FullName:
        return {"name": "N/A", "jobs": []}

    CandidateExperiences = CandidateProfile.get("experience", [])
    CandidateExperiences = sorted(CandidateExperiences, key=lambda x: ParseDate(x["start_date"]), reverse=True)
    
    CandidateJobDetails = []
    PreviousStartDate = None
    
    for JobDetails in CandidateExperiences:
        JobRole = JobDetails.get("title")
        JobStartDate = JobDetails.get("start_date")
        JobEndDate = JobDetails.get("end_date")
        JobLocation = JobDetails.get("location", {}).get("short_display_address")

        if JobRole and JobStartDate and JobEndDate and JobLocation:
            JobInformation = {
                "role": JobRole,
                "start_date": JobStartDate,
                "end_date": JobEndDate,
                "location": JobLocation
            }

            if PreviousStartDate and JobEndDate:
                JobGapDays = JobGaps(JobEndDate, PreviousStartDate)
                if JobGapDays > 1:
                    JobInformation["gap"] = f"Gap in CV for {JobGapDays} days"

            CandidateJobDetails.append(JobInformation)
            PreviousStartDate = JobStartDate

    return {"name": FullName, "jobs": CandidateJobDetails}

# Output Generation Module
def GeneratingOutputString(CandidateProfileString):
    OutputString = f"Hello {CandidateProfileString['name']},\n"
    if CandidateProfileString["jobs"]:
        for JobDetails in CandidateProfileString["jobs"]:
            OutputString += f"- Worked as: {JobDetails['role']}, From {JobDetails['start_date']} To {JobDetails['end_date']} in {JobDetails['location']}"
            if "gap" in JobDetails:
                OutputString += f" {JobDetails['gap']}"
            OutputString += "\n"
    else:
        OutputString += "- There is no experience.\n"
    OutputString += "\n----------------------------------------\n"
    return OutputString

def SaveOutputData(DataOutput, text_filename='PythonCodeOutput.txt'):
    with open(text_filename, 'w') as f:
        for CandidateProfileString in DataOutput:
            f.write(GeneratingOutputString(CandidateProfileString))
            print(GeneratingOutputString(CandidateProfileString))

def main():
    FullCandidatesInformation = FetchData(URL_LINK)
    ProcessedCandidates = [ProcessCandidate(CandidateProfile) for CandidateProfile in FullCandidatesInformation]
    SaveOutputData(ProcessedCandidates)

if __name__ == "__main__":
    main()
