import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

url = 'https://graphql.anilist.co'

def character_inline(search):
    query = '''
    query ($query: String, $page: Int, $perpage: Int) {
        Page(page: $page, perPage: $perpage) {
            pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            }
            characters(search: $query) {
                id
                name {
                    first
                    last
                }
            }
        }
    }
    '''
    c = 0
    variables = {
    'query': search,
    }
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    response = response.json()["data"]["Page"]
    count = response["pageInfo"]["total"]
    keyboard = []
    for i in range(count):
        if c == 6:
            break
        c += 1
        id = response["characters"][i]["id"]
        name = f'{response["characters"][i]["name"]["first"]} {response["characters"][i]["name"]["last"]}'
        keyboard.append(
            [
                InlineKeyboardButton(text=name, callback_data=f"chr {id}")
            ]
        )
    return InlineKeyboardMarkup(keyboard)

def get_character(id):
    query = '''
        query ($id: Int) {
            Character(id: $id) {
                name {
                    full
                    native
                    alternative
                }
                description
                age
                gender
                dateOfBirth {
                    year
                    month
                    day
                }
                image {
                    large
                }
            }
        }
    '''
    variables = {
        'id': id,
    }
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    return response.json()
