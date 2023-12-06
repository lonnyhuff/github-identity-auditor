import requests
import sys
import json
from prettytable import PrettyTable

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

    # Initialize table for output
    table = PrettyTable()
    table.field_names = ["Login", "SAML Name ID", "SCIM Username"]

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
        
        # Process and add user data to table
        for edge in organization_data['edges']:
            user = edge['node']
            
            # Handling potential None values
            user_login = user['user']['login'] if user['user'] else 'None'
            saml_name_id = user['samlIdentity']['nameId'] if user['samlIdentity'] and user['samlIdentity']['nameId'] else 'None'
            scim_username = user['scimIdentity']['username'] if user['scimIdentity'] else 'None'

            table.add_row([user_login, saml_name_id, scim_username])

        # Update cursor for next page
        has_next_page = organization_data['pageInfo']['hasNextPage']
        cursor = organization_data['pageInfo']['endCursor']

    # Print the table after all data is fetched
    print(table)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <organization_name> <personal_access_token>")
        sys.exit(1)

    org_name = sys.argv[1]
    personal_access_token = sys.argv[2]
    fetch_linked_users(org_name, personal_access_token)
