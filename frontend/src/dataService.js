// Data service for fetching real data from APIs
class DataService {
  constructor() {
    this.cache = new Map();
    this.cacheExpiry = 6 * 60 * 60 * 1000; // 6 hours
  }

  // Cache helper
  getCachedData(key) {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }
    return null;
  }

  setCachedData(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  // HackerNews API Integration
  async fetchHackerNewsStories() {
    const cached = this.getCachedData('hackernews_stories');
    if (cached) return cached;

    console.log('Fetching HackerNews stories...');
    try {
      // Fetch top stories
      const topStoriesResponse = await fetch('https://hacker-news.firebaseio.com/v0/topstories.json');
      if (!topStoriesResponse.ok) {
        throw new Error(`HTTP error! status: ${topStoriesResponse.status}`);
      }
      const topStories = await topStoriesResponse.json();
      console.log('Fetched top stories count:', topStories.length);
      
      // Get first 10 stories to reduce load time
      const storyPromises = topStories.slice(0, 10).map(async (id) => {
        const response = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
        if (!response.ok) return null;
        return response.json();
      });

      const stories = await Promise.all(storyPromises);
      const validStories = stories.filter(story => story && story.title);
      console.log('Valid stories fetched:', validStories.length);
      
      // Filter for business/startup related content
      const businessStories = validStories.filter(story => 
        story.title.toLowerCase().includes('startup') ||
        story.title.toLowerCase().includes('business') ||
        story.title.toLowerCase().includes('idea') ||
        story.title.toLowerCase().includes('saas') ||
        story.title.toLowerCase().includes('ask hn') ||
        story.title.toLowerCase().includes('problem') ||
        story.title.toLowerCase().includes('solution') ||
        story.title.toLowerCase().includes('app') ||
        story.title.toLowerCase().includes('tool')
      );

      console.log('Business stories filtered:', businessStories.length);
      
      // If no business stories found, return all valid stories
      const finalStories = businessStories.length > 0 ? businessStories : validStories;
      
      this.setCachedData('hackernews_stories', finalStories);
      return finalStories;
    } catch (error) {
      console.error('Error fetching HackerNews stories:', error);
      return this.getFallbackStories();
    }
  }

  // GitHub API Integration
  async fetchGitHubTrends() {
    const cached = this.getCachedData('github_trends');
    if (cached) return cached;

    console.log('Fetching GitHub trends...');
    try {
      // Fetch trending repositories
      const response = await fetch('https://api.github.com/search/repositories?q=created:>2024-01-01&sort=stars&order=desc&per_page=15');
      if (!response.ok) {
        throw new Error(`GitHub API error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('GitHub API response received, items:', data.items?.length || 0);
      
      if (!data.items) throw new Error('No GitHub data received');

      // Process repositories into trend format
      const trends = data.items.map(repo => ({
        title: this.extractTechTrend(repo.name, repo.description),
        description: repo.description || 'No description available',
        volumeNumber: this.formatNumber(repo.stargazers_count),
        growthNumber: this.calculateGrowthPercentage(repo.stargazers_count, repo.watchers_count),
        volume: '⭐',
        growth: '📈',
        chartPath: this.generateRandomChartPath(),
        category: this.categorizeRepo(repo.language, repo.topics),
        url: repo.html_url,
        language: repo.language
      }));

      console.log('Processed trends:', trends.length);
      this.setCachedData('github_trends', trends);
      return trends;
    } catch (error) {
      console.error('Error fetching GitHub trends:', error);
      return this.getFallbackTrends();
    }
  }

  // Process HackerNews stories into business ideas
  processStoriesIntoIdeas(stories) {
    return stories.map(story => ({
      id: story.id,
      title: this.generateIdeaTitle(story.title),
      description: this.generateIdeaDescription(story.title, story.url),
      tags: this.generateTags(story),
      category: this.categorizeStory(story.title),
      moreCount: Math.floor(Math.random() * 20) + 5,
      source: 'HackerNews',
      url: `https://news.ycombinator.com/item?id=${story.id}`,
      score: story.score,
      comments: story.descendants || 0
    }));
  }

  // Helper methods
  extractTechTrend(name, description) {
    const techKeywords = {
      'ai': 'AI & Machine Learning',
      'ml': 'Machine Learning Tools',
      'blockchain': 'Blockchain Solutions',
      'react': 'React Development',
      'python': 'Python Tools',
      'javascript': 'JavaScript Frameworks',
      'api': 'API Development',
      'database': 'Database Solutions',
      'security': 'Security Tools',
      'mobile': 'Mobile Development'
    };

    const lowerName = name.toLowerCase();
    const lowerDesc = (description || '').toLowerCase();
    
    for (const [keyword, trend] of Object.entries(techKeywords)) {
      if (lowerName.includes(keyword) || lowerDesc.includes(keyword)) {
        return trend;
      }
    }
    
    return name.replace(/-/g, ' ').replace(/([A-Z])/g, ' $1').trim();
  }

  generateIdeaTitle(originalTitle) {
    // Transform HN titles into business idea format
    if (originalTitle.toLowerCase().includes('ask hn')) {
      return originalTitle.replace(/Ask HN:?\s*/i, '').trim();
    }
    
    const businessPrefixes = [
      'Platform for',
      'Solution for',
      'Tool to help',
      'Service that',
      'App for'
    ];
    
    if (originalTitle.includes('?')) {
      return originalTitle.replace('?', '').trim();
    }
    
    return originalTitle;
  }

  generateIdeaDescription(title, url) {
    const templates = [
      `This innovative solution addresses a growing market need identified in the tech community. The concept has gained significant traction and discussion among entrepreneurs and developers.`,
      `A data-driven approach to solving real-world problems. This idea emerged from community discussions and represents a validated market opportunity.`,
      `This business concept leverages current technology trends to create value for users. The solution has been discussed and refined by industry experts.`,
      `An innovative approach to modernizing traditional processes. This idea combines proven business models with emerging technologies.`,
      `This solution targets a specific pain point identified through community feedback and market analysis. The opportunity shows strong potential for growth.`
    ];
    
    return templates[Math.floor(Math.random() * templates.length)];
  }

  generateTags(story) {
    const tagOptions = [
      { label: 'Tech Trend', type: 'timing', icon: '🚀' },
      { label: 'High Engagement', type: 'advantage', icon: '🔥' },
      { label: 'Community Validated', type: 'ready', icon: '✅' },
      { label: 'Growing Market', type: 'timing', icon: '📈' },
      { label: 'Problem Identified', type: 'advantage', icon: '💡' },
      { label: 'Tech Ready', type: 'ready', icon: '⚡' }
    ];

    const selectedTags = [];
    
    // Always add community validated for HN stories
    selectedTags.push({ label: 'Community Validated', type: 'ready', icon: '✅' });
    
    // Add based on score
    if (story.score > 100) {
      selectedTags.push({ label: 'High Engagement', type: 'advantage', icon: '🔥' });
    }
    
    // Add random relevant tag
    const randomTag = tagOptions[Math.floor(Math.random() * tagOptions.length)];
    if (!selectedTags.find(tag => tag.label === randomTag.label)) {
      selectedTags.push(randomTag);
    }

    return selectedTags;
  }

  categorizeStory(title) {
    const categories = {
      'ai': 'Technology',
      'ml': 'Technology', 
      'health': 'Healthcare',
      'finance': 'Business',
      'education': 'Education',
      'climate': 'Sustainability',
      'mobile': 'Technology',
      'web': 'Technology'
    };

    const lowerTitle = title.toLowerCase();
    for (const [keyword, category] of Object.entries(categories)) {
      if (lowerTitle.includes(keyword)) {
        return category;
      }
    }
    
    return 'Technology';
  }

  categorizeRepo(language, topics = []) {
    const languageCategories = {
      'JavaScript': 'Web Development',
      'Python': 'AI & Data Science',
      'Java': 'Enterprise Software',
      'Go': 'Cloud & Infrastructure',
      'Rust': 'Systems Programming',
      'TypeScript': 'Web Development'
    };

    return languageCategories[language] || 'Software Development';
  }

  formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  }

  calculateGrowthPercentage(stars, watchers) {
    const ratio = stars / Math.max(watchers, 1);
    const growth = Math.min(Math.floor(ratio * 50), 999);
    return `+${growth}%`;
  }

  generateRandomChartPath() {
    const paths = [
      "M0,80 Q50,75 100,60 T200,45 T300,20",
      "M0,85 Q75,80 150,50 T300,15", 
      "M0,70 Q100,65 200,55 T300,35",
      "M0,75 Q80,70 160,45 T300,25",
      "M0,90 Q60,85 120,60 T300,30"
    ];
    return paths[Math.floor(Math.random() * paths.length)];
  }

  // Fallback data when APIs fail
  getFallbackStories() {
    console.log('Using fallback stories');
    return [
      {
        id: 'fallback1',
        title: 'AI-Powered Developer Tools Platform',
        score: 156,
        descendants: 89,
        url: 'https://example.com'
      },
      {
        id: 'fallback2', 
        title: 'SaaS Solution for Remote Team Management',
        score: 124,
        descendants: 67,
        url: 'https://example.com'
      },
      {
        id: 'fallback3',
        title: 'Mobile App for Health and Fitness Tracking',
        score: 98,
        descendants: 45,
        url: 'https://example.com'
      }
    ];
  }

  getFallbackTrends() {
    console.log('Using fallback trends');
    return [
      {
        title: 'AI Development Tools',
        description: 'Growing trend in AI-powered development assistance and automation tools',
        volumeNumber: '45.2K',
        growthNumber: '+234%',
        volume: '⭐',
        growth: '📈',
        chartPath: "M0,80 Q50,75 100,60 T200,45 T300,20",
        category: 'AI & Machine Learning',
        language: 'Python'
      },
      {
        title: 'React Development',
        description: 'Modern React frameworks and component libraries for web development',
        volumeNumber: '38.7K',
        growthNumber: '+189%',
        volume: '⭐',
        growth: '📈', 
        chartPath: "M0,85 Q75,80 150,50 T300,15",
        category: 'Web Development',
        language: 'JavaScript'
      },
      {
        title: 'Cloud Infrastructure',
        description: 'Tools and platforms for cloud deployment and infrastructure management',
        volumeNumber: '29.1K',
        growthNumber: '+156%',
        volume: '⭐',
        growth: '📈',
        chartPath: "M0,70 Q100,65 200,55 T300,35",
        category: 'Cloud & Infrastructure',
        language: 'Go'
      }
    ];
  }

  // Main methods for components
  async getIdeaOfTheDay() {
    try {
      const stories = await this.fetchHackerNewsStories();
      const ideas = this.processStoriesIntoIdeas(stories);
      
      // Return the most engaging idea (highest score + comments)
      const topIdea = ideas.reduce((best, current) => {
        const currentEngagement = current.score + current.comments;
        const bestEngagement = best.score + best.comments;
        return currentEngagement > bestEngagement ? current : best;
      });

      return topIdea;
    } catch (error) {
      console.error('Error getting idea of the day:', error);
      return this.getFallbackIdea();
    }
  }

  async getAllIdeas() {
    try {
      const stories = await this.fetchHackerNewsStories();
      return this.processStoriesIntoIdeas(stories);
    } catch (error) {
      console.error('Error getting all ideas:', error);
      return [this.getFallbackIdea()];
    }
  }

  async getTrends() {
    try {
      return await this.fetchGitHubTrends();
    } catch (error) {
      console.error('Error getting trends:', error);
      return this.getFallbackTrends();
    }
  }

  getFallbackIdea() {
    console.log('Using fallback idea');
    return {
      id: 'fallback',
      title: 'Real-time Data Integration Platform',
      description: 'A comprehensive platform that aggregates data from multiple sources including social media, news, and developer communities to identify emerging business opportunities and market trends. This solution addresses the growing need for businesses to stay ahead of market developments.',
      tags: [
        { label: 'Data Driven', type: 'advantage', icon: '📊' },
        { label: 'Market Ready', type: 'ready', icon: '✅' },
        { label: 'High Demand', type: 'timing', icon: '🔥' }
      ],
      category: 'Technology',
      moreCount: 12,
      score: 145,
      comments: 78,
      source: 'Fallback'
    };
  }
}

// Export singleton instance
export const dataService = new DataService();