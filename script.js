// Category colors for dark theme
const categoryColorsDark = [
    "#fd8a09", "#4ade80", "#60a5fa", "#f472b6", "#facc15", "#a78bfa", "#34d399", "#f87171"
];

// Category colors for light theme
const categoryColorsLight = [
    "#dc6803", "#15803d", "#2563eb", "#db2777", "#ca8a04", "#7c3aed", "#0f766e", "#dc2626"
];

let tutorials = [];
let currentCategoryFilter = ''; // DEFAULT TO All Categories
let searchExpanded = false;

const categoryColorMap = {};

function assignCategoryColors() {
    const uniqueCategories = [...new Set(tutorials.map(t => t.category))].sort();
    const colors = currentTheme === 'light' ? categoryColorsLight : categoryColorsDark;
    uniqueCategories.forEach((cat, idx) => {
        categoryColorMap[cat] = colors[idx % colors.length];
    });
}

// Initialize mobile logo and layout
function initializeMobileLayout() {
    const logo = document.getElementById('logo');
    const isMobile = window.innerWidth <= 480;
    
    if (logo) {
        if (isMobile) {
            logo.src = 'https://raw.githubusercontent.com/meluron/assets/refs/heads/main/logos/meluron-codecafe/DevQuest/icon.png';
            logo.alt = 'DevQuest';
        } else {
            logo.src = 'https://raw.githubusercontent.com/meluron/assets/refs/heads/main/logos/meluron-codecafe/DevQuest/icon_with_text.png';
            logo.alt = 'DevQuest Logo';
        }
    }
}

// Update logo on window resize
window.addEventListener('resize', initializeMobileLayout);

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMobileLayout);
} else {
    initializeMobileLayout();
}

let searchBtn, searchInputContainer, searchBox;

function initializeSearch() {
    searchBtn = document.getElementById("searchBtn");
    searchInputContainer = document.getElementById("searchInputContainer");
    searchBox = document.getElementById("searchBox");
    
    if (searchBtn && searchInputContainer && searchBox) {
        searchBtn.addEventListener("click", function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSearch();
        });
        
        searchBtn.addEventListener("touchend", function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSearch();
        });
        
        searchBtn.addEventListener("keydown", function(e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                toggleSearch();
            }
        });

        searchBox.addEventListener("click", function(e) {
            if (window.innerWidth <= 480 && !searchExpanded) {
                e.preventDefault();
                toggleSearch();
            }
        });
    }
}

function toggleSearch() {
    searchExpanded = !searchExpanded;
    
    const buttonContainer = document.querySelector('.button-container');
    const isMobile = window.innerWidth <= 480;
    
    console.log('Search toggled:', searchExpanded, 'Mobile:', isMobile); // Debug log
    
    if (searchExpanded) {
        searchInputContainer.classList.add("expanded");
        searchBtn.classList.add("active");
        buttonContainer.classList.add("search-expanded");
        
        // Force focus after animation
        setTimeout(() => {
            searchBox.focus();
            if (isMobile) {
                searchBox.click();
            }
        }, isMobile ? 100 : 300);
    } else {
        searchInputContainer.classList.remove("expanded");
        searchBtn.classList.remove("active");
        buttonContainer.classList.remove("search-expanded");
        searchBox.blur();
    }
    
    console.log('Classes applied:', {
        expanded: searchInputContainer.classList.contains('expanded'),
        active: searchBtn.classList.contains('active'),
        searchExpanded: buttonContainer.classList.contains('search-expanded')
    }); // Debug log
}

// Enhanced click outside behavior
document.addEventListener("click", (e) => {
    if (searchBtn && searchInputContainer && 
        !searchBtn.contains(e.target) && !searchInputContainer.contains(e.target)) {
        if (searchExpanded) {
            searchExpanded = false;
            searchInputContainer.classList.remove("expanded");
            searchBtn.classList.remove("active");
            document.querySelector('.button-container').classList.remove("search-expanded");
        }
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && searchExpanded) {
        toggleSearch();
    }
});

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSearch);
} else {
    initializeSearch();
}

// Theme management
let currentTheme = 'dark';

const themeToggle = document.getElementById("themeToggle");
const themeIcons = {
    dark: document.querySelector(".theme-icon.dark"),
    light: document.querySelector(".theme-icon.light")
};

function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
    document.body.classList.remove('light-theme', 'dark-theme');
    
    if (theme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.add('dark-theme');
    }
}

function updateThemeToggle() {
    Object.keys(themeIcons).forEach(function(key) {
        themeIcons[key].classList.remove('active');
    });
    
    themeIcons[currentTheme].classList.add('active');
    
    var themeNames = {
        dark: 'Theme: Dark',
        light: 'Theme: Light'
    };
    themeToggle.title = themeNames[currentTheme];
}

function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    applyTheme(currentTheme);
    updateThemeToggle();
    
    if (tutorials.length > 0) {
        assignCategoryColors();
        renderTable();
        setTimeout(addPreviewListeners, 100);
    }
    
    localStorage.setItem('theme-preference', currentTheme);
}

themeToggle.addEventListener("click", toggleTheme);

themeToggle.addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleTheme();
    }
});

currentTheme = getSystemTheme();
applyTheme(currentTheme);
updateThemeToggle();

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    currentTheme = getSystemTheme();
    applyTheme(currentTheme);
    updateThemeToggle();
    
    if (tutorials.length > 0) {
        assignCategoryColors();
        renderTable();
        setTimeout(addPreviewListeners, 100);
    }
    
    localStorage.removeItem('theme-preference');
});

// About modal with enhanced accessibility
const aboutBtn = document.getElementById("aboutBtn");
const aboutModal = document.getElementById("aboutModal");
const aboutModalClose = document.getElementById("aboutModalClose");

aboutBtn.addEventListener("click", openAboutModal);
aboutBtn.addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openAboutModal();
    }
});

function openAboutModal() {
    aboutModal.classList.add("visible");
    aboutModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    aboutModalClose.focus();
}

function closeAboutModal() {
    aboutModal.classList.remove("visible");
    aboutModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    aboutBtn.focus();
}

aboutModalClose.addEventListener("click", closeAboutModal);
aboutModalClose.addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        closeAboutModal();
    }
});

aboutModal.addEventListener("click", (e) => {
    if (e.target === aboutModal) {
        closeAboutModal();
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && aboutModal.classList.contains("visible")) {
        closeAboutModal();
    }
}); 

// Add shake animation CSS
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-4px); }
        75% { transform: translateX(4px); }
    }
`;
document.head.appendChild(shakeStyle);

// Category filter with PASSWORD PROTECTION
const categoryFilterIcon = document.getElementById("categoryFilter");
const categoryFilterDropdown = document.getElementById("categoryFilterDropdown");
let filterDropdownVisible = false;

categoryFilterIcon.addEventListener("click", handleCategoryFilterToggle);
categoryFilterIcon.addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleCategoryFilterToggle(e);
    }
});

function handleCategoryFilterToggle(e) {
    e.preventDefault();
    e.stopPropagation();
    
    if (filterDropdownVisible) {
        hideCategoryFilter();
    } else {
        showCategoryFilterDropdown(categoryFilterIcon)
    }
}

function showCategoryFilterDropdown(triggerElement = null) {
    const categories = [...new Set(tutorials.map(t => t.category))].sort();
    let dropdownContent = `<div class="filter-option ${currentCategoryFilter === '' ? 'active' : ''}" data-category="" role="option">All Categories</div>`;
    
    categories.forEach(cat => {
        dropdownContent += `<div class="filter-option ${currentCategoryFilter === cat ? 'active' : ''}" data-category="${cat}" role="option">${cat}</div>`;
    });
    
    categoryFilterDropdown.innerHTML = dropdownContent;
    
    // Use the trigger element or fall back to the category filter icon
    const referenceElement = triggerElement || categoryFilterIcon;
    const rect = referenceElement.getBoundingClientRect();
    const container = document.querySelector('.container');
    const containerRect = container.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    
    // Position dropdown - simplified since mobile button is removed
    if (viewportWidth <= 480) {
        categoryFilterDropdown.style.left = "50%";
        categoryFilterDropdown.style.transform = "translateX(-50%)";
        categoryFilterDropdown.style.top = (rect.bottom - containerRect.top + 8) + "px";
    } else {
        categoryFilterDropdown.style.left = (rect.left - containerRect.left) + "px";
        categoryFilterDropdown.style.top = (rect.bottom - containerRect.top + 5) + "px";
        categoryFilterDropdown.style.transform = "none";
    }
    
    categoryFilterDropdown.classList.add("visible");
    categoryFilterIcon.classList.add("active");
    filterDropdownVisible = true;
    
    categoryFilterDropdown.querySelectorAll('.filter-option').forEach(option => {
        option.addEventListener('click', handleFilterOptionClick);
        option.addEventListener('keydown', function(e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                handleFilterOptionClick.call(this, e);
            }
        });
        option.setAttribute('tabindex', '0');
    });
}

function handleFilterOptionClick(e) {
    const category = e.target.getAttribute('data-category');
    currentCategoryFilter = category;
    renderTable();
    setTimeout(addPreviewListeners, 100);
    hideCategoryFilter();
}

function hideCategoryFilter() {
    categoryFilterDropdown.classList.remove("visible");
    categoryFilterIcon.classList.remove("active");
    filterDropdownVisible = false;
}

document.addEventListener("click", (e) => {
    if (!categoryFilterIcon.contains(e.target) && !categoryFilterDropdown.contains(e.target)) {
        hideCategoryFilter();
    }
});

// Enhanced preview functionality with image path fixing
const previewTooltip = document.getElementById("previewTooltip");
let previewCache = new Map();
let previewTimeout;
let currentPreviewTarget = null;

function fixImagePaths(htmlContent, filename) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    
    const images = doc.querySelectorAll('img');
    
    images.forEach(img => {
        const src = img.getAttribute('src');
        if (src && src.startsWith('../')) {
            const newSrc = src.replace('../', '');
            img.setAttribute('src', newSrc);
        }
    });
    
    return doc.documentElement.innerHTML;
}

// FIXED EXTRACT QUEST CONTENT FUNCTION
function extractQuestContent(htmlContent, filename) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    
    let questItems = [];
    let questImages = [];
    let authors = [];
    
    // Enhanced quest detection - more flexible text matching
    function isQuestHeading(text) {
        const cleanText = text.trim().toUpperCase()
            .replace(/¶/g, '')
            .replace(/:/g, '')
            .replace(/\s+/g, ' ');
        
        return cleanText === 'QUEST' || 
                cleanText === 'QUESTS' || 
                cleanText.startsWith('QUEST ') ||
                cleanText.endsWith(' QUEST') ||
                cleanText.includes('QUEST:');
    }
    
    // Enhanced author detection
    function isAuthorHeading(text) {
        const cleanText = text.trim().toUpperCase()
            .replace(/¶/g, '')
            .replace(/:/g, '')
            .replace(/\s+/g, ' ');
        
        return cleanText === 'AUTHOR' || 
                cleanText === 'AUTHORS' || 
                cleanText === 'AUTHOR(S)' ||
                cleanText === 'AUTHORS(S)' ||
                cleanText.startsWith('AUTHOR ') ||
                cleanText.startsWith('AUTHORS ') ||
                cleanText.includes('AUTHOR:') ||
                cleanText.includes('AUTHORS:');
    }
    
    // Check if content looks like code/CSS/JS (add this helper function)
    function looksLikeCode(text) {
        const codePatterns = [
            /^\s*[\{\}]/,                    // CSS braces
            /^\s*[\.#][a-zA-Z-_]/,          // CSS selectors
            /^\s*\/\*.*\*\//,               // CSS comments
            /^\s*function\s*\(/,            // JavaScript functions
            /^\s*var\s+|let\s+|const\s+/,  // JavaScript variables
            /^\s*if\s*\(|while\s*\(|for\s*\(/,  // Control structures
            /^\s*<[a-zA-Z]/,                // HTML tags
            /^\s*[a-zA-Z-]+\s*:\s*[^;]*;/,  // CSS properties
            /===+/,                         // Comment separators
            /^\s*\/\/|^\s*#/,              // Comments
            /\w+\(\)/,                      // Function calls
            /\w+\.\w+/                      // Method calls or properties
        ];
        
        return codePatterns.some(pattern => pattern.test(text.trim()));
    }
    
    // Check if content is meaningful Quest content
    function isMeaningfulQuestContent(text) {
        const cleanText = text.trim();
        
        // Too short or too long
        if (cleanText.length < 10 || cleanText.length > 500) {
            return false;
        }
        
        // Looks like code
        if (looksLikeCode(cleanText)) {
            return false;
        }
        
        // Contains too many technical symbols
        const symbolRatio = (cleanText.match(/[\{\}\[\]();:]/g) || []).length / cleanText.length;
        if (symbolRatio > 0.1) {
            return false;
        }
        
        // Should contain some common words
        const commonWords = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'be', 'at', 'have', 'this', 'from', 'or', 'one', 'had', 'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'each', 'which', 'she', 'do', 'how', 'their', 'if', 'will', 'up', 'other', 'about', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'go', 'no', 'way', 'could', 'my', 'than', 'first', 'been', 'call', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part'];
        const words = cleanText.toLowerCase().split(/\s+/);
        const hasCommonWords = words.some(word => commonWords.includes(word));
        
        return hasCommonWords;
    }
    
    // First, try to find quest content by heading
    const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6');
    let questContainer = null;
    let foundQuestHeading = false;
    
    for (let heading of headings) {
        const headingText = heading.textContent || heading.innerText || '';
        
        if (isQuestHeading(headingText)) {
            foundQuestHeading = true;
            console.log(`Found quest heading: "${headingText}"`);
            
            // Strategy 1: Look for next meaningful sibling
            let nextElement = heading.nextElementSibling;
            while (nextElement) {
                // Skip empty elements
                if (nextElement.textContent.trim().length === 0) {
                    nextElement = nextElement.nextElementSibling;
                    continue;
                }
                
                // Found content - check if it's another heading
                if (nextElement.tagName && nextElement.tagName.match(/^H[1-6]$/)) {
                    break; // Stop if we hit another heading
                }
                
                // Check if this is meaningful quest content
                const elementText = nextElement.textContent.trim();
                if (elementText.length > 0 && isMeaningfulQuestContent(elementText)) {
                    questContainer = nextElement;
                    break;
                }
                
                nextElement = nextElement.nextElementSibling;
            }
            
            // Strategy 2: If no sibling found, collect all content until next heading
            if (!questContainer) {
                const parentElement = heading.parentElement;
                if (parentElement) {
                    let foundHeading = false;
                    let contentElements = [];
                    
                    for (let child of parentElement.children) {
                        if (child === heading) {
                            foundHeading = true;
                            continue;
                        }
                        
                        if (foundHeading) {
                            // Stop at next heading
                            if (child.tagName && child.tagName.match(/^H[1-6]$/)) {
                                break;
                            }
                            
                            // Only collect meaningful content
                            const childText = child.textContent.trim();
                            if (childText.length > 0 && isMeaningfulQuestContent(childText)) {
                                contentElements.push(child);
                            }
                        }
                    }
                    
                    if (contentElements.length > 0) {
                        questContainer = doc.createElement('div');
                        contentElements.forEach(el => questContainer.appendChild(el.cloneNode(true)));
                    }
                }
            }
            
            if (questContainer) {
                break; // Found quest content, stop looking
            }
        }
    }
    
    // Fallback: Search for quest content by text patterns (only if no heading found yet)
    if (!foundQuestHeading && !questContainer) {
        console.log('No quest heading found, trying text-based search...');
        
        const allElements = doc.querySelectorAll('*');
        for (let element of allElements) {
            const elementText = element.textContent || element.innerText || '';
            
            if (isQuestHeading(elementText) && elementText.length < 50) {
                foundQuestHeading = true;
                // Found quest marker, look for content nearby
                let searchElement = element.parentElement || element;
                
                // Try to find list or paragraph content after this element
                const nextContent = searchElement.nextElementSibling ||
                                    element.nextElementSibling ||
                                    searchElement.querySelector('ul, ol, p, div');
                
                if (nextContent) {
                    const nextText = nextContent.textContent.trim();
                    if (nextText.length > 0 && isMeaningfulQuestContent(nextText)) {
                        questContainer = nextContent;
                        break;
                    }
                }
            }
        }
    }
    
    // Process the found quest container
    if (questContainer) {
        console.log('Processing quest container:', questContainer.tagName);
        
        // Extract list items
        const listItems = questContainer.querySelectorAll('li');
        if (listItems.length > 0) {
            console.log(`Found ${listItems.length} list items`);
            listItems.forEach((item, index) => {
                const itemText = (item.textContent || item.innerText || '').trim();
                if (itemText && itemText.length > 3 && isMeaningfulQuestContent(itemText)) {
                    questItems.push(itemText);
                }
            });
        }
        
        // Extract paragraphs if no list items
        if (questItems.length === 0) {
            const paragraphs = questContainer.querySelectorAll('p');
            if (paragraphs.length > 0) {
                console.log(`Found ${paragraphs.length} paragraphs`);
                paragraphs.forEach((p) => {
                    const pText = (p.textContent || p.innerText || '').trim();
                    if (pText && pText.length > 10 && pText.length < 1000 && isMeaningfulQuestContent(pText)) {
                        questItems.push(pText);
                    }
                });
            }
        }
        
        // Only try text extraction if we have meaningful content and no items yet
        if (questItems.length === 0) {
            const allText = questContainer.textContent || questContainer.innerText || '';
            console.log('Extracting from raw text, length:', allText.length);
            
            // Only proceed if the text looks meaningful
            if (isMeaningfulQuestContent(allText)) {
                // Try numbered list pattern (1. 2. 3. etc.)
                const numberedMatches = allText.match(/\d+\.\s+[^.]*?(?=\d+\.|$)/gs);
                if (numberedMatches && numberedMatches.length > 0) {
                    console.log(`Found ${numberedMatches.length} numbered items`);
                    numberedMatches.forEach(match => {
                        const cleanItem = match.replace(/^\d+\.\s*/, '').trim();
                        if (cleanItem.length > 5 && isMeaningfulQuestContent(cleanItem)) {
                            questItems.push(cleanItem);
                        }
                    });
                }
                
                // Try bullet point patterns
                if (questItems.length === 0) {
                    const bulletMatches = allText.match(/[-•*]\s+[^\n\r]*(?:\n(?!\s*[-•*])[^\n\r]*)*/g);
                    if (bulletMatches && bulletMatches.length > 0) {
                        console.log(`Found ${bulletMatches.length} bullet items`);
                        bulletMatches.forEach(match => {
                            const cleanItem = match.replace(/^[-•*]\s*/, '').trim();
                            if (cleanItem.length > 5 && isMeaningfulQuestContent(cleanItem)) {
                                questItems.push(cleanItem);
                            }
                        });
                    }
                }
                
                // Try line-based extraction as last resort
                if (questItems.length === 0) {
                    const lines = allText.split(/\r?\n/).filter(line => {
                        const trimmed = line.trim();
                        return trimmed.length > 10 && isMeaningfulQuestContent(trimmed);
                    });
                    if (lines.length > 0 && lines.length <= 10) {
                        console.log(`Found ${lines.length} meaningful text lines`);
                        questItems = lines.map(line => line.trim());
                    }
                }
            }
        }
        
        // Extract images
        const images = questContainer.querySelectorAll('img');
        images.forEach(img => {
            let src = img.getAttribute('src');
            if (src) {
                // Fix relative paths
                if (src.startsWith('../')) {
                    src = src.replace('../', '');
                }
                questImages.push({
                    src: src,
                    alt: img.getAttribute('alt') || 'Quest image',
                    title: img.getAttribute('title') || ''
                });
            }
        });
        
        console.log(`Extracted ${questItems.length} quest items and ${questImages.length} images`);
    } else if (foundQuestHeading) {
        console.log('Found quest heading but no meaningful content');
    } else {
        console.log('No quest container or heading found');
    }
    
    // Extract author information
    const allHeadings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6');
    let authorContainer = null;
    
    for (let heading of allHeadings) {
        const headingText = heading.textContent || heading.innerText || '';
        
        if (isAuthorHeading(headingText)) {
            console.log(`Found author heading: "${headingText}"`);
            
            // Look for next meaningful content
            let nextElement = heading.nextElementSibling;
            while (nextElement) {
                // Skip empty elements
                if (nextElement.textContent.trim().length === 0) {
                    nextElement = nextElement.nextElementSibling;
                    continue;
                }
                
                // Stop if we hit another heading
                if (nextElement.tagName && nextElement.tagName.match(/^H[1-6]$/)) {
                    break;
                }
                
                // Found author content
                if (nextElement.textContent.trim().length > 0) {
                    authorContainer = nextElement;
                    break;
                }
                
                nextElement = nextElement.nextElementSibling;
            }
            
            if (authorContainer) {
                break; // Found author content, stop looking
            }
        }
    }
    
    // Process author information
    if (authorContainer) {
        const authorText = authorContainer.textContent || authorContainer.innerText || '';
        console.log('Processing author text:', authorText);
        
        // Split by commas and clean up
        if (authorText.trim()) {
            authors = authorText.split(',')
                .map(author => author.trim())
                .filter(author => author.length > 0 && author.length < 100)
                .slice(0, 10); // Limit to reasonable number of authors
            
            console.log(`Extracted ${authors.length} authors:`, authors);
        }
    }

    return { 
        items: questItems,
        images: questImages,
        authors: authors,
        found: foundQuestHeading,  // Changed: return true if heading found, regardless of content
        hasContent: questItems.length > 0 || questImages.length > 0  // New: indicates if actual content found
    };
}

async function showPreview(element, filename) {
    currentPreviewTarget = element;
    
    const rect = element.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const isMobile = viewportWidth <= 480;
    
    if (isMobile) {
        previewTooltip.style.position = "fixed";
        previewTooltip.style.left = "12px";
        previewTooltip.style.right = "12px";
        previewTooltip.style.width = "calc(100vw - 24px)";
        previewTooltip.style.maxWidth = "calc(100vw - 24px)";
        previewTooltip.style.top = (rect.bottom + 10) + "px";
        previewTooltip.style.maxHeight = "calc(100vh - " + (rect.bottom + 30) + "px)";
    } else {
        const container = document.querySelector('.container');
        const containerRect = container.getBoundingClientRect();
        previewTooltip.style.position = "absolute";
        previewTooltip.style.left = (rect.left - containerRect.left) + "px";
        previewTooltip.style.top = (rect.bottom - containerRect.top + 10) + "px";
        previewTooltip.style.width = "";
        previewTooltip.style.right = "";
        previewTooltip.style.maxWidth = "500px";
        previewTooltip.style.maxHeight = "";
    }
    
    previewTooltip.innerHTML = `
        <div class="loading">Loading quest preview...</div>
    `;
    previewTooltip.classList.add("visible");
    
    if (previewCache.has(filename)) {
        const cached = previewCache.get(filename);
        displayQuestPreview(element.textContent, cached);
        return;
    }
    
    try {
        const response = await fetch(`htmls/${filename}`);
        if (!response.ok) throw new Error('Failed to load');
        
        const htmlContent = await response.text();
        const questContent = extractQuestContent(htmlContent, filename);
        
        previewCache.set(filename, questContent);
        
        if (currentPreviewTarget === element) {
            displayQuestPreview(element.textContent, questContent);
        }
        
    } catch (error) {
        if (currentPreviewTarget === element) {
            previewTooltip.innerHTML = `
                <div class="error">Quest preview not available</div>
            `;
        }
    }
}

// FIXED DISPLAY QUEST PREVIEW FUNCTION
function displayQuestPreview(title, questContent) {
    let html = ``;
    
    if (!questContent.found) {
        // No quest heading found at all
        html += `<div class="error">Quest section not found</div>`;
    } else if (!questContent.hasContent) {
        // Quest heading found but no meaningful content
        html += `
            <div class="error">Quest content not found</div>
        `;
    } else if (questContent.items && questContent.items.length > 0) {
        // Quest content found and processed
        html += '<div class="quest-section">';
        
        questContent.items.forEach((item, index) => {
            const cleanItem = item.replace(/^\d+\.?\s*/, '').trim();
            html += `<div style="margin: 8px 0; color: var(--text-color);">${index + 1}. ${cleanItem}</div>`;
        });
        
        html += '</div>';
        
        if (questContent.images && questContent.images.length > 0) {
            html += '<div style="margin-top: 12px;">';
            questContent.images.forEach(image => {
                html += `<img src="${image.src}" alt="${image.alt}" title="${image.title}" style="max-width: 100%; height: auto; max-height: 150px; border-radius: 4px; margin: 4px 0;">`;
            });
            html += '</div>';
        }
    } else {
        // Fallback case - shouldn't happen with new logic but keeping for safety
        html += `<div class="error">Quest preview not available</div>`;
    }
    
    // Add authors section if available
    if (questContent.authors && questContent.authors.length > 0) {
        html += `
            <div class="quest-section" 
                style="display: flex; justify-content: flex-end; align-items: center; gap: 6px; 
                        font-size: 13px; color: var(--text-color); text-align: right;
                        border-top: 1px solid var(--border-color); padding-top: 8px; margin-top: 12px;">
                <span style="font-weight: 600; font-style: italic;">
                    ~ Author(s): 
                </span>
                <span style="font-style: italic;">
                    ${questContent.authors.join(', ')}
                </span>
            </div>
        `;
    }
    
    previewTooltip.innerHTML = html;
}

function hidePreview() {
    previewTooltip.classList.remove("visible");
    currentPreviewTarget = null;
}

function addPreviewListeners() {
    const topicLinks = document.querySelectorAll('#tutorialTable a');
    
    topicLinks.forEach(link => {
        const filename = link.getAttribute('href').replace('htmls/', '');
        
        const isMobile = window.innerWidth <= 480;
        const showDelay = isMobile ? 800 : 500;
        const hideDelay = isMobile ? 300 : 200;
        
        link.addEventListener('mouseenter', () => {
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(() => {
                showPreview(link, filename);
            }, showDelay);
        });
        
        link.addEventListener('mouseleave', () => {
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(() => {
                hidePreview();
            }, hideDelay);
        });
        
        if (isMobile) {
            link.addEventListener('touchstart', () => {
                clearTimeout(previewTimeout);
                previewTimeout = setTimeout(() => {
                    showPreview(link, filename);
                }, showDelay);
            });
        }
    });
}

previewTooltip.addEventListener('mouseenter', () => {
    clearTimeout(previewTimeout);
});

previewTooltip.addEventListener('mouseleave', () => {
    hidePreview();
});

// Add mobile-specific event listeners to hide preview
document.addEventListener('scroll', () => {
    if (currentPreviewTarget) {
        hidePreview();
    }
}, { passive: true });

document.addEventListener('touchstart', (e) => {
    if (currentPreviewTarget && !previewTooltip.contains(e.target)) {
        const topicLinks = document.querySelectorAll('#tutorialTable a');
        let clickedOnLink = false;
        topicLinks.forEach(link => {
            if (link.contains(e.target)) {
                clickedOnLink = true;
            }
        });
        if (!clickedOnLink) {
            hidePreview();
        }
    }
}, { passive: true });

document.addEventListener('click', (e) => {
    const isMobile = window.innerWidth <= 480;
    if (isMobile && currentPreviewTarget && !previewTooltip.contains(e.target)) {
        const topicLinks = document.querySelectorAll('#tutorialTable a');
        let clickedOnLink = false;
        topicLinks.forEach(link => {
            if (link.contains(e.target)) {
                clickedOnLink = true;
            }
        });
        if (!clickedOnLink) {
            hidePreview();
        }
    }
});

// Enhanced request topic functionality
function setupRequestTopicLink() {
    const requestLink = document.getElementById('requestTopicLink');
    
    requestLink.addEventListener('click', handleRequestTopicClick);
    requestLink.addEventListener('keydown', function(e) {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            handleRequestTopicClick();
        }
    });
}

function handleRequestTopicClick() {
    const searchValue = searchBox.value.trim();
    const capitalizedValue = searchValue.charAt(0).toUpperCase() + searchValue.slice(1);
    
    const baseUrl = "https://github.com/meluron-codecafe/DevQuest/issues/new";
    const params = new URLSearchParams({
        assignees: "ankit0anand0",
        labels: "tutorials",
        projects: "",
        template: "",
        title: searchValue ? `[TUTORIAL REQUEST] ${capitalizedValue}` : "[TUTORIAL REQUEST]"
    });
    window.open(`${baseUrl}?${params.toString()}`, "_blank");
}

// Load and render data
fetch('tutorials.csv')
.then(response => response.text())
.then(data => {
    const parsed = Papa.parse(data, {
        header: true,
        skipEmptyLines: true
    });
    
    tutorials = parsed.data.map(row => ({
        category: row.category || '',
        topic: row.topic || '',
        keywords: row.keywords || '',
        filename: row.html || ''
    }));
    
    assignCategoryColors();
    renderTable();
    setupRequestTopicLink();
    
    setTimeout(addPreviewListeners, 100);
});

function renderTable() {
    const searchQuery = searchBox.value.toLowerCase();
    const tableBody = document.querySelector('#tutorialTable tbody');
    const noResultsDiv = document.getElementById('noResults');
    const tableWrapper = document.querySelector('.table-wrapper');
    
    tableBody.innerHTML = '';
    
    const filteredTutorials = tutorials.filter(t =>
        (!currentCategoryFilter || t.category.toLowerCase() === currentCategoryFilter.toLowerCase()) &&
        (!searchQuery || (t.topic + ' ' + t.keywords).toLowerCase().includes(searchQuery))
    );
    
    if (filteredTutorials.length === 0) {
        tableWrapper.style.display = 'none';
        noResultsDiv.style.display = 'block';
    } else {
        tableWrapper.style.display = 'block';
        noResultsDiv.style.display = 'none';
        
        filteredTutorials.forEach(t => {
            const tr = document.createElement('tr');
            const color = categoryColorMap[t.category] || "#ddd";
            tr.innerHTML = `
            <td class="category" style="color: ${color};" data-label="Category">
                ${t.category}
            </td>
            <td data-label="Topic"><a href="htmls/${t.filename}">${t.topic}</a></td>
            <td data-label="Keywords">${t.keywords || '-'}</td>
        `;
            tableBody.appendChild(tr);
        });
    }
}

function initializeSearchInput() {
    if (searchBox) {
        searchBox.addEventListener('input', () => {
            renderTable();
            setTimeout(addPreviewListeners, 100);
        });
    }
}

setTimeout(initializeSearchInput, 100);