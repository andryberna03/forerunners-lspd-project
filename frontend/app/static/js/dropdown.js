let teachings = [];
const teachingsListElements = document.querySelector('#teaching-list');
const teachingsInputElements = document.querySelector('#teaching-input');

function fetchTeachings() {
    fetch("http://localhost:8081/get_teachings")
        .then((response) => response.json())
        .then(data => {
            // Check if data contains a result property that is an object
            if (typeof data.result === 'object' && data.result !== null) {
                // Access properties of the result object directly
                teachings = Object.keys(data.result).map(key => data.result[key]);
                teachings.sort();
                loadData(teachings, teachingsListElements);
            }
        })
}

function loadData(data, element) {
    if (data) {
        element.innerHTML = "";
        let innerElement = "";
        data.forEach((item) => {
            innerElement += `<li>${item}</li>`;
        });
        element.innerHTML = innerElement;
        
        // Add click event listener to each option
        const options = element.querySelectorAll('li');
        options.forEach(option => {
            option.addEventListener('click', function() {
                teachingsInputElements.value = option.textContent;
                hideDropdown();
            });
        });
    }
}

function filterData(data, searchText) {
    return data.filter((x) => x.toLowerCase().includes(searchText.toLowerCase()));
}

function hideDropdown() {
    teachingsListElements.innerHTML = ""; // Clear the dropdown
}

fetchTeachings();

teachingsInputElements.addEventListener("input", function () {
    const filteredData = filterData(teachings, teachingsInputElements.value);
    loadData(filteredData, teachingsListElements);
});
