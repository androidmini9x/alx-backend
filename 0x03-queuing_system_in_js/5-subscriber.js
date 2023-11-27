import { createClient } from 'redis';

const subscriber = createClient();
subscriber.subscribe('holberton school channel');

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

subscriber.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

subscriber.on('message', (channel, message) => {
  if (channel === 'holberton school channel') {
    console.log(message);
  }

  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
