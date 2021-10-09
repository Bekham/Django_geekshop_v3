window.onload = function (){
    $('.product_add').on('click', 'input[type="button"]', function () {
        let t_hrep = event.target;
        console.log(t_hrep.name);
        console.log(t_hrep.id);
        $.ajax(
            {
                url: '/products/product_add/' + t_hrep.name + "/" + t_hrep.value + "/",
                success: function (data) {
                    $('.product_add').html(data.result);
                },
            });
        event.preventDefault();
    });
    }