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
    const isMobile = window.innerWidth <= 1000;
    
    if (logo) {
        if (isMobile) {
            logo.src = 'https://raw.githubusercontent.com/meluron/assets/refs/heads/main/logos/meluron-codecafe/devquest/icon.png';
            logo.alt = 'DevQuest';
        } else {
            logo.src = 'https://raw.githubusercontent.com/meluron/assets/refs/heads/main/logos/meluron-codecafe/devquest/icon_with_text.png';
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
            if (!searchExpanded) {
                e.preventDefault();
                toggleSearch();
            }
        });
    }
}

function toggleSearch() {
    searchExpanded = !searchExpanded;
    
    const buttonContainer = document.querySelector('.button-container');
    
    if (searchExpanded) {
        searchInputContainer.classList.add("expanded");
        searchBtn.classList.add("active");
        buttonContainer.classList.add("search-expanded");
        
        // Force focus after animation
        setTimeout(() => {
            searchBox.focus();
            searchBox.click();
        }, 300);
    } else {
        searchInputContainer.classList.remove("expanded");
        searchBtn.classList.remove("active");
        buttonContainer.classList.remove("search-expanded");
        searchBox.blur();
    }
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
    
    // Position dropdown
    categoryFilterDropdown.style.left = (rect.left - containerRect.left) + "px";
    categoryFilterDropdown.style.top = (rect.bottom - containerRect.top + 5) + "px";
    categoryFilterDropdown.style.transform = "none";
    
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

function extractOverview(htmlContent, filename) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    
    const headings = doc.querySelectorAll('h1');
    let overviewHTML = '';
    
    for (let heading of headings) {
        const headingText = heading.textContent.trim().toUpperCase();
        
        if (headingText.startsWith('OVERVIEW')) {
            let nextElement = heading.nextElementSibling;
            
            while (nextElement) {
                // Stop at next h1
                if (nextElement.tagName === 'H1') {
                    break;
                }
                
                overviewHTML += nextElement.outerHTML;
                nextElement = nextElement.nextElementSibling;
            }
            break;
        }
    }
    
    return {
        html: overviewHTML,
        found: overviewHTML.length > 0
    };
}

async function showPreview(element, filename) {
    currentPreviewTarget = element;
    
    const rect = element.getBoundingClientRect();
    const container = document.querySelector('.container');
    const containerRect = container.getBoundingClientRect();
    
    previewTooltip.style.position = "absolute";
    previewTooltip.style.left = (rect.left - containerRect.left) + "px";
    previewTooltip.style.top = (rect.bottom - containerRect.top + 10) + "px";
    previewTooltip.style.width = "";
    previewTooltip.style.right = "";
    previewTooltip.style.maxWidth = "500px";
    previewTooltip.style.maxHeight = "";
    
    previewTooltip.innerHTML = `
        <div class="loading">Loading overview...</div>
    `;
    previewTooltip.classList.add("visible");
    
    if (previewCache.has(filename)) {
        const cached = previewCache.get(filename);
        displayOverviewPreview(element.textContent, cached);
        return;
    }
    
    try {
        const response = await fetch(`htmls/${filename}`);
        if (!response.ok) throw new Error('Failed to load');
        
        const htmlContent = await response.text();
        const overviewContent = extractOverview(htmlContent, filename);
        
        previewCache.set(filename, overviewContent);
        
        if (currentPreviewTarget === element) {
            displayOverviewPreview(element.textContent, overviewContent);
        }
        
    } catch (error) {
        if (currentPreviewTarget === element) {
            previewTooltip.innerHTML = `
                <div class="error">Overview preview not available</div>
            `;
        }
    }
}

function displayOverviewPreview(title, overviewContent) {
    let html = ``;
    
    if (!overviewContent.found || !overviewContent.html) {
        html += `<div class="error">Overview not found</div>`;
    } else {
        html += `<div style="font-weight: bold; margin-bottom: 12px; font-size: 16px;">OVERVIEW</div>`;
        html += '<div class="quest-section">';
        html += overviewContent.html;
        html += '</div>';
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
        
        const showDelay = 500;
        const hideDelay = 200;
        
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
        
        link.addEventListener('touchstart', () => {
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(() => {
                showPreview(link, filename);
            }, showDelay);
        });
    });
}

previewTooltip.addEventListener('mouseenter', () => {
    clearTimeout(previewTimeout);
});

previewTooltip.addEventListener('mouseleave', () => {
    hidePreview();
});

// Add event listeners to hide preview
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
    const searchBoxMobile = document.getElementById('searchBoxMobile');
    const searchValue = (searchBox?.value || searchBoxMobile?.value || '').trim();
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
    const searchBoxMobile = document.getElementById('searchBoxMobile');
    const searchQuery = (searchBox?.value || searchBoxMobile?.value || '').toLowerCase();
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

function initializeMobileSearch() {
    const searchBoxMobile = document.getElementById('searchBoxMobile');
    
    if (searchBoxMobile) {
        searchBoxMobile.addEventListener('input', () => {
            renderTable();
            setTimeout(addPreviewListeners, 100);
        });
    }
}

setTimeout(initializeSearchInput, 100);
setTimeout(initializeMobileSearch, 100);