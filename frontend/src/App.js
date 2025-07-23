import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';

// Simple test component
const TestPage = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">IdeaHero.com</h1>
      <p className="text-xl text-gray-600">Testing React App</p>
      <div className="mt-8 p-4 bg-white rounded-lg shadow">
        <p>If you can see this, React is working!</p>
      </div>
    </div>
  </div>
);

function App() {
  return (
    <div className="App">
      <TestPage />
    </div>
  );
}

export default App;