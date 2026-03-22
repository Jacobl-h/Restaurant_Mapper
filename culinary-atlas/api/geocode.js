// api/geocode.js
// Vercel serverless function — proxies Google Geocoding API.
// Your GOOGLE_API_KEY env var is set in Vercel dashboard and never sent to the browser.

export default async function handler(req, res) {
  // CORS — only allow same origin in production; open for local dev
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { address } = req.query;
  if (!address) return res.status(400).json({ error: 'address param required' });

  const key = process.env.GOOGLE_API_KEY;
  if (!key) return res.status(500).json({ error: 'API key not configured on server' });

  try {
    const url = `https://maps.googleapis.com/maps/api/geocode/json`
      + `?address=${encodeURIComponent(address)}&key=${key}`;

    const upstream = await fetch(url);
    const data = await upstream.json();

    if (data.status !== 'OK') {
      return res.status(400).json({ error: data.status, message: data.error_message });
    }

    const loc = data.results[0].geometry.location;
    return res.status(200).json({
      lat:          loc.lat,
      lng:          loc.lng,
      display_name: data.results[0].formatted_address,
    });
  } catch (err) {
    return res.status(500).json({ error: 'upstream_error', message: err.message });
  }
}
