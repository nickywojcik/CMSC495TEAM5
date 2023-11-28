document.getElementById('file').addEventListener('change', function(event) {
    if (event.target.files && event.target.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var image = document.getElementById('image');
            image.src = e.target.result;
            
            var tempImg = new Image();
            tempImg.onload = function () {
                image.style.width = '400px';
                image.style.height = '400px';
            };
            tempImg.src = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    }
});
