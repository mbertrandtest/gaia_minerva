module.exports = {
    extends: process.cwd() + '/.eslintrc',
    rules: {
        complexity: [2, 12]
    },
    globals: {
        gaia_minerva: true,
        geo: true,
        jsonPath: true,
        colorbrewer: true,
        d3: true,
        Papa: true
    }
};
