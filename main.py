import requests
import sys
import json

def fetch_linked_users(org, token):
    """
    Fetches and prints all linked user identities in a specified GitHub organization.

    Args:
    org (str): The GitHub organization name.
    token (str): Personal access token for GitHub API authorization.
    """
    # GraphQL query to fetch linked identities with pagination
    query = """
    query($org: String!, $cursor: String) {
      organization(login: $org) {
        samlIdentityProvider {
          externalIdentities(first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                user {
                  login
                }
                samlIdentity {
                  nameId
                }
                scimIdentity {
                  username
                }
              }
            }
          }
        }
      }
    }
    """

    # Endpoint for GitHub's GraphQL API
    url = "https://api.github.com/graphql"
    # Headers for authorization and content type
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # Initialize pagination
    has_next_page = True
    cursor = None

    # Loop through pages of results
    while has_next_page:
        variables = {"org": org, "cursor": cursor}
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
        
        # Check for request failure
        if response.status_code != 200:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

        data = response.json()
        organization_data = data['data']['organization']['samlIdentityProvider']['externalIdentities']
        
        # Process and print user data
        for edge in organization_data['edges']:
            user = edge['node']
            print(f"Login: {user['user']['login']}, SAML Name ID: {user['samlIdentity']['nameId']}, SCIM Username: {user['scimIdentity']['username']}")

        # Update cursor for next page
        has_next_page = organization_data['pageInfo']['hasNextPage']
        cursor = organization_data['pageInfo']['endCursor']

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <organization_name> <personal_access_token>")
        sys.exit(1)

    org_name = sys.argv[1]
    personal_access_token = sys.argv[2]
    fetch_linked_users(org_name, personal_access_token)
