"use strict";

const TorAgent = require("toragent");
const request  = require("request");
const mysources = require("./mysources.json");

let websites = mysources.sources;
let agent = null;

/**
 * Gets some random URLs from articles.
 * @param {function} callback This is called when this is done.
 */
function getNews(callback) {
    let newsUrl = "https://newsapi.org/v2/everything?q=snowden&sortBy=publishedAt&apiKey=";
    newsUrl += mysources.newsapi_key;

    // Get the articles.
    get(newsUrl, (error, results) => {
        if (!error) {
            // Parse the results.
            results = JSON.parse(results);

            // Add the articles to the list.
            for (let i = 0; i < results.articles.length; i++) {
                websites.push(results.articles[i].url);
            }
        } else {
            throw(error);
        }

        callback();
    });
}

/**
 * Connects to the Tor network.
 * @param {function} callback The callback function that's called once we're
 *   connected to the network.
 */
function connect(callback) {
    console.log("Getting new identity");

    TorAgent.create(false, function(error, newAgent) {
        if (error) {
            // Unable to connect to the Tor network
            throw(err);
        }

        agent = newAgent;
        callback();
    });
}

/**
 * Creates a simple HTTP GET request.
 * @param {string} url The URL to get.
 * @param {function} callback The function called once the request is done.
 */
function get(url, callback) {
    request({
        url: url,
        agent: agent,
        rejectUnauthorized: false,
    }, function(err, res, body) {
        if(err) {
            websites.splice(websites.indexOf(url), 1);
            callback(err, false);
        } else {
            callback(null, body);
        }
    });
}

/**
 * Gets a random website from the list.
 * @returns {string} A URL of a page to load.
 */
function getRandomPage() {
    let len = websites.length;
    return websites[Math.round(Math.random() * len) % len];
}

/**
 * Generates random traffic.
 */
function loadRandomUrl() {
    let page = getRandomPage();
    get(page, (err) => console.error(err ? err : `GET: ${page}`));

    setTimeout(loadRandomUrl, Math.round(Math.random() * 800) % 800);
}

// Connect to Tor and begin jamming the session.
connect(() => {
    getNews(loadRandomUrl);
});