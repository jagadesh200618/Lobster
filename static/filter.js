document.addEventListener('DOMContentLoaded', () => {
    const filtersContainer = document.getElementById('filtersContainer');
    const addLayerBtn = document.getElementById('addLayerBtn');

    if (addLayerBtn) {
        addLayerBtn.addEventListener('click', () => {
            filtersContainer.appendChild(createFilterGroup());
        });
    }

    if (filtersContainer) {
        filtersContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-depth-btn')) {
                const nestedContainer = e.target.closest('.filter-group').querySelector('.nested-filters');
                if (nestedContainer) {
                    nestedContainer.appendChild(createFilterGroup());
                }
            } else if (e.target.classList.contains('remove-btn')) {
                const filterGroup = e.target.closest('.filter-group');
                if (filterGroup) {
                    filterGroup.remove();
                }
            }
        });
    }
});

/**
 * Creates and returns a new HTML element for a filter group.
 * @returns {HTMLElement} The new filter group element.
 */
function createFilterGroup() {
    const group = document.createElement('div');
    group.className = 'filter-group';
    group.innerHTML = `
        <input type="text" placeholder="Value...">
        <select>
            <option value="xpath">XPath</option>
            <option value="tagname">Tag Name</option>
            <option value="text">Text</option>
        </select>
        <button class="add-depth-btn">+</button>
        <button class="remove-btn">-</button>
        <div class="nested-filters"></div>
    `;
    return group;
}

/**
 * Submits the form data by converting it into a JSON object and
 * placing it into a hidden input field.
 * @param {string} action - The URL endpoint for the form submission.
 */
function submitFilter(url) {
    // Get the container for the filters
    const filterContainer = document.getElementById('filtersContainer');
    const filters = [];
    
    // Iterate through each filter-group div
    filterContainer.querySelectorAll('.filter-group').forEach(group => {
        const filterData = {};
        
        // Find input and select elements within the group
        const input = group.querySelector('input[type="text"]');
        const select = group.querySelector('select');
        
        if (input && select) {
            filterData.type = select.value;
            filterData.value = input.value;
        }

        // Handle nested filters (if any)
        const nestedFiltersContainer = group.querySelector('.nested-filters');
        if (nestedFiltersContainer && nestedFiltersContainer.innerHTML.trim() !== '') {
            filterData.depth_options = getNestedFilters(nestedFiltersContainer);
        }
        
        filters.push(filterData);
    });

    const payload = {
        filters: filters
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.text())
    .then(html => {
        // Find the main-container and replace its content with the new HTML
        const mainContainer = document.querySelector('.main-container');
        if (mainContainer) {
            mainContainer.innerHTML = html;
        }
    })
    .catch(error => console.error('Error:', error));
}

function submitDownload() {

     // Get the container for the filters
    const filterContainer = document.getElementById('filtersContainer');
    const filters = [];
    
    // Iterate through each filter-group div
    filterContainer.querySelectorAll('.filter-group').forEach(group => {
        const filterData = {};
        
        // Find input and select elements within the group
        const input = group.querySelector('input[type="text"]');
        const select = group.querySelector('select');
        
        if (input && select) {
            filterData.type = select.value;
            filterData.value = input.value;
        }

        // Handle nested filters (if any)
        const nestedFiltersContainer = group.querySelector('.nested-filters');
        if (nestedFiltersContainer && nestedFiltersContainer.innerHTML.trim() !== '') {
            filterData.depth_options = getNestedFilters(nestedFiltersContainer);
        }
        
        filters.push(filterData);
    });

    const payload = {
        filters: filters
    };

    fetch('/download', {
        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'result.json';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(downloadUrl);
    })
    .catch(error => {
        console.error('There was a problem with the download operation:', error);
    });
}

/**
 * Recursively traverses the filter groups to build a nested JSON object.
 * @param {HTMLElement} container - The HTML element to start the traversal from.
 * @returns {Array<Object>} An array of filter objects.
 */
function getNestedFilters(container) {
    const nestedFilters = [];
    container.querySelectorAll('.filter-group').forEach(group => {
        const filterData = {};
        
        const input = group.querySelector('input[type="text"]');
        const select = group.querySelector('select');
        
        if (input && select) {
            filterData.type = select.value;
            filterData.value = input.value;
        }

        const nestedFiltersContainer = group.querySelector('.nested-filters');
        if (nestedFiltersContainer && nestedFiltersContainer.innerHTML.trim() !== '') {
            filterData.depth_options = getNestedFilters(nestedFiltersContainer);
        }

        nestedFilters.push(filterData);
    });
    return nestedFilters;
}