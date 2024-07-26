const express = require('express');
const http = require('https');
const path = require('path');

const app = express();
const port = 3000;

const apiKey = 'Your-API-Key-Here';
const apiHost = 'exercisedb.p.rapidapi.com';

app.use(express.static(path.join(__dirname, 'public')));

app.get('/exercises', (req, res) => {
    const target = req.query.target;
    const options = {
        method: 'GET',
        hostname: apiHost,
        port: null,
        path: `/exercises/target/${target}?limit=10&offset=0`,
        headers: {
            'x-rapidapi-key': apiKey,
            'x-rapidapi-host': apiHost
        }
    };

    const reqApi = http.request(options, function (apiRes) {
        const chunks = [];

        apiRes.on('data', function (chunk) {
            chunks.push(chunk);
        });

        apiRes.on('end', function () {
            const body = Buffer.concat(chunks);
            let exercises;

            try {
                exercises = JSON.parse(body.toString());
                res.json(exercises);
            } catch (e) {
                console.error('Error parsing JSON:', e);
                res.status(500).send('Error parsing JSON');
            }
        });
    });

    reqApi.on('error', function(e) {
        console.error(`Problem with request: ${e.message}`);
        res.status(500).send(`Problem with request: ${e.message}`);
    });

    reqApi.end();
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
