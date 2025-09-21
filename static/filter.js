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

// A single function to get all filters, handling nesting
function getFilters() {
    const filtersContainer = document.getElementById('filtersContainer');
    return getNestedFilters(filtersContainer);
}

// Recursively traverses the filter groups to build a nested JSON object.
function getNestedFilters(container) {
    const nestedFilters = [];
    container.querySelectorAll(':scope > .filter-group').forEach(group => {
        const filterData = {};
        
        const input = group.querySelector('input[type="text"]');
        const select = group.querySelector('select');
        
        if (input && select) {
            filterData.type = select.value;
            filterData.value = input.value;
        }

        const nestedFiltersContainer = group.querySelector('.nested-filters');
        if (nestedFiltersContainer && nestedFiltersContainer.children.length > 0) {
            filterData.depth_options = getNestedFilters(nestedFiltersContainer);
        }

        nestedFilters.push(filterData);
    });
    return nestedFilters;
}

// Function to handle the filter action (updating the tree on the page)
function submitFilter() {
    const payload = { filters: getFilters() };

    fetch('/filter', {
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
        return response.text();
    })
    .then(html => {
        document.querySelector('.tree-container').innerHTML = html;
    })
    .catch(error => {
        console.error('There was a problem with the filter operation:', error);
    });
}

// Function to handle the download action (getting a JSON file)
function submitDownload() {
    const payload = { filters: getFilters() };

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

// Creates and returns a new HTML element for a filter group.
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
        <button class="add-depth-btn" type="button">+</button>
        <button class="remove-btn" type="button">-</button>
        <div class="nested-filters"></div>
    `;
    return group;
}