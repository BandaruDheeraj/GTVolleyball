var url = 'http://54.183.166.233:5000/getMatPlotLib';
var otherurl = 'http://54.183.166.233:5000/getPlayerData'
var categories = ['Active Minutes', 'Kinetic Energy (Joules/Pound)', 'Avg Intensity (Watts/Pound)', 'Stress Percentage']
var counter = 0
function request() {
    var searchableName = document.getElementById("userName").value;
    var practice = document.getElementById("practiceName").value;
    var maxG = document.getElementById("maxG").value;
    console.log(searchableName + " " + practice);
    $.ajax({
        type: "POST",
        url: url,
        contentType: 'application/json',
        data: JSON.stringify({"person": searchableName, "practice": practice, "gforce": maxG}),
        dataType: 'json'
    }).done(function(output_img) {
        //console.log(output_img[])
        document.getElementById("graph").src = output_img["img"];
        var t = ""
        document.getElementById("recommendation").innerText = 'Algorithmically Calculated Number of Bad Jumps above GForce Threshold: ' + String(output_img["bad_counts"]);

        if(output_img['bad_counts']>0){
          t = "Because the calculated number of poor jumps for " + searchableName + " exceeds the desired amount, it is recommended that she works on strength and conditioning."
        }
        document.getElementById("explanation").innerText = t + " The black, horizontal dotted line, represents the players mean gforce. The vertical red dotted lines represent jumps which our algorithm finds using index metrics. The solid black line represents the gforce threshold, where any jumps with values greater than this, are catgorized as bad jumps. Bad jump points are marked in green"
        document.getElementById("graph").style.width = '90%';

        otherRequests();
    });
}

function otherRequests() {
  var searchableName = document.getElementById("userName").value;
  if(counter < categories.length)
  {
    $.ajax({
        type: "POST",
        url: otherurl,
        contentType: 'application/json',
        data: JSON.stringify({"person": searchableName, "category": categories[counter]}),
        dataType: 'json'
    }).done(function(output_img) {
        console.log("graph" + (counter+1).toString())
        document.getElementById("graph" + (counter+1).toString()).src = output_img;
        document.getElementById("graph" + (counter+1).toString()).style.width = '90%';

        counter++;
        otherRequests();
    });
  }
  else {
    console.log('Done')
    counter = 0
  }
}
