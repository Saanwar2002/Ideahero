import React, { useState, useEffect } from 'react';
import { dataService } from './dataService';

// Header Component
export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center mr-3">
                <span className="text-white font-bold text-sm">IB</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">ideahero.com</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a href="/ideas" className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
              Idea Database
            </a>
            <a href="/trends" className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
              Trends
            </a>
            <a href="/agent" className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors relative">
              Idea Agent
              <span className="ml-1 bg-blue-500 text-white text-xs px-1.5 py-0.5 rounded-full">NEW</span>
            </a>
            <a href="/pricing" className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
              Pricing
            </a>
            <div className="relative group">
              <button className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors flex items-center">
                More
                <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </nav>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <button className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium transition-colors">
              Login
            </button>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
              Sign Up
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-blue-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t">
              <a href="/ideas" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600">
                Idea Database
              </a>
              <a href="/trends" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600">
                Trends
              </a>
              <a href="/agent" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600">
                Idea Agent <span className="ml-1 bg-blue-500 text-white text-xs px-1.5 py-0.5 rounded-full">NEW</span>
              </a>
              <a href="/pricing" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600">
                Pricing
              </a>
              <div className="flex space-x-2 px-3 py-2">
                <button className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium">
                  Login
                </button>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium">
                  Sign Up
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

// Business Idea Card Component
export const IdeaCard = ({ idea }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex flex-wrap gap-2 mb-4">
        {idea.tags.map((tag, index) => (
          <span
            key={index}
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              tag.type === 'timing' 
                ? 'bg-orange-100 text-orange-800' 
                : tag.type === 'advantage'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-green-100 text-green-800'
            }`}
          >
            {tag.icon} {tag.label}
          </span>
        ))}
        {idea.moreCount && (
          <span className="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
            +{idea.moreCount} more
          </span>
        )}
      </div>
      <h3 className="text-xl font-semibold text-gray-900 mb-3">{idea.title}</h3>
      <p className="text-gray-600 leading-relaxed">{idea.description}</p>
    </div>
  );
};

// Trend Card Component
export const TrendCard = ({ trend }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{trend.title}</h3>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span>Volume {trend.volume}</span>
            <span>Growth {trend.growth}</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-blue-600">{trend.volumeNumber}</div>
          <div className={`text-sm font-medium ${trend.growthNumber.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
            {trend.growthNumber}
          </div>
        </div>
      </div>
      
      {/* Simple Chart Representation */}
      <div className="h-24 bg-blue-50 rounded-lg mb-4 flex items-end justify-center overflow-hidden">
        <svg width="100%" height="100%" viewBox="0 0 300 96" className="text-blue-500">
          <path
            d={trend.chartPath}
            stroke="currentColor"
            strokeWidth="2"
            fill="none"
          />
          <path
            d={trend.chartPath + " L300,96 L0,96 Z"}
            fill="currentColor"
            fillOpacity="0.1"
          />
        </svg>
      </div>
      
      <p className="text-gray-600 text-sm">{trend.description}</p>
    </div>
  );
};

// HomePage Component
export const HomePage = () => {
  const [currentDate] = useState(new Date().toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  }));
  const [todayIdea, setTodayIdea] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTodayIdea = async () => {
      try {
        setLoading(true);
        const idea = await dataService.getIdeaOfTheDay();
        setTodayIdea(idea);
      } catch (error) {
        console.error('Error fetching idea:', error);
        // Fallback to default idea
        setTodayIdea({
          title: "Transparent HVAC Pricing Platform - End Quote Anxiety For Homeowners",
          description: "Homeowners dread HVAC repairs because of unpredictable pricing and questionable quotes. TruPrice HVAC transforms this experience with transparent, real-time pricing that eliminates the uncertainty and mistrust. The platform shows exact costs for parts, labor, and service fees before you commit to anything. For homeowners, it means no more anxiety about getting ripped off or struggling to compare wildly different quotes. For HVAC companies, it's a way to build trust instantly and close deals faster with customers who appreciate honesty.",
          tags: [
            { label: "Perfect Timing", type: "timing", icon: "⏰" },
            { label: "Unfair Advantage", type: "advantage", icon: "⚡" },
            { label: "Product Ready", type: "ready", icon: "✅" }
          ],
          moreCount: 16
        });
      } finally {
        setLoading(false);
      }
    };

    fetchTodayIdea();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section 
        className="relative bg-gradient-to-br from-blue-600 to-purple-700 text-white py-20"
        style={{
          backgroundImage: `linear-gradient(rgba(37, 99, 235, 0.8), rgba(124, 58, 237, 0.8)), url('https://images.unsplash.com/photo-1588856122867-363b0aa7f598?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxzdGFydHVwJTIwaWRlYXN8ZW58MHx8fGJsdWV8MTc1MzI1NTk1MHww&ixlib=rb-4.1.0&q=85')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 inline-flex items-center mb-6">
            <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
            <span className="text-sm font-medium">The #1 Software to Spot Trends and Startup Ideas Worth Building</span>
            <button className="ml-3 w-8 h-8 bg-black/20 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </section>

      {/* Idea of the Day Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-6">Idea of the Day</h1>
            
            <div className="flex items-center justify-center space-x-6 text-gray-600 mb-8">
              <button className="flex items-center hover:text-blue-600 transition-colors">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Previous
              </button>
              
              <div className="flex items-center bg-gray-100 rounded-lg px-4 py-2">
                <svg className="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className="font-medium">{currentDate}</span>
              </div>
              
              <button className="flex items-center hover:text-blue-600 transition-colors">
                Next Idea
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <IdeaCard idea={todayIdea} />

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 animate-pulse">
              <div className="flex flex-wrap gap-2 mb-4">
                <div className="h-6 bg-gray-200 rounded-full w-20"></div>
                <div className="h-6 bg-gray-200 rounded-full w-24"></div>
                <div className="h-6 bg-gray-200 rounded-full w-16"></div>
              </div>
              <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
            </div>
          )}

          {/* Real-time Data Badge */}
          {todayIdea && !loading && (
            <div className="text-center mt-6">
              <div className="inline-flex items-center px-4 py-2 bg-green-50 border border-green-200 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                <span className="text-green-800 text-sm font-medium">
                  Live data from HackerNews & GitHub
                </span>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI-Powered Research</h3>
              <p className="text-gray-600">Get data-driven insights on market trends and startup opportunities</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Trend Analysis</h3>
              <p className="text-gray-600">Track emerging market trends and growth opportunities</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Founder-Fit Assessment</h3>
              <p className="text-gray-600">Match business ideas based on your skills and resources</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// TrendsPage Component
export const TrendsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('Most Recent');
  const [showFilters, setShowFilters] = useState(false);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const trendsData = await dataService.getTrends();
        setTrends(trendsData);
      } catch (error) {
        console.error('Error fetching trends:', error);
        // Fallback trends
        setTrends([
          {
            title: "AI Learning",
            volume: "🔍",
            growth: "📈",
            volumeNumber: "49.5K",
            growthNumber: "+647%",
            description: "AI learning refers to the application of artificial intelligence technologies to enhance and personalize educational experiences.",
            chartPath: "M0,80 Q50,75 100,60 T200,45 T300,20"
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  const filteredTrends = trends.filter(trend =>
    trend.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-4">Trends</h1>
          <p className="text-xl text-gray-600">Discover emerging trends and opportunities</p>
        </div>

        {/* Search and Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search trends..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg className="w-5 h-5 text-gray-400 absolute left-3 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          
          <div className="flex gap-4">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option>📊 Most Recent</option>
              <option>📈 Highest Growth</option>
              <option>🔥 Most Volume</option>
            </select>
            
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-transparent flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z" />
              </svg>
              All Filters
            </button>
          </div>
        </div>

        {/* Trends Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading ? (
            // Loading skeleton
            Array.from({ length: 6 }).map((_, index) => (
              <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <div className="h-6 bg-gray-200 rounded w-32 mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-24"></div>
                  </div>
                  <div className="text-right">
                    <div className="h-8 bg-gray-200 rounded w-16 mb-1"></div>
                    <div className="h-4 bg-gray-200 rounded w-12"></div>
                  </div>
                </div>
                <div className="h-24 bg-gray-200 rounded-lg mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
              </div>
            ))
          ) : (
            filteredTrends.map((trend, index) => (
              <TrendCard key={index} trend={trend} />
            ))
          )}
        </div>

        {/* Real-time Data Status */}
        {!loading && trends.length > 0 && (
          <div className="text-center mt-8">
            <div className="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-full">
              <div className="w-2 h-2 bg-blue-400 rounded-full mr-2 animate-pulse"></div>
              <span className="text-blue-800 text-sm font-medium">
                Live trends from GitHub repositories
              </span>
            </div>
          </div>
        )}

        {filteredTrends.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.5-.935-6.072-2.443" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No trends found</h3>
            <p className="text-gray-600">Try adjusting your search terms or filters</p>
          </div>
        )}
      </div>
    </div>
  );
};

// IdeasPage Component  
export const IdeasPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIdeas = async () => {
      try {
        setLoading(true);
        const ideasData = await dataService.getAllIdeas();
        setIdeas(ideasData);
      } catch (error) {
        console.error('Error fetching ideas:', error);
        // Fallback ideas
        setIdeas([
          {
            id: 1,
            title: "AI-Powered Code Review Assistant",
            description: "Automated code review tool that uses machine learning to identify bugs, security vulnerabilities, and performance issues before deployment.",
            tags: [
              { label: "High Demand", type: "advantage", icon: "🔥" },
              { label: "Tech Ready", type: "ready", icon: "✅" }
            ],
            category: "Technology",
            moreCount: 8
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchIdeas();
  }, []);

  const categories = ['All', 'Technology', 'Healthcare', 'Business', 'Sustainability', 'Health & Fitness'];

  const filteredIdeas = ideas.filter(idea => {
    const matchesSearch = idea.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         idea.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || idea.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-4">Idea Database</h1>
          <p className="text-xl text-gray-600">Browse validated business opportunities</p>
        </div>

        {/* Search and Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search ideas..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg className="w-5 h-5 text-gray-400 absolute left-3 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-2 mb-8">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Ideas Grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          {loading ? (
            // Loading skeleton
            Array.from({ length: 4 }).map((_, index) => (
              <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="flex flex-wrap gap-2 mb-4">
                  <div className="h-6 bg-gray-200 rounded-full w-20"></div>
                  <div className="h-6 bg-gray-200 rounded-full w-24"></div>
                  <div className="h-6 bg-gray-200 rounded-full w-16"></div>
                </div>
                <div className="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            ))
          ) : (
            filteredIdeas.map(idea => (
              <IdeaCard key={idea.id} idea={idea} />
            ))
          )}
        </div>

        {/* Real-time Data Status */}
        {!loading && ideas.length > 0 && (
          <div className="text-center mt-8">
            <div className="inline-flex items-center px-4 py-2 bg-orange-50 border border-orange-200 rounded-full">
              <div className="w-2 h-2 bg-orange-400 rounded-full mr-2 animate-pulse"></div>
              <span className="text-orange-800 text-sm font-medium">
                Live business ideas from HackerNews community
              </span>
            </div>
          </div>
        )}

        {filteredIdeas.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.5-.935-6.072-2.443" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No ideas found</h3>
            <p className="text-gray-600">Try adjusting your search terms or category filter</p>
          </div>
        )}
      </div>
    </div>
  );
};

// PricingPage Component
export const PricingPage = () => {
  const [isAnnual, setIsAnnual] = useState(true);

  const plans = [
    {
      name: "Free",
      subtitle: "Daily Deep Dive",
      price: "$0",
      period: "Forever",
      description: "Get started with daily business insights",
      features: [
        "One fully-researched business opportunity daily",
        "Complete market analysis via email",
        "Trend insights and timing indicators",
        "Community access",
        "Basic market data"
      ],
      buttonText: "Get Started Free",
      buttonStyle: "border border-gray-300 text-gray-700 hover:bg-gray-50",
      popular: false
    },
    {
      name: "Starter",
      subtitle: "Opportunity Hunter",
      price: isAnnual ? "$299" : "$29",
      originalPrice: isAnnual ? "$499" : "$49",
      period: isAnnual ? "/year" : "/month",
      description: "Perfect for entrepreneurs exploring opportunities",
      features: [
        "Browse 200+ validated business opportunities",
        "Advanced trend alerts and notifications",
        "Founder-fit assessment tools",
        "Market size and competition analysis",
        "Download and export data",
        "Priority community access",
        "Weekly strategy insights"
      ],
      buttonText: "Start Hunting",
      buttonStyle: "bg-blue-600 text-white hover:bg-blue-700",
      popular: true
    },
    {
      name: "Pro",
      subtitle: "Builder's Command Center",
      price: isAnnual ? "$999" : "$99",
      originalPrice: isAnnual ? "$1,499" : "$149",
      period: isAnnual ? "/year" : "/month",
      description: "For serious entrepreneurs ready to build",
      features: [
        "Everything in Starter plan",
        "AI-driven custom research requests",
        "1-on-1 strategy sessions monthly",
        "Tailored idea suggestions",
        "Advanced data exports and APIs",
        "Early access to new tools",
        "Exclusive founder community",
        "Direct support channel"
      ],
      buttonText: "Start Building",
      buttonStyle: "bg-purple-600 text-white hover:bg-purple-700",
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-4">Pricing</h1>
          <p className="text-xl text-gray-600 mb-8">Choose the perfect plan for your entrepreneurial journey</p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center mb-8">
            <span className={`mr-3 ${!isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                isAnnual ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  isAnnual ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`ml-3 ${isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Annually
            </span>
            {isAnnual && (
              <span className="ml-2 bg-green-100 text-green-800 text-sm px-2 py-1 rounded-full">
                Save 40%
              </span>
            )}
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`bg-white rounded-2xl shadow-sm border-2 p-8 relative ${
                plan.popular ? 'border-blue-500' : 'border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="text-center mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-1">{plan.name}</h3>
                <p className="text-gray-600 text-sm mb-4">{plan.subtitle}</p>
                
                <div className="mb-2">
                  <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                  {plan.originalPrice && (
                    <span className="text-lg text-gray-500 line-through ml-2">{plan.originalPrice}</span>
                  )}
                  <span className="text-gray-600">{plan.period}</span>
                </div>
                
                <p className="text-gray-600 text-sm">{plan.description}</p>
              </div>
              
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-700 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
              
              <button className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${plan.buttonStyle}`}>
                {plan.buttonText}
              </button>
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-12">Frequently Asked Questions</h2>
          
          <div className="space-y-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">How does the free plan work?</h3>
              <p className="text-gray-600">You'll receive one fully-researched business opportunity via email every day, complete with market analysis and trend insights.</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Can I cancel anytime?</h3>
              <p className="text-gray-600">Yes, you can cancel your subscription at any time. Your access will continue until the end of your billing period.</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">What's included in the AI-driven custom research?</h3>
              <p className="text-gray-600">Our AI will research specific markets, trends, or business ideas based on your requests, providing detailed analysis and actionable insights.</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Do you offer refunds?</h3>
              <p className="text-gray-600">We offer a 30-day money-back guarantee for all paid plans. If you're not satisfied, we'll refund your payment.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};