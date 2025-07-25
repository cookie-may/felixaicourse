const fs = require('fs');
const path = require('path');

function countLessons(baseDir) {
    let count = 0;
    function walk(dir) {
        const items = fs.readdirSync(dir);
        for(let item of items) {
            const full = path.join(dir, item);
            if (fs.statSync(full).isDirectory()) walk(full);
            else if (full.endsWith('.md') && full.includes('phases')) count++;
        }
    }
    try { walk(baseDir); } catch(e) {}
    return count;
}

console.log(`Total lessons found: ${countLessons(path.join(__dirname, '..', 'public', 'phases'))}`);
