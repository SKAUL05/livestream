const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const socketio = require('@feathersjs/socketio');
const moment = require('moment');


// Idea Service

class IdeaService {
    constructor() {
        this.ideas = [];
    }

    async find() {
        return this.ideas;
    }
    async create(data) {
        const idea = {
            id: this.ideas.length,
            text: data.text,
            tech: data.tech,
            viewer: data.viewer
        }
        idea.time = moment().format('h:mm:ss a');
        this.ideas.push(idea);
        return idea;
    }
}

const app = express(feathers());

// Parse JSON

app.use(express.json());

// Config Socket.io realtime APIs

app.configure(socketio());

// Enable Rest APIs

app.configure(express.rest());

// Register services

app.use('/ideas', new IdeaService());

// New connection
app.on('connection', conn => app.channel('stream').join(conn));

// Publish
app.publish(data => app.channel('stream'));

const PORT = process.env.PORT || 3030;

app.listen(PORT).on('listening', () => console.log("Realtime"));


app.service('ideas').create({
    text: "Build a LiveStream",
    tech: "node.js",
    viewer: "Sarath Kaul",
    time: moment().format('h:mm:ss a')
});