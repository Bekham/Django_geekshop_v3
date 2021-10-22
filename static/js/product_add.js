window.onload = function (){
    $('.product_add').on('click', 'input[type="button"]', (e) => {
            let t_href = e.target;
            let csrf_token = $('meta[name="csrf-token"]').attr('content');
            console.log(t_href.id)


            $.ajax(
            {
                type:'POST',

                headers: {"X-CSRFToken": csrf_token},
                url: '/baskets/add/' + t_href.name + "/" ,
                dataType: 'json',
                data: {
                    page_id: t_href.id,

                //     // csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
                //     csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                // cache: false,
                success:  (data) => {
                    if (data) {
                        console.log(data);
                        $('.product_add').html(data.result);
                    }


            },

            });
            e.preventDefault();
        });

    }