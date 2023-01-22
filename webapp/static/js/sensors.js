function updateSensorData(sensorId, value) {
    var url = '../sensors/setdata';

    data = {
            "SensorId": sensorId,
            "Value": value
            };

    var settings = {
        "url": "../sensors/setdata",
        "dataType": "json",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "data": JSON.stringify(data),
    };
    
    console.log(settings);

    $.ajax(settings).done(function (response) {
        console.log(response);
    });
}