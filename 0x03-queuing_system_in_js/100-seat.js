const { createClient } = require("redis");
const { createQueue } = require('kue');
const { promisify } = require('util');
const express = require('express');

const queue = createQueue();
const client = createClient();
const getAsync = promisify(client.get);
let reservationEnabled;

const app = express();
const port = 1245;

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const val = getAsync.call(client, 'available_seats');
  return val;
}

client.on('connect', () => {
  reserveSeat(50);
  reservationEnabled = true;
})

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {

  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat', {});
  job.save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
      return;
    }
    res.json({ status: 'Reservation failed' });
  })
  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`));
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    if (seats <= 0) {
      done(new Error('Not enough seats available'));
    }

    if (seats - 1 == 0) {
      reservationEnabled = false;
    }

    reserveSeat(seats - 1);
    done();
  });
  res.json({ status: 'Queue processing' });
});


app.listen(port);
