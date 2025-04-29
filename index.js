import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app.js';
import './app.css'; // if you have custom styles'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
