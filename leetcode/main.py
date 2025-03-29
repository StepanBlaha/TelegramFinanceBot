import requests
import json

url = "https://leetcode.com/graphql"
user="stepa15"
payload = "{\"query\":\"query userProblemsSolved($username: String!) {\\r\\n    allQuestionsCount {    \\r\\n        difficulty    \\r\\n        count  \\r\\n        }\\r\\n        matchedUser(username: $username) {\\r\\n            problemsSolvedBeatsStats { \\r\\n                difficulty\\r\\n                percentage    \\r\\n                }\\r\\n        submitStatsGlobal {\\r\\n            acSubmissionNum {        \\r\\n                difficulty        \\r\\n                count      \\r\\n                    }    \\r\\n                }  \\r\\n            }             \\r\\n        }\\r\\n\",\"variables\":{\"username\":\""+user+"\"}}"
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=s1TjMN2e7xkhPW220rf6gnzYKvuB4UGuivOpPLv4vPwAH7wkelCSWgN6qvuowUsp'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
