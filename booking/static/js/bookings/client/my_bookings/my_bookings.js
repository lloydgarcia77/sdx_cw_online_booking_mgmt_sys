
$(document).ready(function () { 
    const table = $("#table-services").DataTable({
        'columnDefs': [
            {
            'targets': [6],
            'orderable': false
            }
        ],
        order: [[ 0, 'asc' ]] ,
       
    });
     
});