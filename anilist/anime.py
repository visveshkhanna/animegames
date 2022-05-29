import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

url = 'https://graphql.anilist.co'


def anime_inline(search):
    query = '''
      query ($query: String, $page: Int, $perpage: Int) {
        Page(page: $page, perPage: $perpage) {
          pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
          }
          media(search: $query, type: ANIME) {
            id
            title {
              romaji
              english
              native
            }
            coverImage {
              large
            }
            averageScore
            popularity
            episodes
            season
            hashtag
            isAdult
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
        id = response["media"][i]["id"]
        title = response["media"][i]["title"]["romaji"]
        keyboard.append(
            [
                InlineKeyboardButton(text=title, callback_data=f"ani {id}")
            ]
        )
    return InlineKeyboardMarkup(keyboard)


def get_anime(id):
    query = '''
    query ($id: Int) {
    Media(id: $id, type: ANIME) {
      title {
        romaji
        native
      }
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      staff {
        edges {
          node {
            name {
              full
            }
          }
        }
      }
      studios {
        edges {
          node {
            name
          }
        }
      }
      source
      popularity
      genres
      duration
      format
      isAdult
      status
      episodes
      season
      description
      averageScore
      genres
    }
  }
  '''
    variables = {
        'id': id,
    }
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    return response.json()
