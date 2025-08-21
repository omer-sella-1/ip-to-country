# IP to Country Service

A REST API service that provides IP address geolocation lookup with custom rate limiting and extensible database support.

## Features

- Fast IP address to country/city lookup
- Custom rate limiting (requests per second per client IP)
- Extensible database architecture supporting multiple data sources
- Production-ready Flask application with proper error handling
- Docker containerization support

## Requirements

- Python 3.9+
- Flask web framework
- SQLAlchemy for database operations
- SQLite database (automatically created)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ip_to_country_1
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application:
```bash
python -m src.main
```

The service will start on the configured port (default: 8080).

## API Usage

### Find Country by IP

**Endpoint:** `GET /v1/find-country?ip=<ip_address>`

**Example:**
```bash
curl "http://localhost:8080/v1/find-country?ip=2.22.233.255"
```

**Response:**
```json
{
  "country": "France",
  "city": "Paris"
}
```

**Error Responses:**
- `400` - Missing or invalid IP parameter
- `404` - No location found for the provided IP
- `429` - Rate limit exceeded
- `500` - Server error

### Database Statistics

**Endpoint:** `GET /v1/stats`

Returns information about the database including total records and available countries.

### Root Endpoint

**Endpoint:** `GET /`

Simple welcome message to verify the service is running.

## Configuration

Configure the service using environment variables in your `.env` file:

```bash
PORT=8080                            # Server port (Docker uses 8080)
RATE_LIMIT_PER_SECOND=10            # Rate limit per client IP
IP_DATABASE_TYPE=csv                # Database type (currently supports csv)
IP_DATABASE_FILE=data/ip_database.csv  # Path to IP database file
```

## Rate Limiting

The service implements per-client IP rate limiting using a token bucket algorithm:

- Each client IP has an independent rate limit bucket
- Tokens refill continuously at the configured rate
- Requests are blocked when tokens are exhausted
- Returns HTTP 429 when rate limit is exceeded

## Database Support

The service uses an extensible ETL (Extract, Transform, Load) system that can support multiple data sources:

### Current Support
- CSV files with columns: `start_ip`, `end_ip`, `country`, `city`

### Adding New Data Sources

The factory pattern makes it easy to add new data source types:

1. Create a new extractor in `src/etl/extractors/`
2. Add it to the `ExtractorFactory` registry
3. Update your environment configuration

Example CSV format (from actual `data/ip_database.csv`):
```csv
start_ip,end_ip,country,city
1.0.0.0,1.255.255.255,Australia,Sydney
2.0.0.0,2.255.255.255,France,Paris
8.8.8.0,8.8.8.255,United States,Mountain View
```

## Development

### Project Structure

```
src/
├── main.py                 # Application entry point
├── app.py                  # Flask app factory
├── startup.py              # Database initialization
├── config.py               # Configuration management
├── blueprints/             # Flask blueprints
│   ├── core_routes.py      # Core API routes
│   └── ip_routes.py        # IP lookup routes
├── models/                 # Database models
│   ├── database.py         # Database configuration
│   └── ip_location.py      # IP location model
├── repositories/           # Data access layer
│   └── ip_location_repository.py
├── services/               # Business services
│   └── rate_limiter.py     # Rate limiting service
└── etl/                    # Data processing
    ├── etl_service.py      # Main ETL orchestrator
    ├── extractors/         # Data extractors
    ├── transformers/       # Data transformers
    └── loaders/            # Data loaders
```

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Quick test script
./test.sh

# Run with coverage
python -m pytest tests/ --cov=src
```

### Code Quality

The project includes comprehensive linting and formatting:

```bash
# Run all linters and formatters
./lint.sh
```

This runs:
- Black (code formatting)
- isort (import sorting)  
- Flake8 (style checking)
- mypy (type checking)

All linting configurations are in `pyproject.toml` including SQLAlchemy plugin support for proper type checking.

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Manual Docker Build

```bash
# Build image
docker build -t ip-geolocation-service .

# Run container
docker run -p 8080:8080 --env-file .env ip-geolocation-service
```

## Production Considerations

- The service uses Gunicorn as the WSGI server in Docker
- Database is automatically initialized on startup
- Logging is configured for production use
- Rate limiting prevents abuse
- Proper HTTP status codes for all error conditions

## Architecture Patterns

The application follows several design patterns:

- **Factory Pattern**: For creating different data extractors
- **Repository Pattern**: For data access abstraction
- **ETL Pipeline**: For data processing and loading
- **Middleware Pattern**: For cross-cutting concerns like rate limiting
- **App Factory Pattern**: For Flask application creation