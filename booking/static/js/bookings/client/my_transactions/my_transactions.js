
$(document).ready(function () { 
    const table = $("#table-bookings").DataTable({
        'columnDefs': [
            {
            'targets': [6],
            'orderable': false
            }
        ],
        order: [[ 0, 'desc' ]] ,
       
    });
    $("#table-bookings").on("click", ".view", function(e){
        e.preventDefault(); 
        let url = $(this).attr("href");  

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            beforeSend: () => { 
                $("#modal-default").modal("show");
            },
            success: (data) => {
                $("#modal-default .modal-content").html(data.html_form); 
            },
            complete: (data) => {

            },
            error: (data) => {

            }
        });
        return false;
    });

    
    $("#table-bookings").on("click", ".delete", function(e){
        e.preventDefault(); 
        let url = $(this).attr("href"); 
        let row = $(this).closest('tr'); 

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            beforeSend: () => { 
                $("#modal-default").data('tr',row).modal("show");
            },
            success: (data) => {
                $("#modal-default .modal-content").html(data.html_form); 
            },
            complete: (data) => {

            },
            error: (data) => {

            }
        });
        return false;
    });

    
    $("#modal-default").on("submit", ".delete-booking-form", function(e){
        e.preventDefault();
        let form = $(this);
        let row = $("#modal-default").data('tr');

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: form.attr("data-url"),
            data: form.serialize(),
            cache: false,
            type: form.attr("method"),
            dataType: 'json',
            success: (data) => {
                if(data.form_is_valid){  
                    $("#modal-default").modal("hide");
                    table.row(row).remove().draw();    
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });
     
});