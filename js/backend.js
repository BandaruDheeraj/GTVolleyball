var url = 'http://54.183.166.233:5000/getMatPlotLib';
function request() {
    var searchableName = document.getElementById("userName").value;
    var practice = document.getElementById("practiceName").value;
    console.log(searchableName + " " + practice);
    $.ajax({
        type: "POST",
        url: url,
        contentType: 'application/json',
        data: JSON.stringify({"person": searchableName, "practice": practice}),
        dataType: 'json'
    }).done(function(output_img) {
        document.getElementById("graph").src = output_img;
        document.getElementById("graph").style.width = '90%';
        console.log(output_img)
    });
}