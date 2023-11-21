document.getElementById('imageSelect').addEventListener('change', function(event) 
{
    if (event.target.files && event.target.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image').src = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    }
});
