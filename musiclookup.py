import musicbrainzngs

musicbrainzngs.set_useragent("musiclookup", "0.0", contact=None)
# musicbrainzngs.set_hostname("musicbrainz-mirror.eu:5000")

def get_all_releases_from_artist(s_artist_id):
    limit = 100
    offset = 0
    page = 1
    # d_search_parameters = dict(artist=s_artist_id, release_type=["album"])
    d_search_parameters = dict(artist=s_artist_id, limit=limit)

    first_page = musicbrainzngs.browse_releases(**d_search_parameters)
    page_releases = first_page['release-list']

    yield from ({"title": albums["title"], "date": albums["date"]} for albums in page_releases)

    while len(page_releases) >= limit:
        offset += limit
        page += 1
        print("fetching page number %d.." % page)
        next_page = musicbrainzngs.browse_releases(offset=offset, **d_search_parameters)
        page_releases = next_page['release-list']
        yield from ({"title": albums["title"], "date": albums["date"]} for albums in page_releases if
                    "date" in albums and "title" in albums)


result = musicbrainzngs.search_artists(artist="aerosmith", type="group", strict=True)
for artist in result['artist-list']:
    print("{id} {name}".format(**artist))

    for album in get_all_releases_from_artist(artist["id"]):
        print(album)
