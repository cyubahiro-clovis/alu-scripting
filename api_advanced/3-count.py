#!/usr/bin/python3
"""Count keywords in the titles of a subreddit's hot posts."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of the keywords found in hot post titles."""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return
    data = response.json().get("data", {})
    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for token in title.lower().split():
            if token in counts:
                counts[token] += 1
    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, counts)
    totals = {}
    for word in word_list:
        word = word.lower()
        totals[word] = totals.get(word, 0) + counts.get(word, 0)
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    for word, total in ranked:
        if total > 0:
            print("{}: {}".format(word, total))
