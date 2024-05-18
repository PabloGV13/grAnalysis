import React from 'react';
import { Pie } from 'react-chartjs-2';
import randomcolor from 'randomcolor';
import 'chart.js';
import 'chart.js/auto';

const PieChart = ({ data }) => {

  const labelNumberNights = Object.keys(data)
  const valuesNumberNights = Object.values(data)
  
  const generateNightsNumberChartData = (labels, values) => { 
    const backgroundColorsNights = randomcolor({ count: labels.length, luminosity: 'bright' });
    return {
      labels: labels,
      datasets: [
        {
          data: values,
          backgroundColor: backgroundColorsNights,
        },
      ],
    };
  }    
  
  const chartData = generateNightsNumberChartData(labelNumberNights,valuesNumberNights);

  return (
    <div align="center" className="pie-chart">
      <Pie data={chartData} />
    </div>
  );
};

export default PieChart;