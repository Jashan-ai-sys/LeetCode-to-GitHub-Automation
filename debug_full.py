"""Debug full sync process"""
import json
import requests
import time

with open('config.json', 'r') as f:
    config = json.load(f)

session = requests.Session()
session.cookies.set('LEETCODE_SESSION', config['leetcode_session'], domain='.leetcode.com')
session.headers.update({
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com',
    'Origin': 'https://leetcode.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

# Get submissions first
sub_query = """
query submissionList($offset: Int!, $limit: Int!) {
    submissionList(offset: $offset, limit: $limit) {
        submissions {
            id
            title
            titleSlug
            status
            lang
        }
    }
}
"""

print('Fetching submissions...')
resp = session.post('https://leetcode.com/graphql', json={
    'query': sub_query,
    'variables': {'offset': 0, 'limit': 5}
})
data = resp.json()
submissions = data.get('data', {}).get('submissionList', {}).get('submissions', [])
accepted = [s for s in submissions if s.get('status') == 10]

print(f'Found {len(accepted)} accepted submissions')

if accepted:
    sub = accepted[0]
    print(f'\nTrying to fetch code for: {sub["title"]} (ID: {sub["id"]})')
    print(f'ID type: {type(sub["id"])}')
    
    # Fetch details
    detail_query = """
    query submissionDetails($submissionId: Int!) {
        submissionDetails(submissionId: $submissionId) {
            code
            lang {
                name
            }
            question {
                questionId
                title
                difficulty
            }
        }
    }
    """
    
    # Make sure ID is int
    sub_id = int(sub['id'])
    print(f'Converted ID: {sub_id}')
    
    resp = session.post('https://leetcode.com/graphql', json={
        'query': detail_query,
        'variables': {'submissionId': sub_id}
    })
    
    print(f'Response status: {resp.status_code}')
    result = resp.json()
    
    if result.get('data', {}).get('submissionDetails'):
        details = result['data']['submissionDetails']
        print(f'\nSUCCESS!')
        print(f'Problem: {details["question"]["title"]}')
        print(f'Difficulty: {details["question"]["difficulty"]}')
        print(f'Language: {details["lang"]["name"]}')
        print(f'Code preview: {details["code"][:100]}...')
    else:
        print(f'Failed! Response: {json.dumps(result, indent=2)}')
