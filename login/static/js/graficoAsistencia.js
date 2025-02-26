

    // Datos de ejemplo para tendencia de asistencia (reemplazar con datos reales)
    const tendenciaLabels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct'];
    const tendenciaData = [78, 82, 75, 70, 85, 80, 83, 79, 88, 82];
    
    // Datos de ejemplo para distribución por grupos (reemplazar con datos reales)
    const gruposLabels = ['Jóvenes', 'Damas', 'Caballero', 'General', 'Estudios'];
    const gruposData = [25, 40, 15, 10, 10];
    
    // Actualizar estadísticas de resumen
    document.getElementById('totalMiembros').textContent = '150'; // Ejemplo
    document.getElementById('totalCultos').textContent = '48'; // Ejemplo
    document.getElementById('asistenciaPromedio').textContent = '80%'; // Ejemplo
    document.getElementById('ultimoCulto').textContent = '15 Feb'; // Ejemplo

    // Configuración general para todos los gráficos
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#6c757d';
    
    // Función para crear una paleta de colores
    function generateColors(n, opacity) {
        const baseColors = [
            [247, 37, 133], // Rosa
            [76, 201, 240],  // Azul claro
            [67, 97, 238],   // Azul
            [58, 12, 163],   // Púrpura oscuro
            [114, 9, 183]    // Violeta
        ];
        
        let colors = [];
        for (let i = 0; i < n; i++) {
            const color = baseColors[i % baseColors.length];
            colors.push(`rgba(${color[0]}, ${color[1]}, ${color[2]}, ${opacity})`);
        }
        return colors;
    }

    // Gráfico de Inasistencias
    const inasistenciasChart = new Chart(document.getElementById('inasistenciasChart'), {
        type: 'bar',
        data: {
            labels: inasistenciasLabels,
            datasets: [{
                label: 'Inasistencias',
                data: inasistenciasData,
                backgroundColor: generateColors(inasistenciasLabels.length, 0.7),
                borderColor: generateColors(inasistenciasLabels.length, 1),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    padding: 10,
                    cornerRadius: 4
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    // Gráfico de Cultos con Menos Asistencia
    const cultosChart = new Chart(document.getElementById('cultosChart'), {
        type: 'bar',
        data: {
            labels: cultosLabels,
            datasets: [{
                label: 'Asistencia',
                data: cultosData,
                backgroundColor: generateColors(cultosLabels.length, 0.7).map((_, i) => `rgba(76, 201, 240, 0.7)`),
                borderColor: generateColors(cultosLabels.length, 1).map((_, i) => `rgba(76, 201, 240, 1)`),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    padding: 10,
                    cornerRadius: 4
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Gráfico de Tendencia de Asistencia
    const tendenciaChart = new Chart(document.getElementById('tendenciaChart'), {
        type: 'line',
        data: {
            labels: tendenciaLabels,
            datasets: [{
                label: 'Asistencia (%)',
                data: tendenciaData,
                borderColor: 'rgba(72, 149, 239, 1)',
                backgroundColor: 'rgba(72, 149, 239, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointBackgroundColor: 'rgba(72, 149, 239, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    padding: 10,
                    cornerRadius: 4
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Gráfico de Distribución por Grupos
    const gruposChart = new Chart(document.getElementById('gruposChart'), {
        type: 'doughnut',
        data: {
            labels: gruposLabels,
            datasets: [{
                data: gruposData,
                backgroundColor: [
                    'rgba(247, 37, 133, 0.7)',
                    'rgba(76, 201, 240, 0.7)',
                    'rgba(67, 97, 238, 0.7)',
                    'rgba(58, 12, 163, 0.7)',
                    'rgba(114, 9, 183, 0.7)'
                ],
                borderColor: [
                    'rgba(247, 37, 133, 1)',
                    'rgba(76, 201, 240, 1)',
                    'rgba(67, 97, 238, 1)',
                    'rgba(58, 12, 163, 1)',
                    'rgba(114, 9, 183, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        boxWidth: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    padding: 10,
                    cornerRadius: 4
                }
            },
            cutout: '60%'
        }
    });