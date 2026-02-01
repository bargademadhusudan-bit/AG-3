let currentLang = "en";

const priceBox = document.getElementById("priceBox");
const updateBtn = document.getElementById("updateBtn");
const langSelect = document.getElementById("language");
const cropInput = document.getElementById("cropInput");
const marketInput = document.getElementById("marketInput");

langSelect.addEventListener("change", e => {
  currentLang = e.target.value;
});

updateBtn.addEventListener("click", fetchPrice);

// Support Enter key for both input fields
cropInput.addEventListener("keypress", e => {
  if (e.key === "Enter") fetchPrice();
});

marketInput.addEventListener("keypress", e => {
  if (e.key === "Enter") fetchPrice();
});

function fetchPrice() {
  const crop = cropInput.value.trim().toLowerCase();
  const market = marketInput.value.trim().toLowerCase();

  if (!crop || !market) {
    showError("Enter crop and market.");
    return;
  }

  if (!navigator.onLine) {
    const cached = loadFromCache(crop, market);
    if (cached) return showPrice(cached);
    showError("Offline and no cached data.");
    return;
  }

  showLoading();
  updateBtn.disabled = true;

  fetch(`http://127.0.0.1:5000/price?crop=${crop}&market=${market}`)
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(data => {
      if (data.error) {
        showError(data.error);
        return;
      }
      saveToCache(crop, market, data);
      showPrice(data);
    })
    .catch(err => {
      showError(`Error: ${err.message}`);
    })
    .finally(() => {
      updateBtn.disabled = false;
    });
}

function showPrice(data) {
  if (!data || data.error) {
    showError(data?.error || "Error fetching price.");
    return;
  }
  
  if (!Array.isArray(data) || !data[0]) {
    showError("Invalid data format.");
    return;
  }
  
  const item = data[0];
  
  // Use min/max from API response, fallback to ±50 if not available
  const min = item.min !== undefined ? item.min : (item.price - 50);
  const max = item.max !== undefined ? item.max : (item.price + 50);
  
  const message = getMessage(currentLang, "price_range", {
    min: min,
    max: max
  });
  
  priceBox.innerText = message;
  priceBox.className = "sms-alert success";
}

function showError(message) {
  priceBox.innerText = message;
  priceBox.className = "sms-alert error";
}

function showLoading() {
  priceBox.innerText = "Loading...";
  priceBox.className = "sms-alert loading";
}
