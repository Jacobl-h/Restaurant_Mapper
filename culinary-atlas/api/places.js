// api/places.js
// Vercel serverless function — proxies Google Places API (Nearby Search + Details).
// Handles one page of results per call; the client drives pagination via pagetoken.

const ALLOWED_TYPES = [
  'restaurant', 'cafe', 'bar', 'bakery', 'meal_delivery', 'meal_takeaway',
];

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const key = process.env.GOOGLE_API_KEY;
  if (!key) return res.status(500).json({ error: 'API key not configured on server' });

  const { lat, lng, radius, pagetoken } = req.query;

  try {
    let url;

    if (pagetoken) {
      // Subsequent pages — only the token is needed
      url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json`
        + `?pagetoken=${encodeURIComponent(pagetoken)}&key=${key}`;
    } else {
      if (!lat || !lng || !radius) {
        return res.status(400).json({ error: 'lat, lng, radius params required' });
      }
      // rankby=prominence surfaces the most-reviewed places first
      url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json`
        + `?location=${lat},${lng}`
        + `&radius=${radius}`
        + `&type=restaurant`
        + `&rankby=prominence`
        + `&key=${key}`;
    }

    const upstream = await fetch(url);
    const data = await upstream.json();

    if (data.status !== 'OK' && data.status !== 'ZERO_RESULTS') {
      return res.status(400).json({ error: data.status, message: data.error_message });
    }

    // Shape each result — only send what the frontend needs
    const results = (data.results || []).map(place => ({
      place_id:     place.place_id,
      name:         place.name,
      lat:          place.geometry.location.lat,
      lng:          place.geometry.location.lng,
      rating:       place.rating       ?? null,
      review_count: place.user_ratings_total ?? 0,
      price_level:  place.price_level  ?? null,
      types:        place.types         ?? [],
      vicinity:     place.vicinity      ?? '',
      open_now:     place.opening_hours?.open_now ?? null,
      photo_ref:    place.photos?.[0]?.photo_reference ?? null,
    }));

    return res.status(200).json({
      results,
      next_page_token: data.next_page_token ?? null,
      status: data.status,
    });
  } catch (err) {
    return res.status(500).json({ error: 'upstream_error', message: err.message });
  }
}
