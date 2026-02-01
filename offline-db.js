function saveToCache(crop, market, data) {
  try {
    localStorage.setItem(`price_${crop}_${market}`, JSON.stringify(data));
  } catch (err) {
    console.error("Cache save error:", err);
  }
}

function loadFromCache(crop, market) {
  try {
    const d = localStorage.getItem(`price_${crop}_${market}`);
    return d ? JSON.parse(d) : null;
  } catch (err) {
    console.error("Cache load error:", err);
    return null;
  }
}
