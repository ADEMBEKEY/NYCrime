// Initialize Map
const map = L.map('map').setView([40.7128, -74.0060], 11);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors &copy; <a href=\"https://carto.com/attributions\">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

let marker = L.marker([40.7128, -74.0060], { draggable: true }).addTo(map);

// Update coordinates on click or drag
function updateCoords(lat, lng) {
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lng.toFixed(6);
    document.getElementById('lat-display').textContent = lat.toFixed(4);
    document.getElementById('lng-display').textContent = lng.toFixed(4);
}

map.on('click', (e) => {
    marker.setLatLng(e.latlng);
    updateCoords(e.latlng.lat, e.latlng.lng);
});

marker.on('dragend', () => {
    const latlng = marker.getLatLng();
    updateCoords(latlng.lat, latlng.lng);
});

// Form Submission
const form = document.getElementById('prediction-form');
const predictBtn = document.getElementById('predict-btn');
const welcomeMsg = document.getElementById('welcome-message');
const resultCard = document.getElementById('prediction-result');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI Loading State
    predictBtn.classList.add('loading');
    predictBtn.disabled = true;

    const formData = {
        date: document.getElementById('date').value,
        hour: parseInt(document.getElementById('hour').value),
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        borough: document.getElementById('borough').value,
        precinct: parseInt(document.getElementById('precinct').value),
        place: document.getElementById('place').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        race: document.getElementById('race').value
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Prediction failed');

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        console.error(error);
        alert('Error communicating with the prediction server.');
    } finally {
        predictBtn.classList.remove('loading');
        predictBtn.disabled = false;
    }
});

function displayResult(data) {
    welcomeMsg.classList.add('hidden');
    resultCard.classList.remove('hidden');

    const breakdownContainer = document.getElementById('risk-breakdown');
    const allRisksList = document.getElementById('all-risks-list');
    breakdownContainer.classList.remove('hidden');
    allRisksList.innerHTML = '';

    // 1. Update Primary Risk Card
    const top = data.top_prediction;
    document.getElementById('result-category').textContent = top.category;

    const list = document.getElementById('subcategory-list');
    list.innerHTML = '';
    top.subcategories.slice(0, 8).forEach(sub => {
        const li = document.createElement('li');
        li.textContent = sub;
        list.appendChild(li);
    });

    const confidencePercent = (top.confidence * 100).toFixed(1);
    document.querySelector('.progress').style.width = `${confidencePercent}%`;
    document.getElementById('confidence-value').textContent = `${confidencePercent}%`;

    // 2. Update Risk Breakdown Grid
    data.all_predictions.forEach(pred => {
        const confidence = (pred.confidence * 100).toFixed(1);

        // Determine level class
        let levelClass = 'low';
        if (pred.confidence > 0.6) levelClass = 'high';
        else if (pred.confidence > 0.3) levelClass = 'medium';

        const card = document.createElement('div');
        card.className = `risk-item-card ${levelClass} card`;
        card.innerHTML = `
            <div class="risk-item-header">
                <span class="risk-item-name">${pred.category}</span>
                <span class="risk-item-value">${confidence}%</span>
            </div>
            <div class="risk-item-bar-bg">
                <div class="risk-item-bar" style="width: ${confidence}%"></div>
            </div>
        `;
        allRisksList.appendChild(card);
    });
}

// Set default date to today
document.getElementById('date').valueAsDate = new Date();
