
$(document).ready(function () { 
    const table = $("#table-services").DataTable({
        'columnDefs': [
            {
            'targets': [6],
            'orderable': false
            }
        ],
        order: [[ 0, 'asc' ]] ,
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
    
    $("#create-service").on("click", function(e){
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

    $("#modal-default").on("submit", ".create-service-form", function(e){
        e.preventDefault();
        let form =$(this);

        $.ajax({
            url: form.attr("data-url"),
            data: form.serialize(),
            cache: false,
            type: form.attr("method"),
            dataType: 'json',
            beforeSend: () => {
                $("#modal-default").modal("show");
            },
            success: (data) => {
                if(data.form_is_valid){ 
                    let x = data.object_data;
                    table.row.add([
                       `<td>${x.id}</td>`, 
                        `<td>${x.name}</td>`,
                        `<td>${x.vehicle_type}</td>`,
                        `<td>${x.price}</td>`,
                        `<td>${x.desription}</td>`,
                        `<td>${x.duration}</td> `,
                        `<td> 
                           <a href="${x.edit_url}" class="btn btn-warning btn-circle btn-sm edit">
                               <i class="fas fa-edit"></i>
                           </a> 
                           <a href="${x.delete_url}" class="btn btn-danger btn-circle btn-sm delete">
                               <i class="fas fa-user-minus"></i>
                           </a>
                        </td>`,
                    ]).draw(false); 
                    $("#modal-default").modal("hide");
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
           
            },
            complete: (data) => {

            },
            error: (data) => {

            }

        });
        return false;
    });

    $("#table-services").on("click", ".edit", function(e){
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

    
    $("#modal-default").on("submit", ".edit-services-form", function(e){
        e.preventDefault();
        let form = $(this);
        let row = $("#modal-default").data('tr');

        $.ajax({
            url: form.attr("data-url"),
            data: form.serialize(),
            cache: false,
            type: form.attr("method"),
            dataType: 'json',
            success: (data) => {
                if(data.form_is_valid){  
                    let row_data = table.row(row).data();
                    let x = data.object_data; 
                    row_data[1] = `<td>${x.name}</td>`;
                    row_data[2] = `<td>${x.vehicle_type}</td>`;
                    row_data[3] = `<td>${x.price}</td>`;
                    row_data[4] =  `<td>${x.desription}</td>`;
                    row_data[5] = `<td>${x.duration}</td>`;
                    //https://legacy.datatables.net/ref
                    $('#table-services').dataTable().fnUpdate(row_data,row,undefined,false); 
                    $("#modal-default").modal("hide"); 
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });


    $("#table-services").on("click", ".delete", function(e){
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

    
    $("#modal-default").on("submit", ".delete-services-form", function(e){
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