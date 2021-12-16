
$(document).ready(function () {
    const table_invoice = $("#table-invoice-bookings").DataTable({
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]], // Show all
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
            // 'copy', 'csv', 'excel', 'print', //'pdf',
            // { extend: 'copyHtml5', footer: true },
            { extend: 'csvHtml5', exportOptions: {  columns: 'th:not(:last-child)' } },
            // Do not include last column for export and inlude the footer with title
            { extend: 'excelHtml5',  messageTop: 'Speed Driven Xavierville, #67B Xavierville Ave, Brgy, Quezon City, 1108 Metro Manila',   messageBottom: null, footer: true , exportOptions: {  columns: 'th:not(:last-child)' } },
            { extend: 'pdfHtml5', messageTop: 'Speed Driven Xavierville, #67B Xavierville Ave, Brgy, Quezon City, 1108 Metro Manila',   messageBottom: null,  orientation: 'landscape', pageSize: 'LEGAL', footer: true, exportOptions: {  columns: 'th:not(:last-child)' } }
        ],
        // https://phppot.com/jquery/calculate-sum-total-of-datatables-column-using-footer-callback/
        footerCallback: function( tfoot, data, start, end, display ) {
            var api = this.api();
            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/(<([^>]+)>)/ig, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            $(api.column(5).footer()).html(
                `₱
                ${api.column(5).data().reduce(function ( a, b ) {
                    return intVal(a) + intVal(b);
                }, 0)}
                `
            );
        }
    });
    // var table = $('#example').DataTable();


    $("#table-invoice-bookings").on("click", ".view", function(e){
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


    $("#table-invoice-bookings").on("click", ".delete", function(e){
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


    $("#modal-default").on("submit", ".delete-invoice-client-booking", function(e){
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
                    table_invoice.row(row).remove().draw();
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });

    const table_walkin = $("#table-walkin-bookings").DataTable({
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]], // Show all
        'columnDefs': [
            {
            'targets': [8],
            'orderable': false
            }
        ],
        order: [[ 0, 'desc' ]] ,
        // File Export Option
        // dom: 'Bfrtip',
        dom: 'lBfrtip',
        buttons: [
            // 'copy', 'csv', 'excel', 'print', //'pdf',
            // { extend: 'copyHtml5', footer: true },
            { extend: 'csvHtml5', exportOptions: {  columns: 'th:not(:last-child)' } },
            // Do not include last column for export and inlude the footer with title
            { extend: 'excelHtml5',  messageTop: 'Speed Driven Xavierville, #67B Xavierville Ave, Brgy, Quezon City, 1108 Metro Manila',   messageBottom: null, footer: true , exportOptions: {  columns: 'th:not(:last-child)' } },
            { extend: 'pdfHtml5', messageTop: 'Speed Driven Xavierville, #67B Xavierville Ave, Brgy, Quezon City, 1108 Metro Manila',   messageBottom: null,  orientation: 'landscape', pageSize: 'LEGAL', footer: true, exportOptions: {  columns: 'th:not(:last-child)' } }
        ],
        // https://phppot.com/jquery/calculate-sum-total-of-datatables-column-using-footer-callback/
        footerCallback: function( tfoot, data, start, end, display ) {
            var api = this.api();
            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/(<([^>]+)>)/ig, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            $(api.column(5).footer()).html(
                `₱
                ${api.column(5).data().reduce(function ( a, b ) {
                    return intVal(a) + intVal(b);
                }, 0)}
                `
            );
        }

    });


    $("#walkin_invoice_booking_add").on("click", function(e){
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


    $("#modal-default").on("submit", ".walkin-invoice-booking-add-form", function(e){
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
                    table_walkin.row.add([
                       `<td>${x.id}</td>`,
                        `<td>${x.name}</td>`,
                        `<td>${x.service}</td>`,
                        `<td>${x.date}</td>`,
                        `<td>${x.slot}</td>`,
                        `<td>${x.price}</td> `,
                        `<td>${x.time_from}</td> `,
                        `<td>${x.time_to}</td> `,
                        `<td>
                            <div class="btn-group" role="group" aria-label="button group">
                                <a href="${x.edit_url}" class="btn btn-warning btn-sm edit">
                                    <i class="fas fa-edit"></i>  Edit
                                </a>
                                <a href="${x.delete_url}" class="btn btn-danger btn-sm delete">
                                    <i class="fas fa-trash-alt"></i> Delete
                                </a>
                            </div>
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


    $("#table-walkin-bookings").on("click", ".edit", function(e){
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


    $("#modal-default").on("submit", ".walkin-invoice-booking-edit-form", function(e){
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
                    let row_data = table_walkin.row(row).data();
                    let x = data.object_data;
                    row_data[1] = `<td>${x.name}</td>`;
                    row_data[2] = `<td>${x.service}</td>`;
                    row_data[3] = `<td>${x.date}</td>`;
                    row_data[4] = `<td>${x.slot}</td>`;
                    row_data[5] = `<td>${x.price}</td>`;
                    row_data[6] = `<td>${x.time_from}</td>`;
                    row_data[7] = `<td>${x.time_to}</td>`;
                    //https://legacy.datatables.net/ref
                    $('#table-walkin-bookings').dataTable().fnUpdate(row_data,row,undefined,false);
                    $('#table-walkin-bookings').DataTable().draw(false);
                    $("#modal-default").modal("hide");
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });

    $("#table-walkin-bookings").on("click", ".delete", function(e){
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

    $("#modal-default").on("submit", ".walkin-invoice-booking-delete-form", function(e){
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
                    table_walkin.row(row).remove().draw();
                    // $('#table-walkin-bookings').DataTable().draw(false);
                }else{
                    $("#modal-default .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });
});