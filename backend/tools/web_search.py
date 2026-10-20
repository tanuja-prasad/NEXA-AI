from ddgs import DDGS


def web_search(query, max_results=5):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=max_results
        )

        for result in search_results:

            results.append({
                "title": result.get("title", ""),
                "body": result.get("body", ""),
                "href": result.get("href", "")
            })

    return results