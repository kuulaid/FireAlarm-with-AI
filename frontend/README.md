# Fire Alarm Frontend

A React-based environmental monitoring dashboard for the Fire Alarm System. Built with Vite and React.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AlertBanner.jsx       # Alert/warning display component
│   │   ├── BottomNav.jsx         # Mobile navigation bar
│   │   ├── SensorGrid.jsx        # Sensor readings grid display
│   │   ├── Sidebar.jsx           # Main sidebar navigation
│   │   └── Topbar.jsx            # Top navigation bar
│   ├── pages/
│   │   ├── DetailPage.jsx        # Detailed log view
│   │   ├── HistoryPage.jsx       # Detection history list
│   │   └── HomePage.jsx          # Dashboard home page
│   ├── data/
│   │   └── mockData.js           # Mock data for development
│   ├── styles/
│   │   └── index.css             # Global styles
│   ├── utils/
│   │   └── helpers.js            # Utility functions
│   ├── App.jsx                   # Main app component
│   └── index.jsx                 # Entry point
├── public/                        # Static assets
├── index.html                     # HTML template
├── package.json                   # Dependencies and scripts
├── vite.config.js                # Vite configuration
└── README.md                      # This file
```

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

Build for production:

```bash
npm run build
```

The output will be in the `dist/` directory.

## Features

- **Dashboard**: Real-time sensor readings and system status
- **Detection History**: View all historical detection events
- **Detailed Logs**: Inspect individual sensor readings and analysis
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Alerts**: Visual feedback for dangerous gas levels

## Components

### Pages
- **HomePage**: Main dashboard with live readings and recent activity
- **HistoryPage**: List of all detection events with filtering
- **DetailPage**: Detailed view of a specific detection event

### Components
- **AlertBanner**: Displays current system alert status
- **SensorGrid**: Shows all sensor readings in a grid layout
- **Sidebar**: Main navigation (desktop)
- **Topbar**: Header with title and live indicator
- **BottomNav**: Mobile navigation

### Utilities
- **helpers.js**: Time formatting, color mapping, sensor status calculations

## Styling

All styles are contained in `src/styles/index.css` with CSS variables for theming:
- Dark theme with accent colors (red for danger, orange for warning, green for safe)
- Responsive grid layout
- Mobile-first approach

## Data

Currently uses mock data from `src/data/mockData.js`. To connect to a real API, replace the MOCK_HISTORY with API calls.
