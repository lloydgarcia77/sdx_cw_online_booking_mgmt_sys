
$(document).ready(function () { 
    const table = $("#table-inquiries").DataTable({
        'columnDefs': [
            {
            'targets': [6],
            'orderable': false
            }
        ],
        order: [[ 0, 'desc' ]] ,
          // File Export Option
        // dom: 'Bfrtip',
        dom: 'lBfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'print', //'pdf',
            // landscape orientation
            {
                extend: 'pdfHtml5',
                orientation: 'landscape',
                pageSize: 'LEGAL'
            }
        ]
       
    }); 

    
    $("#table-inquiries").on("click", ".delete", function(e){
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

    
    $("#modal-default").on("submit", ".delete-inquiry-form", function(e){
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