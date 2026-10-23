# Market data API adapter

The UI calls the `MarketDataService` interface in `src/stocks/marketData.ts`. Set `VITE_USE_MOCK_DATA=false` and configure `VITE_MARKET_API_BASE_URL` / `VITE_MARKET_API_KEY` to select the HTTP adapter. Keep provider response mapping inside that adapter so screens retain the internal types.

Expected REST routes and response shapes:

| Request | Response |
| --- | --- |
| `GET /stocks?sector=&capBucket=&sort=&q=` | `StockSummary[]` |
| `GET /stocks/:symbol` | `StockSummary` |
| `GET /stocks/:symbol/history?range=1D\|1W\|1M\|3M\|6M\|1Y\|3Y\|5Y` | `PricePoint[]` |
| `GET /stocks/:symbol/performance` | `DayPerformance` |
| `GET /stocks/:symbol/delivery?period=daily\|weekly\|monthly` | `DeliveryVolume` |
| `GET /stocks/:symbol/indicators?range=&type=SMA\|EMA&period=` | `MovingAverageSeries[]` |
| `GET /stocks/:symbol/news?limit=&cursor=` | `{ items: NewsItem[], nextCursor?: string }` |
| `GET /stocks/:symbol/events` | `StockEvent[]` |
| `GET /stocks/:symbol/fundamentals` | `Fundamentals` |
| `GET /stocks/:symbol/financials` | `FinancialPerformance` |

The adapter sends the API key in `X-API-Key`. Never commit actual credentials. Public Vite environment values are included in the browser bundle, so a production secret should be held and forwarded by a server-side proxy.
