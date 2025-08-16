import requests
import re

def get_job_list(job_num, query_id):
    url = "https://www.seek.com.au/api/jobsearch/v5/search"

    querystring = {"siteKey":"AU-Main","sourcesystem":"houston","where":"All Australia","page":"1","keywords":"software engineer","pageSize": str(job_num),"solId":query_id,"relatedSearchesCount":"12"}


    response_list = requests.get(url, params= querystring).json()

    unique_job_ID_list = list(set([job["id"] for job in response_list.get("data", [])]))

    print(unique_job_ID_list)

    url = "https://www.seek.com.au/graphql"

    variables = {
        f"jobId{i+1}": unique_job_ID_list[i] for i in range(len(unique_job_ID_list))
    }
    variables.update({
        "jobDetailsViewedCorrelationId": "8",
        "sessionId": "e7"
    })

    #Generate query dynamically
    query_parts = []
    for i in range(len(unique_job_ID_list)):
        query_parts.append(f"""
        job{i+1}: jobDetails( 
            id: $jobId{i+1}
            tracking: {{channel: "WEB", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}})
            {{
                job {{
                    content(platform: WEB)
                }}
            }}"""
        )
    query = f"query jobDetails({', '.join([f'$jobId{i+1}: ID!' for i in range(len(unique_job_ID_list))])}, $jobDetailsViewedCorrelationId: String!, $sessionId: String!) {{" + "\n".join(query_parts) + "\n}"

    json_body = {
        "operationName": "jobDetails",
        "variables": variables,
        "query": query
    }

    res_job_content = requests.post(url, json=json_body)

    #filter for just job content
    content_list = [job_data["job"]["content"] for job_data in res_job_content.json()["data"].values()]

    return content_list

def save_to_file(FILE, data):
    with open(FILE, "w", encoding="utf-8") as f:
        for job in data:
            f.write(f"{job}\n\n")

def clean_content(list_):
    results = []
    
    #remove duplicate job posts
    list_ = list(set(list_))
    
    #remove unnecessary strings used for file format
    for content in list_:
        content = re.sub(r"<[^>]+>", " ", content)
        content = re.sub(r"\s+", " ", content).strip()
        results.append(content)
    return results

# Execute only when this file is executed directly
if __name__ == "__main__":
    # Get job content for 100 jobs with a specific query ID
    job_content_list = get_job_list(100, "f925aed3-9cb9-494b-b629-5a72eb35ec9c")
    cleaned_list = clean_content(job_content_list)
    save_to_file("data/job_text.txt", cleaned_list)