"""Debug script to test LeetCode API"""
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

# Check profile
profile_query = """
query globalData {
    userStatus {
        username
        isSignedIn
    }
}
"""

print('Checking profile...')
resp = session.post('https://leetcode.com/graphql', json={'query': profile_query})
print(f'Profile response: {resp.json()}')

# Try fetching recent submissions using the public query
submission_query = """
query recentSubmissions($username: String!, $limit: Int!) {
    recentSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
        statusDisplay
        lang
    }
}
"""

print('\nFetching recent submissions (public query)...')
resp = session.post('https://leetcode.com/graphql', json={
    'query': submission_query,
    'variables': {'username': 'A2354747489', 'limit': 10}
})
print(f'Submissions response: {json.dumps(resp.json(), indent=2)}')

# Try the authenticated submissions endpoint
auth_query = """
query submissionList($offset: Int!, $limit: Int!) {
    submissionList(offset: $offset, limit: $limit) {
        lastKey
        hasNext
        submissions {
            id
            title
            titleSlug
            status
            statusDisplay
            lang
            runtime
            timestamp
        }
    }
}
"""

print('\nFetching submissions (authenticated query, all statuses)...')
resp = session.post('https://leetcode.com/graphql', json={
    'query': auth_query,
    'variables': {'offset': 0, 'limit': 20}
})
print(f'Response: {json.dumps(resp.json(), indent=2)}')
