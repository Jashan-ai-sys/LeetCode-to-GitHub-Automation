"""Test submission details fetch"""
import json
import requests

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

# Test getting submission details
query = """
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

print('Testing submission details for ID 1910968967...')
resp = session.post('https://leetcode.com/graphql', json={
    'query': query,
    'variables': {'submissionId': 1910968967}
})
print(json.dumps(resp.json(), indent=2))
