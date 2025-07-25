/**
 * Felix AI Curriculum - Advanced Metrics Engine
 * 
 * This utility provides standalone metrics calculation decoupled from Python modules,
 * written in JS to ensure environment flexibility and demonstrate polyglot integration.
 */

function computeCosineSimilarity(vecA, vecB) {
    if (vecA.length !== vecB.length) return 0;
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < vecA.length; i++) {
        dotProduct += vecA[i] * vecB[i];
        normA += vecA[i] ** 2;
        normB += vecB[i] ** 2;
    }
    
    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

function calculateMSE(yTrue, yPred) {
    if (yTrue.length !== yPred.length) throw new Error("Mismatched dimensions");
    let errorSum = 0;
    for (let i = 0; i < yTrue.length; i++) {
        errorSum += Math.pow(yTrue[i] - yPred[i], 2);
    }
    return errorSum / yTrue.length;
}

module.exports = {
    computeCosineSimilarity,
    calculateMSE
};
