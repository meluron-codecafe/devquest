// Global variables
    let chapters = [];
    let filteredChapters = [];
    let activeTag = 'all';
    let searchQuery = '';

    // Function to load chapters data
    async function loadChaptersData() {
      try {
        const response = await fetch('./data/toc.json');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        chapters = await response.json();
        
        filteredChapters = [...chapters];
        generateTags();
        generateChapters();
        setupEventListeners();
      } catch (error) {
        console.error('Could not load toc.json:', error);
        // Show error message to user
        const container = document.getElementById('chapters-container');
        const noResults = document.getElementById('no-results');
        container.style.display = 'none';
        noResults.style.display = 'block';
        noResults.innerHTML = '<p>Error loading chapters data. Please check that toc.json exists and is properly formatted.</p>';
      }
    }

    // Function to generate tag buttons
    function generateTags() {
      const allTags = new Set();
      chapters.forEach(chapter => {
        if (chapter.tags && Array.isArray(chapter.tags)) {
          chapter.tags.forEach(tag => allTags.add(tag));
        }
      });

      const tagFilter = document.getElementById('tag-filter');
      if (!tagFilter) return;
      
      const allButton = tagFilter.querySelector('[data-tag="all"]');
      
      // Clear existing tags except "All"
      const existingTags = tagFilter.querySelectorAll('.tag-button:not([data-tag="all"])');
      existingTags.forEach(tag => tag.remove());

      // Add new tags only if there are any
      if (allTags.size > 0) {
        Array.from(allTags).sort().forEach(tag => {
          const button = document.createElement('button');
          button.className = 'tag-button';
          button.setAttribute('data-tag', tag);
          button.textContent = tag.charAt(0).toUpperCase() + tag.slice(1);
          button.onclick = () => filterByTag(tag);
          tagFilter.appendChild(button);
        });
      }
    }

    // Function to filter chapters by tag
    function filterByTag(tag) {
      activeTag = tag;
      
      // Update active tag button
      document.querySelectorAll('.tag-button').forEach(btn => {
        btn.classList.remove('active');
      });
      document.querySelector(`[data-tag="${tag}"]`).classList.add('active');
      
      applyFilters();
    }

    // Function to search chapters
    function searchChapters(query) {
      searchQuery = query.toLowerCase();
      applyFilters();
    }

    // Function to apply both tag and search filters
    function applyFilters() {
      filteredChapters = chapters.filter(chapter => {
        // Tag filter
        const tagMatch = activeTag === 'all' || (chapter.tags && Array.isArray(chapter.tags) && chapter.tags.includes(activeTag));
        
        // Search filter
        const searchMatch = !searchQuery || 
          (chapter.title && chapter.title.toLowerCase().includes(searchQuery)) ||
          (chapter.description && chapter.description.toLowerCase().includes(searchQuery)) ||
          (chapter.topics && Array.isArray(chapter.topics) && chapter.topics.some(topic => 
            (topic.question && topic.question.toLowerCase().includes(searchQuery)) ||
            (topic.description && topic.description.toLowerCase().includes(searchQuery))
          ));
        
        return tagMatch && searchMatch;
      });
      
      generateChapters();
    }

    // Function to toggle chapter expansion
    function toggleChapter(chapterIndex) {
      const chapterCard = document.querySelector(`[data-chapter="${chapterIndex}"]`);
      const isActive = chapterCard.classList.contains('active');
      
      // Close all chapters
      document.querySelectorAll('.chapter-card').forEach(card => {
        card.classList.remove('active');
      });
      
      // Open clicked chapter if it wasn't already active
      if (!isActive) {
        chapterCard.classList.add('active');
      }
    }

    // Function to generate chapters HTML
    function generateChapters() {
      const container = document.getElementById('chapters-container');
      const noResults = document.getElementById('no-results');
      
      if (!container || !noResults) return;
      
      if (filteredChapters.length === 0) {
        container.style.display = 'none';
        noResults.style.display = 'block';
        return;
      }
      
      container.style.display = 'grid';
      noResults.style.display = 'none';
      container.innerHTML = '';
      
      filteredChapters.forEach((chapter, chapterIndex) => {
        // Safety check for chapter structure
        if (!chapter || !chapter.topics || !Array.isArray(chapter.topics)) {
          console.warn('Invalid chapter structure:', chapter);
          return;
        }
        
        const originalIndex = chapters.indexOf(chapter);
        const chapterCard = document.createElement('div');
        chapterCard.className = 'chapter-card';
        chapterCard.setAttribute('data-chapter', originalIndex);
        chapterCard.onclick = () => toggleChapter(originalIndex);
        
        const chapterNumber = String(originalIndex + 1).padStart(2, '0');
        
        const tagsHTML = (chapter.tags && Array.isArray(chapter.tags)) ? chapter.tags.map(tag => 
          `<span class="chapter-tag">${tag}</span>`
        ).join('') : '';
        
        const statsHTML = `
          <div class="stat-item">
            <span>📚</span>
            <span>${chapter.topics.length} topics</span>
          </div>
          ${chapter.difficulty ? `
            <div class="stat-item">
              <span>⭐</span>
              <span>${chapter.difficulty}</span>
            </div>
          ` : ''}
          ${chapter.estimatedTime ? `
            <div class="stat-item">
              <span>⏱️</span>
              <span>${chapter.estimatedTime}</span>
            </div>
          ` : ''}
        `;
        
        const topicsHTML = chapter.topics.map((topic, topicIndex) => {
          if (!topic) return '';
          const topicNumber = String(topicIndex + 1).padStart(2, '0');
          return `
            <div class="topic-item">
              <div class="topic-header">
                <div class="topic-number">Q-${topicNumber}</div>
                <a href="${topic.filepath || '#'}" class="topic-title">${topic.question || 'Untitled Question'}</a>
              </div>
              <p class="topic-description">${topic.description || ''}</p>
            </div>
          `;
        }).join('');
        
        chapterCard.innerHTML = `
          <div class="chapter-header">
            <div class="chapter-info">
              <div class="chapter-number">CH-${chapterNumber}</div>
              <div class="chapter-title">${chapter.title || 'Untitled Chapter'}</div>
            </div>
            <div class="chapter-toggle">▼</div>
          </div>
          <p class="chapter-description">${chapter.description || ''}</p>
          ${tagsHTML ? `<div class="chapter-tags">${tagsHTML}</div>` : ''}
          <div class="chapter-stats">${statsHTML}</div>
          <div class="topics-container">
            ${topicsHTML}
          </div>
        `;
        
        container.appendChild(chapterCard);
      });
    }

    // Function to setup event listeners
    function setupEventListeners() {
      const searchInput = document.getElementById('search-input');
      if (!searchInput) return;
      
      let searchTimeout;
      
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          searchChapters(e.target.value);
        }, 300);
      });
      
      // Set up "All" tag button
      const allTagButton = document.querySelector('[data-tag="all"]');
      if (allTagButton) {
        allTagButton.onclick = () => filterByTag('all');
      }
    }

    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', loadChaptersData);