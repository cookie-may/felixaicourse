const fs = require('fs');

class DataSynthesizer {
    constructor(seed) {
        this.seed = seed;
    }

    randomGaussian(mean = 0, stdev = 1) {
        const u = 1 - Math.random(); 
        const v = Math.random();
        const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
        return z * stdev + mean;
    }

    generateClusters(numPoints, numClusters, dims=2) {
        const data = [];
        for(let c=0; c<numClusters; c++) {
            const centroid = Array.from({length: dims}, () => (Math.random() * 10) - 5);
            for(let p=0; p<numPoints; p++) {
                const point = centroid.map(val => this.randomGaussian(val, 1.5));
                data.push({ point, label: c });
            }
        }
        return data;
    }
    
    exportCSV(data, filename) {
        let csv = 'x,y,label\n';
        data.forEach(d => {
            csv += `${d.point[0]},${d.point[1]},${d.label}\n`;
        });
        fs.writeFileSync(filename, csv);
    }
}

module.exports = DataSynthesizer;
