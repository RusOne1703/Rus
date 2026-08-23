const ccxt = require('ccxt');

exports.handler = async function (event, context) {
  try {
    // We instantiate the exchanges we want to monitor
    const exchangeIds = ['binance', 'bybit', 'okx', 'kraken'];
    const exchanges = exchangeIds.map(id => new ccxt[id]({ enableRateLimit: true }));

    // Define the pairs we want to look at
    const symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT'];

    let arbitrageOpportunities = [];

    // Process each symbol
    for (const symbol of symbols) {
      const tickers = {};

      // Fetch ticker from each exchange
      await Promise.all(exchanges.map(async (exchange) => {
        try {
          // Check if exchange has this market
          await exchange.loadMarkets();
          if (exchange.markets[symbol]) {
            const ticker = await exchange.fetchTicker(symbol);
            if (ticker && ticker.ask && ticker.bid) {
              tickers[exchange.id] = {
                ask: ticker.ask, // Price to buy
                bid: ticker.bid, // Price to sell
                url: exchange.urls.www,
                name: exchange.name
              };
            }
          }
        } catch (e) {
          console.error(`Failed to fetch ${symbol} from ${exchange.id}: ${e.message}`);
        }
      }));

      // Find the lowest ask (buy price) and highest bid (sell price)
      const exchangeNames = Object.keys(tickers);
      if (exchangeNames.length > 1) {
        let lowestAsk = { price: Infinity, exchange: null };
        let highestBid = { price: 0, exchange: null };

        for (const exId of exchangeNames) {
          const ticker = tickers[exId];
          if (ticker.ask < lowestAsk.price) {
            lowestAsk = { price: ticker.ask, exchange: ticker.name, url: ticker.url };
          }
          if (ticker.bid > highestBid.price) {
            highestBid = { price: ticker.bid, exchange: ticker.name, url: ticker.url };
          }
        }

        // Calculate spread
        if (lowestAsk.exchange && highestBid.exchange) {
          const spreadPercentage = ((highestBid.price - lowestAsk.price) / lowestAsk.price) * 100;
          const grossProfit = highestBid.price - lowestAsk.price;

          arbitrageOpportunities.push({
            symbol: symbol,
            buyFrom: {
              exchange: lowestAsk.exchange,
              price: lowestAsk.price,
              url: lowestAsk.url
            },
            sellTo: {
              exchange: highestBid.exchange,
              price: highestBid.price,
              url: highestBid.url
            },
            spreadPercentage: spreadPercentage.toFixed(4),
            grossProfit: grossProfit.toFixed(4)
          });
        }
      }
    }

    // Sort by largest spread first
    arbitrageOpportunities.sort((a, b) => parseFloat(b.spreadPercentage) - parseFloat(a.spreadPercentage));

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*' // allow CORS for local dev
      },
      body: JSON.stringify({
        success: true,
        timestamp: new Date().toISOString(),
        opportunities: arbitrageOpportunities
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
