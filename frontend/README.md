# Statathon Project Frontend

A React-based frontend for the Statathon Project data filtering system.

## Features

- **State and District Filters**: Text input fields for state names and district names
- **Sector Filter**: Dropdown for Rural/Urban selection
- **Additional Filters**: Religion, Social Group, Household Size, Panel, Quarter, Visit
- **Responsive Design**: Works on both desktop and mobile devices
- **Data Table**: Displays filtered results in a clean, sortable table
- **Real-time API Integration**: Connects to your FastAPI backend

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Your FastAPI backend running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

## Usage

1. **Enter State Name**: Type the full state name (e.g., "Maharashtra", "Andhra Pradesh")
2. **Enter District Name**: Type the full district name (e.g., "Mumbai", "Pune")
3. **Select Sector**: Choose from Rural or Urban
4. **Apply Additional Filters**: Use the dropdown menus for other criteria
5. **Click "Apply Filters"**: The system will query your API and display results
6. **View Results**: Data is displayed in a responsive table below the filters

## API Integration

The frontend connects to your FastAPI backend at:
```
http://localhost:8000/api/filter
```

**Example API calls:**
- Filter by state: `?state_name=Maharashtra`
- Filter by state and district: `?state_name=Maharashtra&district_name=Mumbai`
- Filter by sector: `?sector=Rural`

## Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Customization

- **Styling**: Modify `src/App.css` to change the appearance
- **Filters**: Add or remove filter options in `src/App.tsx`
- **API Endpoint**: Update the API URL in the `handleSubmit` function

## Troubleshooting

- **CORS Issues**: Ensure your FastAPI backend has CORS enabled
- **API Connection**: Verify your backend is running on port 8000
- **State Names with Spaces**: Use URL encoding (e.g., "Andhra Pradesh" becomes "Andhra%20Pradesh")

## Technologies Used

- React 18 with TypeScript
- Vite for build tooling
- Axios for HTTP requests
- CSS Grid and Flexbox for responsive layout
- Modern CSS features for animations and styling
