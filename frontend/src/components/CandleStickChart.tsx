import React, { useEffect, useRef } from "react";
import Plotly from "plotly.js-dist-min";
import type { Layout, CandlestickData } from "plotly.js";

export interface StockDatum {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface StockData {
  symbol: string;
  timestamp: number;
  data: StockDatum[];
}

interface CandlestickChartProps {
  stockData: StockData | null;
}

const CandlestickChart: React.FC<CandlestickChartProps> = ({ stockData }) => {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (stockData && chartRef.current) {
      const dates = stockData.data.map((item) => item.date);
      const open = stockData.data.map((item) => item.open);
      const high = stockData.data.map((item) => item.high);
      const low = stockData.data.map((item) => item.low);
      const close = stockData.data.map((item) => item.close);

      const trace: Partial<CandlestickData> = {
        x: dates,
        open,
        high,
        low,
        close,
        type: "candlestick",
        name: stockData.symbol,
        increasing: { line: { color: "limegreen" } },
        decreasing: { line: { color: "crimson" } },
      };

      const layout: Partial<Layout> = {
        title: `${stockData.symbol} Stock Price`,
        template: "plotly_dark" as unknown as Layout["template"],
        margin: { t: 40, b: 40, l: 40, r: 40 },
        xaxis: { title: "Date" },
        yaxis: { title: "Price" },
        plot_bgcolor: "#121212",
        paper_bgcolor: "#121212",
      };

      Plotly.react(chartRef.current, [trace], layout, { responsive: true });
    }
  }, [stockData]);

  return <div ref={chartRef} style={{ width: "100%", height: "400px" }} />;
};

export default CandlestickChart;