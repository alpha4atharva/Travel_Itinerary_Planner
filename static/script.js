document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('travel-form');
    const generateBtn = document.getElementById('generate-btn');
    const statusBox = document.getElementById('status-box');
    const resultContainer = document.getElementById('result-container');
    const featuresSection = document.getElementById('features-section');
    const itineraryContent = document.getElementById('itinerary-content');
    const downloadBtn = document.getElementById('download-btn');
    const clearBtn = document.getElementById('clear-btn');
    const currencySelect = document.getElementById('currency');
    const budgetLabel = document.getElementById('budget-label');

    // Update budget label when currency changes
    currencySelect.addEventListener('change', (e) => {
        const symbol = e.target.value.split('|')[1];
        budgetLabel.textContent = `💰 Budget / Person (${symbol})`;
    });

    let currentMarkdown = "";

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Gather input values
        const origin = document.getElementById('origin').value;
        const destination = document.getElementById('destination').value;
        const currencyValue = document.getElementById('currency').value;
        const [currencyCode, currencySymbol] = currencyValue.split('|');
        const budget = parseInt(document.getElementById('budget').value);
        const numPersons = parseInt(document.getElementById('num_persons').value);
        const startDate = document.getElementById('start_date').value;
        const numDays = parseInt(document.getElementById('num_days').value);
        
        // Gather multiselect values
        const interestsSelect = document.getElementById('interests');
        const selectedInterests = Array.from(interestsSelect.selectedOptions).map(opt => opt.value).join(', ');

        // Update UI state
        featuresSection.classList.add('hidden');
        resultContainer.classList.add('hidden');
        statusBox.classList.remove('hidden');
        
        const totalBudget = budget * numPersons;
        statusBox.innerHTML = `
            <div class="loading-spinner"></div>
            Planning a <strong>${numDays}-day</strong> trip from <strong>${origin}</strong> → <strong>${destination}</strong> 
            for <strong>${numPersons}</strong> traveler(s) <br>
            Budget: <strong>${currencySymbol}${budget.toLocaleString()}</strong>/person (Total: <strong>${currencySymbol}${totalBudget.toLocaleString()}</strong>)<br><br>
            <small>⏳ Agents are researching, calculating, and compiling your itinerary... This may take 1-2 minutes.</small>
        `;

        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    origin: origin,
                    destination: destination,
                    budget: budget,
                    num_persons: numPersons,
                    currency: currencyCode,
                    currency_symbol: currencySymbol,
                    start_date: startDate,
                    num_days: numDays,
                    interests: selectedInterests || "General sightseeing"
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to generate itinerary');
            }

            const data = await response.json();
            currentMarkdown = data.itinerary;
            
            // Render markdown
            itineraryContent.innerHTML = marked.parse(currentMarkdown);
            
            // Show results
            statusBox.classList.add('hidden');
            resultContainer.classList.remove('hidden');

            // Scroll to results
            resultContainer.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            statusBox.innerHTML = `❌ <strong>Error:</strong> ${error.message}<br><small>Check your API keys in the .env file.</small>`;
            statusBox.style.color = '#b91c1c';
            statusBox.style.backgroundColor = '#fef2f2';
            statusBox.style.borderColor = '#fca5a5';
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 Generate My Itinerary';
        }
    });

    // Handle Download
    downloadBtn.addEventListener('click', () => {
        if (!currentMarkdown) return;
        
        const destination = document.getElementById('destination').value;
        const filename = `itinerary_${destination.replace(/\s+/g, '_').toLowerCase()}.md`;
        
        const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // Handle Clear
    clearBtn.addEventListener('click', () => {
        form.reset();
        resultContainer.classList.add('hidden');
        featuresSection.classList.remove('hidden');
        currentMarkdown = "";
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
