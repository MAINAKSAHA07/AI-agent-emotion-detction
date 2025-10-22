// API Configuration
// For Netlify deployment, use proxy to avoid mixed content issues
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

export default API_BASE_URL;
