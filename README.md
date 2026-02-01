# Farm Price Intel - Local Language Alert

A multilingual agricultural commodity price tracking application with offline support. Get real-time trusted prices in English or Hindi, accessible to farmers even without internet connectivity.

## 🌾 Features

- **Multilingual Support**: Display prices in English or Hindi
- **Trust-Weighted Pricing**: Prices calculated using weighted average from trusted sources
- **Offline Access**: Cache prices locally for offline viewing
- **Real-time Updates**: Fetch current prices when online
- **Error Handling**: Clear error messages for invalid inputs or network issues
- **Mobile Responsive**: Works on phones, tablets, and desktops
- **No Dependencies**: Frontend uses vanilla JavaScript, backend uses lightweight Flask

## 📁 Project Structure

```
AG-3-Farm-Price-Intel/
├── backend/
│   ├── app.py              # Flask API server
│   ├── price_logic.py      # Price calculation engine
│   ├── db.py               # SQLite caching
│   ├── clean_data.py       # Data cleaning utilities
│   ├── add_data.py         # Data import utilities
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # UI structure
│   ├── app.js              # Main application logic
│   ├── lang.js             # Multilingual messages
│   ├── offline-db.js       # localStorage cache
│   └── style.css           # Styling
├── data/
│   ├── raw/
│   │   └── mandi_prices.csv    # Raw price data
│   └── processed/
│       └── cleaned_prices.csv  # Cleaned data
├── demo/
│   └── demo-flow.md        # Demo walkthrough
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Web browser (for frontend)

### Installation

1. **Clone or extract the project**
   ```bash
   cd "AG-3-Farm-Price-Intel with local language alert"
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```
   Server runs on `http://127.0.0.1:5000`

2. **Open the frontend in your browser**
   - Open `frontend/index.html` with a local HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   - Visit `http://localhost:8000`
   
   OR simply open with double-click (file protocol will work but with limited features)

3. **Use the app**
   - Select a language (English/Hindi)
   - Enter a crop name
   - Enter a market name
   - Press Enter or click Update
   - View the trusted price range

## 📊 Valid Crop-Market Combinations

| Crop | Markets |
|------|---------|
| wheat | Agri News, Local Trader |
| soybean | Last Week Avg, Local Village, Some Market |
| rice | APMC Market |
| cotton | Cotton News |
| tomato | APMC Market |
| onion | Local Trader |

## 🔌 API Documentation

### GET `/price`

Fetch trusted price range for a crop-market combination.

**Parameters:**
- `crop` (required): Crop name (lowercase)
- `market` (required): Market name (lowercase)

**Example Request:**
```
GET http://127.0.0.1:5000/price?crop=wheat&market=Agri%20News
```

**Success Response (200):**
```json
[
  {
    "crop": "wheat",
    "market": "Agri News",
    "price": 2150,
    "min": 2100,
    "max": 2200
  }
]
```

**Error Responses:**
- **400**: Missing crop or market parameter
- **404**: Crop-market combination not found
- **500**: Server error

## 💾 Caching Strategy

The app uses **dual-layer caching**:

1. **SQLite Database** (backend):
   - Stores price data for faster retrieval
   - Auto-initialized on first run
   - Located at `backend/prices.db`

2. **localStorage** (frontend):
   - Stores prices in browser for offline access
   - Automatically updated when fetching new prices
   - Survives browser refresh

## 🌐 Offline Mode

1. **Fetch prices online** - Prices are cached automatically
2. **Go offline** - Disconnect internet or toggle offline mode
3. **Fetch again** - App checks offline cache
4. **If cached**: Shows stored price with language translation
5. **If not cached**: Shows error message to fetch online first

## 🎨 UI/UX Features

- **Language Toggle**: Switch between English and Hindi anytime
- **Loading State**: Visual feedback while fetching data
- **Error Display**: Clear red background for errors
- **Enter Key Support**: Press Enter on either input field to fetch
- **Accessibility**: ARIA labels and screen reader support
- **Mobile Responsive**: Meta viewport for mobile devices

## 📝 Multilingual Messages

Messages available in English and Hindi:

| Key | English | Hindi |
|-----|---------|-------|
| `price_range` | "Price range: ₹{min} - ₹{max}" | "कीमत सीमा: ₹{min} - ₹{max}" |
| `offline_error` | "Offline and no cached data" | "ऑफलाइन और कोई कैश्ड डेटा नहीं है" |
| `invalid_input` | "Enter crop and market" | "फसल और बाजार दर्ज करें" |

See `frontend/lang.js` for all available messages.

## 🔍 Data Processing

### Price Calculation
Prices are calculated using **weighted average**:
- Each data source has a trust score (0-1)
- Prices weighted by trust scores
- Result is the weighted average price
- Min/Max calculated from actual data, not hardcoded

### Data Flow
```
mandi_prices.csv → clean_data.py → cleaned_prices.csv → price_logic.py → API → Frontend
```

## 🛠️ Technology Stack

**Backend:**
- Flask (Python web framework)
- SQLite (Data caching)
- Pandas (Data processing)

**Frontend:**
- Vanilla JavaScript (No frameworks)
- HTML5 (Semantic structure)
- CSS3 (Responsive styling)
- localStorage (Offline caching)

## 📋 Error Handling

The app handles:
- Missing or invalid input parameters
- Network disconnections
- Invalid crop-market combinations
- Corrupted cache data
- Database connection failures
- JSON parsing errors

All errors show user-friendly messages in the selected language.

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| CORS error | Make sure backend is running on `http://127.0.0.1:5000` |
| 404 Not Found | Check crop/market spelling and case (must be lowercase) |
| No cached data | First fetch a price online before going offline |
| Data not updating | Restart backend server and refresh browser |
| Database locked | Delete `backend/prices.db` and restart app |

## 📞 Demo Flow

See [demo-flow.md](demo/demo-flow.md) for a complete walkthrough of:
- Online mode (real-time price fetching)
- Offline mode (cached data access)
- Error scenarios and handling
- Feature highlights

## 📄 License

This project is created for educational and agricultural support purposes.

## 👨‍💻 Development

### Backend Development
```bash
cd backend
python app.py  # Runs on http://127.0.0.1:5000
```

### Frontend Development
```bash
cd frontend
python -m http.server 8000  # Runs on http://localhost:8000
```

### Running Tests
```bash
cd backend
python -m pytest  # If tests are added
```

## 📌 Notes

- Always use **lowercase** for crop and market names
- Prices are in **Indian Rupees (₹)**
- Trust scores are between **0 and 1** (higher = more trusted)
- All timestamps are in **IST (Indian Standard Time)**

---

**For detailed demo instructions, see [demo/demo-flow.md](demo/demo-flow.md)**
