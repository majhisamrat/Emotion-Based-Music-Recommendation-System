from recommendation.emotion_mapping import EMOTION_TO_MOOD
from recommendation.spotify_client import get_spotify_client



MOOD_SEARCH_QUERY = {
    "happy": "happy upbeat pop playlist",
    "sad": "sad emotional songs playlist",
    "angry": "intense rock metal playlist",
    "fear": "calm ambient focus music playlist",
    "calm": "calm relaxing study music playlist"
}


def recommend_playlist_with_tracks(emotion, track_limit=10):
    sp = get_spotify_client()


    mood = EMOTION_TO_MOOD.get(emotion)
    if not mood:
        return None

    # Search playlist
    search_query = MOOD_SEARCH_QUERY.get(
    emotion.lower(),
    mood["genres"][0] + " music playlist"
    )

    search_result = sp.search(
    q=search_query,
    type="playlist",
    limit=5
    )

    playlists = search_result.get("playlists", {}).get("items", [])

    playlist = None
    for p in playlists:
        if p and p.get("id"):
            playlist = p
            break

    if playlist is None:
        return None

    playlist_id = playlist["id"]

    try:
        tracks_data = sp.playlist_items(playlist_id, limit=track_limit)
    except Exception:
        return None

    track_items = tracks_data.get("items", [])
    if not track_items:
        return None

    tracks = []
    for item in track_items:
        track = item.get("track")
        if not track:
            continue

        tracks.append({
            "track_name": track.get("name"),
            "artist": track.get("artists", [{}])[0].get("name"),
            "album_image": (
                track.get("album", {}).get("images", [{}])[0].get("url")
                if track.get("album", {}).get("images")
                else None
            ),
            "track_url": track.get("external_urls", {}).get("spotify")
        })

    if not tracks:
        return None

    return {
        "playlist_name": playlist.get("name"),
        "playlist_url": playlist.get("external_urls", {}).get("spotify"),
        "tracks": tracks
    }
