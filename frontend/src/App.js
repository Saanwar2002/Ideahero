import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './AuthContext';
import { Header, HomePage, TrendsPage, IdeasPage, PricingPage } from './components';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/trends" element={<TrendsPage />} />
            <Route path="/ideas" element={<IdeasPage />} />
            <Route path="/pricing" element={<PricingPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </AuthProvider>
  );
}

export default App;