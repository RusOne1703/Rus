document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refreshBtn');
    const statusDiv = document.getElementById('status');
    const table = document.getElementById('arbitrageTable');
    const tableBody = document.getElementById('tableBody');

    const fetchData = async () => {
        statusDiv.style.display = 'block';
        statusDiv.textContent = 'Сканируем биржи... (темка грузится, подожди)';
        statusDiv.className = 'loading';
        table.style.display = 'none';
        refreshBtn.disabled = true;

        try {
            // Note: with netlify.toml the redirect will map /api/arbitrage to /.netlify/functions/arbitrage
            const response = await fetch('/api/arbitrage');
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            const data = await response.json();

            if (data.success && data.opportunities) {
                renderTable(data.opportunities);
                statusDiv.style.display = 'none';
                table.style.display = 'table';
            } else {
                throw new Error('Данные не получены или ошибка сервера');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            statusDiv.textContent = `Ошибка: ${error.message} (возможно лимиты API, попробуй позже)`;
            statusDiv.className = 'error';
        } finally {
            refreshBtn.disabled = false;
        }
    };

    const renderTable = (opportunities) => {
        tableBody.innerHTML = ''; // Clear previous data

        if (opportunities.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = 7;
            td.textContent = 'Нет данных или связок не найдено.';
            td.style.textAlign = 'center';
            tr.appendChild(td);
            tableBody.appendChild(tr);
            return;
        }

        opportunities.forEach(opp => {
            const tr = document.createElement('tr');

            const spreadClass = parseFloat(opp.spreadPercentage) > 0 ? 'spread-positive' : 'spread-negative';

            tr.innerHTML = `
                <td><strong>${opp.symbol}</strong></td>
                <td><a href="${opp.buyFrom.url}" target="_blank" style="color: inherit; text-decoration: underline;">${opp.buyFrom.exchange}</a></td>
                <td>$${parseFloat(opp.buyFrom.price).toFixed(4)}</td>
                <td><a href="${opp.sellTo.url}" target="_blank" style="color: inherit; text-decoration: underline;">${opp.sellTo.exchange}</a></td>
                <td>$${parseFloat(opp.sellTo.price).toFixed(4)}</td>
                <td>$${parseFloat(opp.grossProfit).toFixed(4)}</td>
                <td class="${spreadClass}">${opp.spreadPercentage}%</td>
            `;
            tableBody.appendChild(tr);
        });
    };

    // Auto-fetch on load
    fetchData();

    // Fetch on button click
    refreshBtn.addEventListener('click', fetchData);
});
