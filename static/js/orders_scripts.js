window.onload = function () {
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


    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_arr = []
    let price_arr = []

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    console.log(total_forms)


    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;


    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity').val());
        _price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'));

        console.log(_price)
        quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price;

        } else {
            price_arr[i] = 0
        }

    }

    // console.info('PRICE',price_arr)
    // console.info('QUANTITY',quantity_arr)


    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        }else{
            delta_quantity = quantity_arr[orderitem_num];
        }
         orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    });




    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    function  deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        quantity_arr[orderitem_num] = 0;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    }


    function orderSummerUpdate(orderitem_price, delta_quantity) {

        delta_cost = orderitem_price * delta_quantity
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString())
        $('.order_total_cost').html(order_total_price.toString() + ',00');




    }
    if (!order_total_quantity) {
        orderSummaryRecalc();
}
    function orderSummaryRecalc() {
       order_total_quantity = 0;
       order_total_cost = 0;
       total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
       for (var i=0; i < total_forms; i++) {
            _quantity = parseInt($('input[name=orderitems-' + i + '-quantity').val());
            _price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'));
           quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price;

        } else {
            price_arr[i] = 0
        }
           order_total_quantity += quantity_arr[i];
           order_total_cost += quantity_arr[i] * price_arr[i];
           console.log(price_arr[i])
       }
       $('.order_total_quantity').html(order_total_quantity.toString());
       $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }



    $('.order_form select').change(function () {
        var target = event.target;
        console.log(target)
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;
        console.log(orderitem_product_pk)

   if (orderitem_product_pk) {
       $.ajax({
           url: "/orders/product/" + orderitem_product_pk + "/price/",
           success: function (data) {
               if (data.price) {
                   price_arr[orderitem_num] = parseFloat(data.price);
                   if (isNaN(quantity_arr[orderitem_num])) {
                       quantity_arr[orderitem_num] = 0;
                   }
                   let price_html = '<span>' + data.price.toString().replace('.', ',') +'</span> руб';
                   let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                   current_tr.find('td:eq(2)').html(price_html);
                   console.log(data.price)

                   if (isNaN(current_tr.find('input[type="number"]').val())) {
                       current_tr.find('input[type="number"]').val(0);
                   }
                   orderSummaryRecalc();
               }
           },
       });
    }
    });





}