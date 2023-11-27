import { createQueue } from 'kue';

const queue = createQueue();
const data = {
  phoneNumber: 'string',
  message: 'string',
};

const job = queue.create('push_notification_code', data)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  });

job.on('complete', () => console.log('Notification job completed'))
  .on('failed', () => console.log('Notification job failed'));
