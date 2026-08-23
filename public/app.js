document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refreshBtn');
    const systemState = document.getElementById('systemState');
    const tableContainer = document.getElementById('tableContainer');
    const tableBody = document.getElementById('tableBody');
    const statsPanel = document.getElementById('statsPanel');

    // Stats Elements
    const statCount = document.getElementById('statCount');
    const statMaxSpread = document.getElementById('statMaxSpread');
    const statTime = document.getElementById('statTime');

    const showLoadingState = () => {
        refreshBtn.disabled = true;
        refreshBtn.querySelector('span').textContent = 'Анализ...';
        refreshBtn.querySelector('svg').classList.add('animate-spin');

        tableContainer.classList.add('hidden');
        statsPanel.classList.add('hidden');

        systemState.classList.remove('hidden');
        systemState.innerHTML = `
            <div class="flex flex-col items-center justify-center gap-4 py-12">
                <div class="relative w-16 h-16">
                    <div class="absolute inset-0 border-4 border-brand-500/20 rounded-full"></div>
                    <div class="absolute inset-0 border-4 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <h3 class="text-xl font-display font-medium text-white tracking-wide">Сканирование рынков</h3>
                <p class="text-sm text-gray-400">Связываемся с API Binance, Bybit, OKX, Kraken. Загружаем тренды CoinGecko...</p>
            </div>
        `;
    };

    const showErrorState = (message) => {
        refreshBtn.disabled = false;
        refreshBtn.querySelector('span').textContent = 'Повторить попытку';
        refreshBtn.querySelector('svg').classList.remove('animate-spin');

        systemState.classList.remove('hidden');
        systemState.innerHTML = `
            <div class="flex flex-col items-center justify-center gap-4 py-12">
                <div class="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mb-2 text-red-500">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-display font-medium text-red-400 tracking-wide">Ошибка Системы</h3>
                <p class="text-sm text-gray-400 max-w-md mx-auto">${message}</p>
            </div>
        `;
    };

    const showEmptyState = () => {
        systemState.classList.remove('hidden');
        systemState.innerHTML = `
            <div class="flex flex-col items-center justify-center gap-4 py-16">
                <div class="w-16 h-16 rounded-full bg-gray-800/50 flex items-center justify-center mb-2 text-gray-500">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-display font-medium text-white tracking-wide">Нет Арбитражных Ситуаций</h3>
                <p class="text-sm text-gray-400">Рынок спокоен. Спреды между биржами минимальны.</p>
            </div>
        `;
    };

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 6
        }).format(value);
    };

    const updateStats = (opportunities) => {
        statCount.textContent = opportunities.length;

        if (opportunities.length > 0) {
            const maxSpread = Math.max(...opportunities.map(o => parseFloat(o.spreadPercentage)));
            statMaxSpread.textContent = `+${maxSpread.toFixed(2)}%`;
            statMaxSpread.className = 'text-3xl font-display font-bold text-brand-accent';
        } else {
            statMaxSpread.textContent = '0.00%';
            statMaxSpread.className = 'text-3xl font-display font-bold text-gray-500';
        }

        const now = new Date();
        statTime.textContent = now.toLocaleTimeString('ru-RU', { hour12: false });
    };

    const renderTable = (opportunities) => {
        tableBody.innerHTML = '';

        opportunities.forEach((opp, index) => {
            const tr = document.createElement('tr');
            tr.style.animationDelay = `${index * 50}ms`;
            tr.className = 'group animate-[fadeIn_0.3s_ease-out_forwards] opacity-0';

            const spreadVal = parseFloat(opp.spreadPercentage);
            const isPositive = spreadVal > 0;
            const spreadColorClass = isPositive ? 'text-brand-accent drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]' : 'text-red-400';
            const spreadPrefix = isPositive ? '+' : '';

            tr.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                        <div class="font-display font-bold text-white text-base">${opp.symbol.split('/')[0]}</div>
                        <div class="text-gray-500 text-xs ml-1 mt-1">/ ${opp.symbol.split('/')[1]}</div>
                    </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="${opp.buyFrom.url}" target="_blank" class="exchange-badge hover:scale-105">
                        ${opp.buyFrom.exchange}
                    </a>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right font-mono text-gray-300">
                    ${formatCurrency(opp.buyFrom.price)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="${opp.sellTo.url}" target="_blank" class="exchange-badge hover:scale-105">
                        ${opp.sellTo.exchange}
                    </a>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right font-mono text-gray-300">
                    ${formatCurrency(opp.sellTo.price)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right font-mono text-white">
                    ${formatCurrency(opp.grossProfit)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right font-mono font-bold ${spreadColorClass}">
                    ${spreadPrefix}${spreadVal.toFixed(2)}%
                </td>
            `;
            tableBody.appendChild(tr);
        });
    };

    const fetchData = async () => {
        showLoadingState();

        try {
            const response = await fetch('/api/arbitrage');
            if (!response.ok) {
                throw new Error(`Сервер вернул код ${response.status}`);
            }
            const data = await response.json();

            if (data.success) {
                updateStats(data.opportunities || []);

                if (data.opportunities && data.opportunities.length > 0) {
                    systemState.classList.add('hidden');
                    renderTable(data.opportunities);
                    tableContainer.classList.remove('hidden');
                    statsPanel.classList.remove('hidden');
                } else {
                    showEmptyState();
                    statsPanel.classList.remove('hidden');
                }
            } else {
                throw new Error('Неизвестный формат ответа от API');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            showErrorState(`Не удалось получить данные: ${error.message}. Возможно сработали лимиты API бирж или Geo-блокировка.`);
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.querySelector('span').textContent = 'Сканировать рынок';
            refreshBtn.querySelector('svg').classList.remove('animate-spin');
        }
    };

    // Add required keyframes dynamically for stagger animations
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);

    // Initial fetch
    fetchData();

    // Event listeners
    refreshBtn.addEventListener('click', fetchData);
});
