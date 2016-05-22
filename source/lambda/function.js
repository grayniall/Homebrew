'use strict';

exports.handler = (event, context, callback) => {
    console.log('event', event);
    
    callback(null, event.key1);
};