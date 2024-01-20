const ctx = document.getElementById('grafico1');
const ctx2 = document.getElementById('grafico2');
const data = document.currentScript.dataset;

let categories = data.categories.split(',')
for (var a = 0; a < categories.length; a++) {
    categories[a] = categories[a].replace("[", "")
    categories[a] = categories[a].replace("]", "")
    categories[a] = categories[a].replace("\"", "")
    categories[a] = categories[a].replace("\'", "")
    categories[a] = categories[a].replace("\'", "")
    categories[a] = categories[a].trim()
}

let dataPerCategory = data.dataPerCategory
dataPerCategory = dataPerCategory.replace("[", "")
dataPerCategory = dataPerCategory.replace("]", "")
dataPerCategory = dataPerCategory.split(',').map(Number)

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Acertos', 'Erros'],
        datasets: [{
            label: 'Qtd',
            data: [parseInt(data.successes, 10), parseInt(data.mistakes, 10)],
            borderWidth: 1
        }]
    }, 
});

new Chart(ctx2, {
    type: 'radar',
    data: {
        labels: categories,
        datasets: [{
            label: 'Qtd',
            data: dataPerCategory,
            borderWidth: 1,
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        }]
    },
});
