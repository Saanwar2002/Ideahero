import React, { useState, useEffect } from 'react';
import { dataService } from './dataService';
import { useAuth } from './AuthContext';
import { AuthModal } from './AuthComponents';
import { authService } from './authService';

// Header Component
export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const { user, isAuthenticated, logout } = useAuth();

  const handleAuthClick = (mode) => {
    setAuthMode(mode);
    setAuthModalOpen(true);
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center mr-3">
                  <span className="text-white font-bold text-sm">IH</span>
                </div>
                <span className="text-xl font-semibold text-gray-900">ideahero.com</span>
              </div>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              {isAuthenticated && (
                <a href="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
                  Dashboard
                </a>
              )}
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
            </nav>

            {/* Auth Buttons */}
            <div className="hidden md:flex items-center space-x-4">
              {isAuthenticated ? (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-blue-600 text-sm font-medium">
                        {user?.full_name?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-sm font-medium text-gray-900">{user?.full_name}</span>
                      <span className="text-xs text-gray-500">
                        🏆 {user?.reputation_score || 0} points
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={logout}
                    className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium transition-colors"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <>
                  <button
                    onClick={() => handleAuthClick('login')}
                    className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium transition-colors"
                  >
                    Login
                  </button>
                  <button
                    onClick={() => handleAuthClick('register')}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                  >
                    Sign Up
                  </button>
                </>
              )}
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
                  {isAuthenticated ? (
                    <div className="flex items-center justify-between w-full">
                      <span className="text-sm font-medium text-gray-900">
                        Welcome, {user?.full_name}
                      </span>
                      <button
                        onClick={logout}
                        className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium"
                      >
                        Logout
                      </button>
                    </div>
                  ) : (
                    <>
                      <button
                        onClick={() => handleAuthClick('login')}
                        className="text-gray-700 hover:text-blue-600 px-4 py-2 text-sm font-medium"
                      >
                        Login
                      </button>
                      <button
                        onClick={() => handleAuthClick('register')}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                      >
                        Sign Up
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </header>

      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode={authMode}
      />
    </>
  );
};

// Enhanced Business Idea Card Component with Validation Features
export const EnhancedIdeaCard = ({ idea, onVote, onComment, currentUser }) => {
  const [showVoteModal, setShowVoteModal] = useState(false);
  const [showCommentModal, setShowCommentModal] = useState(false);
  const [showImplementationGuide, setShowImplementationGuide] = useState(false);

  const VoteModal = () => {
    const [voteData, setVoteData] = useState({
      vote_type: 'upvote',
      feasibility_score: 3,
      market_potential_score: 3,
      interest_score: 3,
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      try {
        await onVote(idea.id, voteData);
        setShowVoteModal(false);
      } catch (error) {
        console.error('Vote error:', error);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Rate this Idea</h3>
            <button
              onClick={() => setShowVoteModal(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Overall Rating
              </label>
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="upvote"
                    checked={voteData.vote_type === 'upvote'}
                    onChange={(e) => setVoteData({...voteData, vote_type: e.target.value})}
                    className="mr-2"
                  />
                  👍 Upvote
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="downvote"
                    checked={voteData.vote_type === 'downvote'}
                    onChange={(e) => setVoteData({...voteData, vote_type: e.target.value})}
                    className="mr-2"
                  />
                  👎 Downvote
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Feasibility Score: {voteData.feasibility_score}/5
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={voteData.feasibility_score}
                onChange={(e) => setVoteData({...voteData, feasibility_score: parseInt(e.target.value)})}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Market Potential: {voteData.market_potential_score}/5
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={voteData.market_potential_score}
                onChange={(e) => setVoteData({...voteData, market_potential_score: parseInt(e.target.value)})}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Interest Level: {voteData.interest_score}/5
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={voteData.interest_score}
                onChange={(e) => setVoteData({...voteData, interest_score: parseInt(e.target.value)})}
                className="w-full"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Submitting...' : 'Submit Rating'}
            </button>
          </form>
        </div>
      </div>
    );
  };

  const CommentModal = () => {
    const [comment, setComment] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
      e.preventDefault();
      if (comment.trim().length < 10) return;
      
      setLoading(true);
      try {
        await onComment(idea.id, comment);
        setComment('');
        setShowCommentModal(false);
      } catch (error) {
        console.error('Comment error:', error);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Add Comment</h3>
            <button
              onClick={() => setShowCommentModal(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Share your thoughts about this idea..."
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              minLength={10}
              required
            />
            <div className="flex justify-between items-center mt-4">
              <span className="text-sm text-gray-500">
                {comment.length}/10 characters minimum
              </span>
              <button
                type="submit"
                disabled={loading || comment.trim().length < 10}
                className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Posting...' : 'Post Comment'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const ImplementationGuide = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Implementation Guide</h3>
          <button
            onClick={() => setShowImplementationGuide(false)}
            className="text-gray-400 hover:text-gray-600"
          >
            ×
          </button>
        </div>

        {idea.implementation_guide ? (
          <div className="space-y-6">
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">Timeline</h4>
                <p className="text-blue-700">{idea.implementation_guide.estimated_time}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold text-green-900 mb-2">Budget</h4>
                <p className="text-green-700">{idea.implementation_guide.estimated_budget}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-900 mb-2">Difficulty</h4>
                <p className="text-purple-700">{idea.implementation_guide.difficulty}</p>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Required Skills</h4>
              <div className="flex flex-wrap gap-2">
                {idea.implementation_guide.required_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Step-by-Step Guide</h4>
              <ol className="space-y-3">
                {idea.implementation_guide.steps.map((step, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium mr-3 mt-0.5">
                      {index + 1}
                    </span>
                    <span className="text-gray-700">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">Implementation guide not available for this idea.</p>
        )}
      </div>
    </div>
  );

  return (
    <>
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
        {/* Validation Score Badge */}
        <div className="flex justify-between items-start mb-4">
          <div className="flex flex-wrap gap-2">
            {idea.tags && idea.tags.map((tag, index) => (
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
          </div>
          
          {idea.validation_score > 0 && (
            <div className="bg-gradient-to-r from-green-400 to-blue-500 text-white px-3 py-1 rounded-full text-sm font-bold">
              {idea.validation_score}% Validated
            </div>
          )}
        </div>

        <h3 className="text-xl font-semibold text-gray-900 mb-3">{idea.title}</h3>
        <p className="text-gray-600 leading-relaxed mb-4">{idea.description}</p>
        
        {/* Validation Metrics */}
        {idea.total_votes > 0 && (
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <div className="grid grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-600">{idea.total_votes}</div>
                <div className="text-xs text-gray-500">Votes</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{idea.avg_feasibility}</div>
                <div className="text-xs text-gray-500">Feasibility</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">{idea.avg_market_potential}</div>
                <div className="text-xs text-gray-500">Market</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">{idea.avg_interest}</div>
                <div className="text-xs text-gray-500">Interest</div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-2 mb-4">
          {currentUser ? (
            <>
              <button
                onClick={() => setShowVoteModal(true)}
                className="flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200 transition-colors"
              >
                👍 Rate Idea
              </button>
              <button
                onClick={() => setShowCommentModal(true)}
                className="flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm hover:bg-green-200 transition-colors"
              >
                💬 Comment
              </button>
            </>
          ) : (
            <span className="text-sm text-gray-500">Login to rate and comment</span>
          )}
          
          {idea.implementation_guide && (
            <button
              onClick={() => setShowImplementationGuide(true)}
              className="flex items-center px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm hover:bg-purple-200 transition-colors"
            >
              🚀 Implementation Guide
            </button>
          )}
        </div>

        {/* Comments Preview */}
        {idea.comments && idea.comments.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="font-medium text-gray-900 mb-2">Recent Comments</h4>
            <div className="space-y-2">
              {idea.comments.slice(0, 2).map((comment, index) => (
                <div key={index} className="bg-gray-50 p-3 rounded">
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-medium text-sm text-gray-900">{comment.user_name}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(comment.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{comment.content}</p>
                </div>
              ))}
              {idea.comments.length > 2 && (
                <button className="text-sm text-blue-600 hover:text-blue-800">
                  View all {idea.comments.length} comments
                </button>
              )}
            </div>
          </div>
        )}

        {/* Source info */}
        {idea.source && (
          <div className="flex items-center justify-between text-sm text-gray-500 border-t pt-3 mt-4">
            <span className="flex items-center">
              via {idea.source}
            </span>
            {idea.created_at && (
              <span>
                {new Date(idea.created_at).toLocaleDateString()}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Modals */}
      {showVoteModal && <VoteModal />}
      {showCommentModal && <CommentModal />}
      {showImplementationGuide && <ImplementationGuide />}
    </>
  );
};

// Legacy IdeaCard component for backward compatibility
export const IdeaCard = ({ idea }) => {
  return <EnhancedIdeaCard idea={idea} onVote={() => {}} onComment={() => {}} currentUser={null} />;
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
            {trend.language && (
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                {trend.language}
              </span>
            )}
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
      
      <p className="text-gray-600 text-sm mb-3">{trend.description}</p>
      
      {/* GitHub specific info */}
      {trend.url && (
        <div className="flex items-center justify-between text-xs text-gray-500 border-t pt-3">
          <span className="bg-gray-100 px-2 py-1 rounded">
            {trend.category || 'Technology'}
          </span>
          <a 
            href={trend.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 flex items-center"
          >
            View on GitHub 
            <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>
      )}
    </div>
  );
};

// HomePage Component with Enhanced Features
export const HomePage = () => {
  const [currentDate] = useState(new Date().toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  }));
  const [todayIdea, setTodayIdea] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const { user, isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchTodayIdea = async () => {
      try {
        setLoading(true);
        // Try to get enhanced ideas first
        const enhancedIdeas = await authService.getEnhancedIdeas({ limit: 1, sort_by: 'validation_score' });
        if (enhancedIdeas && enhancedIdeas.length > 0) {
          setTodayIdea(enhancedIdeas[0]);
        } else {
          // Fallback to original data service
          const idea = await dataService.getIdeaOfTheDay();
          setTodayIdea(idea);
        }
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

  const handleVote = async (ideaId, voteData) => {
    if (!isAuthenticated) {
      setAuthModalOpen(true);
      return;
    }

    try {
      await authService.voteOnIdea(ideaId, voteData);
      // Refresh the idea to show updated scores
      const updatedIdea = await authService.getIdeaDetails(ideaId);
      setTodayIdea(updatedIdea);
    } catch (error) {
      console.error('Error voting:', error);
      throw error;
    }
  };

  const handleComment = async (ideaId, content) => {
    if (!isAuthenticated) {
      setAuthModalOpen(true);
      return;
    }

    try {
      await authService.commentOnIdea(ideaId, content);
      // Refresh the idea to show updated comments
      const updatedIdea = await authService.getIdeaDetails(ideaId);
      setTodayIdea(updatedIdea);
    } catch (error) {
      console.error('Error commenting:', error);
      throw error;
    }
  };

  const refreshIdea = async () => {
    setLoading(true);
    try {
      const enhancedIdeas = await authService.getEnhancedIdeas({ limit: 5, sort_by: 'created_at' });
      if (enhancedIdeas && enhancedIdeas.length > 0) {
        // Get a random idea from the latest 5
        const randomIdea = enhancedIdeas[Math.floor(Math.random() * enhancedIdeas.length)];
        setTodayIdea(randomIdea);
      } else {
        const idea = await dataService.getIdeaOfTheDay();
        setTodayIdea(idea);
      }
    } catch (error) {
      console.error('Error refreshing idea:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="min-h-screen bg-gray-50">
        {/* Hero Section */}
        <section 
          className="relative bg-gradient-to-br from-blue-600 to-purple-700 text-white py-20"
          style={{
            backgroundImage: `linear-gradient(rgba(37, 99, 235, 0.8), rgba(124, 58, 237, 0.8)), url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="a" cx="0" cy="0" r="1"><stop offset="0%25" stop-color="%2337a2eb"/><stop offset="100%25" stop-color="%23ff6b6b"/></radialGradient></defs><rect width="100%25" height="100%25" fill="url(%23a)"/><g><circle cx="200" cy="200" r="4" fill="%23ffffff" opacity="0.3"/><circle cx="800" cy="150" r="3" fill="%23ffffff" opacity="0.2"/><circle cx="600" cy="300" r="5" fill="%23ffffff" opacity="0.4"/><circle cx="300" cy="800" r="3" fill="%23ffffff" opacity="0.3"/><circle cx="900" cy="700" r="4" fill="%23ffffff" opacity="0.2"/></g></svg>')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 inline-flex items-center mb-6">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
              <span className="text-sm font-medium">
                The #1 Software to Spot Trends and Startup Ideas Worth Building
              </span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Discover & Validate
              <span className="block bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                Startup Ideas
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto opacity-90">
              Join thousands of entrepreneurs using real-time data and community validation to find their next big opportunity
            </p>

            {!isAuthenticated && (
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={() => setAuthModalOpen(true)}
                  className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors"
                >
                  Get Started Free
                </button>
                <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors">
                  Watch Demo
                </button>
              </div>
            )}

            {isAuthenticated && (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 max-w-md mx-auto">
                <p className="text-lg mb-2">Welcome back, {user?.full_name}!</p>
                <p className="text-sm opacity-80">
                  🏆 You have {user?.reputation_score || 0} reputation points
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Idea of the Day Section */}
        <section className="py-16">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-6">
                {todayIdea?.validation_score > 0 ? 'Top Validated Idea' : 'Idea of the Day'}
              </h1>
              
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
                
                <button 
                  onClick={refreshIdea}
                  className="flex items-center hover:text-blue-600 transition-colors"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Refresh Idea
                </button>
              </div>
            </div>

            {todayIdea && !loading && (
              <EnhancedIdeaCard
                idea={todayIdea}
                onVote={handleVote}
                onComment={handleComment}
                currentUser={user}
              />
            )}

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

            {/* Community Validation Badge */}
            {todayIdea && !loading && (
              <div className="text-center mt-6">
                <div className="inline-flex items-center px-4 py-2 bg-green-50 border border-green-200 rounded-full">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                  <span className="text-green-800 text-sm font-medium">
                    {todayIdea.validation_score > 0 
                      ? `${todayIdea.validation_score}% Community Validated`
                      : 'Live data from HackerNews & GitHub'
                    }
                  </span>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Enhanced Features Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Real-World Validation Features
              </h2>
              <p className="text-xl text-gray-600">
                Everything you need to validate and implement your next big idea
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Community Validation</h3>
                <p className="text-gray-600">Get real feedback from entrepreneurs on feasibility, market potential, and interest</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Implementation Guides</h3>
                <p className="text-gray-600">Step-by-step roadmaps with timelines, budgets, and required skills</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-Time Data</h3>
                <p className="text-gray-600">Live insights from HackerNews, GitHub trends, and market analysis</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Community Network</h3>
                <p className="text-gray-600">Connect with like-minded entrepreneurs and potential co-founders</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode="register"
      />
    </>
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

// IdeasPage Component with Enhanced Validation Features
export const IdeasPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [sortBy, setSortBy] = useState('validation_score');
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const { user, isAuthenticated } = useAuth();

  useEffect(() => {
    fetchIdeas();
  }, [selectedCategory, sortBy]);

  const fetchIdeas = async () => {
    try {
      setLoading(true);
      const params = {
        category: selectedCategory === 'All' ? '' : selectedCategory,
        sort_by: sortBy,
        limit: 20
      };
      const ideasData = await authService.getEnhancedIdeas(params);
      setIdeas(ideasData);
    } catch (error) {
      console.error('Error fetching ideas:', error);
      // Fallback to original data service
      try {
        const fallbackIdeas = await dataService.getAllIdeas();
        setIdeas(fallbackIdeas);
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError);
        setIdeas([]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleVote = async (ideaId, voteData) => {
    if (!isAuthenticated) {
      setAuthModalOpen(true);
      return;
    }

    try {
      await authService.voteOnIdea(ideaId, voteData);
      // Refresh ideas to get updated scores
      await fetchIdeas();
    } catch (error) {
      console.error('Error voting:', error);
      throw error;
    }
  };

  const handleComment = async (ideaId, content) => {
    if (!isAuthenticated) {
      setAuthModalOpen(true);
      return;
    }

    try {
      await authService.commentOnIdea(ideaId, content);
      // Refresh ideas to get updated comments
      await fetchIdeas();
    } catch (error) {
      console.error('Error commenting:', error);
      throw error;
    }
  };

  const categories = ['All', 'Technology', 'Healthcare', 'Business', 'Sustainability', 'Education'];
  const sortOptions = [
    { value: 'validation_score', label: '🏆 Highest Validated' },
    { value: 'total_votes', label: '👥 Most Voted' },
    { value: 'created_at', label: '🕒 Most Recent' },
  ];

  const filteredIdeas = ideas.filter(idea => {
    const matchesSearch = idea.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         idea.description?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  return (
    <>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-blue-600 mb-4">Idea Database</h1>
            <p className="text-xl text-gray-600">Community-validated business opportunities with implementation guides</p>
            {!isAuthenticated && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800">
                  <button
                    onClick={() => setAuthModalOpen(true)}
                    className="text-blue-600 hover:text-blue-800 font-medium underline"
                  >
                    Sign up
                  </button>
                  {' '}to rate ideas, leave comments, and access implementation guides!
                </p>
              </div>
            )}
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
            
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {sortOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
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
                <EnhancedIdeaCard
                  key={idea.id}
                  idea={idea}
                  onVote={handleVote}
                  onComment={handleComment}
                  currentUser={user}
                />
              ))
            )}
          </div>

          {/* Real-time Data Status */}
          {!loading && ideas.length > 0 && (
            <div className="text-center mt-8">
              <div className="inline-flex items-center px-4 py-2 bg-green-50 border border-green-200 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                <span className="text-green-800 text-sm font-medium">
                  Live validation data from our community
                </span>
              </div>
            </div>
          )}

          {filteredIdeas.length === 0 && !loading && (
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

      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode="register"
      />
    </>
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