import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-datasets-mcp")

# Initialize FastMCP server
mcp = FastMCP("financial-datasets")

# Constants
FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"


# Helper function to make API requests
async def make_request(url: str) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch income statements or no income statements found."

    # Extract the income statements
    income_statements = data.get("income_statements", [])

    # Check if income statements are found
    if not income_statements:
        return "Unable to fetch income statements or no income statements found."

    # Stringify the income statements
    return json.dumps(income_statements, indent=2)


@mcp.tool()
async def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get balance sheets for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the balance sheet (e.g. annual, quarterly, ttm)
        limit: Number of balance sheets to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Extract the balance sheets
    balance_sheets = data.get("balance_sheets", [])

    # Check if balance sheets are found
    if not balance_sheets:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Stringify the balance sheets
    return json.dumps(balance_sheets, indent=2)


@mcp.tool()
async def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get cash flow statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
        limit: Number of cash flow statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Extract the cash flow statements
    cash_flow_statements = data.get("cash_flow_statements", [])

    # Check if cash flow statements are found
    if not cash_flow_statements:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Stringify the cash flow statements
    return json.dumps(cash_flow_statements, indent=2)


@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch news or no news found."

    # Extract the news
    news = data.get("news", [])

    # Check if news are found
    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)


@mcp.tool()
async def get_available_crypto_tickers() -> str:
    """
    Gets all available crypto tickers.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch available crypto tickers or no available crypto tickers found."

    # Extract the available crypto tickers
    tickers = data.get("tickers", [])

    # Stringify the available crypto tickers
    return json.dumps(tickers, indent=2)


@mcp.tool()
async def get_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """
    Gets historical prices for a crypto currency.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_historical_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical prices for a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_current_crypto_price(ticker: str) -> str:
    """Get the current / latest price of a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


# ------------------- NEW TOOLS: Financial Statements & Metrics -------------------

@mcp.tool()
async def get_all_financial_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
    cik: str = None,
) -> str:
    """Get all financial statements (income, balance, cash flow) for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the statements (e.g. annual, quarterly, ttm)
        limit: Number of statements to return (default: 4)
        cik: Central Index Key (optional)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/?ticker={ticker}&period={period}&limit={limit}"
    if cik:
        url += f"&cik={cik}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch financial statements or no data found."
    financials = data.get("financials", {})
    if not financials:
        return "Unable to fetch financial statements or no data found."
    return json.dumps(financials, indent=2)


@mcp.tool()
async def get_segmented_revenues(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
    cik: str = None,
) -> str:
    """Get segmented revenue data for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the statements (annual or quarterly)
        limit: Number of statements to return (default: 4)
        cik: Central Index Key (optional)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/segmented-revenues/?ticker={ticker}&period={period}&limit={limit}"
    if cik:
        url += f"&cik={cik}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch segmented revenues or no data found."
    segmented_revenues = data.get("segmented_revenues", [])
    if not segmented_revenues:
        return "Unable to fetch segmented revenues or no data found."
    return json.dumps(segmented_revenues, indent=2)


@mcp.tool()
async def search_financials_by_filters(
    filters: list,
    period: str = "ttm",
    limit: int = 100,
    currency: str = None,
) -> str:
    """Search for companies based on financial filters.

    Args:
        filters: List of filter dicts (field, operator, value)
        period: Period (annual, quarterly, ttm)
        limit: Max results (default: 100)
        currency: Currency (optional, e.g. USD)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/search"
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key
    headers["Content-Type"] = "application/json"
    body = {
        "filters": filters,
        "period": period,
        "limit": limit,
    }
    if currency:
        body["currency"] = currency
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return f"Error searching financials: {str(e)}"
    search_results = data.get("search_results", [])
    if not search_results:
        return "No search results found."
    return json.dumps(search_results, indent=2)


@mcp.tool()
async def search_financials_by_line_items(
    tickers: list,
    line_items: list,
    period: str = "ttm",
    limit: int = 1,
) -> str:
    """Search for specific line items for a list of tickers.

    Args:
        tickers: List of ticker symbols
        line_items: List of line item keys
        period: Period (annual, quarterly, ttm)
        limit: Max results per ticker (default: 1)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/search/line-items"
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key
    headers["Content-Type"] = "application/json"
    body = {
        "tickers": tickers,
        "line_items": line_items,
        "period": period,
        "limit": limit,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return f"Error searching line items: {str(e)}"
    search_results = data.get("search_results", [])
    if not search_results:
        return "No search results found."
    return json.dumps(search_results, indent=2)


@mcp.tool()
async def get_financial_metrics(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get historical financial metrics for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period (annual, quarterly, ttm)
        limit: Number of periods to return (default: 4)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financial-metrics/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch financial metrics or no data found."
    # The API may return a list or a dict; return as-is
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_financial_metrics_snapshot(
    ticker: str,
) -> str:
    """Get a real-time snapshot of key financial metrics for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financial-metrics/snapshot/?ticker={ticker}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch financial metrics snapshot or no data found."
    # The API may return a dict; return as-is
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_company_facts(
    ticker: str = None,
    cik: str = None,
) -> str:
    """Get company facts (name, CIK, market cap, etc.) for a company.

    Args:
        ticker: Ticker symbol of the company (optional)
        cik: Central Index Key (optional)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/company/facts?"
    params = []
    if ticker:
        params.append(f"ticker={ticker}")
    if cik:
        params.append(f"cik={cik}")
    url += "&".join(params)
    data = await make_request(url)
    if not data:
        return "Unable to fetch company facts or no data found."
    company_facts = data.get("company_facts", {})
    if not company_facts:
        return "Unable to fetch company facts or no data found."
    return json.dumps(company_facts, indent=2)


@mcp.tool()
async def get_sec_filings(
    ticker: str = None,
    cik: str = None,
    filing_type: str = None,
) -> str:
    """Get SEC filings for a company.

    Args:
        ticker: Ticker symbol of the company (optional)
        cik: Central Index Key (optional)
        filing_type: Type of filing (e.g. 10-K, 10-Q, 8-K, 4, 144) (optional)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings?"
    params = []
    if ticker:
        params.append(f"ticker={ticker}")
    if cik:
        params.append(f"cik={cik}")
    if filing_type:
        params.append(f"filing_type={filing_type}")
    url += "&".join(params)
    data = await make_request(url)
    if not data:
        return "Unable to fetch SEC filings or no data found."
    filings = data.get("filings", [])
    if not filings:
        return "Unable to fetch SEC filings or no data found."
    return json.dumps(filings, indent=2)


@mcp.tool()
async def get_sec_filing_items(
    ticker: str,
    filing_type: str,
    year: int,
    quarter: int = None,
    item: list = None,
) -> str:
    """Get specific items/sections from a SEC filing.

    Args:
        ticker: Ticker symbol of the company (required)
        filing_type: Type of filing (10-K or 10-Q) (required)
        year: Year of the filing (required)
        quarter: Quarter of the filing if 10-Q (optional)
        item: List of item numbers to extract (optional, e.g. ["Item-1", "Item-7A"])
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings/items?ticker={ticker}&filing_type={filing_type}&year={year}"
    if quarter:
        url += f"&quarter={quarter}"
    if item:
        for i in item:
            url += f"&item={i}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch filing items or no data found."
    items = data.get("items", [])
    if not items:
        return "Unable to fetch filing items or no data found."
    return json.dumps(items, indent=2)


@mcp.tool()
async def get_insider_trades(
    ticker: str,
    limit: int = 100,
    filing_date_lte: str = None,
    filing_date_gte: str = None,
) -> str:
    """Get insider trades for a ticker.

    Args:
        ticker: Ticker symbol of the company (required)
        limit: Number of trades to return (default: 100)
        filing_date_lte: End date for filings (optional, format YYYY-MM-DD)
        filing_date_gte: Start date for filings (optional, format YYYY-MM-DD)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/insider-trades?ticker={ticker}&limit={limit}"
    if filing_date_lte:
        url += f"&filing_date_lte={filing_date_lte}"
    if filing_date_gte:
        url += f"&filing_date_gte={filing_date_gte}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch insider trades or no data found."
    insider_trades = data.get("insider_trades", [])
    if not insider_trades:
        return "Unable to fetch insider trades or no data found."
    return json.dumps(insider_trades, indent=2)


@mcp.tool()
async def get_institutional_ownership(
    ticker: str = None,
    investor: str = None,
    limit: int = 10,
    report_period_lte: str = None,
    report_period_gte: str = None,
) -> str:
    """Get institutional ownership by ticker or investor.

    Args:
        ticker: Ticker symbol (optional)
        investor: Investor name (optional)
        limit: Number of results to return (default: 10)
        report_period_lte: End date for report period (optional, format YYYY-MM-DD)
        report_period_gte: Start date for report period (optional, format YYYY-MM-DD)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/institutional-ownership?"
    params = []
    if ticker:
        params.append(f"ticker={ticker}")
    if investor:
        params.append(f"investor={investor}")
    params.append(f"limit={limit}")
    if report_period_lte:
        params.append(f"report_period_lte={report_period_lte}")
    if report_period_gte:
        params.append(f"report_period_gte={report_period_gte}")
    url += "&".join(params)
    data = await make_request(url)
    if not data:
        return "Unable to fetch institutional ownership or no data found."
    institutional_ownership = data.get("institutional_ownership", [])
    if not institutional_ownership:
        return "Unable to fetch institutional ownership or no data found."
    return json.dumps(institutional_ownership, indent=2)


@mcp.tool()
async def get_earnings_press_releases(
    ticker: str,
) -> str:
    """Get earnings press releases for a ticker.

    Args:
        ticker: Ticker symbol of the company (required)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/earnings/press-releases?ticker={ticker}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch earnings press releases or no data found."
    press_releases = data.get("press_releases", [])
    if not press_releases:
        return "Unable to fetch earnings press releases or no data found."
    return json.dumps(press_releases, indent=2)


@mcp.tool()
async def get_options_chain(
    ticker: str,
    strike_price: float = None,
    option_type: str = None,
    expiration_date: str = None,
) -> str:
    """Get real-time options chain data for a ticker.

    Args:
        ticker: Ticker symbol of the company (required)
        strike_price: Strike price (optional)
        option_type: Option type, 'call' or 'put' (optional)
        expiration_date: Expiration date (optional, format YYYY-MM-DD)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/options/chain?ticker={ticker}"
    if strike_price is not None:
        url += f"&strike_price={strike_price}"
    if option_type:
        url += f"&option_type={option_type}"
    if expiration_date:
        url += f"&expiration_date={expiration_date}"
    data = await make_request(url)
    if not data:
        return "Unable to fetch options chain or no data found."
    options_chain = data.get("options_chain", [])
    if not options_chain:
        return "Unable to fetch options chain or no data found."
    return json.dumps(options_chain, indent=2)


@mcp.tool()
async def get_historical_option_prices(
    ticker: str,
    interval: str,
    interval_multiplier: int,
    start_date: str,
    end_date: str,
    limit: int = 5000,
) -> str:
    """Get historical option price data for a ticker.

    Args:
        ticker: Option ticker symbol (required)
        interval: Time interval (required, e.g. minute, day, week)
        interval_multiplier: Multiplier for the interval (required)
        start_date: Start date (required, format YYYY-MM-DD)
        end_date: End date (required, format YYYY-MM-DD)
        limit: Max number of records (default: 5000)
    """
    url = (
        f"{FINANCIAL_DATASETS_API_BASE}/options/?ticker={ticker}"
        f"&interval={interval}"
        f"&interval_multiplier={interval_multiplier}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&limit={limit}"
    )
    data = await make_request(url)
    if not data:
        return "Unable to fetch historical option prices or no data found."
    prices = data.get("prices", [])
    if not prices:
        return "Unable to fetch historical option prices or no data found."
    return json.dumps(prices, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
