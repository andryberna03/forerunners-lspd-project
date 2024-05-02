let teachings = [];
const teachingsListElements = document.querySelector('#teaching-list');
const teachingsInputElements = document.querySelector('#teaching-input');

function fetchTeachings() {
    fetch("http://localhost:8081/get_teachings")
        .then((response) => response.json())
        .then(data => {
            // Controlla se data contiene una proprietà result che è un oggetto
            if (typeof data.result === 'object' && data.result !== null) {
                // Accedi direttamente alle proprietà dell'oggetto result
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
            innerElement += `
            <li>${item}</li>`;
        });
    element.innerHTML = innerElement;
    }
}

function filterData(data, searchText) {
    return data.filter ((x) => x.toLowerCase().includes(searchText.toLowerCase()));
}

fetchTeacings();

teachingsInputElements.addEventListener ("input", function () {
    const filteredData = filterData (teachings, teachingsInputElements.value);
    loadData(filteredData, teachingsListElements);
});