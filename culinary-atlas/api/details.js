// api/details.js
// Fetches full Google Place Details for a single place_id.
// Called lazily when a user clicks a map marker — keeps initial load fast.

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const key = process.env.GOOGLE_API_KEY;
  if (!key) return res.status(500).json({ error: 'API key not configured on server' });

  const { place_id } = req.query;
  if (!place_id) return res.status(400).json({ error: 'place_id param required' });

  const fields = [
    'name', 'rating', 'user_ratings_total', 'price_level',
    'formatted_address', 'formatted_phone_number',
    'website', 'opening_hours', 'editorial_summary',
    'reviews', 'types', 'serves_beer', 'serves_wine',
    'reservable', 'delivery', 'dine_in', 'takeout',
  ].join(',');

  try {
    const url = `https://maps.googleapis.com/maps/api/place/details/json`
      + `?place_id=${encodeURIComponent(place_id)}`
      + `&fields=${fields}`
      + `&key=${key}`;

    const upstream = await fetch(url);
    const data = await upstream.json();

    if (data.status !== 'OK') {
      return res.status(400).json({ error: data.status });
    }

    const r = data.result;
    return res.status(200).json({
      name:             r.name,
      rating:           r.rating           ?? null,
      review_count:     r.user_ratings_total ?? 0,
      price_level:      r.price_level       ?? null,
      address:          r.formatted_address ?? '',
      phone:            r.formatted_phone_number ?? '',
      website:          r.website           ?? '',
      hours:            r.opening_hours?.weekday_text ?? [],
      open_now:         r.opening_hours?.open_now     ?? null,
      summary:          r.editorial_summary?.overview ?? '',
      types:            r.types             ?? [],
      reservable:       r.reservable        ?? null,
      delivery:         r.delivery          ?? null,
      dine_in:          r.dine_in           ?? null,
      takeout:          r.takeout           ?? null,
    });
  } catch (err) {
    return res.status(500).json({ error: 'upstream_error', message: err.message });
  }
}
