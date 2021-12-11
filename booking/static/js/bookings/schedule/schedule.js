
$(document).ready(function () { 
    const TIME_SLOTS = [
        '08:00am - 10:00am',
        '10:00am - 12:00pm',
        '12:00pm - 02:00pm',
        '02:00pm - 04:00pm',
        '04:00pm - 06:00pm',
        '06:00am - 08:00pm',
    ]
    // let today = new Date(), weekLater = new Date();
    // weekLater.setDate(today.getDate() + 6); // Including today 
    // var array = ["2021-12-10","2021-12-11","2021-12-12"]

    // Date Picker Initial Setup
    $( "#datepicker" ).datepicker({
        // disable date 
        // beforeShowDay: function(date){
        //     let string = $.datepicker.formatDate('yy-mm-dd', date);
        //     return [ parsed_schedule_data.fully_booked_dates.indexOf(string) == -1 ]
        // },
        dateFormat: "yy-mm-dd" ,
        // minDate: today,
        // maxDate: weekLater,
        onSelect: function(dateText, inst) { 
            // let date = $(this).val();     
            getSchedule();
         
            // var time = $('#time').val();
            // alert('on select triggered');
            // $("#start").val(date + time.toString(' HH:mm').toString());

        }
    });
  

    function getSchedule(){
        let url = $("#datepicker").attr("data-url");
        let date = $( "#datepicker" ).datepicker("getDate");
        let string = $.datepicker.formatDate('yy-mm-dd', date); 
    
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: url,
            type: 'GET',
            data: { 
                date: string,
            },
            dataType: 'json',
            beforeSend: () => { 
            },
            success: (data) => { 
                let slot1 = data.slot1;
                let slot2 = data.slot2;
                let slot3 = data.slot3;
                const renderedTableBody = TIME_SLOTS.map((e, i)=> (
                    `<tr>
                        <td>${e}</td>
                        <td>${slot1.includes(i+1) ? '<i class="fas fa-times" style="color:red;"></i>' : '<i class="fas fa-check" style="color:green;"></i>'}</td>
                        <td>${slot2.includes(i+1) ? '<i class="fas fa-times" style="color:red;"></i>' : '<i class="fas fa-check" style="color:green;"></i>'}</td>
                        <td>${slot3.includes(i+1) ? '<i class="fas fa-times" style="color:red;"></i>' : '<i class="fas fa-check" style="color:green;"></i>'}</td>
                    </tr>`
                )) 

                const renderedTableFooter = `
                <tr> 
                    <th>Total Occupied:</th>
                    <th>${6-slot1.length}</th>
                    <th>${6-slot2.length}</th>
                    <th>${6-slot3.length}</th> 
                </tr>
                `
                $("#table_schedule tbody").html(renderedTableBody)
                $("#table_schedule tfoot").html(renderedTableFooter) 
            },
            complete: (data) => {

            },
            error: (data) => {

            }
        });
    }

    getSchedule();

});
