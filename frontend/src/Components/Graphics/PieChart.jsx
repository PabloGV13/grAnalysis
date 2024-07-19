import React from 'react';
import { Pie } from 'react-chartjs-2';
import randomcolor from 'randomcolor';
import 'chart.js';
import 'chart.js/auto';
import chroma from 'chroma-js';

const PieChart = ({ data }) => {

  const labelNumberNights = Object.keys(data)
  const valuesNumberNights = Object.values(data)

  const generateContrastingColors = (numColors) => {
    return chroma.scale(['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#33FFF6', '#F3FF33', '#8E33FF', '#FF8833'])
                .mode('lch')
                .colors(numColors);
  }

  const contrastingColors = [

    '#3357FF', // Blue
    '#FF33A6', // Pink
    '#33FFF6', // Cyan
    '#8E33FF', // Purple
    '#FF8833', // Orange
    '#FF5733', // Red
    '#33FF57', // Green
    '#F3FF33', // Yellow
    '#FFD700', // Gold
    '#00FF00', // Lime
    '#00CED1', // DarkTurquoise
    '#FF4500', // OrangeRed
    '#9400D3', // DarkViolet
    '#FF1493', // DeepPink
    '#00BFFF', // DeepSkyBlue
    '#7CFC00', // LawnGreen
    
  ];


  const generateNightsNumberChartData = (labels, values) => { 
    const backgroundColorsNights = generateContrastingColors(labels.lenght);
    {/*const backgroundColorsNights = randomcolor({ count: labels.length, luminosity: 'bright' });*/}
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

  const generateNightsNumberChartDataStaticColors = (labels, values) => { 
    const backgroundColorsNights = labels.map((_, index) => 
      contrastingColors[index % contrastingColors.length]
    );
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
  
  
  

  const chartData = generateNightsNumberChartDataStaticColors(labelNumberNights,valuesNumberNights);

  return (
    <div align="center" className="pie-chart">
      <Pie data={chartData} />
    </div>
  );
};

export default PieChart;