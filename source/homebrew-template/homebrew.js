'use strict';

var uuid = require('uuid');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB({
    apiVersion: '2012-08-10'
});

exports.handler = function(event, context, callback) {
    var eventBody = JSON.parse(event.body);

    var params = {
        "TableName": "homebrew",
        "Item": {
            "id": {
                S: uuid.v1()
            },
            "monitorid": {
                S: eventBody.monitorId
            },
            "dateTime": {
                S: eventBody.datetime
            },
            "celcius": {
                N: eventBody.tempCelsius.toString()
            },
            "farenheit": {
                N: eventBody.tempFarenheit.toString()
            }
        }
    };

    console.log(params);

    dynamodb.putItem(params, function(err, data) {
        if (err) {
            console.log(err);
            callback('error', 'putting item into dynamodb failed: ', err);
        } else {
            callback(null, {
                statusCode: 200,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true
                },
                body: JSON.stringify(event.body)
            });
        };
    });
};