 // Función para mostrar/ocultar pestañas
 function showTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Desactivar todos los botones
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Activar la pestaña seleccionada
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Activar el botón seleccionado
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
}

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

// Opciones comunes para los gráficos
const commonOptions = {
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
};

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
    options: commonOptions
});

// Gráfico de Cultos con Menos Asistencia
const cultosChart = new Chart(document.getElementById('cultosChart'), {
    type: 'bar',
    data: {
        labels: cultosLabels,
        datasets: [{
            label: 'Asistencia',
            data: cultosData,
            backgroundColor: generateColors(cultosLabels.length, 0.7).map(() => 'rgba(76, 201, 240, 0.7)'),
            borderColor: generateColors(cultosLabels.length, 1).map(() => 'rgba(76, 201, 240, 1)'),
            borderWidth: 1
        }]
    },
    options: commonOptions
});

// Actualizar estadísticas de resumen
document.getElementById('totalMiembros').textContent = '150'; // Ejemplo
document.getElementById('totalCultos').textContent = '48'; // Ejemplo
document.getElementById('asistenciaPromedio').textContent = '80%'; // Ejemplo
document.getElementById('ultimoCulto').textContent = '15 Feb'; // Ejemplo

document.getElementById('totalOportunidades').textContent = '120'; // Ejemplo
document.getElementById('totalParticipantes').textContent = '45'; // Ejemplo
document.getElementById('participanteMasActivo').textContent = nombresLabels[0] || 'N/A'; // El primero del top 10
document.getElementById('ultimaOportunidad').textContent = '20 Feb'; // Ejemplo

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

// Gráfico de Participaciones (Nuevo gráfico)
const coloresParticipaciones = [
    'rgba(74, 222, 128, 0.7)', // Verde
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)',
    'rgba(74, 222, 128, 0.7)'
];

const participacionesChart = new Chart(document.getElementById('participacionesChart'), {
    type: 'bar',
    data: {
        labels: nombresLabels,
        datasets: [{
            label: 'Participaciones',
            data: nombresData,
            backgroundColor: coloresParticipaciones,
            borderColor: coloresParticipaciones.map(color => color.replace('0.7', '1')),
            borderWidth: 1
        }]
    },
    options: commonOptions
});

// Gráfico de Tipos de Participación
const tiposParticipacionChart = new Chart(document.getElementById('tiposParticipacionChart'), {
    type: 'pie',
    data: {
        labels: tiposParticipacionLabels,
        datasets: [{
            data: tiposParticipacionData,
            backgroundColor: [
                'rgba(74, 222, 128, 0.7)',
                'rgba(45, 212, 191, 0.7)',
                'rgba(14, 165, 233, 0.7)',
                'rgba(79, 70, 229, 0.7)',
                'rgba(139, 92, 246, 0.7)'
            ],
            borderColor: [
                'rgba(74, 222, 128, 1)',
                'rgba(45, 212, 191, 1)',
                'rgba(14, 165, 233, 1)',
                'rgba(79, 70, 229, 1)',
                'rgba(139, 92, 246, 1)'
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
        }
    }
});

// Gráfico de Tendencia de Participaciones
const tendenciaParticipacionesChart = new Chart(document.getElementById('tendenciaParticipacionesChart'), {
    type: 'line',
    data: {
        labels: tendenciaParticipacionesLabels,
        datasets: [{
            label: 'Participaciones',
            data: tendenciaParticipacionesData,
            borderColor: 'rgba(74, 222, 128, 1)',
            backgroundColor: 'rgba(74, 222, 128, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointBackgroundColor: 'rgba(74, 222, 128, 1)',
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

// Gráfico de Distribución por Género
const generoParticipacionesChart = new Chart(document.getElementById('generoParticipacionesChart'), {
    type: 'doughnut',
    data: {
        labels: generoLabels,
        datasets: [{
            data: generoData,
            backgroundColor: [
                'rgba(14, 165, 233, 0.7)',
                'rgba(236, 72, 153, 0.7)'
            ],
            borderColor: [
                'rgba(14, 165, 233, 1)',
                'rgba(236, 72, 153, 1)'
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