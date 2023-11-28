function updateDateTime() 
{
  var now = new Date();
  var months = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
    
  var ampm = now.getHours() >= 12 ? 'PM' : 'AM';
  var hours = now.getHours() % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
    
  var minutes = now.getMinutes() < 10 ? '0'+now.getMinutes() : now.getMinutes();
  var strTime = months[now.getMonth()] + " " + now.getDate() + ", " + now.getFullYear() + "  " + hours + ':' + minutes + ' ' + ampm;
  document.getElementById("currentDateTime").innerHTML = strTime;
}

setInterval(updateDateTime, 1000);
updateDateTime();
